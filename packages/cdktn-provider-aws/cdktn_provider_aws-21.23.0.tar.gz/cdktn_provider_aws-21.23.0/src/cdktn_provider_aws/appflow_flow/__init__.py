r'''
# `aws_appflow_flow`

Refer to the Terraform Registry for docs: [`aws_appflow_flow`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow).
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


class AppflowFlow(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlow",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow aws_appflow_flow}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        destination_flow_config: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppflowFlowDestinationFlowConfig", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        source_flow_config: typing.Union["AppflowFlowSourceFlowConfig", typing.Dict[builtins.str, typing.Any]],
        task: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppflowFlowTask", typing.Dict[builtins.str, typing.Any]]]],
        trigger_config: typing.Union["AppflowFlowTriggerConfig", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kms_arn: typing.Optional[builtins.str] = None,
        metadata_catalog_config: typing.Optional[typing.Union["AppflowFlowMetadataCatalogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow aws_appflow_flow} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param destination_flow_config: destination_flow_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#destination_flow_config AppflowFlow#destination_flow_config}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#name AppflowFlow#name}.
        :param source_flow_config: source_flow_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#source_flow_config AppflowFlow#source_flow_config}
        :param task: task block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#task AppflowFlow#task}
        :param trigger_config: trigger_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#trigger_config AppflowFlow#trigger_config}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#description AppflowFlow#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#id AppflowFlow#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#kms_arn AppflowFlow#kms_arn}.
        :param metadata_catalog_config: metadata_catalog_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#metadata_catalog_config AppflowFlow#metadata_catalog_config}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#region AppflowFlow#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#tags AppflowFlow#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#tags_all AppflowFlow#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d87b7a889f09084356b4785287e271fe7c7d575dd5706460f25b5785b95cb831)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppflowFlowConfig(
            destination_flow_config=destination_flow_config,
            name=name,
            source_flow_config=source_flow_config,
            task=task,
            trigger_config=trigger_config,
            description=description,
            id=id,
            kms_arn=kms_arn,
            metadata_catalog_config=metadata_catalog_config,
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
        '''Generates CDKTF code for importing a AppflowFlow resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AppflowFlow to import.
        :param import_from_id: The id of the existing AppflowFlow that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AppflowFlow to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70513549323f47dfdfac450681572ceae92e2f214f808171149b6ca6ff2cf5ed)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDestinationFlowConfig")
    def put_destination_flow_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppflowFlowDestinationFlowConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__913968eb2f5b699068dde5a422c098cef6cb5596c18eb8c4d675f9ad736961df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDestinationFlowConfig", [value]))

    @jsii.member(jsii_name="putMetadataCatalogConfig")
    def put_metadata_catalog_config(
        self,
        *,
        glue_data_catalog: typing.Optional[typing.Union["AppflowFlowMetadataCatalogConfigGlueDataCatalog", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param glue_data_catalog: glue_data_catalog block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#glue_data_catalog AppflowFlow#glue_data_catalog}
        '''
        value = AppflowFlowMetadataCatalogConfig(glue_data_catalog=glue_data_catalog)

        return typing.cast(None, jsii.invoke(self, "putMetadataCatalogConfig", [value]))

    @jsii.member(jsii_name="putSourceFlowConfig")
    def put_source_flow_config(
        self,
        *,
        connector_type: builtins.str,
        source_connector_properties: typing.Union["AppflowFlowSourceFlowConfigSourceConnectorProperties", typing.Dict[builtins.str, typing.Any]],
        api_version: typing.Optional[builtins.str] = None,
        connector_profile_name: typing.Optional[builtins.str] = None,
        incremental_pull_config: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigIncrementalPullConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connector_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#connector_type AppflowFlow#connector_type}.
        :param source_connector_properties: source_connector_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#source_connector_properties AppflowFlow#source_connector_properties}
        :param api_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#api_version AppflowFlow#api_version}.
        :param connector_profile_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#connector_profile_name AppflowFlow#connector_profile_name}.
        :param incremental_pull_config: incremental_pull_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#incremental_pull_config AppflowFlow#incremental_pull_config}
        '''
        value = AppflowFlowSourceFlowConfig(
            connector_type=connector_type,
            source_connector_properties=source_connector_properties,
            api_version=api_version,
            connector_profile_name=connector_profile_name,
            incremental_pull_config=incremental_pull_config,
        )

        return typing.cast(None, jsii.invoke(self, "putSourceFlowConfig", [value]))

    @jsii.member(jsii_name="putTask")
    def put_task(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppflowFlowTask", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__953d6700bc06c6a3adbfcd80db48d7a68d05acba8a8ea1a567144dcbb9ffd3cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTask", [value]))

    @jsii.member(jsii_name="putTriggerConfig")
    def put_trigger_config(
        self,
        *,
        trigger_type: builtins.str,
        trigger_properties: typing.Optional[typing.Union["AppflowFlowTriggerConfigTriggerProperties", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param trigger_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#trigger_type AppflowFlow#trigger_type}.
        :param trigger_properties: trigger_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#trigger_properties AppflowFlow#trigger_properties}
        '''
        value = AppflowFlowTriggerConfig(
            trigger_type=trigger_type, trigger_properties=trigger_properties
        )

        return typing.cast(None, jsii.invoke(self, "putTriggerConfig", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsArn")
    def reset_kms_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsArn", []))

    @jsii.member(jsii_name="resetMetadataCatalogConfig")
    def reset_metadata_catalog_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataCatalogConfig", []))

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
    @jsii.member(jsii_name="destinationFlowConfig")
    def destination_flow_config(self) -> "AppflowFlowDestinationFlowConfigList":
        return typing.cast("AppflowFlowDestinationFlowConfigList", jsii.get(self, "destinationFlowConfig"))

    @builtins.property
    @jsii.member(jsii_name="flowStatus")
    def flow_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flowStatus"))

    @builtins.property
    @jsii.member(jsii_name="metadataCatalogConfig")
    def metadata_catalog_config(
        self,
    ) -> "AppflowFlowMetadataCatalogConfigOutputReference":
        return typing.cast("AppflowFlowMetadataCatalogConfigOutputReference", jsii.get(self, "metadataCatalogConfig"))

    @builtins.property
    @jsii.member(jsii_name="sourceFlowConfig")
    def source_flow_config(self) -> "AppflowFlowSourceFlowConfigOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigOutputReference", jsii.get(self, "sourceFlowConfig"))

    @builtins.property
    @jsii.member(jsii_name="task")
    def task(self) -> "AppflowFlowTaskList":
        return typing.cast("AppflowFlowTaskList", jsii.get(self, "task"))

    @builtins.property
    @jsii.member(jsii_name="triggerConfig")
    def trigger_config(self) -> "AppflowFlowTriggerConfigOutputReference":
        return typing.cast("AppflowFlowTriggerConfigOutputReference", jsii.get(self, "triggerConfig"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationFlowConfigInput")
    def destination_flow_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppflowFlowDestinationFlowConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppflowFlowDestinationFlowConfig"]]], jsii.get(self, "destinationFlowConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsArnInput")
    def kms_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsArnInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataCatalogConfigInput")
    def metadata_catalog_config_input(
        self,
    ) -> typing.Optional["AppflowFlowMetadataCatalogConfig"]:
        return typing.cast(typing.Optional["AppflowFlowMetadataCatalogConfig"], jsii.get(self, "metadataCatalogConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFlowConfigInput")
    def source_flow_config_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfig"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfig"], jsii.get(self, "sourceFlowConfigInput"))

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
    @jsii.member(jsii_name="taskInput")
    def task_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppflowFlowTask"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppflowFlowTask"]]], jsii.get(self, "taskInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerConfigInput")
    def trigger_config_input(self) -> typing.Optional["AppflowFlowTriggerConfig"]:
        return typing.cast(typing.Optional["AppflowFlowTriggerConfig"], jsii.get(self, "triggerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b5737fae8c7a42cc58035ae7edbf255236c23d40d1aff41fada6bb7eb8fac3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b59797496b1723c5cd3c3ce57b6ab68b683a78ef92eeedfbcaab7061eb0f082c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsArn")
    def kms_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsArn"))

    @kms_arn.setter
    def kms_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aabff0622f256fda199a512073840fa855719d2a14d26a9a85fc34f97626555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f32637f34d095fc8f327c0c36320467563a45dbe5783acf783b1458c0f29b8f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6ec73e5f95bf8e591fd759a8b8436f9e235aada3ae730b2c55d844575a89f3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ef33f54794f328f0a72ba3c543fa0447edcf5d21a38e520e2af65d84568769f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a19cf89201414855e847d1800699f7061d41ce1e752fd0e619954c7bd13ae79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "destination_flow_config": "destinationFlowConfig",
        "name": "name",
        "source_flow_config": "sourceFlowConfig",
        "task": "task",
        "trigger_config": "triggerConfig",
        "description": "description",
        "id": "id",
        "kms_arn": "kmsArn",
        "metadata_catalog_config": "metadataCatalogConfig",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class AppflowFlowConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        destination_flow_config: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppflowFlowDestinationFlowConfig", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        source_flow_config: typing.Union["AppflowFlowSourceFlowConfig", typing.Dict[builtins.str, typing.Any]],
        task: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppflowFlowTask", typing.Dict[builtins.str, typing.Any]]]],
        trigger_config: typing.Union["AppflowFlowTriggerConfig", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kms_arn: typing.Optional[builtins.str] = None,
        metadata_catalog_config: typing.Optional[typing.Union["AppflowFlowMetadataCatalogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param destination_flow_config: destination_flow_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#destination_flow_config AppflowFlow#destination_flow_config}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#name AppflowFlow#name}.
        :param source_flow_config: source_flow_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#source_flow_config AppflowFlow#source_flow_config}
        :param task: task block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#task AppflowFlow#task}
        :param trigger_config: trigger_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#trigger_config AppflowFlow#trigger_config}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#description AppflowFlow#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#id AppflowFlow#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#kms_arn AppflowFlow#kms_arn}.
        :param metadata_catalog_config: metadata_catalog_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#metadata_catalog_config AppflowFlow#metadata_catalog_config}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#region AppflowFlow#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#tags AppflowFlow#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#tags_all AppflowFlow#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(source_flow_config, dict):
            source_flow_config = AppflowFlowSourceFlowConfig(**source_flow_config)
        if isinstance(trigger_config, dict):
            trigger_config = AppflowFlowTriggerConfig(**trigger_config)
        if isinstance(metadata_catalog_config, dict):
            metadata_catalog_config = AppflowFlowMetadataCatalogConfig(**metadata_catalog_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52215339cd0c23b9ea696463a23422ead294d421baf060b0ef512288278aa7d6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument destination_flow_config", value=destination_flow_config, expected_type=type_hints["destination_flow_config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source_flow_config", value=source_flow_config, expected_type=type_hints["source_flow_config"])
            check_type(argname="argument task", value=task, expected_type=type_hints["task"])
            check_type(argname="argument trigger_config", value=trigger_config, expected_type=type_hints["trigger_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_arn", value=kms_arn, expected_type=type_hints["kms_arn"])
            check_type(argname="argument metadata_catalog_config", value=metadata_catalog_config, expected_type=type_hints["metadata_catalog_config"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_flow_config": destination_flow_config,
            "name": name,
            "source_flow_config": source_flow_config,
            "task": task,
            "trigger_config": trigger_config,
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
        if kms_arn is not None:
            self._values["kms_arn"] = kms_arn
        if metadata_catalog_config is not None:
            self._values["metadata_catalog_config"] = metadata_catalog_config
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
    def destination_flow_config(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppflowFlowDestinationFlowConfig"]]:
        '''destination_flow_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#destination_flow_config AppflowFlow#destination_flow_config}
        '''
        result = self._values.get("destination_flow_config")
        assert result is not None, "Required property 'destination_flow_config' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppflowFlowDestinationFlowConfig"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#name AppflowFlow#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_flow_config(self) -> "AppflowFlowSourceFlowConfig":
        '''source_flow_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#source_flow_config AppflowFlow#source_flow_config}
        '''
        result = self._values.get("source_flow_config")
        assert result is not None, "Required property 'source_flow_config' is missing"
        return typing.cast("AppflowFlowSourceFlowConfig", result)

    @builtins.property
    def task(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppflowFlowTask"]]:
        '''task block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#task AppflowFlow#task}
        '''
        result = self._values.get("task")
        assert result is not None, "Required property 'task' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppflowFlowTask"]], result)

    @builtins.property
    def trigger_config(self) -> "AppflowFlowTriggerConfig":
        '''trigger_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#trigger_config AppflowFlow#trigger_config}
        '''
        result = self._values.get("trigger_config")
        assert result is not None, "Required property 'trigger_config' is missing"
        return typing.cast("AppflowFlowTriggerConfig", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#description AppflowFlow#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#id AppflowFlow#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#kms_arn AppflowFlow#kms_arn}.'''
        result = self._values.get("kms_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata_catalog_config(
        self,
    ) -> typing.Optional["AppflowFlowMetadataCatalogConfig"]:
        '''metadata_catalog_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#metadata_catalog_config AppflowFlow#metadata_catalog_config}
        '''
        result = self._values.get("metadata_catalog_config")
        return typing.cast(typing.Optional["AppflowFlowMetadataCatalogConfig"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#region AppflowFlow#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#tags AppflowFlow#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#tags_all AppflowFlow#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfig",
    jsii_struct_bases=[],
    name_mapping={
        "connector_type": "connectorType",
        "destination_connector_properties": "destinationConnectorProperties",
        "api_version": "apiVersion",
        "connector_profile_name": "connectorProfileName",
    },
)
class AppflowFlowDestinationFlowConfig:
    def __init__(
        self,
        *,
        connector_type: builtins.str,
        destination_connector_properties: typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorProperties", typing.Dict[builtins.str, typing.Any]],
        api_version: typing.Optional[builtins.str] = None,
        connector_profile_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connector_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#connector_type AppflowFlow#connector_type}.
        :param destination_connector_properties: destination_connector_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#destination_connector_properties AppflowFlow#destination_connector_properties}
        :param api_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#api_version AppflowFlow#api_version}.
        :param connector_profile_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#connector_profile_name AppflowFlow#connector_profile_name}.
        '''
        if isinstance(destination_connector_properties, dict):
            destination_connector_properties = AppflowFlowDestinationFlowConfigDestinationConnectorProperties(**destination_connector_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dec8377c34a5db11a8af7937da3304aadc9a7c459fa974485a592fb4661e08f)
            check_type(argname="argument connector_type", value=connector_type, expected_type=type_hints["connector_type"])
            check_type(argname="argument destination_connector_properties", value=destination_connector_properties, expected_type=type_hints["destination_connector_properties"])
            check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
            check_type(argname="argument connector_profile_name", value=connector_profile_name, expected_type=type_hints["connector_profile_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connector_type": connector_type,
            "destination_connector_properties": destination_connector_properties,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if connector_profile_name is not None:
            self._values["connector_profile_name"] = connector_profile_name

    @builtins.property
    def connector_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#connector_type AppflowFlow#connector_type}.'''
        result = self._values.get("connector_type")
        assert result is not None, "Required property 'connector_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_connector_properties(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorProperties":
        '''destination_connector_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#destination_connector_properties AppflowFlow#destination_connector_properties}
        '''
        result = self._values.get("destination_connector_properties")
        assert result is not None, "Required property 'destination_connector_properties' is missing"
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorProperties", result)

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#api_version AppflowFlow#api_version}.'''
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connector_profile_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#connector_profile_name AppflowFlow#connector_profile_name}.'''
        result = self._values.get("connector_profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorProperties",
    jsii_struct_bases=[],
    name_mapping={
        "custom_connector": "customConnector",
        "customer_profiles": "customerProfiles",
        "event_bridge": "eventBridge",
        "honeycode": "honeycode",
        "lookout_metrics": "lookoutMetrics",
        "marketo": "marketo",
        "redshift": "redshift",
        "s3": "s3",
        "salesforce": "salesforce",
        "sapo_data": "sapoData",
        "snowflake": "snowflake",
        "upsolver": "upsolver",
        "zendesk": "zendesk",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorProperties:
    def __init__(
        self,
        *,
        custom_connector: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector", typing.Dict[builtins.str, typing.Any]]] = None,
        customer_profiles: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles", typing.Dict[builtins.str, typing.Any]]] = None,
        event_bridge: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge", typing.Dict[builtins.str, typing.Any]]] = None,
        honeycode: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode", typing.Dict[builtins.str, typing.Any]]] = None,
        lookout_metrics: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
        marketo: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo", typing.Dict[builtins.str, typing.Any]]] = None,
        redshift: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3", typing.Dict[builtins.str, typing.Any]]] = None,
        salesforce: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce", typing.Dict[builtins.str, typing.Any]]] = None,
        sapo_data: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData", typing.Dict[builtins.str, typing.Any]]] = None,
        snowflake: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake", typing.Dict[builtins.str, typing.Any]]] = None,
        upsolver: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver", typing.Dict[builtins.str, typing.Any]]] = None,
        zendesk: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_connector: custom_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#custom_connector AppflowFlow#custom_connector}
        :param customer_profiles: customer_profiles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#customer_profiles AppflowFlow#customer_profiles}
        :param event_bridge: event_bridge block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#event_bridge AppflowFlow#event_bridge}
        :param honeycode: honeycode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#honeycode AppflowFlow#honeycode}
        :param lookout_metrics: lookout_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#lookout_metrics AppflowFlow#lookout_metrics}
        :param marketo: marketo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#marketo AppflowFlow#marketo}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#redshift AppflowFlow#redshift}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#s3 AppflowFlow#s3}
        :param salesforce: salesforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#salesforce AppflowFlow#salesforce}
        :param sapo_data: sapo_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#sapo_data AppflowFlow#sapo_data}
        :param snowflake: snowflake block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#snowflake AppflowFlow#snowflake}
        :param upsolver: upsolver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#upsolver AppflowFlow#upsolver}
        :param zendesk: zendesk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#zendesk AppflowFlow#zendesk}
        '''
        if isinstance(custom_connector, dict):
            custom_connector = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector(**custom_connector)
        if isinstance(customer_profiles, dict):
            customer_profiles = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles(**customer_profiles)
        if isinstance(event_bridge, dict):
            event_bridge = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge(**event_bridge)
        if isinstance(honeycode, dict):
            honeycode = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode(**honeycode)
        if isinstance(lookout_metrics, dict):
            lookout_metrics = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics(**lookout_metrics)
        if isinstance(marketo, dict):
            marketo = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo(**marketo)
        if isinstance(redshift, dict):
            redshift = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift(**redshift)
        if isinstance(s3, dict):
            s3 = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3(**s3)
        if isinstance(salesforce, dict):
            salesforce = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce(**salesforce)
        if isinstance(sapo_data, dict):
            sapo_data = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData(**sapo_data)
        if isinstance(snowflake, dict):
            snowflake = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake(**snowflake)
        if isinstance(upsolver, dict):
            upsolver = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver(**upsolver)
        if isinstance(zendesk, dict):
            zendesk = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk(**zendesk)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed57656833a4a00eafaef3f65ca9cfaf001c4123586b8918f8a1ba34b0723817)
            check_type(argname="argument custom_connector", value=custom_connector, expected_type=type_hints["custom_connector"])
            check_type(argname="argument customer_profiles", value=customer_profiles, expected_type=type_hints["customer_profiles"])
            check_type(argname="argument event_bridge", value=event_bridge, expected_type=type_hints["event_bridge"])
            check_type(argname="argument honeycode", value=honeycode, expected_type=type_hints["honeycode"])
            check_type(argname="argument lookout_metrics", value=lookout_metrics, expected_type=type_hints["lookout_metrics"])
            check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
            check_type(argname="argument redshift", value=redshift, expected_type=type_hints["redshift"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
            check_type(argname="argument sapo_data", value=sapo_data, expected_type=type_hints["sapo_data"])
            check_type(argname="argument snowflake", value=snowflake, expected_type=type_hints["snowflake"])
            check_type(argname="argument upsolver", value=upsolver, expected_type=type_hints["upsolver"])
            check_type(argname="argument zendesk", value=zendesk, expected_type=type_hints["zendesk"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_connector is not None:
            self._values["custom_connector"] = custom_connector
        if customer_profiles is not None:
            self._values["customer_profiles"] = customer_profiles
        if event_bridge is not None:
            self._values["event_bridge"] = event_bridge
        if honeycode is not None:
            self._values["honeycode"] = honeycode
        if lookout_metrics is not None:
            self._values["lookout_metrics"] = lookout_metrics
        if marketo is not None:
            self._values["marketo"] = marketo
        if redshift is not None:
            self._values["redshift"] = redshift
        if s3 is not None:
            self._values["s3"] = s3
        if salesforce is not None:
            self._values["salesforce"] = salesforce
        if sapo_data is not None:
            self._values["sapo_data"] = sapo_data
        if snowflake is not None:
            self._values["snowflake"] = snowflake
        if upsolver is not None:
            self._values["upsolver"] = upsolver
        if zendesk is not None:
            self._values["zendesk"] = zendesk

    @builtins.property
    def custom_connector(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector"]:
        '''custom_connector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#custom_connector AppflowFlow#custom_connector}
        '''
        result = self._values.get("custom_connector")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector"], result)

    @builtins.property
    def customer_profiles(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles"]:
        '''customer_profiles block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#customer_profiles AppflowFlow#customer_profiles}
        '''
        result = self._values.get("customer_profiles")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles"], result)

    @builtins.property
    def event_bridge(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge"]:
        '''event_bridge block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#event_bridge AppflowFlow#event_bridge}
        '''
        result = self._values.get("event_bridge")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge"], result)

    @builtins.property
    def honeycode(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode"]:
        '''honeycode block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#honeycode AppflowFlow#honeycode}
        '''
        result = self._values.get("honeycode")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode"], result)

    @builtins.property
    def lookout_metrics(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics"]:
        '''lookout_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#lookout_metrics AppflowFlow#lookout_metrics}
        '''
        result = self._values.get("lookout_metrics")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics"], result)

    @builtins.property
    def marketo(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo"]:
        '''marketo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#marketo AppflowFlow#marketo}
        '''
        result = self._values.get("marketo")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo"], result)

    @builtins.property
    def redshift(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift"]:
        '''redshift block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#redshift AppflowFlow#redshift}
        '''
        result = self._values.get("redshift")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift"], result)

    @builtins.property
    def s3(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3"]:
        '''s3 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#s3 AppflowFlow#s3}
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3"], result)

    @builtins.property
    def salesforce(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce"]:
        '''salesforce block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#salesforce AppflowFlow#salesforce}
        '''
        result = self._values.get("salesforce")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce"], result)

    @builtins.property
    def sapo_data(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData"]:
        '''sapo_data block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#sapo_data AppflowFlow#sapo_data}
        '''
        result = self._values.get("sapo_data")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData"], result)

    @builtins.property
    def snowflake(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake"]:
        '''snowflake block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#snowflake AppflowFlow#snowflake}
        '''
        result = self._values.get("snowflake")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake"], result)

    @builtins.property
    def upsolver(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver"]:
        '''upsolver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#upsolver AppflowFlow#upsolver}
        '''
        result = self._values.get("upsolver")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver"], result)

    @builtins.property
    def zendesk(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk"]:
        '''zendesk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#zendesk AppflowFlow#zendesk}
        '''
        result = self._values.get("zendesk")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector",
    jsii_struct_bases=[],
    name_mapping={
        "entity_name": "entityName",
        "custom_properties": "customProperties",
        "error_handling_config": "errorHandlingConfig",
        "id_field_names": "idFieldNames",
        "write_operation_type": "writeOperationType",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector:
    def __init__(
        self,
        *,
        entity_name: builtins.str,
        custom_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        write_operation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param entity_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#entity_name AppflowFlow#entity_name}.
        :param custom_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#custom_properties AppflowFlow#custom_properties}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        :param id_field_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.
        :param write_operation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.
        '''
        if isinstance(error_handling_config, dict):
            error_handling_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig(**error_handling_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f83322459e4998728046f7cb8e976b83896bb05622bffb572365cb0018ef5425)
            check_type(argname="argument entity_name", value=entity_name, expected_type=type_hints["entity_name"])
            check_type(argname="argument custom_properties", value=custom_properties, expected_type=type_hints["custom_properties"])
            check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
            check_type(argname="argument id_field_names", value=id_field_names, expected_type=type_hints["id_field_names"])
            check_type(argname="argument write_operation_type", value=write_operation_type, expected_type=type_hints["write_operation_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "entity_name": entity_name,
        }
        if custom_properties is not None:
            self._values["custom_properties"] = custom_properties
        if error_handling_config is not None:
            self._values["error_handling_config"] = error_handling_config
        if id_field_names is not None:
            self._values["id_field_names"] = id_field_names
        if write_operation_type is not None:
            self._values["write_operation_type"] = write_operation_type

    @builtins.property
    def entity_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#entity_name AppflowFlow#entity_name}.'''
        result = self._values.get("entity_name")
        assert result is not None, "Required property 'entity_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#custom_properties AppflowFlow#custom_properties}.'''
        result = self._values.get("custom_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def error_handling_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig"]:
        '''error_handling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        result = self._values.get("error_handling_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig"], result)

    @builtins.property
    def id_field_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.'''
        result = self._values.get("id_field_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def write_operation_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.'''
        result = self._values.get("write_operation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "fail_on_first_destination_error": "failOnFirstDestinationError",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd07cb72b1309efb6bb26b4075c607cb2027ca54f2b827b092622192b284079)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument fail_on_first_destination_error", value=fail_on_first_destination_error, expected_type=type_hints["fail_on_first_destination_error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if fail_on_first_destination_error is not None:
            self._values["fail_on_first_destination_error"] = fail_on_first_destination_error

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_on_first_destination_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.'''
        result = self._values.get("fail_on_first_destination_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12e970b5343a0b1ffdcc445387e5eadf5932bdd2469c0991d55845ff0c774ae0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetFailOnFirstDestinationError")
    def reset_fail_on_first_destination_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOnFirstDestinationError", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationErrorInput")
    def fail_on_first_destination_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOnFirstDestinationErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61a7cbd7a0a22927f7d28d10227d6485103b5eb296d2036dc03d3163ffd421c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c57f2e59f42fe9aa0b3029e9ac6192fe56014900c57f441c37454d8b7598be10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationError")
    def fail_on_first_destination_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOnFirstDestinationError"))

    @fail_on_first_destination_error.setter
    def fail_on_first_destination_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__477296934bac5029bb9ebb0d8bce0c9e7c49cd9ded585d056f5c38833fbc36a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnFirstDestinationError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__602e89d60a44698fb8fb19e2cbf499ce6ac88dc7aa456a5df75484f01dfd184e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73e60110e4ca757f066011371d32661af88a2209d7661dc821554fa70d860484)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putErrorHandlingConfig")
    def put_error_handling_config(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            fail_on_first_destination_error=fail_on_first_destination_error,
        )

        return typing.cast(None, jsii.invoke(self, "putErrorHandlingConfig", [value]))

    @jsii.member(jsii_name="resetCustomProperties")
    def reset_custom_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomProperties", []))

    @jsii.member(jsii_name="resetErrorHandlingConfig")
    def reset_error_handling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorHandlingConfig", []))

    @jsii.member(jsii_name="resetIdFieldNames")
    def reset_id_field_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdFieldNames", []))

    @jsii.member(jsii_name="resetWriteOperationType")
    def reset_write_operation_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteOperationType", []))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfig")
    def error_handling_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfigOutputReference, jsii.get(self, "errorHandlingConfig"))

    @builtins.property
    @jsii.member(jsii_name="customPropertiesInput")
    def custom_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "customPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="entityNameInput")
    def entity_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entityNameInput"))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfigInput")
    def error_handling_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig], jsii.get(self, "errorHandlingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idFieldNamesInput")
    def id_field_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "idFieldNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="writeOperationTypeInput")
    def write_operation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "writeOperationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="customProperties")
    def custom_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "customProperties"))

    @custom_properties.setter
    def custom_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de09bc7c4bb9290646b49a8bc71af167fc303feb6f772352c6cd25051ac40171)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entityName")
    def entity_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entityName"))

    @entity_name.setter
    def entity_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fef7733ddfb66222eb556070f77f7cd71c4049ad63d4ff8952a142642a06932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entityName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idFieldNames")
    def id_field_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "idFieldNames"))

    @id_field_names.setter
    def id_field_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c8c9693cb5008b6db4a46937d679f1f2f26bcdef98d8d4a63f77addba041f9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idFieldNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writeOperationType")
    def write_operation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "writeOperationType"))

    @write_operation_type.setter
    def write_operation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79871b22cc0fadf3c31c91cf3140be8a3db0e2cb73e7cc27af6d2256346b0009)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeOperationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b5009ea5584c86c58f81d1676ce0fe64156d4326d6a3e77c4adc03c8d235fd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles",
    jsii_struct_bases=[],
    name_mapping={"domain_name": "domainName", "object_type_name": "objectTypeName"},
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        object_type_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#domain_name AppflowFlow#domain_name}.
        :param object_type_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object_type_name AppflowFlow#object_type_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42104c8e7a4eaaae81591062604e90776307cc78dca22aae9607fd260e7769bc)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument object_type_name", value=object_type_name, expected_type=type_hints["object_type_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
        }
        if object_type_name is not None:
            self._values["object_type_name"] = object_type_name

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#domain_name AppflowFlow#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object_type_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object_type_name AppflowFlow#object_type_name}.'''
        result = self._values.get("object_type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfilesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfilesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eeb4e56660ce1c47ebc8fb10fd6dba00b85da1eae3438c555861d98522c1ccdc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetObjectTypeName")
    def reset_object_type_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObjectTypeName", []))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="objectTypeNameInput")
    def object_type_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectTypeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a73dc472fbb39544065ef621a43e67101faa902b66ec9290f1c09972514657f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectTypeName")
    def object_type_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectTypeName"))

    @object_type_name.setter
    def object_type_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89a13fcf9656600762db67a92a6a85fd1e31472d341113fb75204c5afd1bb8dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectTypeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51fa46d45e7314e40ee6c4a84b3ad8f2b503a44113a6425ded736c4d15459c8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge",
    jsii_struct_bases=[],
    name_mapping={"object": "object", "error_handling_config": "errorHandlingConfig"},
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge:
    def __init__(
        self,
        *,
        object: builtins.str,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        if isinstance(error_handling_config, dict):
            error_handling_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig(**error_handling_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f01149afa1d7c21f9e88cddc5f8da87144fa6755dfe482e19b9d31fd54efab3)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }
        if error_handling_config is not None:
            self._values["error_handling_config"] = error_handling_config

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def error_handling_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig"]:
        '''error_handling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        result = self._values.get("error_handling_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "fail_on_first_destination_error": "failOnFirstDestinationError",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c86b6a420d9a483a3c0e4ed9741ffbae6f2a012c139db7d9931a5c6eb225246)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument fail_on_first_destination_error", value=fail_on_first_destination_error, expected_type=type_hints["fail_on_first_destination_error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if fail_on_first_destination_error is not None:
            self._values["fail_on_first_destination_error"] = fail_on_first_destination_error

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_on_first_destination_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.'''
        result = self._values.get("fail_on_first_destination_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c17b657618cfcc8e554b7a5ebbf8aea8dd732cf5dc8c0a3b7461407c4239a04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetFailOnFirstDestinationError")
    def reset_fail_on_first_destination_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOnFirstDestinationError", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationErrorInput")
    def fail_on_first_destination_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOnFirstDestinationErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b60e56a348b9104860f73d54171015b996a885e65e8f1fb79a6620a48bbb27c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a834ced275323a69cfb14ec32a3ec466b570621db590548efd226cf6c4f18ed6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationError")
    def fail_on_first_destination_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOnFirstDestinationError"))

    @fail_on_first_destination_error.setter
    def fail_on_first_destination_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc6fc197325ee2725e34a8e64011c14c289b7e921cc7895c1b6e01b6fd28e0a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnFirstDestinationError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c01779b412c71137a57e494a4616db4886a45e572788e890896c7835eb3be0a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd67fcca0a85ed3f3cd2fd8a1200b67d5efd8fa062123e03031658d7589f570f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putErrorHandlingConfig")
    def put_error_handling_config(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            fail_on_first_destination_error=fail_on_first_destination_error,
        )

        return typing.cast(None, jsii.invoke(self, "putErrorHandlingConfig", [value]))

    @jsii.member(jsii_name="resetErrorHandlingConfig")
    def reset_error_handling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorHandlingConfig", []))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfig")
    def error_handling_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfigOutputReference, jsii.get(self, "errorHandlingConfig"))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfigInput")
    def error_handling_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig], jsii.get(self, "errorHandlingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__221a75674ab77a92e68f57a10b551832b58332fbf541684834ee556117cc83bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4465c4b1d73b0827e49e4d9b717ed314290693dc3e95f13fd643a0b6e74fb8c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode",
    jsii_struct_bases=[],
    name_mapping={"object": "object", "error_handling_config": "errorHandlingConfig"},
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode:
    def __init__(
        self,
        *,
        object: builtins.str,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        if isinstance(error_handling_config, dict):
            error_handling_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig(**error_handling_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da8136a24b7c1437a7a9a0f56cb1ff44eb8a3992e39276ca1cea0a1efeef8786)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }
        if error_handling_config is not None:
            self._values["error_handling_config"] = error_handling_config

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def error_handling_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig"]:
        '''error_handling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        result = self._values.get("error_handling_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "fail_on_first_destination_error": "failOnFirstDestinationError",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d7b212ccacab69f176753ae13d35d4e1e344c7dadafa66e031bbeda570036c6)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument fail_on_first_destination_error", value=fail_on_first_destination_error, expected_type=type_hints["fail_on_first_destination_error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if fail_on_first_destination_error is not None:
            self._values["fail_on_first_destination_error"] = fail_on_first_destination_error

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_on_first_destination_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.'''
        result = self._values.get("fail_on_first_destination_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b03ac175ab9b0889d3271ba40765e0e2af064fc4b072d2f2b554f85e81699277)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetFailOnFirstDestinationError")
    def reset_fail_on_first_destination_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOnFirstDestinationError", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationErrorInput")
    def fail_on_first_destination_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOnFirstDestinationErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15007148a3a998948f3278450c193afd681d52a5605e664d3aaa7d106d57887e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30edd3923ffd3c279e1d6cf33e4f232faaeed31d1e73aa1097d01ffc4528b6bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationError")
    def fail_on_first_destination_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOnFirstDestinationError"))

    @fail_on_first_destination_error.setter
    def fail_on_first_destination_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0bf4b761e8ca9b93c54a4692f1539a121c912b25759e51bfd68d8fceb279621)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnFirstDestinationError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ad9cb3d365b7d2446bfe4468d5245c0c8aed0a731b8f4af0de3479410343042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96c286764edc1536a536a25cc3ea5f967428d2e1ccee8e2252ce2e3bc4f30929)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putErrorHandlingConfig")
    def put_error_handling_config(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            fail_on_first_destination_error=fail_on_first_destination_error,
        )

        return typing.cast(None, jsii.invoke(self, "putErrorHandlingConfig", [value]))

    @jsii.member(jsii_name="resetErrorHandlingConfig")
    def reset_error_handling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorHandlingConfig", []))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfig")
    def error_handling_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfigOutputReference, jsii.get(self, "errorHandlingConfig"))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfigInput")
    def error_handling_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig], jsii.get(self, "errorHandlingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__446eda0fea14f5412705b75c1025028b1899234e8e5c390f93ace188abcc591a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58deae5cd564d02518de3bf146c2d324dfacaa98b0a1f96bfd315cb2adf3eace)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics",
    jsii_struct_bases=[],
    name_mapping={},
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c72efdf4d4afae2b2aebf66800f0430a57b6795265f5f8545891dd91e85957bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8302fda89a97d4dde8eb65f95f595cd29e6bcef4dfce7a083335923a5d1ebf25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo",
    jsii_struct_bases=[],
    name_mapping={"object": "object", "error_handling_config": "errorHandlingConfig"},
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo:
    def __init__(
        self,
        *,
        object: builtins.str,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        if isinstance(error_handling_config, dict):
            error_handling_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig(**error_handling_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9db131d1aba3c92118f52dc060e586d479ef45b2676e14180620f71a73f035a5)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }
        if error_handling_config is not None:
            self._values["error_handling_config"] = error_handling_config

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def error_handling_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig"]:
        '''error_handling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        result = self._values.get("error_handling_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "fail_on_first_destination_error": "failOnFirstDestinationError",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4257ebf29e7a19c0d94e29e2ab5634818f14f10c3a71240af3bedda6b0d6841)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument fail_on_first_destination_error", value=fail_on_first_destination_error, expected_type=type_hints["fail_on_first_destination_error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if fail_on_first_destination_error is not None:
            self._values["fail_on_first_destination_error"] = fail_on_first_destination_error

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_on_first_destination_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.'''
        result = self._values.get("fail_on_first_destination_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33edd82e5bed2dd02b3c41b76a293b208111ff76525c5a1f4ec69212f36497bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetFailOnFirstDestinationError")
    def reset_fail_on_first_destination_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOnFirstDestinationError", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationErrorInput")
    def fail_on_first_destination_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOnFirstDestinationErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4fcb8eea924d2da16d3ca07f6bc6bd829e98bf0d7ae970bef36b3a7db7d494e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0526fff870014c0e56079f321b096570b156be1a3addfe3b1ef824204f49fa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationError")
    def fail_on_first_destination_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOnFirstDestinationError"))

    @fail_on_first_destination_error.setter
    def fail_on_first_destination_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb47289fc157b763f5b3141186f105e1a2829af321b02cee2620fdccb967aa87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnFirstDestinationError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef325b4707970350e116516ee1166b4588c046b617d39fa1a90393d9b2bae770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec22d870d5d47a31ab4c4d2fa2f2ec6880c663b895b77b2dab1743d380df4504)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putErrorHandlingConfig")
    def put_error_handling_config(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            fail_on_first_destination_error=fail_on_first_destination_error,
        )

        return typing.cast(None, jsii.invoke(self, "putErrorHandlingConfig", [value]))

    @jsii.member(jsii_name="resetErrorHandlingConfig")
    def reset_error_handling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorHandlingConfig", []))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfig")
    def error_handling_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfigOutputReference, jsii.get(self, "errorHandlingConfig"))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfigInput")
    def error_handling_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig], jsii.get(self, "errorHandlingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b769f600fee0a4c91c2f929b966eb2eb557a665f26397e15b3e6121d1257c076)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d34e4e59452dd6b2556c987b8ea85802cc9f5287fbc01ba8f5ed0a117f44c9ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82f87e84fff61358d402884dd546a5c34b9b5b6430d23d9c4a65accd23ed7d92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomConnector")
    def put_custom_connector(
        self,
        *,
        entity_name: builtins.str,
        custom_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        write_operation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param entity_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#entity_name AppflowFlow#entity_name}.
        :param custom_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#custom_properties AppflowFlow#custom_properties}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        :param id_field_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.
        :param write_operation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector(
            entity_name=entity_name,
            custom_properties=custom_properties,
            error_handling_config=error_handling_config,
            id_field_names=id_field_names,
            write_operation_type=write_operation_type,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomConnector", [value]))

    @jsii.member(jsii_name="putCustomerProfiles")
    def put_customer_profiles(
        self,
        *,
        domain_name: builtins.str,
        object_type_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#domain_name AppflowFlow#domain_name}.
        :param object_type_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object_type_name AppflowFlow#object_type_name}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles(
            domain_name=domain_name, object_type_name=object_type_name
        )

        return typing.cast(None, jsii.invoke(self, "putCustomerProfiles", [value]))

    @jsii.member(jsii_name="putEventBridge")
    def put_event_bridge(
        self,
        *,
        object: builtins.str,
        error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge(
            object=object, error_handling_config=error_handling_config
        )

        return typing.cast(None, jsii.invoke(self, "putEventBridge", [value]))

    @jsii.member(jsii_name="putHoneycode")
    def put_honeycode(
        self,
        *,
        object: builtins.str,
        error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode(
            object=object, error_handling_config=error_handling_config
        )

        return typing.cast(None, jsii.invoke(self, "putHoneycode", [value]))

    @jsii.member(jsii_name="putLookoutMetrics")
    def put_lookout_metrics(self) -> None:
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics()

        return typing.cast(None, jsii.invoke(self, "putLookoutMetrics", [value]))

    @jsii.member(jsii_name="putMarketo")
    def put_marketo(
        self,
        *,
        object: builtins.str,
        error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo(
            object=object, error_handling_config=error_handling_config
        )

        return typing.cast(None, jsii.invoke(self, "putMarketo", [value]))

    @jsii.member(jsii_name="putRedshift")
    def put_redshift(
        self,
        *,
        intermediate_bucket_name: builtins.str,
        object: builtins.str,
        bucket_prefix: typing.Optional[builtins.str] = None,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param intermediate_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#intermediate_bucket_name AppflowFlow#intermediate_bucket_name}.
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift(
            intermediate_bucket_name=intermediate_bucket_name,
            object=object,
            bucket_prefix=bucket_prefix,
            error_handling_config=error_handling_config,
        )

        return typing.cast(None, jsii.invoke(self, "putRedshift", [value]))

    @jsii.member(jsii_name="putS3")
    def put_s3(
        self,
        *,
        bucket_name: builtins.str,
        bucket_prefix: typing.Optional[builtins.str] = None,
        s3_output_format_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param s3_output_format_config: s3_output_format_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#s3_output_format_config AppflowFlow#s3_output_format_config}
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            s3_output_format_config=s3_output_format_config,
        )

        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="putSalesforce")
    def put_salesforce(
        self,
        *,
        object: builtins.str,
        data_transfer_api: typing.Optional[builtins.str] = None,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        write_operation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param data_transfer_api: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#data_transfer_api AppflowFlow#data_transfer_api}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        :param id_field_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.
        :param write_operation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce(
            object=object,
            data_transfer_api=data_transfer_api,
            error_handling_config=error_handling_config,
            id_field_names=id_field_names,
            write_operation_type=write_operation_type,
        )

        return typing.cast(None, jsii.invoke(self, "putSalesforce", [value]))

    @jsii.member(jsii_name="putSapoData")
    def put_sapo_data(
        self,
        *,
        object_path: builtins.str,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        success_response_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        write_operation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object_path AppflowFlow#object_path}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        :param id_field_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.
        :param success_response_handling_config: success_response_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#success_response_handling_config AppflowFlow#success_response_handling_config}
        :param write_operation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData(
            object_path=object_path,
            error_handling_config=error_handling_config,
            id_field_names=id_field_names,
            success_response_handling_config=success_response_handling_config,
            write_operation_type=write_operation_type,
        )

        return typing.cast(None, jsii.invoke(self, "putSapoData", [value]))

    @jsii.member(jsii_name="putSnowflake")
    def put_snowflake(
        self,
        *,
        intermediate_bucket_name: builtins.str,
        object: builtins.str,
        bucket_prefix: typing.Optional[builtins.str] = None,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param intermediate_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#intermediate_bucket_name AppflowFlow#intermediate_bucket_name}.
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake(
            intermediate_bucket_name=intermediate_bucket_name,
            object=object,
            bucket_prefix=bucket_prefix,
            error_handling_config=error_handling_config,
        )

        return typing.cast(None, jsii.invoke(self, "putSnowflake", [value]))

    @jsii.member(jsii_name="putUpsolver")
    def put_upsolver(
        self,
        *,
        bucket_name: builtins.str,
        s3_output_format_config: typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig", typing.Dict[builtins.str, typing.Any]],
        bucket_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param s3_output_format_config: s3_output_format_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#s3_output_format_config AppflowFlow#s3_output_format_config}
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver(
            bucket_name=bucket_name,
            s3_output_format_config=s3_output_format_config,
            bucket_prefix=bucket_prefix,
        )

        return typing.cast(None, jsii.invoke(self, "putUpsolver", [value]))

    @jsii.member(jsii_name="putZendesk")
    def put_zendesk(
        self,
        *,
        object: builtins.str,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        write_operation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        :param id_field_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.
        :param write_operation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk(
            object=object,
            error_handling_config=error_handling_config,
            id_field_names=id_field_names,
            write_operation_type=write_operation_type,
        )

        return typing.cast(None, jsii.invoke(self, "putZendesk", [value]))

    @jsii.member(jsii_name="resetCustomConnector")
    def reset_custom_connector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomConnector", []))

    @jsii.member(jsii_name="resetCustomerProfiles")
    def reset_customer_profiles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerProfiles", []))

    @jsii.member(jsii_name="resetEventBridge")
    def reset_event_bridge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventBridge", []))

    @jsii.member(jsii_name="resetHoneycode")
    def reset_honeycode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHoneycode", []))

    @jsii.member(jsii_name="resetLookoutMetrics")
    def reset_lookout_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLookoutMetrics", []))

    @jsii.member(jsii_name="resetMarketo")
    def reset_marketo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMarketo", []))

    @jsii.member(jsii_name="resetRedshift")
    def reset_redshift(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedshift", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

    @jsii.member(jsii_name="resetSalesforce")
    def reset_salesforce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSalesforce", []))

    @jsii.member(jsii_name="resetSapoData")
    def reset_sapo_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSapoData", []))

    @jsii.member(jsii_name="resetSnowflake")
    def reset_snowflake(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnowflake", []))

    @jsii.member(jsii_name="resetUpsolver")
    def reset_upsolver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpsolver", []))

    @jsii.member(jsii_name="resetZendesk")
    def reset_zendesk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZendesk", []))

    @builtins.property
    @jsii.member(jsii_name="customConnector")
    def custom_connector(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorOutputReference, jsii.get(self, "customConnector"))

    @builtins.property
    @jsii.member(jsii_name="customerProfiles")
    def customer_profiles(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfilesOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfilesOutputReference, jsii.get(self, "customerProfiles"))

    @builtins.property
    @jsii.member(jsii_name="eventBridge")
    def event_bridge(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeOutputReference, jsii.get(self, "eventBridge"))

    @builtins.property
    @jsii.member(jsii_name="honeycode")
    def honeycode(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeOutputReference, jsii.get(self, "honeycode"))

    @builtins.property
    @jsii.member(jsii_name="lookoutMetrics")
    def lookout_metrics(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetricsOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetricsOutputReference, jsii.get(self, "lookoutMetrics"))

    @builtins.property
    @jsii.member(jsii_name="marketo")
    def marketo(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoOutputReference, jsii.get(self, "marketo"))

    @builtins.property
    @jsii.member(jsii_name="redshift")
    def redshift(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftOutputReference", jsii.get(self, "redshift"))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3OutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3OutputReference", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="salesforce")
    def salesforce(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceOutputReference", jsii.get(self, "salesforce"))

    @builtins.property
    @jsii.member(jsii_name="sapoData")
    def sapo_data(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataOutputReference", jsii.get(self, "sapoData"))

    @builtins.property
    @jsii.member(jsii_name="snowflake")
    def snowflake(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeOutputReference", jsii.get(self, "snowflake"))

    @builtins.property
    @jsii.member(jsii_name="upsolver")
    def upsolver(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverOutputReference", jsii.get(self, "upsolver"))

    @builtins.property
    @jsii.member(jsii_name="zendesk")
    def zendesk(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskOutputReference", jsii.get(self, "zendesk"))

    @builtins.property
    @jsii.member(jsii_name="customConnectorInput")
    def custom_connector_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector], jsii.get(self, "customConnectorInput"))

    @builtins.property
    @jsii.member(jsii_name="customerProfilesInput")
    def customer_profiles_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles], jsii.get(self, "customerProfilesInput"))

    @builtins.property
    @jsii.member(jsii_name="eventBridgeInput")
    def event_bridge_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge], jsii.get(self, "eventBridgeInput"))

    @builtins.property
    @jsii.member(jsii_name="honeycodeInput")
    def honeycode_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode], jsii.get(self, "honeycodeInput"))

    @builtins.property
    @jsii.member(jsii_name="lookoutMetricsInput")
    def lookout_metrics_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics], jsii.get(self, "lookoutMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="marketoInput")
    def marketo_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo], jsii.get(self, "marketoInput"))

    @builtins.property
    @jsii.member(jsii_name="redshiftInput")
    def redshift_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift"], jsii.get(self, "redshiftInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3"], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="salesforceInput")
    def salesforce_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce"], jsii.get(self, "salesforceInput"))

    @builtins.property
    @jsii.member(jsii_name="sapoDataInput")
    def sapo_data_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData"], jsii.get(self, "sapoDataInput"))

    @builtins.property
    @jsii.member(jsii_name="snowflakeInput")
    def snowflake_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake"], jsii.get(self, "snowflakeInput"))

    @builtins.property
    @jsii.member(jsii_name="upsolverInput")
    def upsolver_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver"], jsii.get(self, "upsolverInput"))

    @builtins.property
    @jsii.member(jsii_name="zendeskInput")
    def zendesk_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk"], jsii.get(self, "zendeskInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorProperties]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e824fac4774ef3cdb7a8c36c062cead1a5be4bb9062c7d76ed6c9b9bfce6ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift",
    jsii_struct_bases=[],
    name_mapping={
        "intermediate_bucket_name": "intermediateBucketName",
        "object": "object",
        "bucket_prefix": "bucketPrefix",
        "error_handling_config": "errorHandlingConfig",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift:
    def __init__(
        self,
        *,
        intermediate_bucket_name: builtins.str,
        object: builtins.str,
        bucket_prefix: typing.Optional[builtins.str] = None,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param intermediate_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#intermediate_bucket_name AppflowFlow#intermediate_bucket_name}.
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        if isinstance(error_handling_config, dict):
            error_handling_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig(**error_handling_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2998c6235e24a5d8d3745e1cdd7838c56230d7a3ee305e359d0cc5245118bf56)
            check_type(argname="argument intermediate_bucket_name", value=intermediate_bucket_name, expected_type=type_hints["intermediate_bucket_name"])
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "intermediate_bucket_name": intermediate_bucket_name,
            "object": object,
        }
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if error_handling_config is not None:
            self._values["error_handling_config"] = error_handling_config

    @builtins.property
    def intermediate_bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#intermediate_bucket_name AppflowFlow#intermediate_bucket_name}.'''
        result = self._values.get("intermediate_bucket_name")
        assert result is not None, "Required property 'intermediate_bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def error_handling_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig"]:
        '''error_handling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        result = self._values.get("error_handling_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "fail_on_first_destination_error": "failOnFirstDestinationError",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e2caf790073e375667fbcc3ed2d0bbe794889619c57ea897457f775be37147)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument fail_on_first_destination_error", value=fail_on_first_destination_error, expected_type=type_hints["fail_on_first_destination_error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if fail_on_first_destination_error is not None:
            self._values["fail_on_first_destination_error"] = fail_on_first_destination_error

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_on_first_destination_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.'''
        result = self._values.get("fail_on_first_destination_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bbbb7e91a4344f25e2d61e750d0d239e20cf544d07d0e63e3beec69cb543415)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetFailOnFirstDestinationError")
    def reset_fail_on_first_destination_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOnFirstDestinationError", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationErrorInput")
    def fail_on_first_destination_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOnFirstDestinationErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a5c9512258b07c43ba9efb2f61b5a5b34dd4159aec5c2b8ef2025afe648f2ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c717c92fc3cf2ba84a8f8fda1e8fea78a5b8e7b9843587ed1b33d53595df0f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationError")
    def fail_on_first_destination_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOnFirstDestinationError"))

    @fail_on_first_destination_error.setter
    def fail_on_first_destination_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30f2626bc0393f8c610bd40c18e3e6040e2921b7fc244b0c8b03ca2a4faa35ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnFirstDestinationError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17a19afe3f4fa6e1ada916f742d5d10f3a5a0818f4425c086ff9a3d319f62f17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e453869d325bbfe1af90b7ac0c577f326d3cb1c8a03efcaff5ad12c3b34399a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putErrorHandlingConfig")
    def put_error_handling_config(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            fail_on_first_destination_error=fail_on_first_destination_error,
        )

        return typing.cast(None, jsii.invoke(self, "putErrorHandlingConfig", [value]))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetErrorHandlingConfig")
    def reset_error_handling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorHandlingConfig", []))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfig")
    def error_handling_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfigOutputReference, jsii.get(self, "errorHandlingConfig"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfigInput")
    def error_handling_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig], jsii.get(self, "errorHandlingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="intermediateBucketNameInput")
    def intermediate_bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intermediateBucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17dc1b57ef79a273f3bcb714bbc64d6cd3da4f306e17d0e672f2c3b309a18f31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intermediateBucketName")
    def intermediate_bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intermediateBucketName"))

    @intermediate_bucket_name.setter
    def intermediate_bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__207ba1fad613c39aec2ce15f027200ee8f75d29c3b44962e7a731ab8e5c45324)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intermediateBucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e6868af5bb63edc2f5e10b787fb077f9bf0e931d73e9c80811215222ec3d444)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d0590c1a1ef75f56a9c8bdec6c90adab6d9af93b22fdd8e3d3908cf54412d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "s3_output_format_config": "s3OutputFormatConfig",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        bucket_prefix: typing.Optional[builtins.str] = None,
        s3_output_format_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param s3_output_format_config: s3_output_format_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#s3_output_format_config AppflowFlow#s3_output_format_config}
        '''
        if isinstance(s3_output_format_config, dict):
            s3_output_format_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig(**s3_output_format_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45f43f5913d99166a3f2b5c762e62bbc1584c64c779db89bdd5580bf9c05fdcc)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument s3_output_format_config", value=s3_output_format_config, expected_type=type_hints["s3_output_format_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
        }
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if s3_output_format_config is not None:
            self._values["s3_output_format_config"] = s3_output_format_config

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_output_format_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig"]:
        '''s3_output_format_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#s3_output_format_config AppflowFlow#s3_output_format_config}
        '''
        result = self._values.get("s3_output_format_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4552a09d923816d8ceee080019d44f8dc3433b2cf75f8eaf56abacf451b0d60f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putS3OutputFormatConfig")
    def put_s3_output_format_config(
        self,
        *,
        aggregation_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        file_type: typing.Optional[builtins.str] = None,
        prefix_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        preserve_source_data_typing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param aggregation_config: aggregation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#aggregation_config AppflowFlow#aggregation_config}
        :param file_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#file_type AppflowFlow#file_type}.
        :param prefix_config: prefix_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_config AppflowFlow#prefix_config}
        :param preserve_source_data_typing: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#preserve_source_data_typing AppflowFlow#preserve_source_data_typing}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig(
            aggregation_config=aggregation_config,
            file_type=file_type,
            prefix_config=prefix_config,
            preserve_source_data_typing=preserve_source_data_typing,
        )

        return typing.cast(None, jsii.invoke(self, "putS3OutputFormatConfig", [value]))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetS3OutputFormatConfig")
    def reset_s3_output_format_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3OutputFormatConfig", []))

    @builtins.property
    @jsii.member(jsii_name="s3OutputFormatConfig")
    def s3_output_format_config(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigOutputReference", jsii.get(self, "s3OutputFormatConfig"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="s3OutputFormatConfigInput")
    def s3_output_format_config_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig"], jsii.get(self, "s3OutputFormatConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f8258fcd5b37001b0ddaa9479f799deb68d7b58c90f1ca8df021b324701c316)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eafc90758f2a6432c65c9c78220fc3fd1232216bb3ff9aea86a551cb9ff282b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__296489d50976371ffd5805369138a7d0efbb1bf74711beeb236072f42549f5fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig",
    jsii_struct_bases=[],
    name_mapping={
        "aggregation_config": "aggregationConfig",
        "file_type": "fileType",
        "prefix_config": "prefixConfig",
        "preserve_source_data_typing": "preserveSourceDataTyping",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig:
    def __init__(
        self,
        *,
        aggregation_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        file_type: typing.Optional[builtins.str] = None,
        prefix_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        preserve_source_data_typing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param aggregation_config: aggregation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#aggregation_config AppflowFlow#aggregation_config}
        :param file_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#file_type AppflowFlow#file_type}.
        :param prefix_config: prefix_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_config AppflowFlow#prefix_config}
        :param preserve_source_data_typing: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#preserve_source_data_typing AppflowFlow#preserve_source_data_typing}.
        '''
        if isinstance(aggregation_config, dict):
            aggregation_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig(**aggregation_config)
        if isinstance(prefix_config, dict):
            prefix_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig(**prefix_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fa0759e8df962e4cbff933e2ca2accbfc56ba6b55c7352a5f5c325392ff25ee)
            check_type(argname="argument aggregation_config", value=aggregation_config, expected_type=type_hints["aggregation_config"])
            check_type(argname="argument file_type", value=file_type, expected_type=type_hints["file_type"])
            check_type(argname="argument prefix_config", value=prefix_config, expected_type=type_hints["prefix_config"])
            check_type(argname="argument preserve_source_data_typing", value=preserve_source_data_typing, expected_type=type_hints["preserve_source_data_typing"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aggregation_config is not None:
            self._values["aggregation_config"] = aggregation_config
        if file_type is not None:
            self._values["file_type"] = file_type
        if prefix_config is not None:
            self._values["prefix_config"] = prefix_config
        if preserve_source_data_typing is not None:
            self._values["preserve_source_data_typing"] = preserve_source_data_typing

    @builtins.property
    def aggregation_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig"]:
        '''aggregation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#aggregation_config AppflowFlow#aggregation_config}
        '''
        result = self._values.get("aggregation_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig"], result)

    @builtins.property
    def file_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#file_type AppflowFlow#file_type}.'''
        result = self._values.get("file_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig"]:
        '''prefix_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_config AppflowFlow#prefix_config}
        '''
        result = self._values.get("prefix_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig"], result)

    @builtins.property
    def preserve_source_data_typing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#preserve_source_data_typing AppflowFlow#preserve_source_data_typing}.'''
        result = self._values.get("preserve_source_data_typing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "aggregation_type": "aggregationType",
        "target_file_size": "targetFileSize",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig:
    def __init__(
        self,
        *,
        aggregation_type: typing.Optional[builtins.str] = None,
        target_file_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aggregation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#aggregation_type AppflowFlow#aggregation_type}.
        :param target_file_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#target_file_size AppflowFlow#target_file_size}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa4c52ac7281610eb52dca5db723134ac189f4e8fbffbc80f8976304fe7e992)
            check_type(argname="argument aggregation_type", value=aggregation_type, expected_type=type_hints["aggregation_type"])
            check_type(argname="argument target_file_size", value=target_file_size, expected_type=type_hints["target_file_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aggregation_type is not None:
            self._values["aggregation_type"] = aggregation_type
        if target_file_size is not None:
            self._values["target_file_size"] = target_file_size

    @builtins.property
    def aggregation_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#aggregation_type AppflowFlow#aggregation_type}.'''
        result = self._values.get("aggregation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_file_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#target_file_size AppflowFlow#target_file_size}.'''
        result = self._values.get("target_file_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af137783c628dc020711d7a44e8914cd297722de0a9cae2fa55b386c8096a10c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAggregationType")
    def reset_aggregation_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregationType", []))

    @jsii.member(jsii_name="resetTargetFileSize")
    def reset_target_file_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetFileSize", []))

    @builtins.property
    @jsii.member(jsii_name="aggregationTypeInput")
    def aggregation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aggregationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="targetFileSizeInput")
    def target_file_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetFileSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregationType")
    def aggregation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aggregationType"))

    @aggregation_type.setter
    def aggregation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eeb8620b7eea68f6358d5175d346b2888b836c0f07a8e2388a44da3d27f4296)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetFileSize")
    def target_file_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetFileSize"))

    @target_file_size.setter
    def target_file_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c3307fd6991d95b7cf0d6d306344a44727c3759c1b12de6dd1393322d4e65a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetFileSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea7393fbb96aa480f3300f6fbfb528a23dc69e65effc7c894d94d1d92c977cf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0bd65e3aaecf49c53b55c905a6ec07064c3fee0b123af6be676e44070564c80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAggregationConfig")
    def put_aggregation_config(
        self,
        *,
        aggregation_type: typing.Optional[builtins.str] = None,
        target_file_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aggregation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#aggregation_type AppflowFlow#aggregation_type}.
        :param target_file_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#target_file_size AppflowFlow#target_file_size}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig(
            aggregation_type=aggregation_type, target_file_size=target_file_size
        )

        return typing.cast(None, jsii.invoke(self, "putAggregationConfig", [value]))

    @jsii.member(jsii_name="putPrefixConfig")
    def put_prefix_config(
        self,
        *,
        prefix_format: typing.Optional[builtins.str] = None,
        prefix_hierarchy: typing.Optional[typing.Sequence[builtins.str]] = None,
        prefix_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param prefix_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_format AppflowFlow#prefix_format}.
        :param prefix_hierarchy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_hierarchy AppflowFlow#prefix_hierarchy}.
        :param prefix_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_type AppflowFlow#prefix_type}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig(
            prefix_format=prefix_format,
            prefix_hierarchy=prefix_hierarchy,
            prefix_type=prefix_type,
        )

        return typing.cast(None, jsii.invoke(self, "putPrefixConfig", [value]))

    @jsii.member(jsii_name="resetAggregationConfig")
    def reset_aggregation_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregationConfig", []))

    @jsii.member(jsii_name="resetFileType")
    def reset_file_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileType", []))

    @jsii.member(jsii_name="resetPrefixConfig")
    def reset_prefix_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixConfig", []))

    @jsii.member(jsii_name="resetPreserveSourceDataTyping")
    def reset_preserve_source_data_typing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreserveSourceDataTyping", []))

    @builtins.property
    @jsii.member(jsii_name="aggregationConfig")
    def aggregation_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfigOutputReference, jsii.get(self, "aggregationConfig"))

    @builtins.property
    @jsii.member(jsii_name="prefixConfig")
    def prefix_config(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfigOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfigOutputReference", jsii.get(self, "prefixConfig"))

    @builtins.property
    @jsii.member(jsii_name="aggregationConfigInput")
    def aggregation_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig], jsii.get(self, "aggregationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fileTypeInput")
    def file_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixConfigInput")
    def prefix_config_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig"], jsii.get(self, "prefixConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="preserveSourceDataTypingInput")
    def preserve_source_data_typing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preserveSourceDataTypingInput"))

    @builtins.property
    @jsii.member(jsii_name="fileType")
    def file_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileType"))

    @file_type.setter
    def file_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae6e83b85823aca9986c60da4b3c94e54a29a39a28c3bb8b8fb05ebdc6722161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preserveSourceDataTyping")
    def preserve_source_data_typing(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preserveSourceDataTyping"))

    @preserve_source_data_typing.setter
    def preserve_source_data_typing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b8dd5833e45a9b35a9206f4a9377829e21a72123e011a949ffb34a9f02f1730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preserveSourceDataTyping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__865fe35a2b23f0c60359386eea5f9cc6c93dcd95346ed691b2f3982362884429)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig",
    jsii_struct_bases=[],
    name_mapping={
        "prefix_format": "prefixFormat",
        "prefix_hierarchy": "prefixHierarchy",
        "prefix_type": "prefixType",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig:
    def __init__(
        self,
        *,
        prefix_format: typing.Optional[builtins.str] = None,
        prefix_hierarchy: typing.Optional[typing.Sequence[builtins.str]] = None,
        prefix_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param prefix_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_format AppflowFlow#prefix_format}.
        :param prefix_hierarchy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_hierarchy AppflowFlow#prefix_hierarchy}.
        :param prefix_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_type AppflowFlow#prefix_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa36ab04195c4d180938e0b836df2d4b8383afdeb5e124131b2f81d49bc68f64)
            check_type(argname="argument prefix_format", value=prefix_format, expected_type=type_hints["prefix_format"])
            check_type(argname="argument prefix_hierarchy", value=prefix_hierarchy, expected_type=type_hints["prefix_hierarchy"])
            check_type(argname="argument prefix_type", value=prefix_type, expected_type=type_hints["prefix_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if prefix_format is not None:
            self._values["prefix_format"] = prefix_format
        if prefix_hierarchy is not None:
            self._values["prefix_hierarchy"] = prefix_hierarchy
        if prefix_type is not None:
            self._values["prefix_type"] = prefix_type

    @builtins.property
    def prefix_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_format AppflowFlow#prefix_format}.'''
        result = self._values.get("prefix_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix_hierarchy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_hierarchy AppflowFlow#prefix_hierarchy}.'''
        result = self._values.get("prefix_hierarchy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def prefix_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_type AppflowFlow#prefix_type}.'''
        result = self._values.get("prefix_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6abb665f002c69be17a9eee436e8e9a41ad8cb198cec384374839630e6929b60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPrefixFormat")
    def reset_prefix_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixFormat", []))

    @jsii.member(jsii_name="resetPrefixHierarchy")
    def reset_prefix_hierarchy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixHierarchy", []))

    @jsii.member(jsii_name="resetPrefixType")
    def reset_prefix_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixType", []))

    @builtins.property
    @jsii.member(jsii_name="prefixFormatInput")
    def prefix_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixHierarchyInput")
    def prefix_hierarchy_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "prefixHierarchyInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixTypeInput")
    def prefix_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixFormat")
    def prefix_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixFormat"))

    @prefix_format.setter
    def prefix_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83931b9af1efc37e34d5b02fe6bcad8b0549e84cbb279ef51193301289e3a93c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixHierarchy")
    def prefix_hierarchy(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "prefixHierarchy"))

    @prefix_hierarchy.setter
    def prefix_hierarchy(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7a68a5fa12b6cc75bb47232ec2ee6f9d00fb3c5985a106b085b18184f162058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixHierarchy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixType")
    def prefix_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixType"))

    @prefix_type.setter
    def prefix_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3d60e37eee66ecbbdf12bac7a119dbc69f657e7a838b5648d603a3f6c68523e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8269df993070269d8b71d813c4b1620a2df1a700e2cb838f2a70df440fb1e79d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce",
    jsii_struct_bases=[],
    name_mapping={
        "object": "object",
        "data_transfer_api": "dataTransferApi",
        "error_handling_config": "errorHandlingConfig",
        "id_field_names": "idFieldNames",
        "write_operation_type": "writeOperationType",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce:
    def __init__(
        self,
        *,
        object: builtins.str,
        data_transfer_api: typing.Optional[builtins.str] = None,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        write_operation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param data_transfer_api: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#data_transfer_api AppflowFlow#data_transfer_api}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        :param id_field_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.
        :param write_operation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.
        '''
        if isinstance(error_handling_config, dict):
            error_handling_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig(**error_handling_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbfb838829ad1c2d6b3aefe6a50e75185e82ed0d3dbf9164d886602eccc7d94e)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument data_transfer_api", value=data_transfer_api, expected_type=type_hints["data_transfer_api"])
            check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
            check_type(argname="argument id_field_names", value=id_field_names, expected_type=type_hints["id_field_names"])
            check_type(argname="argument write_operation_type", value=write_operation_type, expected_type=type_hints["write_operation_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }
        if data_transfer_api is not None:
            self._values["data_transfer_api"] = data_transfer_api
        if error_handling_config is not None:
            self._values["error_handling_config"] = error_handling_config
        if id_field_names is not None:
            self._values["id_field_names"] = id_field_names
        if write_operation_type is not None:
            self._values["write_operation_type"] = write_operation_type

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_transfer_api(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#data_transfer_api AppflowFlow#data_transfer_api}.'''
        result = self._values.get("data_transfer_api")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def error_handling_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig"]:
        '''error_handling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        result = self._values.get("error_handling_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig"], result)

    @builtins.property
    def id_field_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.'''
        result = self._values.get("id_field_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def write_operation_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.'''
        result = self._values.get("write_operation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "fail_on_first_destination_error": "failOnFirstDestinationError",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48bda400473027f864eb05b987f0e1620ab774312d34c6e122e881cb4def3eff)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument fail_on_first_destination_error", value=fail_on_first_destination_error, expected_type=type_hints["fail_on_first_destination_error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if fail_on_first_destination_error is not None:
            self._values["fail_on_first_destination_error"] = fail_on_first_destination_error

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_on_first_destination_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.'''
        result = self._values.get("fail_on_first_destination_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef0c3b597924a5f3fc8528050a0c1e1878d819199a7d5e903fff53f92c781542)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetFailOnFirstDestinationError")
    def reset_fail_on_first_destination_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOnFirstDestinationError", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationErrorInput")
    def fail_on_first_destination_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOnFirstDestinationErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a586360e80e4b7dfa6eaf581c15a9727b7be450ea0bd7e4902b52b0b47bb9beb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78bd2ff3f392b2eadd9ef5af476e6d74fe9f9dc27a94986b4777127e30475633)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationError")
    def fail_on_first_destination_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOnFirstDestinationError"))

    @fail_on_first_destination_error.setter
    def fail_on_first_destination_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__165f01f3f715dc581f6a6039910e932bc24628843b24f303a01b09f443163cc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnFirstDestinationError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d33101f21186598962786ad718c32471f0e9e14f566e5469bcc51e9d0a907a53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae69e82b67d1ef5c40a73f734178538a882f0a9c961391aeaa0b3f589af49c03)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putErrorHandlingConfig")
    def put_error_handling_config(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            fail_on_first_destination_error=fail_on_first_destination_error,
        )

        return typing.cast(None, jsii.invoke(self, "putErrorHandlingConfig", [value]))

    @jsii.member(jsii_name="resetDataTransferApi")
    def reset_data_transfer_api(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataTransferApi", []))

    @jsii.member(jsii_name="resetErrorHandlingConfig")
    def reset_error_handling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorHandlingConfig", []))

    @jsii.member(jsii_name="resetIdFieldNames")
    def reset_id_field_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdFieldNames", []))

    @jsii.member(jsii_name="resetWriteOperationType")
    def reset_write_operation_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteOperationType", []))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfig")
    def error_handling_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfigOutputReference, jsii.get(self, "errorHandlingConfig"))

    @builtins.property
    @jsii.member(jsii_name="dataTransferApiInput")
    def data_transfer_api_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataTransferApiInput"))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfigInput")
    def error_handling_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig], jsii.get(self, "errorHandlingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idFieldNamesInput")
    def id_field_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "idFieldNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="writeOperationTypeInput")
    def write_operation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "writeOperationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="dataTransferApi")
    def data_transfer_api(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataTransferApi"))

    @data_transfer_api.setter
    def data_transfer_api(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff5f399d5e4a77f97fd67c87d1720d5795df226e7b349f47bb5392c3188e3c5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataTransferApi", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idFieldNames")
    def id_field_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "idFieldNames"))

    @id_field_names.setter
    def id_field_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be0d7b0ec82f5547ab04d75178e13e12d763c0c0375c95816865b913016f3f05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idFieldNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3901a04e10b8540bad830ba0606f196530cff0bcb9f84255ab6c8e8ab68e2232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writeOperationType")
    def write_operation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "writeOperationType"))

    @write_operation_type.setter
    def write_operation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7abea30eca838e33a3a8b67b577e19bbe5ccc5d66a199a4b6fd3a4520b1677a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeOperationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65c43313885a020e2404c8e7812e003276a241e64d99fc3aa7a410dab009c83b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData",
    jsii_struct_bases=[],
    name_mapping={
        "object_path": "objectPath",
        "error_handling_config": "errorHandlingConfig",
        "id_field_names": "idFieldNames",
        "success_response_handling_config": "successResponseHandlingConfig",
        "write_operation_type": "writeOperationType",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData:
    def __init__(
        self,
        *,
        object_path: builtins.str,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        success_response_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        write_operation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object_path AppflowFlow#object_path}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        :param id_field_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.
        :param success_response_handling_config: success_response_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#success_response_handling_config AppflowFlow#success_response_handling_config}
        :param write_operation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.
        '''
        if isinstance(error_handling_config, dict):
            error_handling_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig(**error_handling_config)
        if isinstance(success_response_handling_config, dict):
            success_response_handling_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig(**success_response_handling_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__251adbcaf115accdf370a59ddf68cbed0fb581993f05fa0189bb74ee49f60871)
            check_type(argname="argument object_path", value=object_path, expected_type=type_hints["object_path"])
            check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
            check_type(argname="argument id_field_names", value=id_field_names, expected_type=type_hints["id_field_names"])
            check_type(argname="argument success_response_handling_config", value=success_response_handling_config, expected_type=type_hints["success_response_handling_config"])
            check_type(argname="argument write_operation_type", value=write_operation_type, expected_type=type_hints["write_operation_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_path": object_path,
        }
        if error_handling_config is not None:
            self._values["error_handling_config"] = error_handling_config
        if id_field_names is not None:
            self._values["id_field_names"] = id_field_names
        if success_response_handling_config is not None:
            self._values["success_response_handling_config"] = success_response_handling_config
        if write_operation_type is not None:
            self._values["write_operation_type"] = write_operation_type

    @builtins.property
    def object_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object_path AppflowFlow#object_path}.'''
        result = self._values.get("object_path")
        assert result is not None, "Required property 'object_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def error_handling_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig"]:
        '''error_handling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        result = self._values.get("error_handling_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig"], result)

    @builtins.property
    def id_field_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.'''
        result = self._values.get("id_field_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def success_response_handling_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig"]:
        '''success_response_handling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#success_response_handling_config AppflowFlow#success_response_handling_config}
        '''
        result = self._values.get("success_response_handling_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig"], result)

    @builtins.property
    def write_operation_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.'''
        result = self._values.get("write_operation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "fail_on_first_destination_error": "failOnFirstDestinationError",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aa6294163d3900521af7707bed89c87ae87d8e87ff2f9d599253f6042586f27)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument fail_on_first_destination_error", value=fail_on_first_destination_error, expected_type=type_hints["fail_on_first_destination_error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if fail_on_first_destination_error is not None:
            self._values["fail_on_first_destination_error"] = fail_on_first_destination_error

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_on_first_destination_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.'''
        result = self._values.get("fail_on_first_destination_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32ca68e0cb4e6268b17c1a17d70c99aec84d4654f85524e910368ce5a87de993)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetFailOnFirstDestinationError")
    def reset_fail_on_first_destination_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOnFirstDestinationError", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationErrorInput")
    def fail_on_first_destination_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOnFirstDestinationErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abf962a3bdccfd60a1326a7d2cb30da10786f436bbb3393cc075c42020b7c09b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c5066bea2d20a3d0d87beca4eb15f1f2bc0b16d1e1e1dbf8ddb3cb5d0a9af81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationError")
    def fail_on_first_destination_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOnFirstDestinationError"))

    @fail_on_first_destination_error.setter
    def fail_on_first_destination_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f2ce5f9ab72d619bf08253460b2e3a8a0cec8b4b0cc0355a77629b398bdff98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnFirstDestinationError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f458ee004c008c1f02382f751f97c31dcf725ba833baaafc28762623548ae6a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ff8c724f4dec7e4497336d391b24af8e072b3b036a611855e3ada0555ed0ac2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putErrorHandlingConfig")
    def put_error_handling_config(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            fail_on_first_destination_error=fail_on_first_destination_error,
        )

        return typing.cast(None, jsii.invoke(self, "putErrorHandlingConfig", [value]))

    @jsii.member(jsii_name="putSuccessResponseHandlingConfig")
    def put_success_response_handling_config(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig(
            bucket_name=bucket_name, bucket_prefix=bucket_prefix
        )

        return typing.cast(None, jsii.invoke(self, "putSuccessResponseHandlingConfig", [value]))

    @jsii.member(jsii_name="resetErrorHandlingConfig")
    def reset_error_handling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorHandlingConfig", []))

    @jsii.member(jsii_name="resetIdFieldNames")
    def reset_id_field_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdFieldNames", []))

    @jsii.member(jsii_name="resetSuccessResponseHandlingConfig")
    def reset_success_response_handling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuccessResponseHandlingConfig", []))

    @jsii.member(jsii_name="resetWriteOperationType")
    def reset_write_operation_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteOperationType", []))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfig")
    def error_handling_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfigOutputReference, jsii.get(self, "errorHandlingConfig"))

    @builtins.property
    @jsii.member(jsii_name="successResponseHandlingConfig")
    def success_response_handling_config(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfigOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfigOutputReference", jsii.get(self, "successResponseHandlingConfig"))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfigInput")
    def error_handling_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig], jsii.get(self, "errorHandlingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idFieldNamesInput")
    def id_field_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "idFieldNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="objectPathInput")
    def object_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectPathInput"))

    @builtins.property
    @jsii.member(jsii_name="successResponseHandlingConfigInput")
    def success_response_handling_config_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig"], jsii.get(self, "successResponseHandlingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="writeOperationTypeInput")
    def write_operation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "writeOperationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idFieldNames")
    def id_field_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "idFieldNames"))

    @id_field_names.setter
    def id_field_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a029996b37b1cf0f0a72487d96ef50f5e27cfd3a004f426d488e34a06d9a4d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idFieldNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectPath")
    def object_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectPath"))

    @object_path.setter
    def object_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25f9f32a8726ef528f92964b1278dc2cfc6231dac42582fa33a95d9b7fdf9b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writeOperationType")
    def write_operation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "writeOperationType"))

    @write_operation_type.setter
    def write_operation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c108fbaa82873cc069db155124251116a7ef93e1645001c61122ab64afc82774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeOperationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06109fa729294a121c2c71a5ab326eb769f81e4f7af49ad79e93c9f414b3eac8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig",
    jsii_struct_bases=[],
    name_mapping={"bucket_name": "bucketName", "bucket_prefix": "bucketPrefix"},
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd1eaa6977aa6597d0c24eee2faa18d9955ed9b2ba09fee60c8a563b4cafe8e)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66997c4d669586ec4e11f0f43a547e72573c6a4745c60420a25e4a098a339acf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba42a6b195fb21cf699c21eaffd8509356ab6ca0d8ae672febe4b5fdac2e88b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ca612d9ec16c1c2e35c123d32a1f10b2ddd148fa01fb3e793b09b61e2f92ed6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6c02e43bb4ee3dd03d8aa2d567a415f2a3ffb2179e405f745dfbf4042dd201c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake",
    jsii_struct_bases=[],
    name_mapping={
        "intermediate_bucket_name": "intermediateBucketName",
        "object": "object",
        "bucket_prefix": "bucketPrefix",
        "error_handling_config": "errorHandlingConfig",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake:
    def __init__(
        self,
        *,
        intermediate_bucket_name: builtins.str,
        object: builtins.str,
        bucket_prefix: typing.Optional[builtins.str] = None,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param intermediate_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#intermediate_bucket_name AppflowFlow#intermediate_bucket_name}.
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        if isinstance(error_handling_config, dict):
            error_handling_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig(**error_handling_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc82d02c7d10e51ea422c66aa600d706531c12d3a13405b9aff11de584797a8)
            check_type(argname="argument intermediate_bucket_name", value=intermediate_bucket_name, expected_type=type_hints["intermediate_bucket_name"])
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "intermediate_bucket_name": intermediate_bucket_name,
            "object": object,
        }
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if error_handling_config is not None:
            self._values["error_handling_config"] = error_handling_config

    @builtins.property
    def intermediate_bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#intermediate_bucket_name AppflowFlow#intermediate_bucket_name}.'''
        result = self._values.get("intermediate_bucket_name")
        assert result is not None, "Required property 'intermediate_bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def error_handling_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig"]:
        '''error_handling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        result = self._values.get("error_handling_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "fail_on_first_destination_error": "failOnFirstDestinationError",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__876873e3d46d1a8c9e95997c0e7d6c83d3da783f23800a4e720b929caac0692c)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument fail_on_first_destination_error", value=fail_on_first_destination_error, expected_type=type_hints["fail_on_first_destination_error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if fail_on_first_destination_error is not None:
            self._values["fail_on_first_destination_error"] = fail_on_first_destination_error

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_on_first_destination_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.'''
        result = self._values.get("fail_on_first_destination_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cd91f5d6e439184e5434c482dcac6f8a0cc0be51ad6f23ee2c3f67f83bbf629)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetFailOnFirstDestinationError")
    def reset_fail_on_first_destination_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOnFirstDestinationError", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationErrorInput")
    def fail_on_first_destination_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOnFirstDestinationErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f410c6ff8d976e1d3b7f111cace6ec79a6ad714d8f7070f10dfc3394ebc0a2ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6df876a0ecd0aaa03e831996e91e1a89fbd881c2d9f97b708ad8ff65254212d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationError")
    def fail_on_first_destination_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOnFirstDestinationError"))

    @fail_on_first_destination_error.setter
    def fail_on_first_destination_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ee256d771383cfab6745ecb6f209487260288e05d9ea1330eb65fb7bbb88bc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnFirstDestinationError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed69e7329c1493801571c3ab90e56f33c8c753b342db0c43fb254906e3041ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9e728a7e04df3a972a8df4a28bd33609f29379a920a43383a7f164e1a25a9ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putErrorHandlingConfig")
    def put_error_handling_config(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            fail_on_first_destination_error=fail_on_first_destination_error,
        )

        return typing.cast(None, jsii.invoke(self, "putErrorHandlingConfig", [value]))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetErrorHandlingConfig")
    def reset_error_handling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorHandlingConfig", []))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfig")
    def error_handling_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfigOutputReference, jsii.get(self, "errorHandlingConfig"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfigInput")
    def error_handling_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig], jsii.get(self, "errorHandlingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="intermediateBucketNameInput")
    def intermediate_bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intermediateBucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4d9d2d8e00b6949813ea762780d7adb0beaee923eef0d1eda9c237f2512579e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intermediateBucketName")
    def intermediate_bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intermediateBucketName"))

    @intermediate_bucket_name.setter
    def intermediate_bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ea172f3364a4faae7e9804aed68a94f982608153aa1960fd653422bfc65afa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intermediateBucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f88936428fffc57a7036c2265cf03912e9ffddc1c3274281054cd7181365265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef73ecbfcfa2edb228c4517557337c24f0cd43f2471a42bacb08eb3b09b1d871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "s3_output_format_config": "s3OutputFormatConfig",
        "bucket_prefix": "bucketPrefix",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        s3_output_format_config: typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig", typing.Dict[builtins.str, typing.Any]],
        bucket_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param s3_output_format_config: s3_output_format_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#s3_output_format_config AppflowFlow#s3_output_format_config}
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        '''
        if isinstance(s3_output_format_config, dict):
            s3_output_format_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig(**s3_output_format_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f681a04bf940e20318455a901144c1d9001191d2e13c6ac899b4a481be40d8)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument s3_output_format_config", value=s3_output_format_config, expected_type=type_hints["s3_output_format_config"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "s3_output_format_config": s3_output_format_config,
        }
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_output_format_config(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig":
        '''s3_output_format_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#s3_output_format_config AppflowFlow#s3_output_format_config}
        '''
        result = self._values.get("s3_output_format_config")
        assert result is not None, "Required property 's3_output_format_config' is missing"
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig", result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79fe804a02529d41a0dc619ca0f5ac998ea105fb9a930002a6ab24c14cf084c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putS3OutputFormatConfig")
    def put_s3_output_format_config(
        self,
        *,
        prefix_config: typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig", typing.Dict[builtins.str, typing.Any]],
        aggregation_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        file_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param prefix_config: prefix_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_config AppflowFlow#prefix_config}
        :param aggregation_config: aggregation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#aggregation_config AppflowFlow#aggregation_config}
        :param file_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#file_type AppflowFlow#file_type}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig(
            prefix_config=prefix_config,
            aggregation_config=aggregation_config,
            file_type=file_type,
        )

        return typing.cast(None, jsii.invoke(self, "putS3OutputFormatConfig", [value]))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="s3OutputFormatConfig")
    def s3_output_format_config(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigOutputReference", jsii.get(self, "s3OutputFormatConfig"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="s3OutputFormatConfigInput")
    def s3_output_format_config_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig"], jsii.get(self, "s3OutputFormatConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46cff562a668c3653bd9109460182040a9dbd04f706a74e91f7cfdf53594ede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a975e2a28a8a1dab4eba394f899b86e1ccf2e1957b8b3aeae3402ede227e7689)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b5eb7b5389120b7f9a99a18ede5f31becb003cf9d48828035d51008956174a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig",
    jsii_struct_bases=[],
    name_mapping={
        "prefix_config": "prefixConfig",
        "aggregation_config": "aggregationConfig",
        "file_type": "fileType",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig:
    def __init__(
        self,
        *,
        prefix_config: typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig", typing.Dict[builtins.str, typing.Any]],
        aggregation_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        file_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param prefix_config: prefix_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_config AppflowFlow#prefix_config}
        :param aggregation_config: aggregation_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#aggregation_config AppflowFlow#aggregation_config}
        :param file_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#file_type AppflowFlow#file_type}.
        '''
        if isinstance(prefix_config, dict):
            prefix_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig(**prefix_config)
        if isinstance(aggregation_config, dict):
            aggregation_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig(**aggregation_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c4d5142335176ce61cba0ccee376c4314e37d97c86f72b8c2b24d7280d63e0d)
            check_type(argname="argument prefix_config", value=prefix_config, expected_type=type_hints["prefix_config"])
            check_type(argname="argument aggregation_config", value=aggregation_config, expected_type=type_hints["aggregation_config"])
            check_type(argname="argument file_type", value=file_type, expected_type=type_hints["file_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "prefix_config": prefix_config,
        }
        if aggregation_config is not None:
            self._values["aggregation_config"] = aggregation_config
        if file_type is not None:
            self._values["file_type"] = file_type

    @builtins.property
    def prefix_config(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig":
        '''prefix_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_config AppflowFlow#prefix_config}
        '''
        result = self._values.get("prefix_config")
        assert result is not None, "Required property 'prefix_config' is missing"
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig", result)

    @builtins.property
    def aggregation_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig"]:
        '''aggregation_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#aggregation_config AppflowFlow#aggregation_config}
        '''
        result = self._values.get("aggregation_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig"], result)

    @builtins.property
    def file_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#file_type AppflowFlow#file_type}.'''
        result = self._values.get("file_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig",
    jsii_struct_bases=[],
    name_mapping={"aggregation_type": "aggregationType"},
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig:
    def __init__(
        self,
        *,
        aggregation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aggregation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#aggregation_type AppflowFlow#aggregation_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b17dd36a4adceef7cb25245112cf4d6c2769115e4a07ef785496c908bb22fd11)
            check_type(argname="argument aggregation_type", value=aggregation_type, expected_type=type_hints["aggregation_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aggregation_type is not None:
            self._values["aggregation_type"] = aggregation_type

    @builtins.property
    def aggregation_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#aggregation_type AppflowFlow#aggregation_type}.'''
        result = self._values.get("aggregation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06a6a7335f60368166d727a37fe617b8455f7d8932a8625334820cf8d7b015c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAggregationType")
    def reset_aggregation_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregationType", []))

    @builtins.property
    @jsii.member(jsii_name="aggregationTypeInput")
    def aggregation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aggregationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregationType")
    def aggregation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aggregationType"))

    @aggregation_type.setter
    def aggregation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aef540ee20b13dd22f36c9af55061bfb490026e2a195dfae43c8166ba097723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a0c7dd466e2e9d6565fa6e964246b65fc31621dcd0b6a5666e5c439b5ec3d65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5c6fd0aef3e123e08decf0dfd2f95b4fd7474bd170ab14f7f9af3e08c9ebd9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAggregationConfig")
    def put_aggregation_config(
        self,
        *,
        aggregation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aggregation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#aggregation_type AppflowFlow#aggregation_type}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig(
            aggregation_type=aggregation_type
        )

        return typing.cast(None, jsii.invoke(self, "putAggregationConfig", [value]))

    @jsii.member(jsii_name="putPrefixConfig")
    def put_prefix_config(
        self,
        *,
        prefix_type: builtins.str,
        prefix_format: typing.Optional[builtins.str] = None,
        prefix_hierarchy: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param prefix_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_type AppflowFlow#prefix_type}.
        :param prefix_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_format AppflowFlow#prefix_format}.
        :param prefix_hierarchy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_hierarchy AppflowFlow#prefix_hierarchy}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig(
            prefix_type=prefix_type,
            prefix_format=prefix_format,
            prefix_hierarchy=prefix_hierarchy,
        )

        return typing.cast(None, jsii.invoke(self, "putPrefixConfig", [value]))

    @jsii.member(jsii_name="resetAggregationConfig")
    def reset_aggregation_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregationConfig", []))

    @jsii.member(jsii_name="resetFileType")
    def reset_file_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileType", []))

    @builtins.property
    @jsii.member(jsii_name="aggregationConfig")
    def aggregation_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfigOutputReference, jsii.get(self, "aggregationConfig"))

    @builtins.property
    @jsii.member(jsii_name="prefixConfig")
    def prefix_config(
        self,
    ) -> "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfigOutputReference":
        return typing.cast("AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfigOutputReference", jsii.get(self, "prefixConfig"))

    @builtins.property
    @jsii.member(jsii_name="aggregationConfigInput")
    def aggregation_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig], jsii.get(self, "aggregationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fileTypeInput")
    def file_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixConfigInput")
    def prefix_config_input(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig"]:
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig"], jsii.get(self, "prefixConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="fileType")
    def file_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileType"))

    @file_type.setter
    def file_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b988e6b6481f3bc5ce4db01a6435c0d8ae928d8a237df65e63d8958733d41ede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71657a7cffe7a16daada8bd3e9f484be889ff952f7b24556d84af74a12a95ba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig",
    jsii_struct_bases=[],
    name_mapping={
        "prefix_type": "prefixType",
        "prefix_format": "prefixFormat",
        "prefix_hierarchy": "prefixHierarchy",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig:
    def __init__(
        self,
        *,
        prefix_type: builtins.str,
        prefix_format: typing.Optional[builtins.str] = None,
        prefix_hierarchy: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param prefix_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_type AppflowFlow#prefix_type}.
        :param prefix_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_format AppflowFlow#prefix_format}.
        :param prefix_hierarchy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_hierarchy AppflowFlow#prefix_hierarchy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63b1671bc997f60dacfa21d736714a13eab0d3a5b11eb9fff13599c1ed63d56c)
            check_type(argname="argument prefix_type", value=prefix_type, expected_type=type_hints["prefix_type"])
            check_type(argname="argument prefix_format", value=prefix_format, expected_type=type_hints["prefix_format"])
            check_type(argname="argument prefix_hierarchy", value=prefix_hierarchy, expected_type=type_hints["prefix_hierarchy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "prefix_type": prefix_type,
        }
        if prefix_format is not None:
            self._values["prefix_format"] = prefix_format
        if prefix_hierarchy is not None:
            self._values["prefix_hierarchy"] = prefix_hierarchy

    @builtins.property
    def prefix_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_type AppflowFlow#prefix_type}.'''
        result = self._values.get("prefix_type")
        assert result is not None, "Required property 'prefix_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_format AppflowFlow#prefix_format}.'''
        result = self._values.get("prefix_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix_hierarchy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#prefix_hierarchy AppflowFlow#prefix_hierarchy}.'''
        result = self._values.get("prefix_hierarchy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b07a649f9eb2ece4add17ce3de3f562d96928520bd1276d6015d622135f55571)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPrefixFormat")
    def reset_prefix_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixFormat", []))

    @jsii.member(jsii_name="resetPrefixHierarchy")
    def reset_prefix_hierarchy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixHierarchy", []))

    @builtins.property
    @jsii.member(jsii_name="prefixFormatInput")
    def prefix_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixHierarchyInput")
    def prefix_hierarchy_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "prefixHierarchyInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixTypeInput")
    def prefix_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixFormat")
    def prefix_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixFormat"))

    @prefix_format.setter
    def prefix_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc71f39bb7cf02bc1321cb9d3c5775441346b695ee660554ab8436732a7b32e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixHierarchy")
    def prefix_hierarchy(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "prefixHierarchy"))

    @prefix_hierarchy.setter
    def prefix_hierarchy(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__035f6b98ce5d0b9d7190001beb1219dd075becd7e46c9d6eb9d3fe8c07b2a6c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixHierarchy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixType")
    def prefix_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixType"))

    @prefix_type.setter
    def prefix_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2574c5b9fae860cdfb9b0c41f84df9abcd385ee4e0ae226d7d593b0a77df67d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8dbce57537f4472c4806fe02e6be87901dca2637cfb07aee24d220051f4e958)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk",
    jsii_struct_bases=[],
    name_mapping={
        "object": "object",
        "error_handling_config": "errorHandlingConfig",
        "id_field_names": "idFieldNames",
        "write_operation_type": "writeOperationType",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk:
    def __init__(
        self,
        *,
        object: builtins.str,
        error_handling_config: typing.Optional[typing.Union["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        write_operation_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param error_handling_config: error_handling_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        :param id_field_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.
        :param write_operation_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.
        '''
        if isinstance(error_handling_config, dict):
            error_handling_config = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig(**error_handling_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33afecc984c225c7885ef1523a5e48ca261c9baebca9343239f2ee6fb8310eee)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument error_handling_config", value=error_handling_config, expected_type=type_hints["error_handling_config"])
            check_type(argname="argument id_field_names", value=id_field_names, expected_type=type_hints["id_field_names"])
            check_type(argname="argument write_operation_type", value=write_operation_type, expected_type=type_hints["write_operation_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }
        if error_handling_config is not None:
            self._values["error_handling_config"] = error_handling_config
        if id_field_names is not None:
            self._values["id_field_names"] = id_field_names
        if write_operation_type is not None:
            self._values["write_operation_type"] = write_operation_type

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def error_handling_config(
        self,
    ) -> typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig"]:
        '''error_handling_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#error_handling_config AppflowFlow#error_handling_config}
        '''
        result = self._values.get("error_handling_config")
        return typing.cast(typing.Optional["AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig"], result)

    @builtins.property
    def id_field_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#id_field_names AppflowFlow#id_field_names}.'''
        result = self._values.get("id_field_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def write_operation_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#write_operation_type AppflowFlow#write_operation_type}.'''
        result = self._values.get("write_operation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "fail_on_first_destination_error": "failOnFirstDestinationError",
    },
)
class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01d1583e6540424517d44187f62b3440c9eb598fb2188155eeae76102553c7d7)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument fail_on_first_destination_error", value=fail_on_first_destination_error, expected_type=type_hints["fail_on_first_destination_error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if fail_on_first_destination_error is not None:
            self._values["fail_on_first_destination_error"] = fail_on_first_destination_error

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_on_first_destination_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.'''
        result = self._values.get("fail_on_first_destination_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89af6f358d766f47c708cf3d6f5dd4f09f16065d232e351ceeaa289c8a1cb20a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetBucketPrefix")
    def reset_bucket_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketPrefix", []))

    @jsii.member(jsii_name="resetFailOnFirstDestinationError")
    def reset_fail_on_first_destination_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailOnFirstDestinationError", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationErrorInput")
    def fail_on_first_destination_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failOnFirstDestinationErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9b5888034791753fe87f581d96e7026f19281774d304d989a938de5ad2b7d91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3e558b34782777e52e52ec048a985131293e6230fce5c1e6d69cbc45c33895d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failOnFirstDestinationError")
    def fail_on_first_destination_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failOnFirstDestinationError"))

    @fail_on_first_destination_error.setter
    def fail_on_first_destination_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__008105574581aa7753dc43a1d16232f55982ea6af590d5ab863149701766dcce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failOnFirstDestinationError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d2e0e1aa603776cb110b224f5d245aed131259ef34a55fa92b49c33d22cc884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be29dcead5e24d5d1491bfb6942fce6627b15960ac6bca786d0121d338f88a59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putErrorHandlingConfig")
    def put_error_handling_config(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param fail_on_first_destination_error: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#fail_on_first_destination_error AppflowFlow#fail_on_first_destination_error}.
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            fail_on_first_destination_error=fail_on_first_destination_error,
        )

        return typing.cast(None, jsii.invoke(self, "putErrorHandlingConfig", [value]))

    @jsii.member(jsii_name="resetErrorHandlingConfig")
    def reset_error_handling_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorHandlingConfig", []))

    @jsii.member(jsii_name="resetIdFieldNames")
    def reset_id_field_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdFieldNames", []))

    @jsii.member(jsii_name="resetWriteOperationType")
    def reset_write_operation_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteOperationType", []))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfig")
    def error_handling_config(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfigOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfigOutputReference, jsii.get(self, "errorHandlingConfig"))

    @builtins.property
    @jsii.member(jsii_name="errorHandlingConfigInput")
    def error_handling_config_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig], jsii.get(self, "errorHandlingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idFieldNamesInput")
    def id_field_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "idFieldNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="writeOperationTypeInput")
    def write_operation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "writeOperationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idFieldNames")
    def id_field_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "idFieldNames"))

    @id_field_names.setter
    def id_field_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1abf87819595367018fd360edc3a596cbc522f97ceb9d87ea42575654a8cc26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idFieldNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c879c46304fa4c6a01f77ab340e9d332f85551d377afeb29c82c5ee9d71a43fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writeOperationType")
    def write_operation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "writeOperationType"))

    @write_operation_type.setter
    def write_operation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e08f103266bc74de2b274498ea27d4b81bd79fca3f6b26187440ff57bce382d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeOperationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e676292209be63a9a1d3bcb318ce8fe9110095583ec7febf34d1ce1f9950d8cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__041957e2dabe38c394abf7b53a9e72ced1c6d838fb14d875b454f80d3e79fb02)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppflowFlowDestinationFlowConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69d56ebf26ebc6b6ffec761d4f376eb5db238930c2475badb65099644f73a186)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppflowFlowDestinationFlowConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d7fda571fb1fce7c65854dc39ef5eca5ee46131cc850b51d33b2f557e82ad6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__613e89916dd62dba1b0e4e252abae48dc6a93019c7219b698fc242eada2fc396)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7957d7fd3ed112e39900d7530f748fc6fbc01c38f369b5d6dd9ad4c775c04ab9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowDestinationFlowConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowDestinationFlowConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowDestinationFlowConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e8e0cf58fc0cdaee76fbc3913d2f8a9210900ea227439149721b6a12dbfcf54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowDestinationFlowConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowDestinationFlowConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf3af0ef93758ec2b16a29bb5e93bb4ef75af2a37e85427f307ae5719324a16c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDestinationConnectorProperties")
    def put_destination_connector_properties(
        self,
        *,
        custom_connector: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector, typing.Dict[builtins.str, typing.Any]]] = None,
        customer_profiles: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles, typing.Dict[builtins.str, typing.Any]]] = None,
        event_bridge: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge, typing.Dict[builtins.str, typing.Any]]] = None,
        honeycode: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode, typing.Dict[builtins.str, typing.Any]]] = None,
        lookout_metrics: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
        marketo: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo, typing.Dict[builtins.str, typing.Any]]] = None,
        redshift: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift, typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3, typing.Dict[builtins.str, typing.Any]]] = None,
        salesforce: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce, typing.Dict[builtins.str, typing.Any]]] = None,
        sapo_data: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData, typing.Dict[builtins.str, typing.Any]]] = None,
        snowflake: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake, typing.Dict[builtins.str, typing.Any]]] = None,
        upsolver: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver, typing.Dict[builtins.str, typing.Any]]] = None,
        zendesk: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_connector: custom_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#custom_connector AppflowFlow#custom_connector}
        :param customer_profiles: customer_profiles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#customer_profiles AppflowFlow#customer_profiles}
        :param event_bridge: event_bridge block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#event_bridge AppflowFlow#event_bridge}
        :param honeycode: honeycode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#honeycode AppflowFlow#honeycode}
        :param lookout_metrics: lookout_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#lookout_metrics AppflowFlow#lookout_metrics}
        :param marketo: marketo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#marketo AppflowFlow#marketo}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#redshift AppflowFlow#redshift}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#s3 AppflowFlow#s3}
        :param salesforce: salesforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#salesforce AppflowFlow#salesforce}
        :param sapo_data: sapo_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#sapo_data AppflowFlow#sapo_data}
        :param snowflake: snowflake block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#snowflake AppflowFlow#snowflake}
        :param upsolver: upsolver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#upsolver AppflowFlow#upsolver}
        :param zendesk: zendesk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#zendesk AppflowFlow#zendesk}
        '''
        value = AppflowFlowDestinationFlowConfigDestinationConnectorProperties(
            custom_connector=custom_connector,
            customer_profiles=customer_profiles,
            event_bridge=event_bridge,
            honeycode=honeycode,
            lookout_metrics=lookout_metrics,
            marketo=marketo,
            redshift=redshift,
            s3=s3,
            salesforce=salesforce,
            sapo_data=sapo_data,
            snowflake=snowflake,
            upsolver=upsolver,
            zendesk=zendesk,
        )

        return typing.cast(None, jsii.invoke(self, "putDestinationConnectorProperties", [value]))

    @jsii.member(jsii_name="resetApiVersion")
    def reset_api_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiVersion", []))

    @jsii.member(jsii_name="resetConnectorProfileName")
    def reset_connector_profile_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectorProfileName", []))

    @builtins.property
    @jsii.member(jsii_name="destinationConnectorProperties")
    def destination_connector_properties(
        self,
    ) -> AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesOutputReference:
        return typing.cast(AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesOutputReference, jsii.get(self, "destinationConnectorProperties"))

    @builtins.property
    @jsii.member(jsii_name="apiVersionInput")
    def api_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorProfileNameInput")
    def connector_profile_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorProfileNameInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorTypeInput")
    def connector_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationConnectorPropertiesInput")
    def destination_connector_properties_input(
        self,
    ) -> typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorProperties]:
        return typing.cast(typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorProperties], jsii.get(self, "destinationConnectorPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="apiVersion")
    def api_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiVersion"))

    @api_version.setter
    def api_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c4963312c3c56a2241dafde30d31ad85b24e3de9316da5679ed7dc8bd2f588)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectorProfileName")
    def connector_profile_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorProfileName"))

    @connector_profile_name.setter
    def connector_profile_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22114fb338cec54cdca84355c1f6ba454053f8b3816a17fced09913e61225988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorProfileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectorType")
    def connector_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorType"))

    @connector_type.setter
    def connector_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d3a3ebeae9ba7962f29dffb6331b28554ba543f0cca43d4fca0c8858935263b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowDestinationFlowConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowDestinationFlowConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowDestinationFlowConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b1701cd4a4564475b6acf861719a8938dde2b54d0f9918fa74e9ec7eea59891)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowMetadataCatalogConfig",
    jsii_struct_bases=[],
    name_mapping={"glue_data_catalog": "glueDataCatalog"},
)
class AppflowFlowMetadataCatalogConfig:
    def __init__(
        self,
        *,
        glue_data_catalog: typing.Optional[typing.Union["AppflowFlowMetadataCatalogConfigGlueDataCatalog", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param glue_data_catalog: glue_data_catalog block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#glue_data_catalog AppflowFlow#glue_data_catalog}
        '''
        if isinstance(glue_data_catalog, dict):
            glue_data_catalog = AppflowFlowMetadataCatalogConfigGlueDataCatalog(**glue_data_catalog)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55c0d08d8622f2e2e56e6ac5fadb071c91296540d108a875c87eddaf43e65cda)
            check_type(argname="argument glue_data_catalog", value=glue_data_catalog, expected_type=type_hints["glue_data_catalog"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if glue_data_catalog is not None:
            self._values["glue_data_catalog"] = glue_data_catalog

    @builtins.property
    def glue_data_catalog(
        self,
    ) -> typing.Optional["AppflowFlowMetadataCatalogConfigGlueDataCatalog"]:
        '''glue_data_catalog block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#glue_data_catalog AppflowFlow#glue_data_catalog}
        '''
        result = self._values.get("glue_data_catalog")
        return typing.cast(typing.Optional["AppflowFlowMetadataCatalogConfigGlueDataCatalog"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowMetadataCatalogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowMetadataCatalogConfigGlueDataCatalog",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "role_arn": "roleArn",
        "table_prefix": "tablePrefix",
    },
)
class AppflowFlowMetadataCatalogConfigGlueDataCatalog:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        role_arn: builtins.str,
        table_prefix: builtins.str,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#database_name AppflowFlow#database_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#role_arn AppflowFlow#role_arn}.
        :param table_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#table_prefix AppflowFlow#table_prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b33004c6963107cc50e36efb9f06553e2321d4087b08fea2a60e7d800f19435)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument table_prefix", value=table_prefix, expected_type=type_hints["table_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
            "role_arn": role_arn,
            "table_prefix": table_prefix,
        }

    @builtins.property
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#database_name AppflowFlow#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#role_arn AppflowFlow#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_prefix(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#table_prefix AppflowFlow#table_prefix}.'''
        result = self._values.get("table_prefix")
        assert result is not None, "Required property 'table_prefix' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowMetadataCatalogConfigGlueDataCatalog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowMetadataCatalogConfigGlueDataCatalogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowMetadataCatalogConfigGlueDataCatalogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__574a01f44a245b886590086233a7c8cb2576f1fe9a8cb6576d01012ff62ee61d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="tablePrefixInput")
    def table_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tablePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f98fd1900ee66262f9a9018c1922baf0aee5375cee399cd007627f23169ae356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6a2a4f6d2f819feb09557746471707bda72d803df5760c1d35f9af09a830f96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tablePrefix")
    def table_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tablePrefix"))

    @table_prefix.setter
    def table_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__212b8c337cabb02ce252f0a6aa01423515593964ae228abe9b6ff73251084549)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tablePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowMetadataCatalogConfigGlueDataCatalog]:
        return typing.cast(typing.Optional[AppflowFlowMetadataCatalogConfigGlueDataCatalog], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowMetadataCatalogConfigGlueDataCatalog],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d08f9588fe41fe39a8505d336c1acd3f9c64577e9e31d9d89b30dea9a3048470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowMetadataCatalogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowMetadataCatalogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f81504c7da70b881dcba4127375552b2bb7cb361b1b0da8bf1aaf36f10c1432f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGlueDataCatalog")
    def put_glue_data_catalog(
        self,
        *,
        database_name: builtins.str,
        role_arn: builtins.str,
        table_prefix: builtins.str,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#database_name AppflowFlow#database_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#role_arn AppflowFlow#role_arn}.
        :param table_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#table_prefix AppflowFlow#table_prefix}.
        '''
        value = AppflowFlowMetadataCatalogConfigGlueDataCatalog(
            database_name=database_name, role_arn=role_arn, table_prefix=table_prefix
        )

        return typing.cast(None, jsii.invoke(self, "putGlueDataCatalog", [value]))

    @jsii.member(jsii_name="resetGlueDataCatalog")
    def reset_glue_data_catalog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlueDataCatalog", []))

    @builtins.property
    @jsii.member(jsii_name="glueDataCatalog")
    def glue_data_catalog(
        self,
    ) -> AppflowFlowMetadataCatalogConfigGlueDataCatalogOutputReference:
        return typing.cast(AppflowFlowMetadataCatalogConfigGlueDataCatalogOutputReference, jsii.get(self, "glueDataCatalog"))

    @builtins.property
    @jsii.member(jsii_name="glueDataCatalogInput")
    def glue_data_catalog_input(
        self,
    ) -> typing.Optional[AppflowFlowMetadataCatalogConfigGlueDataCatalog]:
        return typing.cast(typing.Optional[AppflowFlowMetadataCatalogConfigGlueDataCatalog], jsii.get(self, "glueDataCatalogInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppflowFlowMetadataCatalogConfig]:
        return typing.cast(typing.Optional[AppflowFlowMetadataCatalogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowMetadataCatalogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f665fdc987b3ed117279b6de2cebd819543f9dd29e1affaa423c6ac5fab1796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfig",
    jsii_struct_bases=[],
    name_mapping={
        "connector_type": "connectorType",
        "source_connector_properties": "sourceConnectorProperties",
        "api_version": "apiVersion",
        "connector_profile_name": "connectorProfileName",
        "incremental_pull_config": "incrementalPullConfig",
    },
)
class AppflowFlowSourceFlowConfig:
    def __init__(
        self,
        *,
        connector_type: builtins.str,
        source_connector_properties: typing.Union["AppflowFlowSourceFlowConfigSourceConnectorProperties", typing.Dict[builtins.str, typing.Any]],
        api_version: typing.Optional[builtins.str] = None,
        connector_profile_name: typing.Optional[builtins.str] = None,
        incremental_pull_config: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigIncrementalPullConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connector_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#connector_type AppflowFlow#connector_type}.
        :param source_connector_properties: source_connector_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#source_connector_properties AppflowFlow#source_connector_properties}
        :param api_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#api_version AppflowFlow#api_version}.
        :param connector_profile_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#connector_profile_name AppflowFlow#connector_profile_name}.
        :param incremental_pull_config: incremental_pull_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#incremental_pull_config AppflowFlow#incremental_pull_config}
        '''
        if isinstance(source_connector_properties, dict):
            source_connector_properties = AppflowFlowSourceFlowConfigSourceConnectorProperties(**source_connector_properties)
        if isinstance(incremental_pull_config, dict):
            incremental_pull_config = AppflowFlowSourceFlowConfigIncrementalPullConfig(**incremental_pull_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b98232112d244a63bcc735a27235157bf505b83049fb2c19240658a347f33e5)
            check_type(argname="argument connector_type", value=connector_type, expected_type=type_hints["connector_type"])
            check_type(argname="argument source_connector_properties", value=source_connector_properties, expected_type=type_hints["source_connector_properties"])
            check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
            check_type(argname="argument connector_profile_name", value=connector_profile_name, expected_type=type_hints["connector_profile_name"])
            check_type(argname="argument incremental_pull_config", value=incremental_pull_config, expected_type=type_hints["incremental_pull_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connector_type": connector_type,
            "source_connector_properties": source_connector_properties,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if connector_profile_name is not None:
            self._values["connector_profile_name"] = connector_profile_name
        if incremental_pull_config is not None:
            self._values["incremental_pull_config"] = incremental_pull_config

    @builtins.property
    def connector_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#connector_type AppflowFlow#connector_type}.'''
        result = self._values.get("connector_type")
        assert result is not None, "Required property 'connector_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_connector_properties(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorProperties":
        '''source_connector_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#source_connector_properties AppflowFlow#source_connector_properties}
        '''
        result = self._values.get("source_connector_properties")
        assert result is not None, "Required property 'source_connector_properties' is missing"
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorProperties", result)

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#api_version AppflowFlow#api_version}.'''
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connector_profile_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#connector_profile_name AppflowFlow#connector_profile_name}.'''
        result = self._values.get("connector_profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def incremental_pull_config(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigIncrementalPullConfig"]:
        '''incremental_pull_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#incremental_pull_config AppflowFlow#incremental_pull_config}
        '''
        result = self._values.get("incremental_pull_config")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigIncrementalPullConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigIncrementalPullConfig",
    jsii_struct_bases=[],
    name_mapping={"datetime_type_field_name": "datetimeTypeFieldName"},
)
class AppflowFlowSourceFlowConfigIncrementalPullConfig:
    def __init__(
        self,
        *,
        datetime_type_field_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param datetime_type_field_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#datetime_type_field_name AppflowFlow#datetime_type_field_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e849db34f51bdd89c287819d2d6e6dce6ec87ac5dddd22948fbaa21304b40ca9)
            check_type(argname="argument datetime_type_field_name", value=datetime_type_field_name, expected_type=type_hints["datetime_type_field_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if datetime_type_field_name is not None:
            self._values["datetime_type_field_name"] = datetime_type_field_name

    @builtins.property
    def datetime_type_field_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#datetime_type_field_name AppflowFlow#datetime_type_field_name}.'''
        result = self._values.get("datetime_type_field_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigIncrementalPullConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigIncrementalPullConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigIncrementalPullConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__742947b1a71420646e6d08b1210a40bca908f79f43b9ce73b730d339b3df1b34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDatetimeTypeFieldName")
    def reset_datetime_type_field_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatetimeTypeFieldName", []))

    @builtins.property
    @jsii.member(jsii_name="datetimeTypeFieldNameInput")
    def datetime_type_field_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datetimeTypeFieldNameInput"))

    @builtins.property
    @jsii.member(jsii_name="datetimeTypeFieldName")
    def datetime_type_field_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datetimeTypeFieldName"))

    @datetime_type_field_name.setter
    def datetime_type_field_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af5681b1ff44b4ad7037fcfe155b21b1d2bdfed01efaf7f2711e03dd05943484)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datetimeTypeFieldName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigIncrementalPullConfig]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigIncrementalPullConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigIncrementalPullConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e0bd845545737b6a7d995a17e2300c94991c8c0cb89975b6bf3c1388d37ac4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowSourceFlowConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__222e6492ea60a667e17c51ee104cebcb650805115f6f3ca5a181212f0c822dc7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIncrementalPullConfig")
    def put_incremental_pull_config(
        self,
        *,
        datetime_type_field_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param datetime_type_field_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#datetime_type_field_name AppflowFlow#datetime_type_field_name}.
        '''
        value = AppflowFlowSourceFlowConfigIncrementalPullConfig(
            datetime_type_field_name=datetime_type_field_name
        )

        return typing.cast(None, jsii.invoke(self, "putIncrementalPullConfig", [value]))

    @jsii.member(jsii_name="putSourceConnectorProperties")
    def put_source_connector_properties(
        self,
        *,
        amplitude: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_connector: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector", typing.Dict[builtins.str, typing.Any]]] = None,
        datadog: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog", typing.Dict[builtins.str, typing.Any]]] = None,
        dynatrace: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace", typing.Dict[builtins.str, typing.Any]]] = None,
        google_analytics: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics", typing.Dict[builtins.str, typing.Any]]] = None,
        infor_nexus: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus", typing.Dict[builtins.str, typing.Any]]] = None,
        marketo: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3", typing.Dict[builtins.str, typing.Any]]] = None,
        salesforce: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce", typing.Dict[builtins.str, typing.Any]]] = None,
        sapo_data: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData", typing.Dict[builtins.str, typing.Any]]] = None,
        service_now: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow", typing.Dict[builtins.str, typing.Any]]] = None,
        singular: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular", typing.Dict[builtins.str, typing.Any]]] = None,
        slack: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack", typing.Dict[builtins.str, typing.Any]]] = None,
        trendmicro: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro", typing.Dict[builtins.str, typing.Any]]] = None,
        veeva: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva", typing.Dict[builtins.str, typing.Any]]] = None,
        zendesk: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param amplitude: amplitude block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#amplitude AppflowFlow#amplitude}
        :param custom_connector: custom_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#custom_connector AppflowFlow#custom_connector}
        :param datadog: datadog block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#datadog AppflowFlow#datadog}
        :param dynatrace: dynatrace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#dynatrace AppflowFlow#dynatrace}
        :param google_analytics: google_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#google_analytics AppflowFlow#google_analytics}
        :param infor_nexus: infor_nexus block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#infor_nexus AppflowFlow#infor_nexus}
        :param marketo: marketo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#marketo AppflowFlow#marketo}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#s3 AppflowFlow#s3}
        :param salesforce: salesforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#salesforce AppflowFlow#salesforce}
        :param sapo_data: sapo_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#sapo_data AppflowFlow#sapo_data}
        :param service_now: service_now block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#service_now AppflowFlow#service_now}
        :param singular: singular block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#singular AppflowFlow#singular}
        :param slack: slack block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#slack AppflowFlow#slack}
        :param trendmicro: trendmicro block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#trendmicro AppflowFlow#trendmicro}
        :param veeva: veeva block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#veeva AppflowFlow#veeva}
        :param zendesk: zendesk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#zendesk AppflowFlow#zendesk}
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorProperties(
            amplitude=amplitude,
            custom_connector=custom_connector,
            datadog=datadog,
            dynatrace=dynatrace,
            google_analytics=google_analytics,
            infor_nexus=infor_nexus,
            marketo=marketo,
            s3=s3,
            salesforce=salesforce,
            sapo_data=sapo_data,
            service_now=service_now,
            singular=singular,
            slack=slack,
            trendmicro=trendmicro,
            veeva=veeva,
            zendesk=zendesk,
        )

        return typing.cast(None, jsii.invoke(self, "putSourceConnectorProperties", [value]))

    @jsii.member(jsii_name="resetApiVersion")
    def reset_api_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiVersion", []))

    @jsii.member(jsii_name="resetConnectorProfileName")
    def reset_connector_profile_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectorProfileName", []))

    @jsii.member(jsii_name="resetIncrementalPullConfig")
    def reset_incremental_pull_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncrementalPullConfig", []))

    @builtins.property
    @jsii.member(jsii_name="incrementalPullConfig")
    def incremental_pull_config(
        self,
    ) -> AppflowFlowSourceFlowConfigIncrementalPullConfigOutputReference:
        return typing.cast(AppflowFlowSourceFlowConfigIncrementalPullConfigOutputReference, jsii.get(self, "incrementalPullConfig"))

    @builtins.property
    @jsii.member(jsii_name="sourceConnectorProperties")
    def source_connector_properties(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesOutputReference", jsii.get(self, "sourceConnectorProperties"))

    @builtins.property
    @jsii.member(jsii_name="apiVersionInput")
    def api_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorProfileNameInput")
    def connector_profile_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorProfileNameInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorTypeInput")
    def connector_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="incrementalPullConfigInput")
    def incremental_pull_config_input(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigIncrementalPullConfig]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigIncrementalPullConfig], jsii.get(self, "incrementalPullConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceConnectorPropertiesInput")
    def source_connector_properties_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorProperties"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorProperties"], jsii.get(self, "sourceConnectorPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="apiVersion")
    def api_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiVersion"))

    @api_version.setter
    def api_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa0184b09cd4b5c917be3a6405553c54fb033d56f3063c6f7870d8075e00368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectorProfileName")
    def connector_profile_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorProfileName"))

    @connector_profile_name.setter
    def connector_profile_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88e261f77a5d377820261ca192a876502670d0e901479193ce2a279817507740)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorProfileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectorType")
    def connector_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectorType"))

    @connector_type.setter
    def connector_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f986eb4a3877c9e04e501268cc48f7880ebbfdec6ccf426615a6a1e5b03240d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppflowFlowSourceFlowConfig]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f353cba675138f4533f77e97debe18c719272bdeed3429939afa16c62351f17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorProperties",
    jsii_struct_bases=[],
    name_mapping={
        "amplitude": "amplitude",
        "custom_connector": "customConnector",
        "datadog": "datadog",
        "dynatrace": "dynatrace",
        "google_analytics": "googleAnalytics",
        "infor_nexus": "inforNexus",
        "marketo": "marketo",
        "s3": "s3",
        "salesforce": "salesforce",
        "sapo_data": "sapoData",
        "service_now": "serviceNow",
        "singular": "singular",
        "slack": "slack",
        "trendmicro": "trendmicro",
        "veeva": "veeva",
        "zendesk": "zendesk",
    },
)
class AppflowFlowSourceFlowConfigSourceConnectorProperties:
    def __init__(
        self,
        *,
        amplitude: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_connector: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector", typing.Dict[builtins.str, typing.Any]]] = None,
        datadog: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog", typing.Dict[builtins.str, typing.Any]]] = None,
        dynatrace: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace", typing.Dict[builtins.str, typing.Any]]] = None,
        google_analytics: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics", typing.Dict[builtins.str, typing.Any]]] = None,
        infor_nexus: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus", typing.Dict[builtins.str, typing.Any]]] = None,
        marketo: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3", typing.Dict[builtins.str, typing.Any]]] = None,
        salesforce: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce", typing.Dict[builtins.str, typing.Any]]] = None,
        sapo_data: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData", typing.Dict[builtins.str, typing.Any]]] = None,
        service_now: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow", typing.Dict[builtins.str, typing.Any]]] = None,
        singular: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular", typing.Dict[builtins.str, typing.Any]]] = None,
        slack: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack", typing.Dict[builtins.str, typing.Any]]] = None,
        trendmicro: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro", typing.Dict[builtins.str, typing.Any]]] = None,
        veeva: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva", typing.Dict[builtins.str, typing.Any]]] = None,
        zendesk: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param amplitude: amplitude block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#amplitude AppflowFlow#amplitude}
        :param custom_connector: custom_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#custom_connector AppflowFlow#custom_connector}
        :param datadog: datadog block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#datadog AppflowFlow#datadog}
        :param dynatrace: dynatrace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#dynatrace AppflowFlow#dynatrace}
        :param google_analytics: google_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#google_analytics AppflowFlow#google_analytics}
        :param infor_nexus: infor_nexus block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#infor_nexus AppflowFlow#infor_nexus}
        :param marketo: marketo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#marketo AppflowFlow#marketo}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#s3 AppflowFlow#s3}
        :param salesforce: salesforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#salesforce AppflowFlow#salesforce}
        :param sapo_data: sapo_data block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#sapo_data AppflowFlow#sapo_data}
        :param service_now: service_now block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#service_now AppflowFlow#service_now}
        :param singular: singular block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#singular AppflowFlow#singular}
        :param slack: slack block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#slack AppflowFlow#slack}
        :param trendmicro: trendmicro block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#trendmicro AppflowFlow#trendmicro}
        :param veeva: veeva block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#veeva AppflowFlow#veeva}
        :param zendesk: zendesk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#zendesk AppflowFlow#zendesk}
        '''
        if isinstance(amplitude, dict):
            amplitude = AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude(**amplitude)
        if isinstance(custom_connector, dict):
            custom_connector = AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector(**custom_connector)
        if isinstance(datadog, dict):
            datadog = AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog(**datadog)
        if isinstance(dynatrace, dict):
            dynatrace = AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace(**dynatrace)
        if isinstance(google_analytics, dict):
            google_analytics = AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics(**google_analytics)
        if isinstance(infor_nexus, dict):
            infor_nexus = AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus(**infor_nexus)
        if isinstance(marketo, dict):
            marketo = AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo(**marketo)
        if isinstance(s3, dict):
            s3 = AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3(**s3)
        if isinstance(salesforce, dict):
            salesforce = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce(**salesforce)
        if isinstance(sapo_data, dict):
            sapo_data = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData(**sapo_data)
        if isinstance(service_now, dict):
            service_now = AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow(**service_now)
        if isinstance(singular, dict):
            singular = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular(**singular)
        if isinstance(slack, dict):
            slack = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack(**slack)
        if isinstance(trendmicro, dict):
            trendmicro = AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro(**trendmicro)
        if isinstance(veeva, dict):
            veeva = AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva(**veeva)
        if isinstance(zendesk, dict):
            zendesk = AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk(**zendesk)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a7beb5c36c9c288e80d704b1af876a43b0f17e5aad5e3a8c130d93f5b811030)
            check_type(argname="argument amplitude", value=amplitude, expected_type=type_hints["amplitude"])
            check_type(argname="argument custom_connector", value=custom_connector, expected_type=type_hints["custom_connector"])
            check_type(argname="argument datadog", value=datadog, expected_type=type_hints["datadog"])
            check_type(argname="argument dynatrace", value=dynatrace, expected_type=type_hints["dynatrace"])
            check_type(argname="argument google_analytics", value=google_analytics, expected_type=type_hints["google_analytics"])
            check_type(argname="argument infor_nexus", value=infor_nexus, expected_type=type_hints["infor_nexus"])
            check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
            check_type(argname="argument sapo_data", value=sapo_data, expected_type=type_hints["sapo_data"])
            check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
            check_type(argname="argument singular", value=singular, expected_type=type_hints["singular"])
            check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
            check_type(argname="argument trendmicro", value=trendmicro, expected_type=type_hints["trendmicro"])
            check_type(argname="argument veeva", value=veeva, expected_type=type_hints["veeva"])
            check_type(argname="argument zendesk", value=zendesk, expected_type=type_hints["zendesk"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if amplitude is not None:
            self._values["amplitude"] = amplitude
        if custom_connector is not None:
            self._values["custom_connector"] = custom_connector
        if datadog is not None:
            self._values["datadog"] = datadog
        if dynatrace is not None:
            self._values["dynatrace"] = dynatrace
        if google_analytics is not None:
            self._values["google_analytics"] = google_analytics
        if infor_nexus is not None:
            self._values["infor_nexus"] = infor_nexus
        if marketo is not None:
            self._values["marketo"] = marketo
        if s3 is not None:
            self._values["s3"] = s3
        if salesforce is not None:
            self._values["salesforce"] = salesforce
        if sapo_data is not None:
            self._values["sapo_data"] = sapo_data
        if service_now is not None:
            self._values["service_now"] = service_now
        if singular is not None:
            self._values["singular"] = singular
        if slack is not None:
            self._values["slack"] = slack
        if trendmicro is not None:
            self._values["trendmicro"] = trendmicro
        if veeva is not None:
            self._values["veeva"] = veeva
        if zendesk is not None:
            self._values["zendesk"] = zendesk

    @builtins.property
    def amplitude(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude"]:
        '''amplitude block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#amplitude AppflowFlow#amplitude}
        '''
        result = self._values.get("amplitude")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude"], result)

    @builtins.property
    def custom_connector(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector"]:
        '''custom_connector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#custom_connector AppflowFlow#custom_connector}
        '''
        result = self._values.get("custom_connector")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector"], result)

    @builtins.property
    def datadog(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog"]:
        '''datadog block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#datadog AppflowFlow#datadog}
        '''
        result = self._values.get("datadog")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog"], result)

    @builtins.property
    def dynatrace(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace"]:
        '''dynatrace block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#dynatrace AppflowFlow#dynatrace}
        '''
        result = self._values.get("dynatrace")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace"], result)

    @builtins.property
    def google_analytics(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics"]:
        '''google_analytics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#google_analytics AppflowFlow#google_analytics}
        '''
        result = self._values.get("google_analytics")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics"], result)

    @builtins.property
    def infor_nexus(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus"]:
        '''infor_nexus block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#infor_nexus AppflowFlow#infor_nexus}
        '''
        result = self._values.get("infor_nexus")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus"], result)

    @builtins.property
    def marketo(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo"]:
        '''marketo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#marketo AppflowFlow#marketo}
        '''
        result = self._values.get("marketo")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo"], result)

    @builtins.property
    def s3(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3"]:
        '''s3 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#s3 AppflowFlow#s3}
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3"], result)

    @builtins.property
    def salesforce(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce"]:
        '''salesforce block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#salesforce AppflowFlow#salesforce}
        '''
        result = self._values.get("salesforce")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce"], result)

    @builtins.property
    def sapo_data(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData"]:
        '''sapo_data block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#sapo_data AppflowFlow#sapo_data}
        '''
        result = self._values.get("sapo_data")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData"], result)

    @builtins.property
    def service_now(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow"]:
        '''service_now block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#service_now AppflowFlow#service_now}
        '''
        result = self._values.get("service_now")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow"], result)

    @builtins.property
    def singular(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular"]:
        '''singular block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#singular AppflowFlow#singular}
        '''
        result = self._values.get("singular")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular"], result)

    @builtins.property
    def slack(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack"]:
        '''slack block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#slack AppflowFlow#slack}
        '''
        result = self._values.get("slack")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack"], result)

    @builtins.property
    def trendmicro(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro"]:
        '''trendmicro block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#trendmicro AppflowFlow#trendmicro}
        '''
        result = self._values.get("trendmicro")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro"], result)

    @builtins.property
    def veeva(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva"]:
        '''veeva block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#veeva AppflowFlow#veeva}
        '''
        result = self._values.get("veeva")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva"], result)

    @builtins.property
    def zendesk(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk"]:
        '''zendesk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#zendesk AppflowFlow#zendesk}
        '''
        result = self._values.get("zendesk")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc5affa045e0a3c17e9c5552f249dc32f3344807db92204e14339d5158cd2e90)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitudeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitudeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9c6f1bafef59deb1fa81dd1fe6d920a90c345857d1135b6d9095cc640909808)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3418ce032bbcdb95a7c7eacdf2856236e28b33d4ba6ea8f5bd946b7366398ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6400137fe3051b4ad3606333f38eabc3cfd765060902f93858365128c18870c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector",
    jsii_struct_bases=[],
    name_mapping={
        "entity_name": "entityName",
        "custom_properties": "customProperties",
    },
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector:
    def __init__(
        self,
        *,
        entity_name: builtins.str,
        custom_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param entity_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#entity_name AppflowFlow#entity_name}.
        :param custom_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#custom_properties AppflowFlow#custom_properties}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1769cd7bd487dc90b9719132ce34f491d4efa4b8623e32664bbbd66bd5bc5ea2)
            check_type(argname="argument entity_name", value=entity_name, expected_type=type_hints["entity_name"])
            check_type(argname="argument custom_properties", value=custom_properties, expected_type=type_hints["custom_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "entity_name": entity_name,
        }
        if custom_properties is not None:
            self._values["custom_properties"] = custom_properties

    @builtins.property
    def entity_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#entity_name AppflowFlow#entity_name}.'''
        result = self._values.get("entity_name")
        assert result is not None, "Required property 'entity_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#custom_properties AppflowFlow#custom_properties}.'''
        result = self._values.get("custom_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__100818bcb735cd59ebc7bf215363ebfad2af90ce98f25fd96fc85aad06e3e969)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCustomProperties")
    def reset_custom_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomProperties", []))

    @builtins.property
    @jsii.member(jsii_name="customPropertiesInput")
    def custom_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "customPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="entityNameInput")
    def entity_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entityNameInput"))

    @builtins.property
    @jsii.member(jsii_name="customProperties")
    def custom_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "customProperties"))

    @custom_properties.setter
    def custom_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f36615e0c6efa699e607da38327d0afdd5a72046b70900bb1b4eb7da1e4ef6b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="entityName")
    def entity_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entityName"))

    @entity_name.setter
    def entity_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__112c9f07bc3e2754bada4e7cdde2e9103b9a82d580708019b7b8bb3427b0428e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entityName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__472cca29798919e58f86e83c5e9d1fa63bf3b39c71a1b8882baa5e72638510a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09617de1703d4c787c55bfc3d70a7f454a950d740bb6879b7acfe77caba66f29)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c64627a9685f81b3b672fede26f39539a7fc6711dea1a35ecc2ec357d9e78f34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c984f2968ea039b5f6023a3e216812507ae06fc1f6376704d7eb482d1a05b65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ca593869e26d483b54f94efb27cb3f16372fae6748711a04578d78e0a926b7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac5e07b7b22b21c48f5f8179f4bf2895e88ac9093a8f596dfcd7fd95a08b22c3)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatraceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatraceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5a36d86c7753225645551d21eadb9503407497c9d415dd17ac9b95e3e34ca71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f0127727e70d4deea9734bf94bd83edff2041bbc331a59524daf00fdf1174d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd5e6abd09c8d5f99dcda1e1e064bc200aa5df4dccbfb4ec0a0f428f2dbeed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a9654a2a2d7063238de8535700af544bf0036656d22a62bb40c05acff36d742)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalyticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalyticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18139a6408cb72dd7efbdac0167c32e6dff44b4494d052ea0dad2abe57f80c54)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc230ab0a27309ee8a97cb31cad5ea3a88efcbd12232554125f90ccb17aef3d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f05160c3da193245bd7f3b8da4a2f33d767be32ea9b85029aa4e8fd443b4096d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f7afcf85edf877ebc91ab4bd9e609dc63dbd58c79d761a179cbf7ca73134366)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07ab2a8870c1040ee5edb14f0a11bcc98502b3def08f526761ecee88729c10d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aee02a1579a05d2f545cdc9059c7423d9e90249978e3080e4b429f9d46d6ac0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cccdea102850e2b4e92c5f507028aabd96fd054a6893df2040ba83420bccc96e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__395cd8d5defc871ec3aa88e75608028d6f148d43be89752da2fbd582dd06cf99)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2f0c42ec03d8db060799772695c88633f0fc4c7c092bae81ecd964756da0f47)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0362319a8e6f9dce31ffab6752f3d54469a8ade02c0bb7a72b676dc188d0c7af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17c156bd293f2667cb96aadd4bbb53903e72a75b7e6935de96fa2a504843b036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7feb30c4bb03e789ba3e3ca9c5eb1cbb16bc9c11e755256260ecf5eb2e51e73b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAmplitude")
    def put_amplitude(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putAmplitude", [value]))

    @jsii.member(jsii_name="putCustomConnector")
    def put_custom_connector(
        self,
        *,
        entity_name: builtins.str,
        custom_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param entity_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#entity_name AppflowFlow#entity_name}.
        :param custom_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#custom_properties AppflowFlow#custom_properties}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector(
            entity_name=entity_name, custom_properties=custom_properties
        )

        return typing.cast(None, jsii.invoke(self, "putCustomConnector", [value]))

    @jsii.member(jsii_name="putDatadog")
    def put_datadog(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putDatadog", [value]))

    @jsii.member(jsii_name="putDynatrace")
    def put_dynatrace(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putDynatrace", [value]))

    @jsii.member(jsii_name="putGoogleAnalytics")
    def put_google_analytics(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putGoogleAnalytics", [value]))

    @jsii.member(jsii_name="putInforNexus")
    def put_infor_nexus(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putInforNexus", [value]))

    @jsii.member(jsii_name="putMarketo")
    def put_marketo(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putMarketo", [value]))

    @jsii.member(jsii_name="putS3")
    def put_s3(
        self,
        *,
        bucket_name: builtins.str,
        bucket_prefix: builtins.str,
        s3_input_format_config: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param s3_input_format_config: s3_input_format_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#s3_input_format_config AppflowFlow#s3_input_format_config}
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3(
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            s3_input_format_config=s3_input_format_config,
        )

        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="putSalesforce")
    def put_salesforce(
        self,
        *,
        object: builtins.str,
        data_transfer_api: typing.Optional[builtins.str] = None,
        enable_dynamic_field_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_deleted_records: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param data_transfer_api: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#data_transfer_api AppflowFlow#data_transfer_api}.
        :param enable_dynamic_field_update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#enable_dynamic_field_update AppflowFlow#enable_dynamic_field_update}.
        :param include_deleted_records: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#include_deleted_records AppflowFlow#include_deleted_records}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce(
            object=object,
            data_transfer_api=data_transfer_api,
            enable_dynamic_field_update=enable_dynamic_field_update,
            include_deleted_records=include_deleted_records,
        )

        return typing.cast(None, jsii.invoke(self, "putSalesforce", [value]))

    @jsii.member(jsii_name="putSapoData")
    def put_sapo_data(
        self,
        *,
        object_path: builtins.str,
        pagination_config: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        parallelism_config: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param object_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object_path AppflowFlow#object_path}.
        :param pagination_config: pagination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#pagination_config AppflowFlow#pagination_config}
        :param parallelism_config: parallelism_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#parallelism_config AppflowFlow#parallelism_config}
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData(
            object_path=object_path,
            pagination_config=pagination_config,
            parallelism_config=parallelism_config,
        )

        return typing.cast(None, jsii.invoke(self, "putSapoData", [value]))

    @jsii.member(jsii_name="putServiceNow")
    def put_service_now(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putServiceNow", [value]))

    @jsii.member(jsii_name="putSingular")
    def put_singular(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putSingular", [value]))

    @jsii.member(jsii_name="putSlack")
    def put_slack(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putSlack", [value]))

    @jsii.member(jsii_name="putTrendmicro")
    def put_trendmicro(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putTrendmicro", [value]))

    @jsii.member(jsii_name="putVeeva")
    def put_veeva(
        self,
        *,
        object: builtins.str,
        document_type: typing.Optional[builtins.str] = None,
        include_all_versions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_renditions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_source_files: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param document_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#document_type AppflowFlow#document_type}.
        :param include_all_versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#include_all_versions AppflowFlow#include_all_versions}.
        :param include_renditions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#include_renditions AppflowFlow#include_renditions}.
        :param include_source_files: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#include_source_files AppflowFlow#include_source_files}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva(
            object=object,
            document_type=document_type,
            include_all_versions=include_all_versions,
            include_renditions=include_renditions,
            include_source_files=include_source_files,
        )

        return typing.cast(None, jsii.invoke(self, "putVeeva", [value]))

    @jsii.member(jsii_name="putZendesk")
    def put_zendesk(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk(
            object=object
        )

        return typing.cast(None, jsii.invoke(self, "putZendesk", [value]))

    @jsii.member(jsii_name="resetAmplitude")
    def reset_amplitude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmplitude", []))

    @jsii.member(jsii_name="resetCustomConnector")
    def reset_custom_connector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomConnector", []))

    @jsii.member(jsii_name="resetDatadog")
    def reset_datadog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatadog", []))

    @jsii.member(jsii_name="resetDynatrace")
    def reset_dynatrace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynatrace", []))

    @jsii.member(jsii_name="resetGoogleAnalytics")
    def reset_google_analytics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogleAnalytics", []))

    @jsii.member(jsii_name="resetInforNexus")
    def reset_infor_nexus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInforNexus", []))

    @jsii.member(jsii_name="resetMarketo")
    def reset_marketo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMarketo", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

    @jsii.member(jsii_name="resetSalesforce")
    def reset_salesforce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSalesforce", []))

    @jsii.member(jsii_name="resetSapoData")
    def reset_sapo_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSapoData", []))

    @jsii.member(jsii_name="resetServiceNow")
    def reset_service_now(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceNow", []))

    @jsii.member(jsii_name="resetSingular")
    def reset_singular(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingular", []))

    @jsii.member(jsii_name="resetSlack")
    def reset_slack(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSlack", []))

    @jsii.member(jsii_name="resetTrendmicro")
    def reset_trendmicro(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrendmicro", []))

    @jsii.member(jsii_name="resetVeeva")
    def reset_veeva(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVeeva", []))

    @jsii.member(jsii_name="resetZendesk")
    def reset_zendesk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZendesk", []))

    @builtins.property
    @jsii.member(jsii_name="amplitude")
    def amplitude(
        self,
    ) -> AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitudeOutputReference:
        return typing.cast(AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitudeOutputReference, jsii.get(self, "amplitude"))

    @builtins.property
    @jsii.member(jsii_name="customConnector")
    def custom_connector(
        self,
    ) -> AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnectorOutputReference:
        return typing.cast(AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnectorOutputReference, jsii.get(self, "customConnector"))

    @builtins.property
    @jsii.member(jsii_name="datadog")
    def datadog(
        self,
    ) -> AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadogOutputReference:
        return typing.cast(AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadogOutputReference, jsii.get(self, "datadog"))

    @builtins.property
    @jsii.member(jsii_name="dynatrace")
    def dynatrace(
        self,
    ) -> AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatraceOutputReference:
        return typing.cast(AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatraceOutputReference, jsii.get(self, "dynatrace"))

    @builtins.property
    @jsii.member(jsii_name="googleAnalytics")
    def google_analytics(
        self,
    ) -> AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalyticsOutputReference:
        return typing.cast(AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalyticsOutputReference, jsii.get(self, "googleAnalytics"))

    @builtins.property
    @jsii.member(jsii_name="inforNexus")
    def infor_nexus(
        self,
    ) -> AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexusOutputReference:
        return typing.cast(AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexusOutputReference, jsii.get(self, "inforNexus"))

    @builtins.property
    @jsii.member(jsii_name="marketo")
    def marketo(
        self,
    ) -> AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketoOutputReference:
        return typing.cast(AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketoOutputReference, jsii.get(self, "marketo"))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3OutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3OutputReference", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="salesforce")
    def salesforce(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforceOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforceOutputReference", jsii.get(self, "salesforce"))

    @builtins.property
    @jsii.member(jsii_name="sapoData")
    def sapo_data(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataOutputReference", jsii.get(self, "sapoData"))

    @builtins.property
    @jsii.member(jsii_name="serviceNow")
    def service_now(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNowOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNowOutputReference", jsii.get(self, "serviceNow"))

    @builtins.property
    @jsii.member(jsii_name="singular")
    def singular(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingularOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingularOutputReference", jsii.get(self, "singular"))

    @builtins.property
    @jsii.member(jsii_name="slack")
    def slack(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlackOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlackOutputReference", jsii.get(self, "slack"))

    @builtins.property
    @jsii.member(jsii_name="trendmicro")
    def trendmicro(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicroOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicroOutputReference", jsii.get(self, "trendmicro"))

    @builtins.property
    @jsii.member(jsii_name="veeva")
    def veeva(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeevaOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeevaOutputReference", jsii.get(self, "veeva"))

    @builtins.property
    @jsii.member(jsii_name="zendesk")
    def zendesk(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendeskOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendeskOutputReference", jsii.get(self, "zendesk"))

    @builtins.property
    @jsii.member(jsii_name="amplitudeInput")
    def amplitude_input(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude], jsii.get(self, "amplitudeInput"))

    @builtins.property
    @jsii.member(jsii_name="customConnectorInput")
    def custom_connector_input(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector], jsii.get(self, "customConnectorInput"))

    @builtins.property
    @jsii.member(jsii_name="datadogInput")
    def datadog_input(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog], jsii.get(self, "datadogInput"))

    @builtins.property
    @jsii.member(jsii_name="dynatraceInput")
    def dynatrace_input(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace], jsii.get(self, "dynatraceInput"))

    @builtins.property
    @jsii.member(jsii_name="googleAnalyticsInput")
    def google_analytics_input(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics], jsii.get(self, "googleAnalyticsInput"))

    @builtins.property
    @jsii.member(jsii_name="inforNexusInput")
    def infor_nexus_input(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus], jsii.get(self, "inforNexusInput"))

    @builtins.property
    @jsii.member(jsii_name="marketoInput")
    def marketo_input(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo], jsii.get(self, "marketoInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3"], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="salesforceInput")
    def salesforce_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce"], jsii.get(self, "salesforceInput"))

    @builtins.property
    @jsii.member(jsii_name="sapoDataInput")
    def sapo_data_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData"], jsii.get(self, "sapoDataInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNowInput")
    def service_now_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow"], jsii.get(self, "serviceNowInput"))

    @builtins.property
    @jsii.member(jsii_name="singularInput")
    def singular_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular"], jsii.get(self, "singularInput"))

    @builtins.property
    @jsii.member(jsii_name="slackInput")
    def slack_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack"], jsii.get(self, "slackInput"))

    @builtins.property
    @jsii.member(jsii_name="trendmicroInput")
    def trendmicro_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro"], jsii.get(self, "trendmicroInput"))

    @builtins.property
    @jsii.member(jsii_name="veevaInput")
    def veeva_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva"], jsii.get(self, "veevaInput"))

    @builtins.property
    @jsii.member(jsii_name="zendeskInput")
    def zendesk_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk"], jsii.get(self, "zendeskInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorProperties]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24965ba715da9256975addfa661e259641c584e24d058b10ff49086f674d43c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "s3_input_format_config": "s3InputFormatConfig",
    },
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        bucket_prefix: builtins.str,
        s3_input_format_config: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.
        :param bucket_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.
        :param s3_input_format_config: s3_input_format_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#s3_input_format_config AppflowFlow#s3_input_format_config}
        '''
        if isinstance(s3_input_format_config, dict):
            s3_input_format_config = AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig(**s3_input_format_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0906abac59491666d6a198cd529c84dbd393c16feb00db8e15b53beeb7f9a7ee)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument s3_input_format_config", value=s3_input_format_config, expected_type=type_hints["s3_input_format_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "bucket_prefix": bucket_prefix,
        }
        if s3_input_format_config is not None:
            self._values["s3_input_format_config"] = s3_input_format_config

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_name AppflowFlow#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_prefix(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#bucket_prefix AppflowFlow#bucket_prefix}.'''
        result = self._values.get("bucket_prefix")
        assert result is not None, "Required property 'bucket_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_input_format_config(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig"]:
        '''s3_input_format_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#s3_input_format_config AppflowFlow#s3_input_format_config}
        '''
        result = self._values.get("s3_input_format_config")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f0653cea340b81eca1e9178b1d0d5868b6bf4efb08e762b364358baa3d35f79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putS3InputFormatConfig")
    def put_s3_input_format_config(
        self,
        *,
        s3_input_file_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_input_file_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#s3_input_file_type AppflowFlow#s3_input_file_type}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig(
            s3_input_file_type=s3_input_file_type
        )

        return typing.cast(None, jsii.invoke(self, "putS3InputFormatConfig", [value]))

    @jsii.member(jsii_name="resetS3InputFormatConfig")
    def reset_s3_input_format_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3InputFormatConfig", []))

    @builtins.property
    @jsii.member(jsii_name="s3InputFormatConfig")
    def s3_input_format_config(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfigOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfigOutputReference", jsii.get(self, "s3InputFormatConfig"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketPrefixInput")
    def bucket_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="s3InputFormatConfigInput")
    def s3_input_format_config_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig"], jsii.get(self, "s3InputFormatConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56b644f3183783b81a41aceb2ca3d71e55cf75bbe6effe35d61f694ea909d676)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketPrefix")
    def bucket_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketPrefix"))

    @bucket_prefix.setter
    def bucket_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3aba6ea3e3e3b41977e86667c6f57b7dac74ac8f3873e1124e9c206a1cce6b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b502f8c0e0b3f97e4bd42116c38c18a1dc0d42d6d554ee2ebeef42fdb430504)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig",
    jsii_struct_bases=[],
    name_mapping={"s3_input_file_type": "s3InputFileType"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig:
    def __init__(
        self,
        *,
        s3_input_file_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_input_file_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#s3_input_file_type AppflowFlow#s3_input_file_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05a3b222af4ce1aa53d3d75a80358c7972529da632999ee3b88a2cb2af058f3c)
            check_type(argname="argument s3_input_file_type", value=s3_input_file_type, expected_type=type_hints["s3_input_file_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if s3_input_file_type is not None:
            self._values["s3_input_file_type"] = s3_input_file_type

    @builtins.property
    def s3_input_file_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#s3_input_file_type AppflowFlow#s3_input_file_type}.'''
        result = self._values.get("s3_input_file_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87ac5f939a396714c66209298c1de0cfcc8310b64197810edebe66c631103d27)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetS3InputFileType")
    def reset_s3_input_file_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3InputFileType", []))

    @builtins.property
    @jsii.member(jsii_name="s3InputFileTypeInput")
    def s3_input_file_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3InputFileTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="s3InputFileType")
    def s3_input_file_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3InputFileType"))

    @s3_input_file_type.setter
    def s3_input_file_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__841b6f45ccbc523e57863161bd7b31764eebfac16938b7f4a0b10c2c95862c41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3InputFileType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbdcbf97fc8a7e252998cada51d91636e468a7262b8a5ab928d560b75ab78ab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce",
    jsii_struct_bases=[],
    name_mapping={
        "object": "object",
        "data_transfer_api": "dataTransferApi",
        "enable_dynamic_field_update": "enableDynamicFieldUpdate",
        "include_deleted_records": "includeDeletedRecords",
    },
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce:
    def __init__(
        self,
        *,
        object: builtins.str,
        data_transfer_api: typing.Optional[builtins.str] = None,
        enable_dynamic_field_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_deleted_records: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param data_transfer_api: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#data_transfer_api AppflowFlow#data_transfer_api}.
        :param enable_dynamic_field_update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#enable_dynamic_field_update AppflowFlow#enable_dynamic_field_update}.
        :param include_deleted_records: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#include_deleted_records AppflowFlow#include_deleted_records}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a76fe62c8e612023f4b60fe54d6953e87d8ae925d601d5c9a3f469c363627a7)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument data_transfer_api", value=data_transfer_api, expected_type=type_hints["data_transfer_api"])
            check_type(argname="argument enable_dynamic_field_update", value=enable_dynamic_field_update, expected_type=type_hints["enable_dynamic_field_update"])
            check_type(argname="argument include_deleted_records", value=include_deleted_records, expected_type=type_hints["include_deleted_records"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }
        if data_transfer_api is not None:
            self._values["data_transfer_api"] = data_transfer_api
        if enable_dynamic_field_update is not None:
            self._values["enable_dynamic_field_update"] = enable_dynamic_field_update
        if include_deleted_records is not None:
            self._values["include_deleted_records"] = include_deleted_records

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_transfer_api(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#data_transfer_api AppflowFlow#data_transfer_api}.'''
        result = self._values.get("data_transfer_api")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_dynamic_field_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#enable_dynamic_field_update AppflowFlow#enable_dynamic_field_update}.'''
        result = self._values.get("enable_dynamic_field_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_deleted_records(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#include_deleted_records AppflowFlow#include_deleted_records}.'''
        result = self._values.get("include_deleted_records")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__472bb8ef1eb8ff15ffd4b9f3f4e9506f6db166fc2b73592756e9ccc818cf1602)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDataTransferApi")
    def reset_data_transfer_api(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataTransferApi", []))

    @jsii.member(jsii_name="resetEnableDynamicFieldUpdate")
    def reset_enable_dynamic_field_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableDynamicFieldUpdate", []))

    @jsii.member(jsii_name="resetIncludeDeletedRecords")
    def reset_include_deleted_records(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeDeletedRecords", []))

    @builtins.property
    @jsii.member(jsii_name="dataTransferApiInput")
    def data_transfer_api_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataTransferApiInput"))

    @builtins.property
    @jsii.member(jsii_name="enableDynamicFieldUpdateInput")
    def enable_dynamic_field_update_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableDynamicFieldUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="includeDeletedRecordsInput")
    def include_deleted_records_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeDeletedRecordsInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="dataTransferApi")
    def data_transfer_api(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataTransferApi"))

    @data_transfer_api.setter
    def data_transfer_api(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf98fe03374ebc0e8abf1ddf03d2f0c89c5ea2d70906678c64307f2f927e9ab0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataTransferApi", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableDynamicFieldUpdate")
    def enable_dynamic_field_update(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableDynamicFieldUpdate"))

    @enable_dynamic_field_update.setter
    def enable_dynamic_field_update(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70d4704eb37ca1010f3f3ee14a4f65e5387247580d72d6dc926674d2182a9d92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableDynamicFieldUpdate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeDeletedRecords")
    def include_deleted_records(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeDeletedRecords"))

    @include_deleted_records.setter
    def include_deleted_records(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12c9c91e54967a7a2e715512fd0eee20d146b636d33c3ef225103a5701b2ec7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeDeletedRecords", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55b9867888d36433d6106605ad23cafb0cb2b62417468f2c874b801efc435414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6692c1ab443d2864b9e6399ee2e569b7e32971cfda2894700105e66e0236d33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData",
    jsii_struct_bases=[],
    name_mapping={
        "object_path": "objectPath",
        "pagination_config": "paginationConfig",
        "parallelism_config": "parallelismConfig",
    },
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData:
    def __init__(
        self,
        *,
        object_path: builtins.str,
        pagination_config: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        parallelism_config: typing.Optional[typing.Union["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param object_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object_path AppflowFlow#object_path}.
        :param pagination_config: pagination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#pagination_config AppflowFlow#pagination_config}
        :param parallelism_config: parallelism_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#parallelism_config AppflowFlow#parallelism_config}
        '''
        if isinstance(pagination_config, dict):
            pagination_config = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig(**pagination_config)
        if isinstance(parallelism_config, dict):
            parallelism_config = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig(**parallelism_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fbcb61821b3b9064899af8a6bdec0acd0afcaa14fc73b98c39fbce771602c51)
            check_type(argname="argument object_path", value=object_path, expected_type=type_hints["object_path"])
            check_type(argname="argument pagination_config", value=pagination_config, expected_type=type_hints["pagination_config"])
            check_type(argname="argument parallelism_config", value=parallelism_config, expected_type=type_hints["parallelism_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_path": object_path,
        }
        if pagination_config is not None:
            self._values["pagination_config"] = pagination_config
        if parallelism_config is not None:
            self._values["parallelism_config"] = parallelism_config

    @builtins.property
    def object_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object_path AppflowFlow#object_path}.'''
        result = self._values.get("object_path")
        assert result is not None, "Required property 'object_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pagination_config(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig"]:
        '''pagination_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#pagination_config AppflowFlow#pagination_config}
        '''
        result = self._values.get("pagination_config")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig"], result)

    @builtins.property
    def parallelism_config(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig"]:
        '''parallelism_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#parallelism_config AppflowFlow#parallelism_config}
        '''
        result = self._values.get("parallelism_config")
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed4ca2d53c1a8f6fa2913fd57e606ca9086e694e6107c19e8a1d45eacee8b869)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPaginationConfig")
    def put_pagination_config(self, *, max_page_size: jsii.Number) -> None:
        '''
        :param max_page_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#max_page_size AppflowFlow#max_page_size}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig(
            max_page_size=max_page_size
        )

        return typing.cast(None, jsii.invoke(self, "putPaginationConfig", [value]))

    @jsii.member(jsii_name="putParallelismConfig")
    def put_parallelism_config(self, *, max_page_size: jsii.Number) -> None:
        '''
        :param max_page_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#max_page_size AppflowFlow#max_page_size}.
        '''
        value = AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig(
            max_page_size=max_page_size
        )

        return typing.cast(None, jsii.invoke(self, "putParallelismConfig", [value]))

    @jsii.member(jsii_name="resetPaginationConfig")
    def reset_pagination_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPaginationConfig", []))

    @jsii.member(jsii_name="resetParallelismConfig")
    def reset_parallelism_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelismConfig", []))

    @builtins.property
    @jsii.member(jsii_name="paginationConfig")
    def pagination_config(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfigOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfigOutputReference", jsii.get(self, "paginationConfig"))

    @builtins.property
    @jsii.member(jsii_name="parallelismConfig")
    def parallelism_config(
        self,
    ) -> "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfigOutputReference":
        return typing.cast("AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfigOutputReference", jsii.get(self, "parallelismConfig"))

    @builtins.property
    @jsii.member(jsii_name="objectPathInput")
    def object_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectPathInput"))

    @builtins.property
    @jsii.member(jsii_name="paginationConfigInput")
    def pagination_config_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig"], jsii.get(self, "paginationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelismConfigInput")
    def parallelism_config_input(
        self,
    ) -> typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig"]:
        return typing.cast(typing.Optional["AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig"], jsii.get(self, "parallelismConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="objectPath")
    def object_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectPath"))

    @object_path.setter
    def object_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98704b4acae3e4b965e20e32adadc030db92d1d6db5fd62eece2a10789ba99cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe04322ff055bc4c21ef67da8485d16eefdf4cbd3a2fc1e40497a0c6bffc7032)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig",
    jsii_struct_bases=[],
    name_mapping={"max_page_size": "maxPageSize"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig:
    def __init__(self, *, max_page_size: jsii.Number) -> None:
        '''
        :param max_page_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#max_page_size AppflowFlow#max_page_size}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc5bfc3d3abebaf0f8e2ee1ee501114857c5d91b83d604ba31acdae9443f2a0)
            check_type(argname="argument max_page_size", value=max_page_size, expected_type=type_hints["max_page_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_page_size": max_page_size,
        }

    @builtins.property
    def max_page_size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#max_page_size AppflowFlow#max_page_size}.'''
        result = self._values.get("max_page_size")
        assert result is not None, "Required property 'max_page_size' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44c5042650ba7839b67c86032f917295af923a9c3c6771a605183a42a1f4737c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="maxPageSizeInput")
    def max_page_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPageSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPageSize")
    def max_page_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPageSize"))

    @max_page_size.setter
    def max_page_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd2ab5a5073c2cd38c0586c891ee91cec1de5b28997ae4899a307b7b1aac11ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPageSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e9d4645052b990b867f41b30363e0b4057ec370092715bd051bd8792c37b8a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig",
    jsii_struct_bases=[],
    name_mapping={"max_page_size": "maxPageSize"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig:
    def __init__(self, *, max_page_size: jsii.Number) -> None:
        '''
        :param max_page_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#max_page_size AppflowFlow#max_page_size}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95c7f1b97dd1de21bad90abf9ce0557391ac0c0482faa5155b83f04183d32f58)
            check_type(argname="argument max_page_size", value=max_page_size, expected_type=type_hints["max_page_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_page_size": max_page_size,
        }

    @builtins.property
    def max_page_size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#max_page_size AppflowFlow#max_page_size}.'''
        result = self._values.get("max_page_size")
        assert result is not None, "Required property 'max_page_size' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc9fc147a4c8ccdf5312ceb99bd6882b5eec10a51325c0faba54725600f3a388)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="maxPageSizeInput")
    def max_page_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPageSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPageSize")
    def max_page_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPageSize"))

    @max_page_size.setter
    def max_page_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3062dadc935c501df71bfd91bd8e3d84b230d8bb516b7aa87a87f94d8adeb77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPageSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0271addcdab27af66c7028cdecb5f014d24d96a69ad940f1a0b1af1cfa2dfa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__003573c72f59db51dcc71bea44cca7da0801d968cab1af0b91c05c70eff393df)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c68bb434cf11448a0b10ef62edfe81cf5e5b39917863dc6b065bb4c3564baa4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__522c5758a6bb792169cdfa23ff2a8515deabb7624ad7f143f78db4fff11d8059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc8e6ebeaf25dcf4d87d995979ddb1c3f3977b24e3b5c7cb1a24982add28c3db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7459e4ef2741fe1819f8bf67f85a681f5bfa765257471a8945444479c1e51864)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingularOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingularOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59f3c460f8c4e79921ebf32c83aafbede2b2799ed18c96e0557287e70230d7eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fed4974e698c5ec45b5ad3bb1ef6fb7ff9a0be521963eb39350c193bbb8bf40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7a1bf42fa3e64d94db68208b51f0e1bef80ca608063b81465cfb841126e4fcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e935dda13dac212878155b0db654bbb39603c63efd75c473d18aba1383b9f2a8)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlackOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlackOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7282d2cc7164d3f9feb3b480a9bcf3e1361d5470a2a8c5c0a30d385e66662cc7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0daa262733511c72bfbcb696bf2c6ef6748e3fbac5ea9778d568620f26e726dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11549c7c8a58d085a276693a1badbbed30f46a2dce34bdf0ffc65bd1dbb99450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a81d999d67de441e848d5db03533bc27615ad432127a3b53fd8e217030ae509f)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicroOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicroOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffb26598a46c6f236d0651e6f9354bed30c7475bdf9e98961e44355968eeee9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ef636042556fe0cac8b4489909cd3d0231834ca3416edc97a6f7fad744fa059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__699c2ceb688da3cddc83a0175614abde9159852d1797251ad5d2d16e3e545761)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva",
    jsii_struct_bases=[],
    name_mapping={
        "object": "object",
        "document_type": "documentType",
        "include_all_versions": "includeAllVersions",
        "include_renditions": "includeRenditions",
        "include_source_files": "includeSourceFiles",
    },
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva:
    def __init__(
        self,
        *,
        object: builtins.str,
        document_type: typing.Optional[builtins.str] = None,
        include_all_versions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_renditions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_source_files: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        :param document_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#document_type AppflowFlow#document_type}.
        :param include_all_versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#include_all_versions AppflowFlow#include_all_versions}.
        :param include_renditions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#include_renditions AppflowFlow#include_renditions}.
        :param include_source_files: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#include_source_files AppflowFlow#include_source_files}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca72438fa6c47bae59448adbe74d85cd9fa8a5abbc0816fca0edd423bca07302)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument document_type", value=document_type, expected_type=type_hints["document_type"])
            check_type(argname="argument include_all_versions", value=include_all_versions, expected_type=type_hints["include_all_versions"])
            check_type(argname="argument include_renditions", value=include_renditions, expected_type=type_hints["include_renditions"])
            check_type(argname="argument include_source_files", value=include_source_files, expected_type=type_hints["include_source_files"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }
        if document_type is not None:
            self._values["document_type"] = document_type
        if include_all_versions is not None:
            self._values["include_all_versions"] = include_all_versions
        if include_renditions is not None:
            self._values["include_renditions"] = include_renditions
        if include_source_files is not None:
            self._values["include_source_files"] = include_source_files

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def document_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#document_type AppflowFlow#document_type}.'''
        result = self._values.get("document_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_all_versions(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#include_all_versions AppflowFlow#include_all_versions}.'''
        result = self._values.get("include_all_versions")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_renditions(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#include_renditions AppflowFlow#include_renditions}.'''
        result = self._values.get("include_renditions")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_source_files(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#include_source_files AppflowFlow#include_source_files}.'''
        result = self._values.get("include_source_files")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeevaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeevaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43dffa0477959d5d39c0be2eb579b45070282f595ed635b7a7c88adfec116c7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDocumentType")
    def reset_document_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentType", []))

    @jsii.member(jsii_name="resetIncludeAllVersions")
    def reset_include_all_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeAllVersions", []))

    @jsii.member(jsii_name="resetIncludeRenditions")
    def reset_include_renditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeRenditions", []))

    @jsii.member(jsii_name="resetIncludeSourceFiles")
    def reset_include_source_files(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeSourceFiles", []))

    @builtins.property
    @jsii.member(jsii_name="documentTypeInput")
    def document_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "documentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="includeAllVersionsInput")
    def include_all_versions_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeAllVersionsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeRenditionsInput")
    def include_renditions_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeRenditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeSourceFilesInput")
    def include_source_files_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeSourceFilesInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="documentType")
    def document_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "documentType"))

    @document_type.setter
    def document_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe4b9ab34e189b0009e00c8cf51a731db87cdd0cec2b718c321c6194410bf343)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeAllVersions")
    def include_all_versions(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeAllVersions"))

    @include_all_versions.setter
    def include_all_versions(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__053f70727c0814e710c27facc22299ed4f245f5861ba5c27f9ab52e04299a301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeAllVersions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeRenditions")
    def include_renditions(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeRenditions"))

    @include_renditions.setter
    def include_renditions(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab7af7d436a55dc83acacbda2ea9ca719009595a651e71101d42a8d66e2babc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeRenditions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeSourceFiles")
    def include_source_files(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeSourceFiles"))

    @include_source_files.setter
    def include_source_files(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa5f6921b9a40584643745e554285c6fd869c55b440d44933ffc7b319998881e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeSourceFiles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed3310520a4666956b8b2104952fee1466dde9e7c1dc020f4defc5f532378099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__963852ccb306c7413a4dead4a24d1d19627808f227897bbbcc5d5c3e31f56966)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk",
    jsii_struct_bases=[],
    name_mapping={"object": "object"},
)
class AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk:
    def __init__(self, *, object: builtins.str) -> None:
        '''
        :param object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4adda9c9037726a1d2a42d49bf638e81453ab723f13617b27688902d1dddfb1)
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object": object,
        }

    @builtins.property
    def object(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#object AppflowFlow#object}.'''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendeskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendeskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b96adcea84a0f36ff1a748aca9b30e9cfbea01ef4001326e98fe44987df8718)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__effdd60ae7104a1a1acbf99d0866c661370e77f0c1ba8004df99a75477a6d57b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk]:
        return typing.cast(typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c27d156331dba5366a33bb5204a581538aea76ba54e9a2be76c1b85e799118c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowTask",
    jsii_struct_bases=[],
    name_mapping={
        "task_type": "taskType",
        "connector_operator": "connectorOperator",
        "destination_field": "destinationField",
        "source_fields": "sourceFields",
        "task_properties": "taskProperties",
    },
)
class AppflowFlowTask:
    def __init__(
        self,
        *,
        task_type: builtins.str,
        connector_operator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppflowFlowTaskConnectorOperator", typing.Dict[builtins.str, typing.Any]]]]] = None,
        destination_field: typing.Optional[builtins.str] = None,
        source_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        task_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param task_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#task_type AppflowFlow#task_type}.
        :param connector_operator: connector_operator block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#connector_operator AppflowFlow#connector_operator}
        :param destination_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#destination_field AppflowFlow#destination_field}.
        :param source_fields: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#source_fields AppflowFlow#source_fields}.
        :param task_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#task_properties AppflowFlow#task_properties}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__032f0b3320debf0283e94c645551125f796c53208e981bfc9e35473262686971)
            check_type(argname="argument task_type", value=task_type, expected_type=type_hints["task_type"])
            check_type(argname="argument connector_operator", value=connector_operator, expected_type=type_hints["connector_operator"])
            check_type(argname="argument destination_field", value=destination_field, expected_type=type_hints["destination_field"])
            check_type(argname="argument source_fields", value=source_fields, expected_type=type_hints["source_fields"])
            check_type(argname="argument task_properties", value=task_properties, expected_type=type_hints["task_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "task_type": task_type,
        }
        if connector_operator is not None:
            self._values["connector_operator"] = connector_operator
        if destination_field is not None:
            self._values["destination_field"] = destination_field
        if source_fields is not None:
            self._values["source_fields"] = source_fields
        if task_properties is not None:
            self._values["task_properties"] = task_properties

    @builtins.property
    def task_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#task_type AppflowFlow#task_type}.'''
        result = self._values.get("task_type")
        assert result is not None, "Required property 'task_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connector_operator(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppflowFlowTaskConnectorOperator"]]]:
        '''connector_operator block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#connector_operator AppflowFlow#connector_operator}
        '''
        result = self._values.get("connector_operator")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppflowFlowTaskConnectorOperator"]]], result)

    @builtins.property
    def destination_field(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#destination_field AppflowFlow#destination_field}.'''
        result = self._values.get("destination_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#source_fields AppflowFlow#source_fields}.'''
        result = self._values.get("source_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def task_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#task_properties AppflowFlow#task_properties}.'''
        result = self._values.get("task_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowTask(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowTaskConnectorOperator",
    jsii_struct_bases=[],
    name_mapping={
        "amplitude": "amplitude",
        "custom_connector": "customConnector",
        "datadog": "datadog",
        "dynatrace": "dynatrace",
        "google_analytics": "googleAnalytics",
        "infor_nexus": "inforNexus",
        "marketo": "marketo",
        "s3": "s3",
        "salesforce": "salesforce",
        "sapo_data": "sapoData",
        "service_now": "serviceNow",
        "singular": "singular",
        "slack": "slack",
        "trendmicro": "trendmicro",
        "veeva": "veeva",
        "zendesk": "zendesk",
    },
)
class AppflowFlowTaskConnectorOperator:
    def __init__(
        self,
        *,
        amplitude: typing.Optional[builtins.str] = None,
        custom_connector: typing.Optional[builtins.str] = None,
        datadog: typing.Optional[builtins.str] = None,
        dynatrace: typing.Optional[builtins.str] = None,
        google_analytics: typing.Optional[builtins.str] = None,
        infor_nexus: typing.Optional[builtins.str] = None,
        marketo: typing.Optional[builtins.str] = None,
        s3: typing.Optional[builtins.str] = None,
        salesforce: typing.Optional[builtins.str] = None,
        sapo_data: typing.Optional[builtins.str] = None,
        service_now: typing.Optional[builtins.str] = None,
        singular: typing.Optional[builtins.str] = None,
        slack: typing.Optional[builtins.str] = None,
        trendmicro: typing.Optional[builtins.str] = None,
        veeva: typing.Optional[builtins.str] = None,
        zendesk: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param amplitude: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#amplitude AppflowFlow#amplitude}.
        :param custom_connector: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#custom_connector AppflowFlow#custom_connector}.
        :param datadog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#datadog AppflowFlow#datadog}.
        :param dynatrace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#dynatrace AppflowFlow#dynatrace}.
        :param google_analytics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#google_analytics AppflowFlow#google_analytics}.
        :param infor_nexus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#infor_nexus AppflowFlow#infor_nexus}.
        :param marketo: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#marketo AppflowFlow#marketo}.
        :param s3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#s3 AppflowFlow#s3}.
        :param salesforce: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#salesforce AppflowFlow#salesforce}.
        :param sapo_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#sapo_data AppflowFlow#sapo_data}.
        :param service_now: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#service_now AppflowFlow#service_now}.
        :param singular: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#singular AppflowFlow#singular}.
        :param slack: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#slack AppflowFlow#slack}.
        :param trendmicro: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#trendmicro AppflowFlow#trendmicro}.
        :param veeva: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#veeva AppflowFlow#veeva}.
        :param zendesk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#zendesk AppflowFlow#zendesk}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b564d03e2b87d941eea2e4c8d73e5a99c234f237d7443b653f5c1d0af3e8bc)
            check_type(argname="argument amplitude", value=amplitude, expected_type=type_hints["amplitude"])
            check_type(argname="argument custom_connector", value=custom_connector, expected_type=type_hints["custom_connector"])
            check_type(argname="argument datadog", value=datadog, expected_type=type_hints["datadog"])
            check_type(argname="argument dynatrace", value=dynatrace, expected_type=type_hints["dynatrace"])
            check_type(argname="argument google_analytics", value=google_analytics, expected_type=type_hints["google_analytics"])
            check_type(argname="argument infor_nexus", value=infor_nexus, expected_type=type_hints["infor_nexus"])
            check_type(argname="argument marketo", value=marketo, expected_type=type_hints["marketo"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument salesforce", value=salesforce, expected_type=type_hints["salesforce"])
            check_type(argname="argument sapo_data", value=sapo_data, expected_type=type_hints["sapo_data"])
            check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
            check_type(argname="argument singular", value=singular, expected_type=type_hints["singular"])
            check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
            check_type(argname="argument trendmicro", value=trendmicro, expected_type=type_hints["trendmicro"])
            check_type(argname="argument veeva", value=veeva, expected_type=type_hints["veeva"])
            check_type(argname="argument zendesk", value=zendesk, expected_type=type_hints["zendesk"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if amplitude is not None:
            self._values["amplitude"] = amplitude
        if custom_connector is not None:
            self._values["custom_connector"] = custom_connector
        if datadog is not None:
            self._values["datadog"] = datadog
        if dynatrace is not None:
            self._values["dynatrace"] = dynatrace
        if google_analytics is not None:
            self._values["google_analytics"] = google_analytics
        if infor_nexus is not None:
            self._values["infor_nexus"] = infor_nexus
        if marketo is not None:
            self._values["marketo"] = marketo
        if s3 is not None:
            self._values["s3"] = s3
        if salesforce is not None:
            self._values["salesforce"] = salesforce
        if sapo_data is not None:
            self._values["sapo_data"] = sapo_data
        if service_now is not None:
            self._values["service_now"] = service_now
        if singular is not None:
            self._values["singular"] = singular
        if slack is not None:
            self._values["slack"] = slack
        if trendmicro is not None:
            self._values["trendmicro"] = trendmicro
        if veeva is not None:
            self._values["veeva"] = veeva
        if zendesk is not None:
            self._values["zendesk"] = zendesk

    @builtins.property
    def amplitude(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#amplitude AppflowFlow#amplitude}.'''
        result = self._values.get("amplitude")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_connector(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#custom_connector AppflowFlow#custom_connector}.'''
        result = self._values.get("custom_connector")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datadog(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#datadog AppflowFlow#datadog}.'''
        result = self._values.get("datadog")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dynatrace(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#dynatrace AppflowFlow#dynatrace}.'''
        result = self._values.get("dynatrace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def google_analytics(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#google_analytics AppflowFlow#google_analytics}.'''
        result = self._values.get("google_analytics")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def infor_nexus(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#infor_nexus AppflowFlow#infor_nexus}.'''
        result = self._values.get("infor_nexus")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def marketo(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#marketo AppflowFlow#marketo}.'''
        result = self._values.get("marketo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#s3 AppflowFlow#s3}.'''
        result = self._values.get("s3")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def salesforce(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#salesforce AppflowFlow#salesforce}.'''
        result = self._values.get("salesforce")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sapo_data(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#sapo_data AppflowFlow#sapo_data}.'''
        result = self._values.get("sapo_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_now(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#service_now AppflowFlow#service_now}.'''
        result = self._values.get("service_now")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def singular(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#singular AppflowFlow#singular}.'''
        result = self._values.get("singular")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slack(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#slack AppflowFlow#slack}.'''
        result = self._values.get("slack")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trendmicro(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#trendmicro AppflowFlow#trendmicro}.'''
        result = self._values.get("trendmicro")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def veeva(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#veeva AppflowFlow#veeva}.'''
        result = self._values.get("veeva")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zendesk(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#zendesk AppflowFlow#zendesk}.'''
        result = self._values.get("zendesk")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowTaskConnectorOperator(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowTaskConnectorOperatorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowTaskConnectorOperatorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6de6e551eebf67ec29b3002802241b86a43a73cbf76af08b3f6f3cc984b10876)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppflowFlowTaskConnectorOperatorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__899f616de9aa687077a5d90ecf3192a77254c0d748d16c69e4d57acee0fe83aa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppflowFlowTaskConnectorOperatorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f34252512e695c00403e5896dd70e1d157ce3d6b898537edb8fc36a21026706)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b14be611b7a1d35a545b3eabadece012cc330f050fb6fbbeba8b45bf67dbadd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa1ac3e897f3f80d4fc2806533ce8cacb38a55f11e6d5c65a0345a2301810506)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowTaskConnectorOperator]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowTaskConnectorOperator]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowTaskConnectorOperator]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4699f91a39a0753f79c890fea7c9861ef1d6c3789ceaa3574bcdb192f2b0bd94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowTaskConnectorOperatorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowTaskConnectorOperatorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__297fa2ec808e5888ae3f8f7bf1e233b3ba31f19303952e284f6458fc65aa2afc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAmplitude")
    def reset_amplitude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmplitude", []))

    @jsii.member(jsii_name="resetCustomConnector")
    def reset_custom_connector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomConnector", []))

    @jsii.member(jsii_name="resetDatadog")
    def reset_datadog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatadog", []))

    @jsii.member(jsii_name="resetDynatrace")
    def reset_dynatrace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynatrace", []))

    @jsii.member(jsii_name="resetGoogleAnalytics")
    def reset_google_analytics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogleAnalytics", []))

    @jsii.member(jsii_name="resetInforNexus")
    def reset_infor_nexus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInforNexus", []))

    @jsii.member(jsii_name="resetMarketo")
    def reset_marketo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMarketo", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

    @jsii.member(jsii_name="resetSalesforce")
    def reset_salesforce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSalesforce", []))

    @jsii.member(jsii_name="resetSapoData")
    def reset_sapo_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSapoData", []))

    @jsii.member(jsii_name="resetServiceNow")
    def reset_service_now(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceNow", []))

    @jsii.member(jsii_name="resetSingular")
    def reset_singular(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingular", []))

    @jsii.member(jsii_name="resetSlack")
    def reset_slack(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSlack", []))

    @jsii.member(jsii_name="resetTrendmicro")
    def reset_trendmicro(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrendmicro", []))

    @jsii.member(jsii_name="resetVeeva")
    def reset_veeva(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVeeva", []))

    @jsii.member(jsii_name="resetZendesk")
    def reset_zendesk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZendesk", []))

    @builtins.property
    @jsii.member(jsii_name="amplitudeInput")
    def amplitude_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "amplitudeInput"))

    @builtins.property
    @jsii.member(jsii_name="customConnectorInput")
    def custom_connector_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customConnectorInput"))

    @builtins.property
    @jsii.member(jsii_name="datadogInput")
    def datadog_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datadogInput"))

    @builtins.property
    @jsii.member(jsii_name="dynatraceInput")
    def dynatrace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dynatraceInput"))

    @builtins.property
    @jsii.member(jsii_name="googleAnalyticsInput")
    def google_analytics_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "googleAnalyticsInput"))

    @builtins.property
    @jsii.member(jsii_name="inforNexusInput")
    def infor_nexus_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inforNexusInput"))

    @builtins.property
    @jsii.member(jsii_name="marketoInput")
    def marketo_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "marketoInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="salesforceInput")
    def salesforce_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "salesforceInput"))

    @builtins.property
    @jsii.member(jsii_name="sapoDataInput")
    def sapo_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sapoDataInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNowInput")
    def service_now_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNowInput"))

    @builtins.property
    @jsii.member(jsii_name="singularInput")
    def singular_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "singularInput"))

    @builtins.property
    @jsii.member(jsii_name="slackInput")
    def slack_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "slackInput"))

    @builtins.property
    @jsii.member(jsii_name="trendmicroInput")
    def trendmicro_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trendmicroInput"))

    @builtins.property
    @jsii.member(jsii_name="veevaInput")
    def veeva_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "veevaInput"))

    @builtins.property
    @jsii.member(jsii_name="zendeskInput")
    def zendesk_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zendeskInput"))

    @builtins.property
    @jsii.member(jsii_name="amplitude")
    def amplitude(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "amplitude"))

    @amplitude.setter
    def amplitude(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba8114eb6829e1acecd1521557a412069f42741c875b32fafe4db7c73e0fb6e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "amplitude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customConnector")
    def custom_connector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customConnector"))

    @custom_connector.setter
    def custom_connector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ad9e99d92bfbce263411f993884067670920b5d39ff0ba831802216ec2a3a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customConnector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datadog")
    def datadog(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datadog"))

    @datadog.setter
    def datadog(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e32b53437ff2326b99bfa58d8d94dbdcf5e9a36b237141dbf969a051f3d883)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datadog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dynatrace")
    def dynatrace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dynatrace"))

    @dynatrace.setter
    def dynatrace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f14724deb8864f8d74ef1642972fe4a171161032a06acb338de358af19ff3ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dynatrace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="googleAnalytics")
    def google_analytics(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "googleAnalytics"))

    @google_analytics.setter
    def google_analytics(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ee92764e4889ebf51dab03f1b7ded7cc7e54c7428df050e2eca757df901144b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "googleAnalytics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inforNexus")
    def infor_nexus(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inforNexus"))

    @infor_nexus.setter
    def infor_nexus(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c6dc1e91a62489a21480648caeb9951f15ac3b46bdcc4a7cfa39ec38d2cfc2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inforNexus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="marketo")
    def marketo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "marketo"))

    @marketo.setter
    def marketo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__863cbd8eef90602a62aee1af7299274fef4c5f7f9248dbb77a1798935e29143d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "marketo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3"))

    @s3.setter
    def s3(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84685f32d0153a27cfdca9bbe6f3548e3ec16438595c1fafbe7a414aa756fb17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="salesforce")
    def salesforce(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "salesforce"))

    @salesforce.setter
    def salesforce(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efddaab84664c4ac3de52983d2416825202ea8cf5eff58d574a4e79ea3879851)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "salesforce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sapoData")
    def sapo_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sapoData"))

    @sapo_data.setter
    def sapo_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e33f6b1894d00cec0d47a022251836c0e0efae7c7fc3fad2ac185456fde3616)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sapoData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceNow")
    def service_now(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceNow"))

    @service_now.setter
    def service_now(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce4286ee4a90ca8176266944cb35ac1d76d7251dbc4c519cce71a0ee781fe9af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceNow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="singular")
    def singular(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "singular"))

    @singular.setter
    def singular(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d54c0e8b14a27e19d52f638eee6f7b1c01e97c0c351f1ee18a8dfe1b1fa1f44f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "singular", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="slack")
    def slack(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "slack"))

    @slack.setter
    def slack(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9453b1a979cbf8db4a88c9d30e34f7d4144aac78e864b40f0807af4d9c33dfe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slack", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trendmicro")
    def trendmicro(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trendmicro"))

    @trendmicro.setter
    def trendmicro(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4e71749c147f9eb4835d3d3b25854eab06bd980dbc83b1dbb92e206a5dcd827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trendmicro", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="veeva")
    def veeva(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "veeva"))

    @veeva.setter
    def veeva(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31d1108bae8652e116e2790dca75ec389c311c4f0919a4bf9438fac8031d5d9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "veeva", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zendesk")
    def zendesk(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zendesk"))

    @zendesk.setter
    def zendesk(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e871c1efa9aca4cb1a6e7480d2ea68c082f92b46c638952bc2c52f8a72db95d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zendesk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowTaskConnectorOperator]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowTaskConnectorOperator]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowTaskConnectorOperator]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88c9382daeff73f33a1de4c70dbb9f0f831d81d7b1e50fef54982d0ebce0cbd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowTaskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowTaskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fd0da3847d3cb91fd1d08da13e24462cd2d119414086ab002ca4ac87fd3cdd3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AppflowFlowTaskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af4769efa92edceb67d9da1029ea9a06b58dcc5467f6bc086e61b37104642db8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppflowFlowTaskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11d865c26a7a5e7d7e87283d5fc0fd63091e61b0404bd596cfc96b8d998a92a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b167624c32796a8b608a5db0ec59371f61268da6f65934ef63ece87904db8271)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b6ce201d119473652f177e283f95e299febe7cec12a2fa11c90c5afd71eb80d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowTask]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowTask]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowTask]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01217ff218ddea0ff17bd3b27404f8c176b17a9f21ab8b9703f7320bb5be96d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppflowFlowTaskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowTaskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__249de5ae529ca125cfce51a256f338c70df4a951cd37bc12f24b30a9752089f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putConnectorOperator")
    def put_connector_operator(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppflowFlowTaskConnectorOperator, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a1bffd5711bdda174788416f1ac3a9b18483b72fc7adabe739b208e6605ed1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConnectorOperator", [value]))

    @jsii.member(jsii_name="resetConnectorOperator")
    def reset_connector_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectorOperator", []))

    @jsii.member(jsii_name="resetDestinationField")
    def reset_destination_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationField", []))

    @jsii.member(jsii_name="resetSourceFields")
    def reset_source_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceFields", []))

    @jsii.member(jsii_name="resetTaskProperties")
    def reset_task_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaskProperties", []))

    @builtins.property
    @jsii.member(jsii_name="connectorOperator")
    def connector_operator(self) -> AppflowFlowTaskConnectorOperatorList:
        return typing.cast(AppflowFlowTaskConnectorOperatorList, jsii.get(self, "connectorOperator"))

    @builtins.property
    @jsii.member(jsii_name="connectorOperatorInput")
    def connector_operator_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowTaskConnectorOperator]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowTaskConnectorOperator]]], jsii.get(self, "connectorOperatorInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationFieldInput")
    def destination_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFieldsInput")
    def source_fields_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sourceFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="taskPropertiesInput")
    def task_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "taskPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="taskTypeInput")
    def task_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "taskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationField")
    def destination_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationField"))

    @destination_field.setter
    def destination_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5c90f2d01c61b6158013709cf4414d0fa82f06622eb4c86c6ee5eef3abb926c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceFields")
    def source_fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sourceFields"))

    @source_fields.setter
    def source_fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e1278fa3ecf68b81a023cb4e45b0dba24b1fd11da53feb97d635c4c7c570cca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskProperties")
    def task_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "taskProperties"))

    @task_properties.setter
    def task_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3fcef36856c663449e30b9867997ec345e00ef9fb0501c959e1990f08459758)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskType")
    def task_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskType"))

    @task_type.setter
    def task_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc0f3edbe2d0091b295b99a3c4ef4acc73bff4eb5e65dff738a8eda6df5733c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowTask]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowTask]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowTask]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__164be8a02a72a49ce6949e2a1400137c87fcb6ccb810763147a2bc8526a7ef8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowTriggerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "trigger_type": "triggerType",
        "trigger_properties": "triggerProperties",
    },
)
class AppflowFlowTriggerConfig:
    def __init__(
        self,
        *,
        trigger_type: builtins.str,
        trigger_properties: typing.Optional[typing.Union["AppflowFlowTriggerConfigTriggerProperties", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param trigger_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#trigger_type AppflowFlow#trigger_type}.
        :param trigger_properties: trigger_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#trigger_properties AppflowFlow#trigger_properties}
        '''
        if isinstance(trigger_properties, dict):
            trigger_properties = AppflowFlowTriggerConfigTriggerProperties(**trigger_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f02605cf1c48838b54b5b9b91d7420bbb6d342b5714005818ccda94319a89e6)
            check_type(argname="argument trigger_type", value=trigger_type, expected_type=type_hints["trigger_type"])
            check_type(argname="argument trigger_properties", value=trigger_properties, expected_type=type_hints["trigger_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "trigger_type": trigger_type,
        }
        if trigger_properties is not None:
            self._values["trigger_properties"] = trigger_properties

    @builtins.property
    def trigger_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#trigger_type AppflowFlow#trigger_type}.'''
        result = self._values.get("trigger_type")
        assert result is not None, "Required property 'trigger_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trigger_properties(
        self,
    ) -> typing.Optional["AppflowFlowTriggerConfigTriggerProperties"]:
        '''trigger_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#trigger_properties AppflowFlow#trigger_properties}
        '''
        result = self._values.get("trigger_properties")
        return typing.cast(typing.Optional["AppflowFlowTriggerConfigTriggerProperties"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowTriggerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowTriggerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowTriggerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03784bfcceea61ed1f71cd0f1b689123dba57298d06abfd06f7496bd60db9577)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTriggerProperties")
    def put_trigger_properties(
        self,
        *,
        scheduled: typing.Optional[typing.Union["AppflowFlowTriggerConfigTriggerPropertiesScheduled", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scheduled: scheduled block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#scheduled AppflowFlow#scheduled}
        '''
        value = AppflowFlowTriggerConfigTriggerProperties(scheduled=scheduled)

        return typing.cast(None, jsii.invoke(self, "putTriggerProperties", [value]))

    @jsii.member(jsii_name="resetTriggerProperties")
    def reset_trigger_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerProperties", []))

    @builtins.property
    @jsii.member(jsii_name="triggerProperties")
    def trigger_properties(
        self,
    ) -> "AppflowFlowTriggerConfigTriggerPropertiesOutputReference":
        return typing.cast("AppflowFlowTriggerConfigTriggerPropertiesOutputReference", jsii.get(self, "triggerProperties"))

    @builtins.property
    @jsii.member(jsii_name="triggerPropertiesInput")
    def trigger_properties_input(
        self,
    ) -> typing.Optional["AppflowFlowTriggerConfigTriggerProperties"]:
        return typing.cast(typing.Optional["AppflowFlowTriggerConfigTriggerProperties"], jsii.get(self, "triggerPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerTypeInput")
    def trigger_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "triggerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerType")
    def trigger_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerType"))

    @trigger_type.setter
    def trigger_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74c1460a10f2c207d5fbfe9b2fb4293b48f8b56d41aec979a3bab194ead0558f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppflowFlowTriggerConfig]:
        return typing.cast(typing.Optional[AppflowFlowTriggerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AppflowFlowTriggerConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3504b794331a8e898dc761e271c7d23b65deb9caf2529d78fb8fe805a6e324ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowTriggerConfigTriggerProperties",
    jsii_struct_bases=[],
    name_mapping={"scheduled": "scheduled"},
)
class AppflowFlowTriggerConfigTriggerProperties:
    def __init__(
        self,
        *,
        scheduled: typing.Optional[typing.Union["AppflowFlowTriggerConfigTriggerPropertiesScheduled", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scheduled: scheduled block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#scheduled AppflowFlow#scheduled}
        '''
        if isinstance(scheduled, dict):
            scheduled = AppflowFlowTriggerConfigTriggerPropertiesScheduled(**scheduled)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8444b7978d00c69ef1cd0f31692447e8630d2e57ae0751707b8c554b9cac9fde)
            check_type(argname="argument scheduled", value=scheduled, expected_type=type_hints["scheduled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if scheduled is not None:
            self._values["scheduled"] = scheduled

    @builtins.property
    def scheduled(
        self,
    ) -> typing.Optional["AppflowFlowTriggerConfigTriggerPropertiesScheduled"]:
        '''scheduled block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#scheduled AppflowFlow#scheduled}
        '''
        result = self._values.get("scheduled")
        return typing.cast(typing.Optional["AppflowFlowTriggerConfigTriggerPropertiesScheduled"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowTriggerConfigTriggerProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowTriggerConfigTriggerPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowTriggerConfigTriggerPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7b22e53c39700d6c44c087298024d449c161fec5cce81489e99617ac3689ce7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putScheduled")
    def put_scheduled(
        self,
        *,
        schedule_expression: builtins.str,
        data_pull_mode: typing.Optional[builtins.str] = None,
        first_execution_from: typing.Optional[builtins.str] = None,
        schedule_end_time: typing.Optional[builtins.str] = None,
        schedule_offset: typing.Optional[jsii.Number] = None,
        schedule_start_time: typing.Optional[builtins.str] = None,
        timezone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schedule_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#schedule_expression AppflowFlow#schedule_expression}.
        :param data_pull_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#data_pull_mode AppflowFlow#data_pull_mode}.
        :param first_execution_from: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#first_execution_from AppflowFlow#first_execution_from}.
        :param schedule_end_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#schedule_end_time AppflowFlow#schedule_end_time}.
        :param schedule_offset: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#schedule_offset AppflowFlow#schedule_offset}.
        :param schedule_start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#schedule_start_time AppflowFlow#schedule_start_time}.
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#timezone AppflowFlow#timezone}.
        '''
        value = AppflowFlowTriggerConfigTriggerPropertiesScheduled(
            schedule_expression=schedule_expression,
            data_pull_mode=data_pull_mode,
            first_execution_from=first_execution_from,
            schedule_end_time=schedule_end_time,
            schedule_offset=schedule_offset,
            schedule_start_time=schedule_start_time,
            timezone=timezone,
        )

        return typing.cast(None, jsii.invoke(self, "putScheduled", [value]))

    @jsii.member(jsii_name="resetScheduled")
    def reset_scheduled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduled", []))

    @builtins.property
    @jsii.member(jsii_name="scheduled")
    def scheduled(
        self,
    ) -> "AppflowFlowTriggerConfigTriggerPropertiesScheduledOutputReference":
        return typing.cast("AppflowFlowTriggerConfigTriggerPropertiesScheduledOutputReference", jsii.get(self, "scheduled"))

    @builtins.property
    @jsii.member(jsii_name="scheduledInput")
    def scheduled_input(
        self,
    ) -> typing.Optional["AppflowFlowTriggerConfigTriggerPropertiesScheduled"]:
        return typing.cast(typing.Optional["AppflowFlowTriggerConfigTriggerPropertiesScheduled"], jsii.get(self, "scheduledInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowTriggerConfigTriggerProperties]:
        return typing.cast(typing.Optional[AppflowFlowTriggerConfigTriggerProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowTriggerConfigTriggerProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94fa974da1248f3e83382dd3c02e65a5357d6b8c952727310c8e5457ce556bd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowTriggerConfigTriggerPropertiesScheduled",
    jsii_struct_bases=[],
    name_mapping={
        "schedule_expression": "scheduleExpression",
        "data_pull_mode": "dataPullMode",
        "first_execution_from": "firstExecutionFrom",
        "schedule_end_time": "scheduleEndTime",
        "schedule_offset": "scheduleOffset",
        "schedule_start_time": "scheduleStartTime",
        "timezone": "timezone",
    },
)
class AppflowFlowTriggerConfigTriggerPropertiesScheduled:
    def __init__(
        self,
        *,
        schedule_expression: builtins.str,
        data_pull_mode: typing.Optional[builtins.str] = None,
        first_execution_from: typing.Optional[builtins.str] = None,
        schedule_end_time: typing.Optional[builtins.str] = None,
        schedule_offset: typing.Optional[jsii.Number] = None,
        schedule_start_time: typing.Optional[builtins.str] = None,
        timezone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schedule_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#schedule_expression AppflowFlow#schedule_expression}.
        :param data_pull_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#data_pull_mode AppflowFlow#data_pull_mode}.
        :param first_execution_from: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#first_execution_from AppflowFlow#first_execution_from}.
        :param schedule_end_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#schedule_end_time AppflowFlow#schedule_end_time}.
        :param schedule_offset: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#schedule_offset AppflowFlow#schedule_offset}.
        :param schedule_start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#schedule_start_time AppflowFlow#schedule_start_time}.
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#timezone AppflowFlow#timezone}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a74662ec2243a2072d7d6e2637b26d4cce0b8a68989e65f11207421d6e7730d)
            check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
            check_type(argname="argument data_pull_mode", value=data_pull_mode, expected_type=type_hints["data_pull_mode"])
            check_type(argname="argument first_execution_from", value=first_execution_from, expected_type=type_hints["first_execution_from"])
            check_type(argname="argument schedule_end_time", value=schedule_end_time, expected_type=type_hints["schedule_end_time"])
            check_type(argname="argument schedule_offset", value=schedule_offset, expected_type=type_hints["schedule_offset"])
            check_type(argname="argument schedule_start_time", value=schedule_start_time, expected_type=type_hints["schedule_start_time"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schedule_expression": schedule_expression,
        }
        if data_pull_mode is not None:
            self._values["data_pull_mode"] = data_pull_mode
        if first_execution_from is not None:
            self._values["first_execution_from"] = first_execution_from
        if schedule_end_time is not None:
            self._values["schedule_end_time"] = schedule_end_time
        if schedule_offset is not None:
            self._values["schedule_offset"] = schedule_offset
        if schedule_start_time is not None:
            self._values["schedule_start_time"] = schedule_start_time
        if timezone is not None:
            self._values["timezone"] = timezone

    @builtins.property
    def schedule_expression(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#schedule_expression AppflowFlow#schedule_expression}.'''
        result = self._values.get("schedule_expression")
        assert result is not None, "Required property 'schedule_expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_pull_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#data_pull_mode AppflowFlow#data_pull_mode}.'''
        result = self._values.get("data_pull_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def first_execution_from(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#first_execution_from AppflowFlow#first_execution_from}.'''
        result = self._values.get("first_execution_from")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_end_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#schedule_end_time AppflowFlow#schedule_end_time}.'''
        result = self._values.get("schedule_end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_offset(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#schedule_offset AppflowFlow#schedule_offset}.'''
        result = self._values.get("schedule_offset")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def schedule_start_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#schedule_start_time AppflowFlow#schedule_start_time}.'''
        result = self._values.get("schedule_start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appflow_flow#timezone AppflowFlow#timezone}.'''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppflowFlowTriggerConfigTriggerPropertiesScheduled(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppflowFlowTriggerConfigTriggerPropertiesScheduledOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appflowFlow.AppflowFlowTriggerConfigTriggerPropertiesScheduledOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93d189d7753b6aacef4b0fe4aa9c854b4675e6dc8f55239df3c283a87aba1caa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDataPullMode")
    def reset_data_pull_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataPullMode", []))

    @jsii.member(jsii_name="resetFirstExecutionFrom")
    def reset_first_execution_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstExecutionFrom", []))

    @jsii.member(jsii_name="resetScheduleEndTime")
    def reset_schedule_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleEndTime", []))

    @jsii.member(jsii_name="resetScheduleOffset")
    def reset_schedule_offset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleOffset", []))

    @jsii.member(jsii_name="resetScheduleStartTime")
    def reset_schedule_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleStartTime", []))

    @jsii.member(jsii_name="resetTimezone")
    def reset_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimezone", []))

    @builtins.property
    @jsii.member(jsii_name="dataPullModeInput")
    def data_pull_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataPullModeInput"))

    @builtins.property
    @jsii.member(jsii_name="firstExecutionFromInput")
    def first_execution_from_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firstExecutionFromInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleEndTimeInput")
    def schedule_end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleEndTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleExpressionInput")
    def schedule_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleOffsetInput")
    def schedule_offset_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scheduleOffsetInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleStartTimeInput")
    def schedule_start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleStartTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="timezoneInput")
    def timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="dataPullMode")
    def data_pull_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataPullMode"))

    @data_pull_mode.setter
    def data_pull_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d7a36e2a8de737866e9c8444d4da6312306cbf8748d2c0df81a791d0546dd67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataPullMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firstExecutionFrom")
    def first_execution_from(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firstExecutionFrom"))

    @first_execution_from.setter
    def first_execution_from(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3a57d6b986f70124b5b4c9319e84b49ff7f912527026ca94e2e50af4b6fd5bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstExecutionFrom", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduleEndTime")
    def schedule_end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduleEndTime"))

    @schedule_end_time.setter
    def schedule_end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__215789b1bb9fc834eec20455975c9faff4d0326163b6a4b844795b79400f98cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleEndTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduleExpression")
    def schedule_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduleExpression"))

    @schedule_expression.setter
    def schedule_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6820a9bac949a0652f776a7cf5db47cf1724a0d9d72ea70ed8c714dee28be12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduleOffset")
    def schedule_offset(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scheduleOffset"))

    @schedule_offset.setter
    def schedule_offset(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f246b74cea6070aaa0a4e4eade4efa5933e154969cd61c0979c3be7a3b1158c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleOffset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduleStartTime")
    def schedule_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduleStartTime"))

    @schedule_start_time.setter
    def schedule_start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4958fe502c0bccd9943c9efcd7dddca7fefaa2b2b0b9b9c8cc713437a9ef4392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleStartTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd758aa24be8f82f1e7b92add92bf219411ce80787bf6ab0b4c5036aad327870)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppflowFlowTriggerConfigTriggerPropertiesScheduled]:
        return typing.cast(typing.Optional[AppflowFlowTriggerConfigTriggerPropertiesScheduled], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppflowFlowTriggerConfigTriggerPropertiesScheduled],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13fe73649002222d98ab18216ea00bc4c3de175cc1b2052f10a04a2d5cae8c7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AppflowFlow",
    "AppflowFlowConfig",
    "AppflowFlowDestinationFlowConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorProperties",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfilesOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetricsOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3OutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfigOutputReference",
    "AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskOutputReference",
    "AppflowFlowDestinationFlowConfigList",
    "AppflowFlowDestinationFlowConfigOutputReference",
    "AppflowFlowMetadataCatalogConfig",
    "AppflowFlowMetadataCatalogConfigGlueDataCatalog",
    "AppflowFlowMetadataCatalogConfigGlueDataCatalogOutputReference",
    "AppflowFlowMetadataCatalogConfigOutputReference",
    "AppflowFlowSourceFlowConfig",
    "AppflowFlowSourceFlowConfigIncrementalPullConfig",
    "AppflowFlowSourceFlowConfigIncrementalPullConfigOutputReference",
    "AppflowFlowSourceFlowConfigOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorProperties",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitudeOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnectorOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadogOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatraceOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalyticsOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexusOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketoOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3OutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfigOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforceOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfigOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfigOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNowOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingularOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlackOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicroOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeevaOutputReference",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk",
    "AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendeskOutputReference",
    "AppflowFlowTask",
    "AppflowFlowTaskConnectorOperator",
    "AppflowFlowTaskConnectorOperatorList",
    "AppflowFlowTaskConnectorOperatorOutputReference",
    "AppflowFlowTaskList",
    "AppflowFlowTaskOutputReference",
    "AppflowFlowTriggerConfig",
    "AppflowFlowTriggerConfigOutputReference",
    "AppflowFlowTriggerConfigTriggerProperties",
    "AppflowFlowTriggerConfigTriggerPropertiesOutputReference",
    "AppflowFlowTriggerConfigTriggerPropertiesScheduled",
    "AppflowFlowTriggerConfigTriggerPropertiesScheduledOutputReference",
]

publication.publish()

def _typecheckingstub__d87b7a889f09084356b4785287e271fe7c7d575dd5706460f25b5785b95cb831(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    destination_flow_config: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppflowFlowDestinationFlowConfig, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    source_flow_config: typing.Union[AppflowFlowSourceFlowConfig, typing.Dict[builtins.str, typing.Any]],
    task: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppflowFlowTask, typing.Dict[builtins.str, typing.Any]]]],
    trigger_config: typing.Union[AppflowFlowTriggerConfig, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kms_arn: typing.Optional[builtins.str] = None,
    metadata_catalog_config: typing.Optional[typing.Union[AppflowFlowMetadataCatalogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__70513549323f47dfdfac450681572ceae92e2f214f808171149b6ca6ff2cf5ed(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__913968eb2f5b699068dde5a422c098cef6cb5596c18eb8c4d675f9ad736961df(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppflowFlowDestinationFlowConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__953d6700bc06c6a3adbfcd80db48d7a68d05acba8a8ea1a567144dcbb9ffd3cb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppflowFlowTask, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b5737fae8c7a42cc58035ae7edbf255236c23d40d1aff41fada6bb7eb8fac3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b59797496b1723c5cd3c3ce57b6ab68b683a78ef92eeedfbcaab7061eb0f082c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aabff0622f256fda199a512073840fa855719d2a14d26a9a85fc34f97626555(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f32637f34d095fc8f327c0c36320467563a45dbe5783acf783b1458c0f29b8f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6ec73e5f95bf8e591fd759a8b8436f9e235aada3ae730b2c55d844575a89f3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef33f54794f328f0a72ba3c543fa0447edcf5d21a38e520e2af65d84568769f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a19cf89201414855e847d1800699f7061d41ce1e752fd0e619954c7bd13ae79(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52215339cd0c23b9ea696463a23422ead294d421baf060b0ef512288278aa7d6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    destination_flow_config: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppflowFlowDestinationFlowConfig, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    source_flow_config: typing.Union[AppflowFlowSourceFlowConfig, typing.Dict[builtins.str, typing.Any]],
    task: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppflowFlowTask, typing.Dict[builtins.str, typing.Any]]]],
    trigger_config: typing.Union[AppflowFlowTriggerConfig, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kms_arn: typing.Optional[builtins.str] = None,
    metadata_catalog_config: typing.Optional[typing.Union[AppflowFlowMetadataCatalogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dec8377c34a5db11a8af7937da3304aadc9a7c459fa974485a592fb4661e08f(
    *,
    connector_type: builtins.str,
    destination_connector_properties: typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorProperties, typing.Dict[builtins.str, typing.Any]],
    api_version: typing.Optional[builtins.str] = None,
    connector_profile_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed57656833a4a00eafaef3f65ca9cfaf001c4123586b8918f8a1ba34b0723817(
    *,
    custom_connector: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector, typing.Dict[builtins.str, typing.Any]]] = None,
    customer_profiles: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles, typing.Dict[builtins.str, typing.Any]]] = None,
    event_bridge: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge, typing.Dict[builtins.str, typing.Any]]] = None,
    honeycode: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode, typing.Dict[builtins.str, typing.Any]]] = None,
    lookout_metrics: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
    marketo: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo, typing.Dict[builtins.str, typing.Any]]] = None,
    redshift: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift, typing.Dict[builtins.str, typing.Any]]] = None,
    s3: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3, typing.Dict[builtins.str, typing.Any]]] = None,
    salesforce: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce, typing.Dict[builtins.str, typing.Any]]] = None,
    sapo_data: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData, typing.Dict[builtins.str, typing.Any]]] = None,
    snowflake: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake, typing.Dict[builtins.str, typing.Any]]] = None,
    upsolver: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver, typing.Dict[builtins.str, typing.Any]]] = None,
    zendesk: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83322459e4998728046f7cb8e976b83896bb05622bffb572365cb0018ef5425(
    *,
    entity_name: builtins.str,
    custom_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    write_operation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd07cb72b1309efb6bb26b4075c607cb2027ca54f2b827b092622192b284079(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12e970b5343a0b1ffdcc445387e5eadf5932bdd2469c0991d55845ff0c774ae0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a7cbd7a0a22927f7d28d10227d6485103b5eb296d2036dc03d3163ffd421c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c57f2e59f42fe9aa0b3029e9ac6192fe56014900c57f441c37454d8b7598be10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__477296934bac5029bb9ebb0d8bce0c9e7c49cd9ded585d056f5c38833fbc36a3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602e89d60a44698fb8fb19e2cbf499ce6ac88dc7aa456a5df75484f01dfd184e(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnectorErrorHandlingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e60110e4ca757f066011371d32661af88a2209d7661dc821554fa70d860484(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de09bc7c4bb9290646b49a8bc71af167fc303feb6f772352c6cd25051ac40171(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fef7733ddfb66222eb556070f77f7cd71c4049ad63d4ff8952a142642a06932(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c8c9693cb5008b6db4a46937d679f1f2f26bcdef98d8d4a63f77addba041f9c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79871b22cc0fadf3c31c91cf3140be8a3db0e2cb73e7cc27af6d2256346b0009(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b5009ea5584c86c58f81d1676ce0fe64156d4326d6a3e77c4adc03c8d235fd3(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomConnector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42104c8e7a4eaaae81591062604e90776307cc78dca22aae9607fd260e7769bc(
    *,
    domain_name: builtins.str,
    object_type_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb4e56660ce1c47ebc8fb10fd6dba00b85da1eae3438c555861d98522c1ccdc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73dc472fbb39544065ef621a43e67101faa902b66ec9290f1c09972514657f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a13fcf9656600762db67a92a6a85fd1e31472d341113fb75204c5afd1bb8dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51fa46d45e7314e40ee6c4a84b3ad8f2b503a44113a6425ded736c4d15459c8e(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesCustomerProfiles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f01149afa1d7c21f9e88cddc5f8da87144fa6755dfe482e19b9d31fd54efab3(
    *,
    object: builtins.str,
    error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c86b6a420d9a483a3c0e4ed9741ffbae6f2a012c139db7d9931a5c6eb225246(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c17b657618cfcc8e554b7a5ebbf8aea8dd732cf5dc8c0a3b7461407c4239a04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b60e56a348b9104860f73d54171015b996a885e65e8f1fb79a6620a48bbb27c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a834ced275323a69cfb14ec32a3ec466b570621db590548efd226cf6c4f18ed6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6fc197325ee2725e34a8e64011c14c289b7e921cc7895c1b6e01b6fd28e0a6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c01779b412c71137a57e494a4616db4886a45e572788e890896c7835eb3be0a6(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridgeErrorHandlingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd67fcca0a85ed3f3cd2fd8a1200b67d5efd8fa062123e03031658d7589f570f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__221a75674ab77a92e68f57a10b551832b58332fbf541684834ee556117cc83bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4465c4b1d73b0827e49e4d9b717ed314290693dc3e95f13fd643a0b6e74fb8c3(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesEventBridge],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da8136a24b7c1437a7a9a0f56cb1ff44eb8a3992e39276ca1cea0a1efeef8786(
    *,
    object: builtins.str,
    error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d7b212ccacab69f176753ae13d35d4e1e344c7dadafa66e031bbeda570036c6(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b03ac175ab9b0889d3271ba40765e0e2af064fc4b072d2f2b554f85e81699277(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15007148a3a998948f3278450c193afd681d52a5605e664d3aaa7d106d57887e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30edd3923ffd3c279e1d6cf33e4f232faaeed31d1e73aa1097d01ffc4528b6bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0bf4b761e8ca9b93c54a4692f1539a121c912b25759e51bfd68d8fceb279621(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ad9cb3d365b7d2446bfe4468d5245c0c8aed0a731b8f4af0de3479410343042(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycodeErrorHandlingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c286764edc1536a536a25cc3ea5f967428d2e1ccee8e2252ce2e3bc4f30929(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__446eda0fea14f5412705b75c1025028b1899234e8e5c390f93ace188abcc591a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58deae5cd564d02518de3bf146c2d324dfacaa98b0a1f96bfd315cb2adf3eace(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesHoneycode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72efdf4d4afae2b2aebf66800f0430a57b6795265f5f8545891dd91e85957bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8302fda89a97d4dde8eb65f95f595cd29e6bcef4dfce7a083335923a5d1ebf25(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesLookoutMetrics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db131d1aba3c92118f52dc060e586d479ef45b2676e14180620f71a73f035a5(
    *,
    object: builtins.str,
    error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4257ebf29e7a19c0d94e29e2ab5634818f14f10c3a71240af3bedda6b0d6841(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33edd82e5bed2dd02b3c41b76a293b208111ff76525c5a1f4ec69212f36497bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4fcb8eea924d2da16d3ca07f6bc6bd829e98bf0d7ae970bef36b3a7db7d494e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0526fff870014c0e56079f321b096570b156be1a3addfe3b1ef824204f49fa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb47289fc157b763f5b3141186f105e1a2829af321b02cee2620fdccb967aa87(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef325b4707970350e116516ee1166b4588c046b617d39fa1a90393d9b2bae770(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketoErrorHandlingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec22d870d5d47a31ab4c4d2fa2f2ec6880c663b895b77b2dab1743d380df4504(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b769f600fee0a4c91c2f929b966eb2eb557a665f26397e15b3e6121d1257c076(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34e4e59452dd6b2556c987b8ea85802cc9f5287fbc01ba8f5ed0a117f44c9ad(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesMarketo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f87e84fff61358d402884dd546a5c34b9b5b6430d23d9c4a65accd23ed7d92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e824fac4774ef3cdb7a8c36c062cead1a5be4bb9062c7d76ed6c9b9bfce6ae(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2998c6235e24a5d8d3745e1cdd7838c56230d7a3ee305e359d0cc5245118bf56(
    *,
    intermediate_bucket_name: builtins.str,
    object: builtins.str,
    bucket_prefix: typing.Optional[builtins.str] = None,
    error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e2caf790073e375667fbcc3ed2d0bbe794889619c57ea897457f775be37147(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bbbb7e91a4344f25e2d61e750d0d239e20cf544d07d0e63e3beec69cb543415(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a5c9512258b07c43ba9efb2f61b5a5b34dd4159aec5c2b8ef2025afe648f2ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c717c92fc3cf2ba84a8f8fda1e8fea78a5b8e7b9843587ed1b33d53595df0f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f2626bc0393f8c610bd40c18e3e6040e2921b7fc244b0c8b03ca2a4faa35ae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a19afe3f4fa6e1ada916f742d5d10f3a5a0818f4425c086ff9a3d319f62f17(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshiftErrorHandlingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e453869d325bbfe1af90b7ac0c577f326d3cb1c8a03efcaff5ad12c3b34399a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17dc1b57ef79a273f3bcb714bbc64d6cd3da4f306e17d0e672f2c3b309a18f31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207ba1fad613c39aec2ce15f027200ee8f75d29c3b44962e7a731ab8e5c45324(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e6868af5bb63edc2f5e10b787fb077f9bf0e931d73e9c80811215222ec3d444(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d0590c1a1ef75f56a9c8bdec6c90adab6d9af93b22fdd8e3d3908cf54412d9(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesRedshift],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f43f5913d99166a3f2b5c762e62bbc1584c64c779db89bdd5580bf9c05fdcc(
    *,
    bucket_name: builtins.str,
    bucket_prefix: typing.Optional[builtins.str] = None,
    s3_output_format_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4552a09d923816d8ceee080019d44f8dc3433b2cf75f8eaf56abacf451b0d60f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f8258fcd5b37001b0ddaa9479f799deb68d7b58c90f1ca8df021b324701c316(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eafc90758f2a6432c65c9c78220fc3fd1232216bb3ff9aea86a551cb9ff282b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__296489d50976371ffd5805369138a7d0efbb1bf74711beeb236072f42549f5fd(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa0759e8df962e4cbff933e2ca2accbfc56ba6b55c7352a5f5c325392ff25ee(
    *,
    aggregation_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    file_type: typing.Optional[builtins.str] = None,
    prefix_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    preserve_source_data_typing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa4c52ac7281610eb52dca5db723134ac189f4e8fbffbc80f8976304fe7e992(
    *,
    aggregation_type: typing.Optional[builtins.str] = None,
    target_file_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af137783c628dc020711d7a44e8914cd297722de0a9cae2fa55b386c8096a10c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eeb8620b7eea68f6358d5175d346b2888b836c0f07a8e2388a44da3d27f4296(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c3307fd6991d95b7cf0d6d306344a44727c3759c1b12de6dd1393322d4e65a1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea7393fbb96aa480f3300f6fbfb528a23dc69e65effc7c894d94d1d92c977cf8(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigAggregationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0bd65e3aaecf49c53b55c905a6ec07064c3fee0b123af6be676e44070564c80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae6e83b85823aca9986c60da4b3c94e54a29a39a28c3bb8b8fb05ebdc6722161(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8dd5833e45a9b35a9206f4a9377829e21a72123e011a949ffb34a9f02f1730(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__865fe35a2b23f0c60359386eea5f9cc6c93dcd95346ed691b2f3982362884429(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa36ab04195c4d180938e0b836df2d4b8383afdeb5e124131b2f81d49bc68f64(
    *,
    prefix_format: typing.Optional[builtins.str] = None,
    prefix_hierarchy: typing.Optional[typing.Sequence[builtins.str]] = None,
    prefix_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6abb665f002c69be17a9eee436e8e9a41ad8cb198cec384374839630e6929b60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83931b9af1efc37e34d5b02fe6bcad8b0549e84cbb279ef51193301289e3a93c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a68a5fa12b6cc75bb47232ec2ee6f9d00fb3c5985a106b085b18184f162058(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d60e37eee66ecbbdf12bac7a119dbc69f657e7a838b5648d603a3f6c68523e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8269df993070269d8b71d813c4b1620a2df1a700e2cb838f2a70df440fb1e79d(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesS3S3OutputFormatConfigPrefixConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbfb838829ad1c2d6b3aefe6a50e75185e82ed0d3dbf9164d886602eccc7d94e(
    *,
    object: builtins.str,
    data_transfer_api: typing.Optional[builtins.str] = None,
    error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    write_operation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48bda400473027f864eb05b987f0e1620ab774312d34c6e122e881cb4def3eff(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef0c3b597924a5f3fc8528050a0c1e1878d819199a7d5e903fff53f92c781542(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a586360e80e4b7dfa6eaf581c15a9727b7be450ea0bd7e4902b52b0b47bb9beb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78bd2ff3f392b2eadd9ef5af476e6d74fe9f9dc27a94986b4777127e30475633(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__165f01f3f715dc581f6a6039910e932bc24628843b24f303a01b09f443163cc2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d33101f21186598962786ad718c32471f0e9e14f566e5469bcc51e9d0a907a53(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforceErrorHandlingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae69e82b67d1ef5c40a73f734178538a882f0a9c961391aeaa0b3f589af49c03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff5f399d5e4a77f97fd67c87d1720d5795df226e7b349f47bb5392c3188e3c5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be0d7b0ec82f5547ab04d75178e13e12d763c0c0375c95816865b913016f3f05(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3901a04e10b8540bad830ba0606f196530cff0bcb9f84255ab6c8e8ab68e2232(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abea30eca838e33a3a8b67b577e19bbe5ccc5d66a199a4b6fd3a4520b1677a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c43313885a020e2404c8e7812e003276a241e64d99fc3aa7a410dab009c83b(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSalesforce],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__251adbcaf115accdf370a59ddf68cbed0fb581993f05fa0189bb74ee49f60871(
    *,
    object_path: builtins.str,
    error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    success_response_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    write_operation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aa6294163d3900521af7707bed89c87ae87d8e87ff2f9d599253f6042586f27(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ca68e0cb4e6268b17c1a17d70c99aec84d4654f85524e910368ce5a87de993(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf962a3bdccfd60a1326a7d2cb30da10786f436bbb3393cc075c42020b7c09b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c5066bea2d20a3d0d87beca4eb15f1f2bc0b16d1e1e1dbf8ddb3cb5d0a9af81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2ce5f9ab72d619bf08253460b2e3a8a0cec8b4b0cc0355a77629b398bdff98(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f458ee004c008c1f02382f751f97c31dcf725ba833baaafc28762623548ae6a3(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataErrorHandlingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff8c724f4dec7e4497336d391b24af8e072b3b036a611855e3ada0555ed0ac2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a029996b37b1cf0f0a72487d96ef50f5e27cfd3a004f426d488e34a06d9a4d5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25f9f32a8726ef528f92964b1278dc2cfc6231dac42582fa33a95d9b7fdf9b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c108fbaa82873cc069db155124251116a7ef93e1645001c61122ab64afc82774(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06109fa729294a121c2c71a5ab326eb769f81e4f7af49ad79e93c9f414b3eac8(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoData],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd1eaa6977aa6597d0c24eee2faa18d9955ed9b2ba09fee60c8a563b4cafe8e(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66997c4d669586ec4e11f0f43a547e72573c6a4745c60420a25e4a098a339acf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba42a6b195fb21cf699c21eaffd8509356ab6ca0d8ae672febe4b5fdac2e88b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ca612d9ec16c1c2e35c123d32a1f10b2ddd148fa01fb3e793b09b61e2f92ed6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6c02e43bb4ee3dd03d8aa2d567a415f2a3ffb2179e405f745dfbf4042dd201c(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSapoDataSuccessResponseHandlingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc82d02c7d10e51ea422c66aa600d706531c12d3a13405b9aff11de584797a8(
    *,
    intermediate_bucket_name: builtins.str,
    object: builtins.str,
    bucket_prefix: typing.Optional[builtins.str] = None,
    error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876873e3d46d1a8c9e95997c0e7d6c83d3da783f23800a4e720b929caac0692c(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd91f5d6e439184e5434c482dcac6f8a0cc0be51ad6f23ee2c3f67f83bbf629(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f410c6ff8d976e1d3b7f111cace6ec79a6ad714d8f7070f10dfc3394ebc0a2ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6df876a0ecd0aaa03e831996e91e1a89fbd881c2d9f97b708ad8ff65254212d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee256d771383cfab6745ecb6f209487260288e05d9ea1330eb65fb7bbb88bc8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed69e7329c1493801571c3ab90e56f33c8c753b342db0c43fb254906e3041ac(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflakeErrorHandlingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9e728a7e04df3a972a8df4a28bd33609f29379a920a43383a7f164e1a25a9ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d9d2d8e00b6949813ea762780d7adb0beaee923eef0d1eda9c237f2512579e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ea172f3364a4faae7e9804aed68a94f982608153aa1960fd653422bfc65afa1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f88936428fffc57a7036c2265cf03912e9ffddc1c3274281054cd7181365265(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef73ecbfcfa2edb228c4517557337c24f0cd43f2471a42bacb08eb3b09b1d871(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesSnowflake],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f681a04bf940e20318455a901144c1d9001191d2e13c6ac899b4a481be40d8(
    *,
    bucket_name: builtins.str,
    s3_output_format_config: typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig, typing.Dict[builtins.str, typing.Any]],
    bucket_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79fe804a02529d41a0dc619ca0f5ac998ea105fb9a930002a6ab24c14cf084c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46cff562a668c3653bd9109460182040a9dbd04f706a74e91f7cfdf53594ede(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a975e2a28a8a1dab4eba394f899b86e1ccf2e1957b8b3aeae3402ede227e7689(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b5eb7b5389120b7f9a99a18ede5f31becb003cf9d48828035d51008956174a(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolver],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c4d5142335176ce61cba0ccee376c4314e37d97c86f72b8c2b24d7280d63e0d(
    *,
    prefix_config: typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig, typing.Dict[builtins.str, typing.Any]],
    aggregation_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    file_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b17dd36a4adceef7cb25245112cf4d6c2769115e4a07ef785496c908bb22fd11(
    *,
    aggregation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a6a7335f60368166d727a37fe617b8455f7d8932a8625334820cf8d7b015c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aef540ee20b13dd22f36c9af55061bfb490026e2a195dfae43c8166ba097723(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a0c7dd466e2e9d6565fa6e964246b65fc31621dcd0b6a5666e5c439b5ec3d65(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigAggregationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c6fd0aef3e123e08decf0dfd2f95b4fd7474bd170ab14f7f9af3e08c9ebd9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b988e6b6481f3bc5ce4db01a6435c0d8ae928d8a237df65e63d8958733d41ede(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71657a7cffe7a16daada8bd3e9f484be889ff952f7b24556d84af74a12a95ba8(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63b1671bc997f60dacfa21d736714a13eab0d3a5b11eb9fff13599c1ed63d56c(
    *,
    prefix_type: builtins.str,
    prefix_format: typing.Optional[builtins.str] = None,
    prefix_hierarchy: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b07a649f9eb2ece4add17ce3de3f562d96928520bd1276d6015d622135f55571(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc71f39bb7cf02bc1321cb9d3c5775441346b695ee660554ab8436732a7b32e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035f6b98ce5d0b9d7190001beb1219dd075becd7e46c9d6eb9d3fe8c07b2a6c5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2574c5b9fae860cdfb9b0c41f84df9abcd385ee4e0ae226d7d593b0a77df67d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8dbce57537f4472c4806fe02e6be87901dca2637cfb07aee24d220051f4e958(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesUpsolverS3OutputFormatConfigPrefixConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33afecc984c225c7885ef1523a5e48ca261c9baebca9343239f2ee6fb8310eee(
    *,
    object: builtins.str,
    error_handling_config: typing.Optional[typing.Union[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id_field_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    write_operation_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01d1583e6540424517d44187f62b3440c9eb598fb2188155eeae76102553c7d7(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    fail_on_first_destination_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89af6f358d766f47c708cf3d6f5dd4f09f16065d232e351ceeaa289c8a1cb20a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9b5888034791753fe87f581d96e7026f19281774d304d989a938de5ad2b7d91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e558b34782777e52e52ec048a985131293e6230fce5c1e6d69cbc45c33895d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008105574581aa7753dc43a1d16232f55982ea6af590d5ab863149701766dcce(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d2e0e1aa603776cb110b224f5d245aed131259ef34a55fa92b49c33d22cc884(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendeskErrorHandlingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be29dcead5e24d5d1491bfb6942fce6627b15960ac6bca786d0121d338f88a59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1abf87819595367018fd360edc3a596cbc522f97ceb9d87ea42575654a8cc26(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c879c46304fa4c6a01f77ab340e9d332f85551d377afeb29c82c5ee9d71a43fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e08f103266bc74de2b274498ea27d4b81bd79fca3f6b26187440ff57bce382d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e676292209be63a9a1d3bcb318ce8fe9110095583ec7febf34d1ce1f9950d8cb(
    value: typing.Optional[AppflowFlowDestinationFlowConfigDestinationConnectorPropertiesZendesk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041957e2dabe38c394abf7b53a9e72ced1c6d838fb14d875b454f80d3e79fb02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d56ebf26ebc6b6ffec761d4f376eb5db238930c2475badb65099644f73a186(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d7fda571fb1fce7c65854dc39ef5eca5ee46131cc850b51d33b2f557e82ad6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__613e89916dd62dba1b0e4e252abae48dc6a93019c7219b698fc242eada2fc396(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7957d7fd3ed112e39900d7530f748fc6fbc01c38f369b5d6dd9ad4c775c04ab9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e8e0cf58fc0cdaee76fbc3913d2f8a9210900ea227439149721b6a12dbfcf54(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowDestinationFlowConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf3af0ef93758ec2b16a29bb5e93bb4ef75af2a37e85427f307ae5719324a16c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c4963312c3c56a2241dafde30d31ad85b24e3de9316da5679ed7dc8bd2f588(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22114fb338cec54cdca84355c1f6ba454053f8b3816a17fced09913e61225988(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3a3ebeae9ba7962f29dffb6331b28554ba543f0cca43d4fca0c8858935263b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b1701cd4a4564475b6acf861719a8938dde2b54d0f9918fa74e9ec7eea59891(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowDestinationFlowConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55c0d08d8622f2e2e56e6ac5fadb071c91296540d108a875c87eddaf43e65cda(
    *,
    glue_data_catalog: typing.Optional[typing.Union[AppflowFlowMetadataCatalogConfigGlueDataCatalog, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b33004c6963107cc50e36efb9f06553e2321d4087b08fea2a60e7d800f19435(
    *,
    database_name: builtins.str,
    role_arn: builtins.str,
    table_prefix: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574a01f44a245b886590086233a7c8cb2576f1fe9a8cb6576d01012ff62ee61d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f98fd1900ee66262f9a9018c1922baf0aee5375cee399cd007627f23169ae356(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6a2a4f6d2f819feb09557746471707bda72d803df5760c1d35f9af09a830f96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__212b8c337cabb02ce252f0a6aa01423515593964ae228abe9b6ff73251084549(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d08f9588fe41fe39a8505d336c1acd3f9c64577e9e31d9d89b30dea9a3048470(
    value: typing.Optional[AppflowFlowMetadataCatalogConfigGlueDataCatalog],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81504c7da70b881dcba4127375552b2bb7cb361b1b0da8bf1aaf36f10c1432f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f665fdc987b3ed117279b6de2cebd819543f9dd29e1affaa423c6ac5fab1796(
    value: typing.Optional[AppflowFlowMetadataCatalogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b98232112d244a63bcc735a27235157bf505b83049fb2c19240658a347f33e5(
    *,
    connector_type: builtins.str,
    source_connector_properties: typing.Union[AppflowFlowSourceFlowConfigSourceConnectorProperties, typing.Dict[builtins.str, typing.Any]],
    api_version: typing.Optional[builtins.str] = None,
    connector_profile_name: typing.Optional[builtins.str] = None,
    incremental_pull_config: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigIncrementalPullConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e849db34f51bdd89c287819d2d6e6dce6ec87ac5dddd22948fbaa21304b40ca9(
    *,
    datetime_type_field_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742947b1a71420646e6d08b1210a40bca908f79f43b9ce73b730d339b3df1b34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af5681b1ff44b4ad7037fcfe155b21b1d2bdfed01efaf7f2711e03dd05943484(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e0bd845545737b6a7d995a17e2300c94991c8c0cb89975b6bf3c1388d37ac4d(
    value: typing.Optional[AppflowFlowSourceFlowConfigIncrementalPullConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__222e6492ea60a667e17c51ee104cebcb650805115f6f3ca5a181212f0c822dc7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa0184b09cd4b5c917be3a6405553c54fb033d56f3063c6f7870d8075e00368(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e261f77a5d377820261ca192a876502670d0e901479193ce2a279817507740(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f986eb4a3877c9e04e501268cc48f7880ebbfdec6ccf426615a6a1e5b03240d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f353cba675138f4533f77e97debe18c719272bdeed3429939afa16c62351f17(
    value: typing.Optional[AppflowFlowSourceFlowConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7beb5c36c9c288e80d704b1af876a43b0f17e5aad5e3a8c130d93f5b811030(
    *,
    amplitude: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_connector: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector, typing.Dict[builtins.str, typing.Any]]] = None,
    datadog: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog, typing.Dict[builtins.str, typing.Any]]] = None,
    dynatrace: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace, typing.Dict[builtins.str, typing.Any]]] = None,
    google_analytics: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics, typing.Dict[builtins.str, typing.Any]]] = None,
    infor_nexus: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus, typing.Dict[builtins.str, typing.Any]]] = None,
    marketo: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo, typing.Dict[builtins.str, typing.Any]]] = None,
    s3: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3, typing.Dict[builtins.str, typing.Any]]] = None,
    salesforce: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce, typing.Dict[builtins.str, typing.Any]]] = None,
    sapo_data: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData, typing.Dict[builtins.str, typing.Any]]] = None,
    service_now: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow, typing.Dict[builtins.str, typing.Any]]] = None,
    singular: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular, typing.Dict[builtins.str, typing.Any]]] = None,
    slack: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack, typing.Dict[builtins.str, typing.Any]]] = None,
    trendmicro: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro, typing.Dict[builtins.str, typing.Any]]] = None,
    veeva: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva, typing.Dict[builtins.str, typing.Any]]] = None,
    zendesk: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc5affa045e0a3c17e9c5552f249dc32f3344807db92204e14339d5158cd2e90(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c6f1bafef59deb1fa81dd1fe6d920a90c345857d1135b6d9095cc640909808(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3418ce032bbcdb95a7c7eacdf2856236e28b33d4ba6ea8f5bd946b7366398ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6400137fe3051b4ad3606333f38eabc3cfd765060902f93858365128c18870c(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesAmplitude],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1769cd7bd487dc90b9719132ce34f491d4efa4b8623e32664bbbd66bd5bc5ea2(
    *,
    entity_name: builtins.str,
    custom_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__100818bcb735cd59ebc7bf215363ebfad2af90ce98f25fd96fc85aad06e3e969(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f36615e0c6efa699e607da38327d0afdd5a72046b70900bb1b4eb7da1e4ef6b6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__112c9f07bc3e2754bada4e7cdde2e9103b9a82d580708019b7b8bb3427b0428e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472cca29798919e58f86e83c5e9d1fa63bf3b39c71a1b8882baa5e72638510a7(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesCustomConnector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09617de1703d4c787c55bfc3d70a7f454a950d740bb6879b7acfe77caba66f29(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c64627a9685f81b3b672fede26f39539a7fc6711dea1a35ecc2ec357d9e78f34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c984f2968ea039b5f6023a3e216812507ae06fc1f6376704d7eb482d1a05b65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca593869e26d483b54f94efb27cb3f16372fae6748711a04578d78e0a926b7c(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDatadog],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5e07b7b22b21c48f5f8179f4bf2895e88ac9093a8f596dfcd7fd95a08b22c3(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5a36d86c7753225645551d21eadb9503407497c9d415dd17ac9b95e3e34ca71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f0127727e70d4deea9734bf94bd83edff2041bbc331a59524daf00fdf1174d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd5e6abd09c8d5f99dcda1e1e064bc200aa5df4dccbfb4ec0a0f428f2dbeed0(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesDynatrace],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a9654a2a2d7063238de8535700af544bf0036656d22a62bb40c05acff36d742(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18139a6408cb72dd7efbdac0167c32e6dff44b4494d052ea0dad2abe57f80c54(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc230ab0a27309ee8a97cb31cad5ea3a88efcbd12232554125f90ccb17aef3d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05160c3da193245bd7f3b8da4a2f33d767be32ea9b85029aa4e8fd443b4096d(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesGoogleAnalytics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f7afcf85edf877ebc91ab4bd9e609dc63dbd58c79d761a179cbf7ca73134366(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ab2a8870c1040ee5edb14f0a11bcc98502b3def08f526761ecee88729c10d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee02a1579a05d2f545cdc9059c7423d9e90249978e3080e4b429f9d46d6ac0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cccdea102850e2b4e92c5f507028aabd96fd054a6893df2040ba83420bccc96e(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesInforNexus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395cd8d5defc871ec3aa88e75608028d6f148d43be89752da2fbd582dd06cf99(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f0c42ec03d8db060799772695c88633f0fc4c7c092bae81ecd964756da0f47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0362319a8e6f9dce31ffab6752f3d54469a8ade02c0bb7a72b676dc188d0c7af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17c156bd293f2667cb96aadd4bbb53903e72a75b7e6935de96fa2a504843b036(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesMarketo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7feb30c4bb03e789ba3e3ca9c5eb1cbb16bc9c11e755256260ecf5eb2e51e73b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24965ba715da9256975addfa661e259641c584e24d058b10ff49086f674d43c4(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0906abac59491666d6a198cd529c84dbd393c16feb00db8e15b53beeb7f9a7ee(
    *,
    bucket_name: builtins.str,
    bucket_prefix: builtins.str,
    s3_input_format_config: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f0653cea340b81eca1e9178b1d0d5868b6bf4efb08e762b364358baa3d35f79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56b644f3183783b81a41aceb2ca3d71e55cf75bbe6effe35d61f694ea909d676(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3aba6ea3e3e3b41977e86667c6f57b7dac74ac8f3873e1124e9c206a1cce6b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b502f8c0e0b3f97e4bd42116c38c18a1dc0d42d6d554ee2ebeef42fdb430504(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a3b222af4ce1aa53d3d75a80358c7972529da632999ee3b88a2cb2af058f3c(
    *,
    s3_input_file_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ac5f939a396714c66209298c1de0cfcc8310b64197810edebe66c631103d27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__841b6f45ccbc523e57863161bd7b31764eebfac16938b7f4a0b10c2c95862c41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbdcbf97fc8a7e252998cada51d91636e468a7262b8a5ab928d560b75ab78ab5(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesS3S3InputFormatConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a76fe62c8e612023f4b60fe54d6953e87d8ae925d601d5c9a3f469c363627a7(
    *,
    object: builtins.str,
    data_transfer_api: typing.Optional[builtins.str] = None,
    enable_dynamic_field_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_deleted_records: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472bb8ef1eb8ff15ffd4b9f3f4e9506f6db166fc2b73592756e9ccc818cf1602(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf98fe03374ebc0e8abf1ddf03d2f0c89c5ea2d70906678c64307f2f927e9ab0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d4704eb37ca1010f3f3ee14a4f65e5387247580d72d6dc926674d2182a9d92(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c9c91e54967a7a2e715512fd0eee20d146b636d33c3ef225103a5701b2ec7b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55b9867888d36433d6106605ad23cafb0cb2b62417468f2c874b801efc435414(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6692c1ab443d2864b9e6399ee2e569b7e32971cfda2894700105e66e0236d33(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSalesforce],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fbcb61821b3b9064899af8a6bdec0acd0afcaa14fc73b98c39fbce771602c51(
    *,
    object_path: builtins.str,
    pagination_config: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    parallelism_config: typing.Optional[typing.Union[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed4ca2d53c1a8f6fa2913fd57e606ca9086e694e6107c19e8a1d45eacee8b869(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98704b4acae3e4b965e20e32adadc030db92d1d6db5fd62eece2a10789ba99cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe04322ff055bc4c21ef67da8485d16eefdf4cbd3a2fc1e40497a0c6bffc7032(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoData],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc5bfc3d3abebaf0f8e2ee1ee501114857c5d91b83d604ba31acdae9443f2a0(
    *,
    max_page_size: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c5042650ba7839b67c86032f917295af923a9c3c6771a605183a42a1f4737c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd2ab5a5073c2cd38c0586c891ee91cec1de5b28997ae4899a307b7b1aac11ce(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9d4645052b990b867f41b30363e0b4057ec370092715bd051bd8792c37b8a3(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataPaginationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95c7f1b97dd1de21bad90abf9ce0557391ac0c0482faa5155b83f04183d32f58(
    *,
    max_page_size: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc9fc147a4c8ccdf5312ceb99bd6882b5eec10a51325c0faba54725600f3a388(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3062dadc935c501df71bfd91bd8e3d84b230d8bb516b7aa87a87f94d8adeb77(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0271addcdab27af66c7028cdecb5f014d24d96a69ad940f1a0b1af1cfa2dfa2(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSapoDataParallelismConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__003573c72f59db51dcc71bea44cca7da0801d968cab1af0b91c05c70eff393df(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c68bb434cf11448a0b10ef62edfe81cf5e5b39917863dc6b065bb4c3564baa4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__522c5758a6bb792169cdfa23ff2a8515deabb7624ad7f143f78db4fff11d8059(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc8e6ebeaf25dcf4d87d995979ddb1c3f3977b24e3b5c7cb1a24982add28c3db(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesServiceNow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7459e4ef2741fe1819f8bf67f85a681f5bfa765257471a8945444479c1e51864(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f3c460f8c4e79921ebf32c83aafbede2b2799ed18c96e0557287e70230d7eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fed4974e698c5ec45b5ad3bb1ef6fb7ff9a0be521963eb39350c193bbb8bf40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a1bf42fa3e64d94db68208b51f0e1bef80ca608063b81465cfb841126e4fcd(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSingular],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e935dda13dac212878155b0db654bbb39603c63efd75c473d18aba1383b9f2a8(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7282d2cc7164d3f9feb3b480a9bcf3e1361d5470a2a8c5c0a30d385e66662cc7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0daa262733511c72bfbcb696bf2c6ef6748e3fbac5ea9778d568620f26e726dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11549c7c8a58d085a276693a1badbbed30f46a2dce34bdf0ffc65bd1dbb99450(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesSlack],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81d999d67de441e848d5db03533bc27615ad432127a3b53fd8e217030ae509f(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb26598a46c6f236d0651e6f9354bed30c7475bdf9e98961e44355968eeee9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef636042556fe0cac8b4489909cd3d0231834ca3416edc97a6f7fad744fa059(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699c2ceb688da3cddc83a0175614abde9159852d1797251ad5d2d16e3e545761(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesTrendmicro],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca72438fa6c47bae59448adbe74d85cd9fa8a5abbc0816fca0edd423bca07302(
    *,
    object: builtins.str,
    document_type: typing.Optional[builtins.str] = None,
    include_all_versions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_renditions: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_source_files: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43dffa0477959d5d39c0be2eb579b45070282f595ed635b7a7c88adfec116c7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4b9ab34e189b0009e00c8cf51a731db87cdd0cec2b718c321c6194410bf343(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__053f70727c0814e710c27facc22299ed4f245f5861ba5c27f9ab52e04299a301(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7af7d436a55dc83acacbda2ea9ca719009595a651e71101d42a8d66e2babc1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa5f6921b9a40584643745e554285c6fd869c55b440d44933ffc7b319998881e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed3310520a4666956b8b2104952fee1466dde9e7c1dc020f4defc5f532378099(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963852ccb306c7413a4dead4a24d1d19627808f227897bbbcc5d5c3e31f56966(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesVeeva],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4adda9c9037726a1d2a42d49bf638e81453ab723f13617b27688902d1dddfb1(
    *,
    object: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b96adcea84a0f36ff1a748aca9b30e9cfbea01ef4001326e98fe44987df8718(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__effdd60ae7104a1a1acbf99d0866c661370e77f0c1ba8004df99a75477a6d57b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27d156331dba5366a33bb5204a581538aea76ba54e9a2be76c1b85e799118c4(
    value: typing.Optional[AppflowFlowSourceFlowConfigSourceConnectorPropertiesZendesk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032f0b3320debf0283e94c645551125f796c53208e981bfc9e35473262686971(
    *,
    task_type: builtins.str,
    connector_operator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppflowFlowTaskConnectorOperator, typing.Dict[builtins.str, typing.Any]]]]] = None,
    destination_field: typing.Optional[builtins.str] = None,
    source_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    task_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b564d03e2b87d941eea2e4c8d73e5a99c234f237d7443b653f5c1d0af3e8bc(
    *,
    amplitude: typing.Optional[builtins.str] = None,
    custom_connector: typing.Optional[builtins.str] = None,
    datadog: typing.Optional[builtins.str] = None,
    dynatrace: typing.Optional[builtins.str] = None,
    google_analytics: typing.Optional[builtins.str] = None,
    infor_nexus: typing.Optional[builtins.str] = None,
    marketo: typing.Optional[builtins.str] = None,
    s3: typing.Optional[builtins.str] = None,
    salesforce: typing.Optional[builtins.str] = None,
    sapo_data: typing.Optional[builtins.str] = None,
    service_now: typing.Optional[builtins.str] = None,
    singular: typing.Optional[builtins.str] = None,
    slack: typing.Optional[builtins.str] = None,
    trendmicro: typing.Optional[builtins.str] = None,
    veeva: typing.Optional[builtins.str] = None,
    zendesk: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de6e551eebf67ec29b3002802241b86a43a73cbf76af08b3f6f3cc984b10876(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899f616de9aa687077a5d90ecf3192a77254c0d748d16c69e4d57acee0fe83aa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f34252512e695c00403e5896dd70e1d157ce3d6b898537edb8fc36a21026706(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14be611b7a1d35a545b3eabadece012cc330f050fb6fbbeba8b45bf67dbadd2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1ac3e897f3f80d4fc2806533ce8cacb38a55f11e6d5c65a0345a2301810506(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4699f91a39a0753f79c890fea7c9861ef1d6c3789ceaa3574bcdb192f2b0bd94(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowTaskConnectorOperator]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297fa2ec808e5888ae3f8f7bf1e233b3ba31f19303952e284f6458fc65aa2afc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba8114eb6829e1acecd1521557a412069f42741c875b32fafe4db7c73e0fb6e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ad9e99d92bfbce263411f993884067670920b5d39ff0ba831802216ec2a3a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e32b53437ff2326b99bfa58d8d94dbdcf5e9a36b237141dbf969a051f3d883(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f14724deb8864f8d74ef1642972fe4a171161032a06acb338de358af19ff3ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee92764e4889ebf51dab03f1b7ded7cc7e54c7428df050e2eca757df901144b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6dc1e91a62489a21480648caeb9951f15ac3b46bdcc4a7cfa39ec38d2cfc2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__863cbd8eef90602a62aee1af7299274fef4c5f7f9248dbb77a1798935e29143d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84685f32d0153a27cfdca9bbe6f3548e3ec16438595c1fafbe7a414aa756fb17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efddaab84664c4ac3de52983d2416825202ea8cf5eff58d574a4e79ea3879851(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e33f6b1894d00cec0d47a022251836c0e0efae7c7fc3fad2ac185456fde3616(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4286ee4a90ca8176266944cb35ac1d76d7251dbc4c519cce71a0ee781fe9af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d54c0e8b14a27e19d52f638eee6f7b1c01e97c0c351f1ee18a8dfe1b1fa1f44f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9453b1a979cbf8db4a88c9d30e34f7d4144aac78e864b40f0807af4d9c33dfe6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e71749c147f9eb4835d3d3b25854eab06bd980dbc83b1dbb92e206a5dcd827(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d1108bae8652e116e2790dca75ec389c311c4f0919a4bf9438fac8031d5d9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e871c1efa9aca4cb1a6e7480d2ea68c082f92b46c638952bc2c52f8a72db95d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c9382daeff73f33a1de4c70dbb9f0f831d81d7b1e50fef54982d0ebce0cbd9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowTaskConnectorOperator]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fd0da3847d3cb91fd1d08da13e24462cd2d119414086ab002ca4ac87fd3cdd3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af4769efa92edceb67d9da1029ea9a06b58dcc5467f6bc086e61b37104642db8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d865c26a7a5e7d7e87283d5fc0fd63091e61b0404bd596cfc96b8d998a92a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b167624c32796a8b608a5db0ec59371f61268da6f65934ef63ece87904db8271(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b6ce201d119473652f177e283f95e299febe7cec12a2fa11c90c5afd71eb80d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01217ff218ddea0ff17bd3b27404f8c176b17a9f21ab8b9703f7320bb5be96d3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppflowFlowTask]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__249de5ae529ca125cfce51a256f338c70df4a951cd37bc12f24b30a9752089f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a1bffd5711bdda174788416f1ac3a9b18483b72fc7adabe739b208e6605ed1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppflowFlowTaskConnectorOperator, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c90f2d01c61b6158013709cf4414d0fa82f06622eb4c86c6ee5eef3abb926c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1278fa3ecf68b81a023cb4e45b0dba24b1fd11da53feb97d635c4c7c570cca(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3fcef36856c663449e30b9867997ec345e00ef9fb0501c959e1990f08459758(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0f3edbe2d0091b295b99a3c4ef4acc73bff4eb5e65dff738a8eda6df5733c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__164be8a02a72a49ce6949e2a1400137c87fcb6ccb810763147a2bc8526a7ef8e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppflowFlowTask]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f02605cf1c48838b54b5b9b91d7420bbb6d342b5714005818ccda94319a89e6(
    *,
    trigger_type: builtins.str,
    trigger_properties: typing.Optional[typing.Union[AppflowFlowTriggerConfigTriggerProperties, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03784bfcceea61ed1f71cd0f1b689123dba57298d06abfd06f7496bd60db9577(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c1460a10f2c207d5fbfe9b2fb4293b48f8b56d41aec979a3bab194ead0558f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3504b794331a8e898dc761e271c7d23b65deb9caf2529d78fb8fe805a6e324ed(
    value: typing.Optional[AppflowFlowTriggerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8444b7978d00c69ef1cd0f31692447e8630d2e57ae0751707b8c554b9cac9fde(
    *,
    scheduled: typing.Optional[typing.Union[AppflowFlowTriggerConfigTriggerPropertiesScheduled, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7b22e53c39700d6c44c087298024d449c161fec5cce81489e99617ac3689ce7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94fa974da1248f3e83382dd3c02e65a5357d6b8c952727310c8e5457ce556bd7(
    value: typing.Optional[AppflowFlowTriggerConfigTriggerProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a74662ec2243a2072d7d6e2637b26d4cce0b8a68989e65f11207421d6e7730d(
    *,
    schedule_expression: builtins.str,
    data_pull_mode: typing.Optional[builtins.str] = None,
    first_execution_from: typing.Optional[builtins.str] = None,
    schedule_end_time: typing.Optional[builtins.str] = None,
    schedule_offset: typing.Optional[jsii.Number] = None,
    schedule_start_time: typing.Optional[builtins.str] = None,
    timezone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d189d7753b6aacef4b0fe4aa9c854b4675e6dc8f55239df3c283a87aba1caa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d7a36e2a8de737866e9c8444d4da6312306cbf8748d2c0df81a791d0546dd67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a57d6b986f70124b5b4c9319e84b49ff7f912527026ca94e2e50af4b6fd5bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__215789b1bb9fc834eec20455975c9faff4d0326163b6a4b844795b79400f98cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6820a9bac949a0652f776a7cf5db47cf1724a0d9d72ea70ed8c714dee28be12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f246b74cea6070aaa0a4e4eade4efa5933e154969cd61c0979c3be7a3b1158c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4958fe502c0bccd9943c9efcd7dddca7fefaa2b2b0b9b9c8cc713437a9ef4392(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd758aa24be8f82f1e7b92add92bf219411ce80787bf6ab0b4c5036aad327870(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13fe73649002222d98ab18216ea00bc4c3de175cc1b2052f10a04a2d5cae8c7a(
    value: typing.Optional[AppflowFlowTriggerConfigTriggerPropertiesScheduled],
) -> None:
    """Type checking stubs"""
    pass
