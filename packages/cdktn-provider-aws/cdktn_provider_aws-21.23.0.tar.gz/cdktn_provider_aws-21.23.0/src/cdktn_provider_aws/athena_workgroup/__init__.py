r'''
# `aws_athena_workgroup`

Refer to the Terraform Registry for docs: [`aws_athena_workgroup`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup).
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


class AthenaWorkgroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroup",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup aws_athena_workgroup}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        configuration: typing.Optional[typing.Union["AthenaWorkgroupConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup aws_athena_workgroup} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#name AthenaWorkgroup#name}.
        :param configuration: configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#configuration AthenaWorkgroup#configuration}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#description AthenaWorkgroup#description}.
        :param force_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#force_destroy AthenaWorkgroup#force_destroy}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#id AthenaWorkgroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#region AthenaWorkgroup#region}
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#state AthenaWorkgroup#state}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#tags AthenaWorkgroup#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#tags_all AthenaWorkgroup#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6fd9fbc14cfb419ecd6e370e9de9d09953b07c33eb453c6ee34a3c2169564d9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AthenaWorkgroupConfig(
            name=name,
            configuration=configuration,
            description=description,
            force_destroy=force_destroy,
            id=id,
            region=region,
            state=state,
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
        '''Generates CDKTF code for importing a AthenaWorkgroup resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AthenaWorkgroup to import.
        :param import_from_id: The id of the existing AthenaWorkgroup that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AthenaWorkgroup to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bfc43ae045ec1fd9f4ab41865f327f8f23cf2f8de702cd638dc97fb754ed065)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfiguration")
    def put_configuration(
        self,
        *,
        bytes_scanned_cutoff_per_query: typing.Optional[jsii.Number] = None,
        customer_content_encryption_configuration: typing.Optional[typing.Union["AthenaWorkgroupConfigurationCustomerContentEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_minimum_encryption_configuration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enforce_workgroup_configuration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        engine_version: typing.Optional[typing.Union["AthenaWorkgroupConfigurationEngineVersion", typing.Dict[builtins.str, typing.Any]]] = None,
        execution_role: typing.Optional[builtins.str] = None,
        identity_center_configuration: typing.Optional[typing.Union["AthenaWorkgroupConfigurationIdentityCenterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_query_results_configuration: typing.Optional[typing.Union["AthenaWorkgroupConfigurationManagedQueryResultsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        monitoring_configuration: typing.Optional[typing.Union["AthenaWorkgroupConfigurationMonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        publish_cloudwatch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        requester_pays_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        result_configuration: typing.Optional[typing.Union["AthenaWorkgroupConfigurationResultConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bytes_scanned_cutoff_per_query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#bytes_scanned_cutoff_per_query AthenaWorkgroup#bytes_scanned_cutoff_per_query}.
        :param customer_content_encryption_configuration: customer_content_encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#customer_content_encryption_configuration AthenaWorkgroup#customer_content_encryption_configuration}
        :param enable_minimum_encryption_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enable_minimum_encryption_configuration AthenaWorkgroup#enable_minimum_encryption_configuration}.
        :param enforce_workgroup_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enforce_workgroup_configuration AthenaWorkgroup#enforce_workgroup_configuration}.
        :param engine_version: engine_version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#engine_version AthenaWorkgroup#engine_version}
        :param execution_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#execution_role AthenaWorkgroup#execution_role}.
        :param identity_center_configuration: identity_center_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#identity_center_configuration AthenaWorkgroup#identity_center_configuration}
        :param managed_query_results_configuration: managed_query_results_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#managed_query_results_configuration AthenaWorkgroup#managed_query_results_configuration}
        :param monitoring_configuration: monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#monitoring_configuration AthenaWorkgroup#monitoring_configuration}
        :param publish_cloudwatch_metrics_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#publish_cloudwatch_metrics_enabled AthenaWorkgroup#publish_cloudwatch_metrics_enabled}.
        :param requester_pays_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#requester_pays_enabled AthenaWorkgroup#requester_pays_enabled}.
        :param result_configuration: result_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#result_configuration AthenaWorkgroup#result_configuration}
        '''
        value = AthenaWorkgroupConfiguration(
            bytes_scanned_cutoff_per_query=bytes_scanned_cutoff_per_query,
            customer_content_encryption_configuration=customer_content_encryption_configuration,
            enable_minimum_encryption_configuration=enable_minimum_encryption_configuration,
            enforce_workgroup_configuration=enforce_workgroup_configuration,
            engine_version=engine_version,
            execution_role=execution_role,
            identity_center_configuration=identity_center_configuration,
            managed_query_results_configuration=managed_query_results_configuration,
            monitoring_configuration=monitoring_configuration,
            publish_cloudwatch_metrics_enabled=publish_cloudwatch_metrics_enabled,
            requester_pays_enabled=requester_pays_enabled,
            result_configuration=result_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putConfiguration", [value]))

    @jsii.member(jsii_name="resetConfiguration")
    def reset_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfiguration", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetForceDestroy")
    def reset_force_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceDestroy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

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
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> "AthenaWorkgroupConfigurationOutputReference":
        return typing.cast("AthenaWorkgroupConfigurationOutputReference", jsii.get(self, "configuration"))

    @builtins.property
    @jsii.member(jsii_name="configurationInput")
    def configuration_input(self) -> typing.Optional["AthenaWorkgroupConfiguration"]:
        return typing.cast(typing.Optional["AthenaWorkgroupConfiguration"], jsii.get(self, "configurationInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="forceDestroyInput")
    def force_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

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
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00ebbffd53d6029eb35bac34fff9f95328d90102c78f5bf014c9a69e6eb1767a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceDestroy")
    def force_destroy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceDestroy"))

    @force_destroy.setter
    def force_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18750dc44847f8c781b522c9a6620f9f7cfdc3667a3b78488210d1435af50b72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c305a333762bdea2f687abc46d594c8ce02fe7460bf71527818a2d1e935d457b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__673c3cb024fb60698db1e844675a44488b9ff7c1c7a396f7ff3a5de2c881febd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d8c3b0ff542015c9ea203c0223641d388d17a1dc292e9f00d60bb2902ffb82f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ed7d12fe0aca6ca57f2ac5a0fb1f13a7dd91bfdb198e4fd4c73604d5fd87b2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1630cf22145007decdcbf132372bc25abd83f899113564bf9a6d6dcfb26ef325)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be3fdedb1fffc9f7242abcc7ae07dcf1a71205b6a47a20286ff1054d998126ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfig",
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
        "configuration": "configuration",
        "description": "description",
        "force_destroy": "forceDestroy",
        "id": "id",
        "region": "region",
        "state": "state",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class AthenaWorkgroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        configuration: typing.Optional[typing.Union["AthenaWorkgroupConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
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
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#name AthenaWorkgroup#name}.
        :param configuration: configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#configuration AthenaWorkgroup#configuration}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#description AthenaWorkgroup#description}.
        :param force_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#force_destroy AthenaWorkgroup#force_destroy}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#id AthenaWorkgroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#region AthenaWorkgroup#region}
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#state AthenaWorkgroup#state}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#tags AthenaWorkgroup#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#tags_all AthenaWorkgroup#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(configuration, dict):
            configuration = AthenaWorkgroupConfiguration(**configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a957d32df481f630a6d31807b2895ac26d6643f2db179efce26c6875625b6909)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument force_destroy", value=force_destroy, expected_type=type_hints["force_destroy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if configuration is not None:
            self._values["configuration"] = configuration
        if description is not None:
            self._values["description"] = description
        if force_destroy is not None:
            self._values["force_destroy"] = force_destroy
        if id is not None:
            self._values["id"] = id
        if region is not None:
            self._values["region"] = region
        if state is not None:
            self._values["state"] = state
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#name AthenaWorkgroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration(self) -> typing.Optional["AthenaWorkgroupConfiguration"]:
        '''configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#configuration AthenaWorkgroup#configuration}
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional["AthenaWorkgroupConfiguration"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#description AthenaWorkgroup#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#force_destroy AthenaWorkgroup#force_destroy}.'''
        result = self._values.get("force_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#id AthenaWorkgroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#region AthenaWorkgroup#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#state AthenaWorkgroup#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#tags AthenaWorkgroup#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#tags_all AthenaWorkgroup#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AthenaWorkgroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "bytes_scanned_cutoff_per_query": "bytesScannedCutoffPerQuery",
        "customer_content_encryption_configuration": "customerContentEncryptionConfiguration",
        "enable_minimum_encryption_configuration": "enableMinimumEncryptionConfiguration",
        "enforce_workgroup_configuration": "enforceWorkgroupConfiguration",
        "engine_version": "engineVersion",
        "execution_role": "executionRole",
        "identity_center_configuration": "identityCenterConfiguration",
        "managed_query_results_configuration": "managedQueryResultsConfiguration",
        "monitoring_configuration": "monitoringConfiguration",
        "publish_cloudwatch_metrics_enabled": "publishCloudwatchMetricsEnabled",
        "requester_pays_enabled": "requesterPaysEnabled",
        "result_configuration": "resultConfiguration",
    },
)
class AthenaWorkgroupConfiguration:
    def __init__(
        self,
        *,
        bytes_scanned_cutoff_per_query: typing.Optional[jsii.Number] = None,
        customer_content_encryption_configuration: typing.Optional[typing.Union["AthenaWorkgroupConfigurationCustomerContentEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_minimum_encryption_configuration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enforce_workgroup_configuration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        engine_version: typing.Optional[typing.Union["AthenaWorkgroupConfigurationEngineVersion", typing.Dict[builtins.str, typing.Any]]] = None,
        execution_role: typing.Optional[builtins.str] = None,
        identity_center_configuration: typing.Optional[typing.Union["AthenaWorkgroupConfigurationIdentityCenterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_query_results_configuration: typing.Optional[typing.Union["AthenaWorkgroupConfigurationManagedQueryResultsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        monitoring_configuration: typing.Optional[typing.Union["AthenaWorkgroupConfigurationMonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        publish_cloudwatch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        requester_pays_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        result_configuration: typing.Optional[typing.Union["AthenaWorkgroupConfigurationResultConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bytes_scanned_cutoff_per_query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#bytes_scanned_cutoff_per_query AthenaWorkgroup#bytes_scanned_cutoff_per_query}.
        :param customer_content_encryption_configuration: customer_content_encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#customer_content_encryption_configuration AthenaWorkgroup#customer_content_encryption_configuration}
        :param enable_minimum_encryption_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enable_minimum_encryption_configuration AthenaWorkgroup#enable_minimum_encryption_configuration}.
        :param enforce_workgroup_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enforce_workgroup_configuration AthenaWorkgroup#enforce_workgroup_configuration}.
        :param engine_version: engine_version block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#engine_version AthenaWorkgroup#engine_version}
        :param execution_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#execution_role AthenaWorkgroup#execution_role}.
        :param identity_center_configuration: identity_center_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#identity_center_configuration AthenaWorkgroup#identity_center_configuration}
        :param managed_query_results_configuration: managed_query_results_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#managed_query_results_configuration AthenaWorkgroup#managed_query_results_configuration}
        :param monitoring_configuration: monitoring_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#monitoring_configuration AthenaWorkgroup#monitoring_configuration}
        :param publish_cloudwatch_metrics_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#publish_cloudwatch_metrics_enabled AthenaWorkgroup#publish_cloudwatch_metrics_enabled}.
        :param requester_pays_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#requester_pays_enabled AthenaWorkgroup#requester_pays_enabled}.
        :param result_configuration: result_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#result_configuration AthenaWorkgroup#result_configuration}
        '''
        if isinstance(customer_content_encryption_configuration, dict):
            customer_content_encryption_configuration = AthenaWorkgroupConfigurationCustomerContentEncryptionConfiguration(**customer_content_encryption_configuration)
        if isinstance(engine_version, dict):
            engine_version = AthenaWorkgroupConfigurationEngineVersion(**engine_version)
        if isinstance(identity_center_configuration, dict):
            identity_center_configuration = AthenaWorkgroupConfigurationIdentityCenterConfiguration(**identity_center_configuration)
        if isinstance(managed_query_results_configuration, dict):
            managed_query_results_configuration = AthenaWorkgroupConfigurationManagedQueryResultsConfiguration(**managed_query_results_configuration)
        if isinstance(monitoring_configuration, dict):
            monitoring_configuration = AthenaWorkgroupConfigurationMonitoringConfiguration(**monitoring_configuration)
        if isinstance(result_configuration, dict):
            result_configuration = AthenaWorkgroupConfigurationResultConfiguration(**result_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fbdff6ebdc5e12441e70c618b13652eab9d337558f59672be65135ceae03ecc)
            check_type(argname="argument bytes_scanned_cutoff_per_query", value=bytes_scanned_cutoff_per_query, expected_type=type_hints["bytes_scanned_cutoff_per_query"])
            check_type(argname="argument customer_content_encryption_configuration", value=customer_content_encryption_configuration, expected_type=type_hints["customer_content_encryption_configuration"])
            check_type(argname="argument enable_minimum_encryption_configuration", value=enable_minimum_encryption_configuration, expected_type=type_hints["enable_minimum_encryption_configuration"])
            check_type(argname="argument enforce_workgroup_configuration", value=enforce_workgroup_configuration, expected_type=type_hints["enforce_workgroup_configuration"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument identity_center_configuration", value=identity_center_configuration, expected_type=type_hints["identity_center_configuration"])
            check_type(argname="argument managed_query_results_configuration", value=managed_query_results_configuration, expected_type=type_hints["managed_query_results_configuration"])
            check_type(argname="argument monitoring_configuration", value=monitoring_configuration, expected_type=type_hints["monitoring_configuration"])
            check_type(argname="argument publish_cloudwatch_metrics_enabled", value=publish_cloudwatch_metrics_enabled, expected_type=type_hints["publish_cloudwatch_metrics_enabled"])
            check_type(argname="argument requester_pays_enabled", value=requester_pays_enabled, expected_type=type_hints["requester_pays_enabled"])
            check_type(argname="argument result_configuration", value=result_configuration, expected_type=type_hints["result_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bytes_scanned_cutoff_per_query is not None:
            self._values["bytes_scanned_cutoff_per_query"] = bytes_scanned_cutoff_per_query
        if customer_content_encryption_configuration is not None:
            self._values["customer_content_encryption_configuration"] = customer_content_encryption_configuration
        if enable_minimum_encryption_configuration is not None:
            self._values["enable_minimum_encryption_configuration"] = enable_minimum_encryption_configuration
        if enforce_workgroup_configuration is not None:
            self._values["enforce_workgroup_configuration"] = enforce_workgroup_configuration
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if identity_center_configuration is not None:
            self._values["identity_center_configuration"] = identity_center_configuration
        if managed_query_results_configuration is not None:
            self._values["managed_query_results_configuration"] = managed_query_results_configuration
        if monitoring_configuration is not None:
            self._values["monitoring_configuration"] = monitoring_configuration
        if publish_cloudwatch_metrics_enabled is not None:
            self._values["publish_cloudwatch_metrics_enabled"] = publish_cloudwatch_metrics_enabled
        if requester_pays_enabled is not None:
            self._values["requester_pays_enabled"] = requester_pays_enabled
        if result_configuration is not None:
            self._values["result_configuration"] = result_configuration

    @builtins.property
    def bytes_scanned_cutoff_per_query(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#bytes_scanned_cutoff_per_query AthenaWorkgroup#bytes_scanned_cutoff_per_query}.'''
        result = self._values.get("bytes_scanned_cutoff_per_query")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def customer_content_encryption_configuration(
        self,
    ) -> typing.Optional["AthenaWorkgroupConfigurationCustomerContentEncryptionConfiguration"]:
        '''customer_content_encryption_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#customer_content_encryption_configuration AthenaWorkgroup#customer_content_encryption_configuration}
        '''
        result = self._values.get("customer_content_encryption_configuration")
        return typing.cast(typing.Optional["AthenaWorkgroupConfigurationCustomerContentEncryptionConfiguration"], result)

    @builtins.property
    def enable_minimum_encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enable_minimum_encryption_configuration AthenaWorkgroup#enable_minimum_encryption_configuration}.'''
        result = self._values.get("enable_minimum_encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enforce_workgroup_configuration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enforce_workgroup_configuration AthenaWorkgroup#enforce_workgroup_configuration}.'''
        result = self._values.get("enforce_workgroup_configuration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def engine_version(
        self,
    ) -> typing.Optional["AthenaWorkgroupConfigurationEngineVersion"]:
        '''engine_version block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#engine_version AthenaWorkgroup#engine_version}
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional["AthenaWorkgroupConfigurationEngineVersion"], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#execution_role AthenaWorkgroup#execution_role}.'''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_center_configuration(
        self,
    ) -> typing.Optional["AthenaWorkgroupConfigurationIdentityCenterConfiguration"]:
        '''identity_center_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#identity_center_configuration AthenaWorkgroup#identity_center_configuration}
        '''
        result = self._values.get("identity_center_configuration")
        return typing.cast(typing.Optional["AthenaWorkgroupConfigurationIdentityCenterConfiguration"], result)

    @builtins.property
    def managed_query_results_configuration(
        self,
    ) -> typing.Optional["AthenaWorkgroupConfigurationManagedQueryResultsConfiguration"]:
        '''managed_query_results_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#managed_query_results_configuration AthenaWorkgroup#managed_query_results_configuration}
        '''
        result = self._values.get("managed_query_results_configuration")
        return typing.cast(typing.Optional["AthenaWorkgroupConfigurationManagedQueryResultsConfiguration"], result)

    @builtins.property
    def monitoring_configuration(
        self,
    ) -> typing.Optional["AthenaWorkgroupConfigurationMonitoringConfiguration"]:
        '''monitoring_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#monitoring_configuration AthenaWorkgroup#monitoring_configuration}
        '''
        result = self._values.get("monitoring_configuration")
        return typing.cast(typing.Optional["AthenaWorkgroupConfigurationMonitoringConfiguration"], result)

    @builtins.property
    def publish_cloudwatch_metrics_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#publish_cloudwatch_metrics_enabled AthenaWorkgroup#publish_cloudwatch_metrics_enabled}.'''
        result = self._values.get("publish_cloudwatch_metrics_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def requester_pays_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#requester_pays_enabled AthenaWorkgroup#requester_pays_enabled}.'''
        result = self._values.get("requester_pays_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def result_configuration(
        self,
    ) -> typing.Optional["AthenaWorkgroupConfigurationResultConfiguration"]:
        '''result_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#result_configuration AthenaWorkgroup#result_configuration}
        '''
        result = self._values.get("result_configuration")
        return typing.cast(typing.Optional["AthenaWorkgroupConfigurationResultConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AthenaWorkgroupConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationCustomerContentEncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"kms_key": "kmsKey"},
)
class AthenaWorkgroupConfigurationCustomerContentEncryptionConfiguration:
    def __init__(self, *, kms_key: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#kms_key AthenaWorkgroup#kms_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff80ce886896191ba1f492f6f63860b3cf28a58b33171312a2764fdde12ea540)
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#kms_key AthenaWorkgroup#kms_key}.'''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AthenaWorkgroupConfigurationCustomerContentEncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AthenaWorkgroupConfigurationCustomerContentEncryptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationCustomerContentEncryptionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b028367acfa8585d8191567da0d2b06eda396ee4623f9868703db11fb4704816)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__07e7b1666b3a8af224de021d11d5f18ca9f3b2e1dec4f025bdd3480d277d77b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationCustomerContentEncryptionConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationCustomerContentEncryptionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AthenaWorkgroupConfigurationCustomerContentEncryptionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__968192a62f329575b3414357f7b4b47d642b2cff55af28c91866616d92cca1a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationEngineVersion",
    jsii_struct_bases=[],
    name_mapping={"selected_engine_version": "selectedEngineVersion"},
)
class AthenaWorkgroupConfigurationEngineVersion:
    def __init__(
        self,
        *,
        selected_engine_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param selected_engine_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#selected_engine_version AthenaWorkgroup#selected_engine_version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b58849dfbeaac619d23e36850ecd7672963be82a6b0e9f01f3ed4080d8e9ad7d)
            check_type(argname="argument selected_engine_version", value=selected_engine_version, expected_type=type_hints["selected_engine_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if selected_engine_version is not None:
            self._values["selected_engine_version"] = selected_engine_version

    @builtins.property
    def selected_engine_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#selected_engine_version AthenaWorkgroup#selected_engine_version}.'''
        result = self._values.get("selected_engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AthenaWorkgroupConfigurationEngineVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AthenaWorkgroupConfigurationEngineVersionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationEngineVersionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34c408e7c9b0724c3b0e510dbdd563ec08b65c5dcb7d1d8b02e9cfda57322cfd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSelectedEngineVersion")
    def reset_selected_engine_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectedEngineVersion", []))

    @builtins.property
    @jsii.member(jsii_name="effectiveEngineVersion")
    def effective_engine_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effectiveEngineVersion"))

    @builtins.property
    @jsii.member(jsii_name="selectedEngineVersionInput")
    def selected_engine_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selectedEngineVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="selectedEngineVersion")
    def selected_engine_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selectedEngineVersion"))

    @selected_engine_version.setter
    def selected_engine_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9b6d2f546821478ebfd69cea553ecbe806e969869050665d3e1adaccfcf0a49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selectedEngineVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationEngineVersion]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationEngineVersion], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AthenaWorkgroupConfigurationEngineVersion],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da72a36ace1008b9565c6ff1d9eaa0122d65b4df7573460e0513b65d715432a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationIdentityCenterConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "enable_identity_center": "enableIdentityCenter",
        "identity_center_instance_arn": "identityCenterInstanceArn",
    },
)
class AthenaWorkgroupConfigurationIdentityCenterConfiguration:
    def __init__(
        self,
        *,
        enable_identity_center: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        identity_center_instance_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enable_identity_center: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enable_identity_center AthenaWorkgroup#enable_identity_center}.
        :param identity_center_instance_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#identity_center_instance_arn AthenaWorkgroup#identity_center_instance_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad68224f9a0a30f41d3d6212e38717cbb0ed0b739cef5861c5ce1e77d776be64)
            check_type(argname="argument enable_identity_center", value=enable_identity_center, expected_type=type_hints["enable_identity_center"])
            check_type(argname="argument identity_center_instance_arn", value=identity_center_instance_arn, expected_type=type_hints["identity_center_instance_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_identity_center is not None:
            self._values["enable_identity_center"] = enable_identity_center
        if identity_center_instance_arn is not None:
            self._values["identity_center_instance_arn"] = identity_center_instance_arn

    @builtins.property
    def enable_identity_center(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enable_identity_center AthenaWorkgroup#enable_identity_center}.'''
        result = self._values.get("enable_identity_center")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def identity_center_instance_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#identity_center_instance_arn AthenaWorkgroup#identity_center_instance_arn}.'''
        result = self._values.get("identity_center_instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AthenaWorkgroupConfigurationIdentityCenterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AthenaWorkgroupConfigurationIdentityCenterConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationIdentityCenterConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20c2b9c1148ac7c42a838e5c3847a2c5f9cd06cb3fee69308842e51a2aa143ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableIdentityCenter")
    def reset_enable_identity_center(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableIdentityCenter", []))

    @jsii.member(jsii_name="resetIdentityCenterInstanceArn")
    def reset_identity_center_instance_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityCenterInstanceArn", []))

    @builtins.property
    @jsii.member(jsii_name="enableIdentityCenterInput")
    def enable_identity_center_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableIdentityCenterInput"))

    @builtins.property
    @jsii.member(jsii_name="identityCenterInstanceArnInput")
    def identity_center_instance_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityCenterInstanceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="enableIdentityCenter")
    def enable_identity_center(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableIdentityCenter"))

    @enable_identity_center.setter
    def enable_identity_center(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__752f9788b52409e5029c2cb2fa586d07a511566e53eaea7fa298a5088c05ec18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIdentityCenter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityCenterInstanceArn")
    def identity_center_instance_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityCenterInstanceArn"))

    @identity_center_instance_arn.setter
    def identity_center_instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b66a79148b77d0f2fb5a4c67d9faa65a4c26dd471631d15c0fd25f04f4a89e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityCenterInstanceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationIdentityCenterConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationIdentityCenterConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AthenaWorkgroupConfigurationIdentityCenterConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d9ed039836495e60c99f6dfd5efe93b791086f14c8cdbbd794f9f4d56c9fe5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationManagedQueryResultsConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "encryption_configuration": "encryptionConfiguration",
    },
)
class AthenaWorkgroupConfigurationManagedQueryResultsConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_configuration: typing.Optional[typing.Union["AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enabled AthenaWorkgroup#enabled}.
        :param encryption_configuration: encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#encryption_configuration AthenaWorkgroup#encryption_configuration}
        '''
        if isinstance(encryption_configuration, dict):
            encryption_configuration = AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfiguration(**encryption_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c762f86fc7d8f742e9a4aa9385de50498d198a9c039a670b11a001ba7035aa7e)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enabled AthenaWorkgroup#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional["AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfiguration"]:
        '''encryption_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#encryption_configuration AthenaWorkgroup#encryption_configuration}
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional["AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AthenaWorkgroupConfigurationManagedQueryResultsConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"kms_key": "kmsKey"},
)
class AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfiguration:
    def __init__(self, *, kms_key: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#kms_key AthenaWorkgroup#kms_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ce65eb1d36cbee34385639bfcbd8c1f4a9d51af9e92b452dfa0b038149a830e)
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#kms_key AthenaWorkgroup#kms_key}.'''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc4145e7d3c99b6eda2045b2b2ae0683406817fb5d1c4bdb3694dfddf6af6864)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__eba0d14e14fa9dfcf6048d4549ee1df50bfe31412f0cf62d721713bf05e305e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad59695abb918cc19eccee687a2bf3545de4afbae08c2f80c6f13f00529c7de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AthenaWorkgroupConfigurationManagedQueryResultsConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationManagedQueryResultsConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a83f2ac753854a3d5fe7661cfeb4dd08cfd4786ede44aca7b45929feaf242f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEncryptionConfiguration")
    def put_encryption_configuration(
        self,
        *,
        kms_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#kms_key AthenaWorkgroup#kms_key}.
        '''
        value = AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfiguration(
            kms_key=kms_key
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfiguration", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEncryptionConfiguration")
    def reset_encryption_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfiguration")
    def encryption_configuration(
        self,
    ) -> AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfigurationOutputReference:
        return typing.cast(AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfigurationOutputReference, jsii.get(self, "encryptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigurationInput")
    def encryption_configuration_input(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfiguration], jsii.get(self, "encryptionConfigurationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1b375985fe3464a1def958465bc128a8bd14a526f7b4a3f1d2278664bc4d7b06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationManagedQueryResultsConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationManagedQueryResultsConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AthenaWorkgroupConfigurationManagedQueryResultsConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b762f6f65a37905c91af164a078b1f536c853a6ca652cf6dfdd479618002754f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationMonitoringConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_watch_logging_configuration": "cloudWatchLoggingConfiguration",
        "managed_logging_configuration": "managedLoggingConfiguration",
        "s3_logging_configuration": "s3LoggingConfiguration",
    },
)
class AthenaWorkgroupConfigurationMonitoringConfiguration:
    def __init__(
        self,
        *,
        cloud_watch_logging_configuration: typing.Optional[typing.Union["AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        managed_logging_configuration: typing.Optional[typing.Union["AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_logging_configuration: typing.Optional[typing.Union["AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_watch_logging_configuration: cloud_watch_logging_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#cloud_watch_logging_configuration AthenaWorkgroup#cloud_watch_logging_configuration}
        :param managed_logging_configuration: managed_logging_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#managed_logging_configuration AthenaWorkgroup#managed_logging_configuration}
        :param s3_logging_configuration: s3_logging_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#s3_logging_configuration AthenaWorkgroup#s3_logging_configuration}
        '''
        if isinstance(cloud_watch_logging_configuration, dict):
            cloud_watch_logging_configuration = AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfiguration(**cloud_watch_logging_configuration)
        if isinstance(managed_logging_configuration, dict):
            managed_logging_configuration = AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfiguration(**managed_logging_configuration)
        if isinstance(s3_logging_configuration, dict):
            s3_logging_configuration = AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfiguration(**s3_logging_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__900616b55c436bed4efb983bce0bbd5bf9c3fa75d9f32a6aacd2cc5a19981c2f)
            check_type(argname="argument cloud_watch_logging_configuration", value=cloud_watch_logging_configuration, expected_type=type_hints["cloud_watch_logging_configuration"])
            check_type(argname="argument managed_logging_configuration", value=managed_logging_configuration, expected_type=type_hints["managed_logging_configuration"])
            check_type(argname="argument s3_logging_configuration", value=s3_logging_configuration, expected_type=type_hints["s3_logging_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_watch_logging_configuration is not None:
            self._values["cloud_watch_logging_configuration"] = cloud_watch_logging_configuration
        if managed_logging_configuration is not None:
            self._values["managed_logging_configuration"] = managed_logging_configuration
        if s3_logging_configuration is not None:
            self._values["s3_logging_configuration"] = s3_logging_configuration

    @builtins.property
    def cloud_watch_logging_configuration(
        self,
    ) -> typing.Optional["AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfiguration"]:
        '''cloud_watch_logging_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#cloud_watch_logging_configuration AthenaWorkgroup#cloud_watch_logging_configuration}
        '''
        result = self._values.get("cloud_watch_logging_configuration")
        return typing.cast(typing.Optional["AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfiguration"], result)

    @builtins.property
    def managed_logging_configuration(
        self,
    ) -> typing.Optional["AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfiguration"]:
        '''managed_logging_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#managed_logging_configuration AthenaWorkgroup#managed_logging_configuration}
        '''
        result = self._values.get("managed_logging_configuration")
        return typing.cast(typing.Optional["AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfiguration"], result)

    @builtins.property
    def s3_logging_configuration(
        self,
    ) -> typing.Optional["AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfiguration"]:
        '''s3_logging_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#s3_logging_configuration AthenaWorkgroup#s3_logging_configuration}
        '''
        result = self._values.get("s3_logging_configuration")
        return typing.cast(typing.Optional["AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AthenaWorkgroupConfigurationMonitoringConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "log_group": "logGroup",
        "log_stream_name_prefix": "logStreamNamePrefix",
        "log_type": "logType",
    },
)
class AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        log_group: typing.Optional[builtins.str] = None,
        log_stream_name_prefix: typing.Optional[builtins.str] = None,
        log_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enabled AthenaWorkgroup#enabled}.
        :param log_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#log_group AthenaWorkgroup#log_group}.
        :param log_stream_name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#log_stream_name_prefix AthenaWorkgroup#log_stream_name_prefix}.
        :param log_type: log_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#log_type AthenaWorkgroup#log_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c437e488793a8b33c583bba02f569c089e0d599909e1e4e55cd14bc3806511fc)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument log_stream_name_prefix", value=log_stream_name_prefix, expected_type=type_hints["log_stream_name_prefix"])
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if log_group is not None:
            self._values["log_group"] = log_group
        if log_stream_name_prefix is not None:
            self._values["log_stream_name_prefix"] = log_stream_name_prefix
        if log_type is not None:
            self._values["log_type"] = log_type

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enabled AthenaWorkgroup#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def log_group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#log_group AthenaWorkgroup#log_group}.'''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_stream_name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#log_stream_name_prefix AthenaWorkgroup#log_stream_name_prefix}.'''
        result = self._values.get("log_stream_name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_type(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType"]]]:
        '''log_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#log_type AthenaWorkgroup#log_type}
        '''
        result = self._values.get("log_type")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#key AthenaWorkgroup#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#values AthenaWorkgroup#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1402e2fd32678623c88a7c1e9de8e9c72c172a20506fd574aae6c7a38c86ec9e)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#key AthenaWorkgroup#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#values AthenaWorkgroup#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogTypeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogTypeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd5a26e0e7f6a7c6cd0c078aed433d142cbedcaae988c74ac0cfeaee41e2a92a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogTypeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b21127fa95144a95868eb70555e744f9fc17c747e991e0f81141c52c7a636fe6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogTypeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f15d567b86792181263c7e0caa12daef49b178f997b2f068516845d62b3bb7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b9881f6d321878743c32626aaa0eae988bb3918fcf6cbd8fc902ffae92a310f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cc36c2c65d2272a55f47e2bab7a63b7182813b7c98be5f54d482720451c3884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55e386405196c1af8ccc04b388ae870134e00626a2397418c1ce40c76db43b05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__053e0a7c54384b4492e3afdac2a52a2598afa6691e97376bbd6181a3bfc187ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__010be9514e1a56b783d7f38af5a5ce5cb2c9d8de21e9fdb285ed3c504b92d493)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e1b20de825ef17d22017b4cb84f098d936889855848ecd0295886002477062b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6e279c398db12f2639a05291a66c9674e9f2d017ae2ee30f1444bffabad9990)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc35a0b2b391f67c10ccf398478e2a21616e41a5a9b0131ff009050520ee3a59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLogType")
    def put_log_type(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df527fba0b08f084ca4b38cbe3a53300357b82aabe47f491368f3d89e00899b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLogType", [value]))

    @jsii.member(jsii_name="resetLogGroup")
    def reset_log_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogGroup", []))

    @jsii.member(jsii_name="resetLogStreamNamePrefix")
    def reset_log_stream_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogStreamNamePrefix", []))

    @jsii.member(jsii_name="resetLogType")
    def reset_log_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogType", []))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def log_type(
        self,
    ) -> AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogTypeList:
        return typing.cast(AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogTypeList, jsii.get(self, "logType"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupInput")
    def log_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamNamePrefixInput")
    def log_stream_name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamNamePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="logTypeInput")
    def log_type_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType]]], jsii.get(self, "logTypeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a5bf7ff6eab484e68d2c6772e2e93dbbaaa620c81a7fcfe05e63a4b4c6faeb2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroup"))

    @log_group.setter
    def log_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__942edc79a5075d8b5f5ef6eae424fdc989766b786b04002232adea26690a2dc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logStreamNamePrefix")
    def log_stream_name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamNamePrefix"))

    @log_stream_name_prefix.setter
    def log_stream_name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d6f8a755385b0777b17ca7ec1c1d964a5cddf96239a1b3789851c4d4e1a9255)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamNamePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1142e0c3c43b19b762e51cb34d248cc4b585b8b643eee2587d561893a8a31638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "kms_key": "kmsKey"},
)
class AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        kms_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enabled AthenaWorkgroup#enabled}.
        :param kms_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#kms_key AthenaWorkgroup#kms_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30cfb4c6a5c4f190f5772bc078743036a8c0a304633fed06fd332585f41ed3dd)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enabled AthenaWorkgroup#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#kms_key AthenaWorkgroup#kms_key}.'''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28040c942501f1af4bd8f079279999e8bc55464631b07a5cf51c4d55800757fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__10da0b3e94714e4595f7b1eb1a29d7a898631d16c433cd4a1bfa47f77ec96f16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88f14c8749944c7b5b2ce6bd668eab2764967e11b2f381a215b7c889c4d09ed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c92ed12560db06f66d1a29465be7973107316d6d1548083c2a014cee01bb1ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AthenaWorkgroupConfigurationMonitoringConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationMonitoringConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__743742a8ee4c985b7323388a5be13df49a6073a2a727e559a73e981f1bfcf773)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudWatchLoggingConfiguration")
    def put_cloud_watch_logging_configuration(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        log_group: typing.Optional[builtins.str] = None,
        log_stream_name_prefix: typing.Optional[builtins.str] = None,
        log_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enabled AthenaWorkgroup#enabled}.
        :param log_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#log_group AthenaWorkgroup#log_group}.
        :param log_stream_name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#log_stream_name_prefix AthenaWorkgroup#log_stream_name_prefix}.
        :param log_type: log_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#log_type AthenaWorkgroup#log_type}
        '''
        value = AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfiguration(
            enabled=enabled,
            log_group=log_group,
            log_stream_name_prefix=log_stream_name_prefix,
            log_type=log_type,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudWatchLoggingConfiguration", [value]))

    @jsii.member(jsii_name="putManagedLoggingConfiguration")
    def put_managed_logging_configuration(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        kms_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enabled AthenaWorkgroup#enabled}.
        :param kms_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#kms_key AthenaWorkgroup#kms_key}.
        '''
        value = AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfiguration(
            enabled=enabled, kms_key=kms_key
        )

        return typing.cast(None, jsii.invoke(self, "putManagedLoggingConfiguration", [value]))

    @jsii.member(jsii_name="putS3LoggingConfiguration")
    def put_s3_logging_configuration(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        kms_key: typing.Optional[builtins.str] = None,
        log_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enabled AthenaWorkgroup#enabled}.
        :param kms_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#kms_key AthenaWorkgroup#kms_key}.
        :param log_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#log_location AthenaWorkgroup#log_location}.
        '''
        value = AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfiguration(
            enabled=enabled, kms_key=kms_key, log_location=log_location
        )

        return typing.cast(None, jsii.invoke(self, "putS3LoggingConfiguration", [value]))

    @jsii.member(jsii_name="resetCloudWatchLoggingConfiguration")
    def reset_cloud_watch_logging_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudWatchLoggingConfiguration", []))

    @jsii.member(jsii_name="resetManagedLoggingConfiguration")
    def reset_managed_logging_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedLoggingConfiguration", []))

    @jsii.member(jsii_name="resetS3LoggingConfiguration")
    def reset_s3_logging_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3LoggingConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchLoggingConfiguration")
    def cloud_watch_logging_configuration(
        self,
    ) -> AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationOutputReference:
        return typing.cast(AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationOutputReference, jsii.get(self, "cloudWatchLoggingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="managedLoggingConfiguration")
    def managed_logging_configuration(
        self,
    ) -> AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfigurationOutputReference:
        return typing.cast(AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfigurationOutputReference, jsii.get(self, "managedLoggingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="s3LoggingConfiguration")
    def s3_logging_configuration(
        self,
    ) -> "AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfigurationOutputReference":
        return typing.cast("AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfigurationOutputReference", jsii.get(self, "s3LoggingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchLoggingConfigurationInput")
    def cloud_watch_logging_configuration_input(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfiguration], jsii.get(self, "cloudWatchLoggingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="managedLoggingConfigurationInput")
    def managed_logging_configuration_input(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfiguration], jsii.get(self, "managedLoggingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="s3LoggingConfigurationInput")
    def s3_logging_configuration_input(
        self,
    ) -> typing.Optional["AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfiguration"]:
        return typing.cast(typing.Optional["AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfiguration"], jsii.get(self, "s3LoggingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationMonitoringConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationMonitoringConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AthenaWorkgroupConfigurationMonitoringConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b24713bcae66df1966b1a19b8cec21cc7ff79788d0db3e3343ccdb37ca55db93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "kms_key": "kmsKey",
        "log_location": "logLocation",
    },
)
class AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        kms_key: typing.Optional[builtins.str] = None,
        log_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enabled AthenaWorkgroup#enabled}.
        :param kms_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#kms_key AthenaWorkgroup#kms_key}.
        :param log_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#log_location AthenaWorkgroup#log_location}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cf93aff8c9c7fa572e0e3b85a2d9f91109df4ba25195da146534ed710cdf568)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument log_location", value=log_location, expected_type=type_hints["log_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if log_location is not None:
            self._values["log_location"] = log_location

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enabled AthenaWorkgroup#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#kms_key AthenaWorkgroup#kms_key}.'''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#log_location AthenaWorkgroup#log_location}.'''
        result = self._values.get("log_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b019265d3dc5eb7a59fd9a12aa3efdf7ee0b6753bc3809be9b0cf628dae4c60a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @jsii.member(jsii_name="resetLogLocation")
    def reset_log_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogLocation", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="logLocationInput")
    def log_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logLocationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__42d49b7179fca3574d3349d49f64556657d67f62322e6c3c722fe24fce483cdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a763a694335acbfd6bd5d1d628d16c643de194716088c231e309c5eb75e9926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLocation")
    def log_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLocation"))

    @log_location.setter
    def log_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebffb4b054e807b1f425b28b48c870b6c68d0b0ec8c7ce441e761aa60a70f35a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39aff74bb8f34dc4a9bc3b998becb1176fcdee56667283754cc8494e86989b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AthenaWorkgroupConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f49dea61e9e4a75f43296b0594116add80daa058acd310447c00f19aee714414)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomerContentEncryptionConfiguration")
    def put_customer_content_encryption_configuration(
        self,
        *,
        kms_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#kms_key AthenaWorkgroup#kms_key}.
        '''
        value = AthenaWorkgroupConfigurationCustomerContentEncryptionConfiguration(
            kms_key=kms_key
        )

        return typing.cast(None, jsii.invoke(self, "putCustomerContentEncryptionConfiguration", [value]))

    @jsii.member(jsii_name="putEngineVersion")
    def put_engine_version(
        self,
        *,
        selected_engine_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param selected_engine_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#selected_engine_version AthenaWorkgroup#selected_engine_version}.
        '''
        value = AthenaWorkgroupConfigurationEngineVersion(
            selected_engine_version=selected_engine_version
        )

        return typing.cast(None, jsii.invoke(self, "putEngineVersion", [value]))

    @jsii.member(jsii_name="putIdentityCenterConfiguration")
    def put_identity_center_configuration(
        self,
        *,
        enable_identity_center: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        identity_center_instance_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enable_identity_center: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enable_identity_center AthenaWorkgroup#enable_identity_center}.
        :param identity_center_instance_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#identity_center_instance_arn AthenaWorkgroup#identity_center_instance_arn}.
        '''
        value = AthenaWorkgroupConfigurationIdentityCenterConfiguration(
            enable_identity_center=enable_identity_center,
            identity_center_instance_arn=identity_center_instance_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putIdentityCenterConfiguration", [value]))

    @jsii.member(jsii_name="putManagedQueryResultsConfiguration")
    def put_managed_query_results_configuration(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_configuration: typing.Optional[typing.Union[AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#enabled AthenaWorkgroup#enabled}.
        :param encryption_configuration: encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#encryption_configuration AthenaWorkgroup#encryption_configuration}
        '''
        value = AthenaWorkgroupConfigurationManagedQueryResultsConfiguration(
            enabled=enabled, encryption_configuration=encryption_configuration
        )

        return typing.cast(None, jsii.invoke(self, "putManagedQueryResultsConfiguration", [value]))

    @jsii.member(jsii_name="putMonitoringConfiguration")
    def put_monitoring_configuration(
        self,
        *,
        cloud_watch_logging_configuration: typing.Optional[typing.Union[AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        managed_logging_configuration: typing.Optional[typing.Union[AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        s3_logging_configuration: typing.Optional[typing.Union[AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloud_watch_logging_configuration: cloud_watch_logging_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#cloud_watch_logging_configuration AthenaWorkgroup#cloud_watch_logging_configuration}
        :param managed_logging_configuration: managed_logging_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#managed_logging_configuration AthenaWorkgroup#managed_logging_configuration}
        :param s3_logging_configuration: s3_logging_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#s3_logging_configuration AthenaWorkgroup#s3_logging_configuration}
        '''
        value = AthenaWorkgroupConfigurationMonitoringConfiguration(
            cloud_watch_logging_configuration=cloud_watch_logging_configuration,
            managed_logging_configuration=managed_logging_configuration,
            s3_logging_configuration=s3_logging_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putMonitoringConfiguration", [value]))

    @jsii.member(jsii_name="putResultConfiguration")
    def put_result_configuration(
        self,
        *,
        acl_configuration: typing.Optional[typing.Union["AthenaWorkgroupConfigurationResultConfigurationAclConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_configuration: typing.Optional[typing.Union["AthenaWorkgroupConfigurationResultConfigurationEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        expected_bucket_owner: typing.Optional[builtins.str] = None,
        output_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param acl_configuration: acl_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#acl_configuration AthenaWorkgroup#acl_configuration}
        :param encryption_configuration: encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#encryption_configuration AthenaWorkgroup#encryption_configuration}
        :param expected_bucket_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#expected_bucket_owner AthenaWorkgroup#expected_bucket_owner}.
        :param output_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#output_location AthenaWorkgroup#output_location}.
        '''
        value = AthenaWorkgroupConfigurationResultConfiguration(
            acl_configuration=acl_configuration,
            encryption_configuration=encryption_configuration,
            expected_bucket_owner=expected_bucket_owner,
            output_location=output_location,
        )

        return typing.cast(None, jsii.invoke(self, "putResultConfiguration", [value]))

    @jsii.member(jsii_name="resetBytesScannedCutoffPerQuery")
    def reset_bytes_scanned_cutoff_per_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBytesScannedCutoffPerQuery", []))

    @jsii.member(jsii_name="resetCustomerContentEncryptionConfiguration")
    def reset_customer_content_encryption_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerContentEncryptionConfiguration", []))

    @jsii.member(jsii_name="resetEnableMinimumEncryptionConfiguration")
    def reset_enable_minimum_encryption_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableMinimumEncryptionConfiguration", []))

    @jsii.member(jsii_name="resetEnforceWorkgroupConfiguration")
    def reset_enforce_workgroup_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceWorkgroupConfiguration", []))

    @jsii.member(jsii_name="resetEngineVersion")
    def reset_engine_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEngineVersion", []))

    @jsii.member(jsii_name="resetExecutionRole")
    def reset_execution_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionRole", []))

    @jsii.member(jsii_name="resetIdentityCenterConfiguration")
    def reset_identity_center_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityCenterConfiguration", []))

    @jsii.member(jsii_name="resetManagedQueryResultsConfiguration")
    def reset_managed_query_results_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedQueryResultsConfiguration", []))

    @jsii.member(jsii_name="resetMonitoringConfiguration")
    def reset_monitoring_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitoringConfiguration", []))

    @jsii.member(jsii_name="resetPublishCloudwatchMetricsEnabled")
    def reset_publish_cloudwatch_metrics_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublishCloudwatchMetricsEnabled", []))

    @jsii.member(jsii_name="resetRequesterPaysEnabled")
    def reset_requester_pays_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequesterPaysEnabled", []))

    @jsii.member(jsii_name="resetResultConfiguration")
    def reset_result_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResultConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="customerContentEncryptionConfiguration")
    def customer_content_encryption_configuration(
        self,
    ) -> AthenaWorkgroupConfigurationCustomerContentEncryptionConfigurationOutputReference:
        return typing.cast(AthenaWorkgroupConfigurationCustomerContentEncryptionConfigurationOutputReference, jsii.get(self, "customerContentEncryptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(
        self,
    ) -> AthenaWorkgroupConfigurationEngineVersionOutputReference:
        return typing.cast(AthenaWorkgroupConfigurationEngineVersionOutputReference, jsii.get(self, "engineVersion"))

    @builtins.property
    @jsii.member(jsii_name="identityCenterConfiguration")
    def identity_center_configuration(
        self,
    ) -> AthenaWorkgroupConfigurationIdentityCenterConfigurationOutputReference:
        return typing.cast(AthenaWorkgroupConfigurationIdentityCenterConfigurationOutputReference, jsii.get(self, "identityCenterConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="managedQueryResultsConfiguration")
    def managed_query_results_configuration(
        self,
    ) -> AthenaWorkgroupConfigurationManagedQueryResultsConfigurationOutputReference:
        return typing.cast(AthenaWorkgroupConfigurationManagedQueryResultsConfigurationOutputReference, jsii.get(self, "managedQueryResultsConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="monitoringConfiguration")
    def monitoring_configuration(
        self,
    ) -> AthenaWorkgroupConfigurationMonitoringConfigurationOutputReference:
        return typing.cast(AthenaWorkgroupConfigurationMonitoringConfigurationOutputReference, jsii.get(self, "monitoringConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="resultConfiguration")
    def result_configuration(
        self,
    ) -> "AthenaWorkgroupConfigurationResultConfigurationOutputReference":
        return typing.cast("AthenaWorkgroupConfigurationResultConfigurationOutputReference", jsii.get(self, "resultConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="bytesScannedCutoffPerQueryInput")
    def bytes_scanned_cutoff_per_query_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bytesScannedCutoffPerQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="customerContentEncryptionConfigurationInput")
    def customer_content_encryption_configuration_input(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationCustomerContentEncryptionConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationCustomerContentEncryptionConfiguration], jsii.get(self, "customerContentEncryptionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="enableMinimumEncryptionConfigurationInput")
    def enable_minimum_encryption_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableMinimumEncryptionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceWorkgroupConfigurationInput")
    def enforce_workgroup_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforceWorkgroupConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="engineVersionInput")
    def engine_version_input(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationEngineVersion]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationEngineVersion], jsii.get(self, "engineVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRoleInput")
    def execution_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="identityCenterConfigurationInput")
    def identity_center_configuration_input(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationIdentityCenterConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationIdentityCenterConfiguration], jsii.get(self, "identityCenterConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="managedQueryResultsConfigurationInput")
    def managed_query_results_configuration_input(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationManagedQueryResultsConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationManagedQueryResultsConfiguration], jsii.get(self, "managedQueryResultsConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="monitoringConfigurationInput")
    def monitoring_configuration_input(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationMonitoringConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationMonitoringConfiguration], jsii.get(self, "monitoringConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="publishCloudwatchMetricsEnabledInput")
    def publish_cloudwatch_metrics_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publishCloudwatchMetricsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="requesterPaysEnabledInput")
    def requester_pays_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requesterPaysEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="resultConfigurationInput")
    def result_configuration_input(
        self,
    ) -> typing.Optional["AthenaWorkgroupConfigurationResultConfiguration"]:
        return typing.cast(typing.Optional["AthenaWorkgroupConfigurationResultConfiguration"], jsii.get(self, "resultConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="bytesScannedCutoffPerQuery")
    def bytes_scanned_cutoff_per_query(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bytesScannedCutoffPerQuery"))

    @bytes_scanned_cutoff_per_query.setter
    def bytes_scanned_cutoff_per_query(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daa4abeb41e8c02434879be524796c5fa7113d72591b5ef46631502d23aeb9cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bytesScannedCutoffPerQuery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableMinimumEncryptionConfiguration")
    def enable_minimum_encryption_configuration(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableMinimumEncryptionConfiguration"))

    @enable_minimum_encryption_configuration.setter
    def enable_minimum_encryption_configuration(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0cc65a5e9ffc6a3aa0013d41dc8c69ff8562d311666232cc1523805acd67a5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableMinimumEncryptionConfiguration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceWorkgroupConfiguration")
    def enforce_workgroup_configuration(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforceWorkgroupConfiguration"))

    @enforce_workgroup_configuration.setter
    def enforce_workgroup_configuration(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__535d998f91102efffc42d1b7d1e81cae1df82bf958deef76c00c9d3a6aed8bcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceWorkgroupConfiguration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionRole"))

    @execution_role.setter
    def execution_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a3eda39211d786c6f8777f4934eb06419efdf73c3ed7adb4ba640251d62608b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publishCloudwatchMetricsEnabled")
    def publish_cloudwatch_metrics_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publishCloudwatchMetricsEnabled"))

    @publish_cloudwatch_metrics_enabled.setter
    def publish_cloudwatch_metrics_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b5ae27e152e14b32219d276047103743bb3439bfa0323c6c18d67499b4812af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publishCloudwatchMetricsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requesterPaysEnabled")
    def requester_pays_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requesterPaysEnabled"))

    @requester_pays_enabled.setter
    def requester_pays_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05699ccf75eb5cb8782f745b0f38bb052f6297f6ff267f81db1fd858ff27dcd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requesterPaysEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AthenaWorkgroupConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AthenaWorkgroupConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c38b3d08babafdf1e0be01664122660c98f14276a850f6300544973a903a143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationResultConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "acl_configuration": "aclConfiguration",
        "encryption_configuration": "encryptionConfiguration",
        "expected_bucket_owner": "expectedBucketOwner",
        "output_location": "outputLocation",
    },
)
class AthenaWorkgroupConfigurationResultConfiguration:
    def __init__(
        self,
        *,
        acl_configuration: typing.Optional[typing.Union["AthenaWorkgroupConfigurationResultConfigurationAclConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_configuration: typing.Optional[typing.Union["AthenaWorkgroupConfigurationResultConfigurationEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        expected_bucket_owner: typing.Optional[builtins.str] = None,
        output_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param acl_configuration: acl_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#acl_configuration AthenaWorkgroup#acl_configuration}
        :param encryption_configuration: encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#encryption_configuration AthenaWorkgroup#encryption_configuration}
        :param expected_bucket_owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#expected_bucket_owner AthenaWorkgroup#expected_bucket_owner}.
        :param output_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#output_location AthenaWorkgroup#output_location}.
        '''
        if isinstance(acl_configuration, dict):
            acl_configuration = AthenaWorkgroupConfigurationResultConfigurationAclConfiguration(**acl_configuration)
        if isinstance(encryption_configuration, dict):
            encryption_configuration = AthenaWorkgroupConfigurationResultConfigurationEncryptionConfiguration(**encryption_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3492de4d5df5964ee6e0a2051af610e6d9ec3f537c4239c891911caa7718aeef)
            check_type(argname="argument acl_configuration", value=acl_configuration, expected_type=type_hints["acl_configuration"])
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument expected_bucket_owner", value=expected_bucket_owner, expected_type=type_hints["expected_bucket_owner"])
            check_type(argname="argument output_location", value=output_location, expected_type=type_hints["output_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if acl_configuration is not None:
            self._values["acl_configuration"] = acl_configuration
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if expected_bucket_owner is not None:
            self._values["expected_bucket_owner"] = expected_bucket_owner
        if output_location is not None:
            self._values["output_location"] = output_location

    @builtins.property
    def acl_configuration(
        self,
    ) -> typing.Optional["AthenaWorkgroupConfigurationResultConfigurationAclConfiguration"]:
        '''acl_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#acl_configuration AthenaWorkgroup#acl_configuration}
        '''
        result = self._values.get("acl_configuration")
        return typing.cast(typing.Optional["AthenaWorkgroupConfigurationResultConfigurationAclConfiguration"], result)

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional["AthenaWorkgroupConfigurationResultConfigurationEncryptionConfiguration"]:
        '''encryption_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#encryption_configuration AthenaWorkgroup#encryption_configuration}
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional["AthenaWorkgroupConfigurationResultConfigurationEncryptionConfiguration"], result)

    @builtins.property
    def expected_bucket_owner(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#expected_bucket_owner AthenaWorkgroup#expected_bucket_owner}.'''
        result = self._values.get("expected_bucket_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#output_location AthenaWorkgroup#output_location}.'''
        result = self._values.get("output_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AthenaWorkgroupConfigurationResultConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationResultConfigurationAclConfiguration",
    jsii_struct_bases=[],
    name_mapping={"s3_acl_option": "s3AclOption"},
)
class AthenaWorkgroupConfigurationResultConfigurationAclConfiguration:
    def __init__(self, *, s3_acl_option: builtins.str) -> None:
        '''
        :param s3_acl_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#s3_acl_option AthenaWorkgroup#s3_acl_option}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0814ccacc0f924260c4e0059dd9e57ff3beddc1c66cda05ff83664f2061b5e6)
            check_type(argname="argument s3_acl_option", value=s3_acl_option, expected_type=type_hints["s3_acl_option"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_acl_option": s3_acl_option,
        }

    @builtins.property
    def s3_acl_option(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#s3_acl_option AthenaWorkgroup#s3_acl_option}.'''
        result = self._values.get("s3_acl_option")
        assert result is not None, "Required property 's3_acl_option' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AthenaWorkgroupConfigurationResultConfigurationAclConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AthenaWorkgroupConfigurationResultConfigurationAclConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationResultConfigurationAclConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4df5def788f07855531f3313adc5c02a57470f3b51ec66cd56f9cd59021e1c09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="s3AclOptionInput")
    def s3_acl_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3AclOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="s3AclOption")
    def s3_acl_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3AclOption"))

    @s3_acl_option.setter
    def s3_acl_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce3d677801de733f9dfa18b6a1334f8429cdc170ef2aee6ea64a4474138236e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3AclOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationResultConfigurationAclConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationResultConfigurationAclConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AthenaWorkgroupConfigurationResultConfigurationAclConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01e9266a1923ee489b5d60dc742e0356d4290bcedf665e2a4431ff35920c5b11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationResultConfigurationEncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"encryption_option": "encryptionOption", "kms_key_arn": "kmsKeyArn"},
)
class AthenaWorkgroupConfigurationResultConfigurationEncryptionConfiguration:
    def __init__(
        self,
        *,
        encryption_option: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encryption_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#encryption_option AthenaWorkgroup#encryption_option}.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#kms_key_arn AthenaWorkgroup#kms_key_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a71c0e1c544df3ab0072bb98fa7730418db0f87868c1b7ef5d3803373051238)
            check_type(argname="argument encryption_option", value=encryption_option, expected_type=type_hints["encryption_option"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encryption_option is not None:
            self._values["encryption_option"] = encryption_option
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn

    @builtins.property
    def encryption_option(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#encryption_option AthenaWorkgroup#encryption_option}.'''
        result = self._values.get("encryption_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#kms_key_arn AthenaWorkgroup#kms_key_arn}.'''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AthenaWorkgroupConfigurationResultConfigurationEncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AthenaWorkgroupConfigurationResultConfigurationEncryptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationResultConfigurationEncryptionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__edf3e6ca2fbcb08122eea9e34e99911cbb6559df4f9b5f52c0de10646fe8a374)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEncryptionOption")
    def reset_encryption_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionOption", []))

    @jsii.member(jsii_name="resetKmsKeyArn")
    def reset_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyArn", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionOptionInput")
    def encryption_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionOption")
    def encryption_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionOption"))

    @encryption_option.setter
    def encryption_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76b409518ac4c1222c92d925b7a0071ba7a7a7b9b3639baf1bf7a8170b68574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ceefa764a522f3c74b0eee33bb9a2d349517e512a4ba95bf3f4d30eccf65d03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationResultConfigurationEncryptionConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationResultConfigurationEncryptionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AthenaWorkgroupConfigurationResultConfigurationEncryptionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66d96aa62098b40a7a6775e2180eaa7401d9fc3b90544d640cd59f61b14cacce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AthenaWorkgroupConfigurationResultConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.athenaWorkgroup.AthenaWorkgroupConfigurationResultConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f08e078ff998ed3c8834ebe4f2292028db5bd00a5f039302d833cceb52be83cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAclConfiguration")
    def put_acl_configuration(self, *, s3_acl_option: builtins.str) -> None:
        '''
        :param s3_acl_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#s3_acl_option AthenaWorkgroup#s3_acl_option}.
        '''
        value = AthenaWorkgroupConfigurationResultConfigurationAclConfiguration(
            s3_acl_option=s3_acl_option
        )

        return typing.cast(None, jsii.invoke(self, "putAclConfiguration", [value]))

    @jsii.member(jsii_name="putEncryptionConfiguration")
    def put_encryption_configuration(
        self,
        *,
        encryption_option: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encryption_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#encryption_option AthenaWorkgroup#encryption_option}.
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/athena_workgroup#kms_key_arn AthenaWorkgroup#kms_key_arn}.
        '''
        value = AthenaWorkgroupConfigurationResultConfigurationEncryptionConfiguration(
            encryption_option=encryption_option, kms_key_arn=kms_key_arn
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfiguration", [value]))

    @jsii.member(jsii_name="resetAclConfiguration")
    def reset_acl_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAclConfiguration", []))

    @jsii.member(jsii_name="resetEncryptionConfiguration")
    def reset_encryption_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfiguration", []))

    @jsii.member(jsii_name="resetExpectedBucketOwner")
    def reset_expected_bucket_owner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpectedBucketOwner", []))

    @jsii.member(jsii_name="resetOutputLocation")
    def reset_output_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputLocation", []))

    @builtins.property
    @jsii.member(jsii_name="aclConfiguration")
    def acl_configuration(
        self,
    ) -> AthenaWorkgroupConfigurationResultConfigurationAclConfigurationOutputReference:
        return typing.cast(AthenaWorkgroupConfigurationResultConfigurationAclConfigurationOutputReference, jsii.get(self, "aclConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfiguration")
    def encryption_configuration(
        self,
    ) -> AthenaWorkgroupConfigurationResultConfigurationEncryptionConfigurationOutputReference:
        return typing.cast(AthenaWorkgroupConfigurationResultConfigurationEncryptionConfigurationOutputReference, jsii.get(self, "encryptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="aclConfigurationInput")
    def acl_configuration_input(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationResultConfigurationAclConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationResultConfigurationAclConfiguration], jsii.get(self, "aclConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigurationInput")
    def encryption_configuration_input(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationResultConfigurationEncryptionConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationResultConfigurationEncryptionConfiguration], jsii.get(self, "encryptionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="expectedBucketOwnerInput")
    def expected_bucket_owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expectedBucketOwnerInput"))

    @builtins.property
    @jsii.member(jsii_name="outputLocationInput")
    def output_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="expectedBucketOwner")
    def expected_bucket_owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expectedBucketOwner"))

    @expected_bucket_owner.setter
    def expected_bucket_owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e6a0b80c0f51a4a53b7604a302dae8c8afddf32a3b56daa4d44cbd79cc4d6a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expectedBucketOwner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputLocation")
    def output_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputLocation"))

    @output_location.setter
    def output_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35d230167403c5e10061d75eb49fbfa61f52e317e84c425d8b8f3295fbe59127)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AthenaWorkgroupConfigurationResultConfiguration]:
        return typing.cast(typing.Optional[AthenaWorkgroupConfigurationResultConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AthenaWorkgroupConfigurationResultConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae8a7a6477f3138dd34e2c25832303314fd532c72b549882adcc8ab6ccff49d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AthenaWorkgroup",
    "AthenaWorkgroupConfig",
    "AthenaWorkgroupConfiguration",
    "AthenaWorkgroupConfigurationCustomerContentEncryptionConfiguration",
    "AthenaWorkgroupConfigurationCustomerContentEncryptionConfigurationOutputReference",
    "AthenaWorkgroupConfigurationEngineVersion",
    "AthenaWorkgroupConfigurationEngineVersionOutputReference",
    "AthenaWorkgroupConfigurationIdentityCenterConfiguration",
    "AthenaWorkgroupConfigurationIdentityCenterConfigurationOutputReference",
    "AthenaWorkgroupConfigurationManagedQueryResultsConfiguration",
    "AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfiguration",
    "AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfigurationOutputReference",
    "AthenaWorkgroupConfigurationManagedQueryResultsConfigurationOutputReference",
    "AthenaWorkgroupConfigurationMonitoringConfiguration",
    "AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfiguration",
    "AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType",
    "AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogTypeList",
    "AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogTypeOutputReference",
    "AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationOutputReference",
    "AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfiguration",
    "AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfigurationOutputReference",
    "AthenaWorkgroupConfigurationMonitoringConfigurationOutputReference",
    "AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfiguration",
    "AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfigurationOutputReference",
    "AthenaWorkgroupConfigurationOutputReference",
    "AthenaWorkgroupConfigurationResultConfiguration",
    "AthenaWorkgroupConfigurationResultConfigurationAclConfiguration",
    "AthenaWorkgroupConfigurationResultConfigurationAclConfigurationOutputReference",
    "AthenaWorkgroupConfigurationResultConfigurationEncryptionConfiguration",
    "AthenaWorkgroupConfigurationResultConfigurationEncryptionConfigurationOutputReference",
    "AthenaWorkgroupConfigurationResultConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__e6fd9fbc14cfb419ecd6e370e9de9d09953b07c33eb453c6ee34a3c2169564d9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    configuration: typing.Optional[typing.Union[AthenaWorkgroupConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__8bfc43ae045ec1fd9f4ab41865f327f8f23cf2f8de702cd638dc97fb754ed065(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ebbffd53d6029eb35bac34fff9f95328d90102c78f5bf014c9a69e6eb1767a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18750dc44847f8c781b522c9a6620f9f7cfdc3667a3b78488210d1435af50b72(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c305a333762bdea2f687abc46d594c8ce02fe7460bf71527818a2d1e935d457b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673c3cb024fb60698db1e844675a44488b9ff7c1c7a396f7ff3a5de2c881febd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d8c3b0ff542015c9ea203c0223641d388d17a1dc292e9f00d60bb2902ffb82f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed7d12fe0aca6ca57f2ac5a0fb1f13a7dd91bfdb198e4fd4c73604d5fd87b2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1630cf22145007decdcbf132372bc25abd83f899113564bf9a6d6dcfb26ef325(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be3fdedb1fffc9f7242abcc7ae07dcf1a71205b6a47a20286ff1054d998126ac(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a957d32df481f630a6d31807b2895ac26d6643f2db179efce26c6875625b6909(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    configuration: typing.Optional[typing.Union[AthenaWorkgroupConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    force_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fbdff6ebdc5e12441e70c618b13652eab9d337558f59672be65135ceae03ecc(
    *,
    bytes_scanned_cutoff_per_query: typing.Optional[jsii.Number] = None,
    customer_content_encryption_configuration: typing.Optional[typing.Union[AthenaWorkgroupConfigurationCustomerContentEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_minimum_encryption_configuration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enforce_workgroup_configuration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    engine_version: typing.Optional[typing.Union[AthenaWorkgroupConfigurationEngineVersion, typing.Dict[builtins.str, typing.Any]]] = None,
    execution_role: typing.Optional[builtins.str] = None,
    identity_center_configuration: typing.Optional[typing.Union[AthenaWorkgroupConfigurationIdentityCenterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_query_results_configuration: typing.Optional[typing.Union[AthenaWorkgroupConfigurationManagedQueryResultsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    monitoring_configuration: typing.Optional[typing.Union[AthenaWorkgroupConfigurationMonitoringConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    publish_cloudwatch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    requester_pays_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    result_configuration: typing.Optional[typing.Union[AthenaWorkgroupConfigurationResultConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff80ce886896191ba1f492f6f63860b3cf28a58b33171312a2764fdde12ea540(
    *,
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b028367acfa8585d8191567da0d2b06eda396ee4623f9868703db11fb4704816(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07e7b1666b3a8af224de021d11d5f18ca9f3b2e1dec4f025bdd3480d277d77b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__968192a62f329575b3414357f7b4b47d642b2cff55af28c91866616d92cca1a8(
    value: typing.Optional[AthenaWorkgroupConfigurationCustomerContentEncryptionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58849dfbeaac619d23e36850ecd7672963be82a6b0e9f01f3ed4080d8e9ad7d(
    *,
    selected_engine_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c408e7c9b0724c3b0e510dbdd563ec08b65c5dcb7d1d8b02e9cfda57322cfd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9b6d2f546821478ebfd69cea553ecbe806e969869050665d3e1adaccfcf0a49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da72a36ace1008b9565c6ff1d9eaa0122d65b4df7573460e0513b65d715432a2(
    value: typing.Optional[AthenaWorkgroupConfigurationEngineVersion],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad68224f9a0a30f41d3d6212e38717cbb0ed0b739cef5861c5ce1e77d776be64(
    *,
    enable_identity_center: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    identity_center_instance_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c2b9c1148ac7c42a838e5c3847a2c5f9cd06cb3fee69308842e51a2aa143ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__752f9788b52409e5029c2cb2fa586d07a511566e53eaea7fa298a5088c05ec18(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b66a79148b77d0f2fb5a4c67d9faa65a4c26dd471631d15c0fd25f04f4a89e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d9ed039836495e60c99f6dfd5efe93b791086f14c8cdbbd794f9f4d56c9fe5d(
    value: typing.Optional[AthenaWorkgroupConfigurationIdentityCenterConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c762f86fc7d8f742e9a4aa9385de50498d198a9c039a670b11a001ba7035aa7e(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_configuration: typing.Optional[typing.Union[AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce65eb1d36cbee34385639bfcbd8c1f4a9d51af9e92b452dfa0b038149a830e(
    *,
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc4145e7d3c99b6eda2045b2b2ae0683406817fb5d1c4bdb3694dfddf6af6864(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba0d14e14fa9dfcf6048d4549ee1df50bfe31412f0cf62d721713bf05e305e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad59695abb918cc19eccee687a2bf3545de4afbae08c2f80c6f13f00529c7de(
    value: typing.Optional[AthenaWorkgroupConfigurationManagedQueryResultsConfigurationEncryptionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a83f2ac753854a3d5fe7661cfeb4dd08cfd4786ede44aca7b45929feaf242f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b375985fe3464a1def958465bc128a8bd14a526f7b4a3f1d2278664bc4d7b06(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b762f6f65a37905c91af164a078b1f536c853a6ca652cf6dfdd479618002754f(
    value: typing.Optional[AthenaWorkgroupConfigurationManagedQueryResultsConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__900616b55c436bed4efb983bce0bbd5bf9c3fa75d9f32a6aacd2cc5a19981c2f(
    *,
    cloud_watch_logging_configuration: typing.Optional[typing.Union[AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    managed_logging_configuration: typing.Optional[typing.Union[AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_logging_configuration: typing.Optional[typing.Union[AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c437e488793a8b33c583bba02f569c089e0d599909e1e4e55cd14bc3806511fc(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    log_group: typing.Optional[builtins.str] = None,
    log_stream_name_prefix: typing.Optional[builtins.str] = None,
    log_type: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1402e2fd32678623c88a7c1e9de8e9c72c172a20506fd574aae6c7a38c86ec9e(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd5a26e0e7f6a7c6cd0c078aed433d142cbedcaae988c74ac0cfeaee41e2a92a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21127fa95144a95868eb70555e744f9fc17c747e991e0f81141c52c7a636fe6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f15d567b86792181263c7e0caa12daef49b178f997b2f068516845d62b3bb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b9881f6d321878743c32626aaa0eae988bb3918fcf6cbd8fc902ffae92a310f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc36c2c65d2272a55f47e2bab7a63b7182813b7c98be5f54d482720451c3884(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e386405196c1af8ccc04b388ae870134e00626a2397418c1ce40c76db43b05(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__053e0a7c54384b4492e3afdac2a52a2598afa6691e97376bbd6181a3bfc187ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010be9514e1a56b783d7f38af5a5ce5cb2c9d8de21e9fdb285ed3c504b92d493(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1b20de825ef17d22017b4cb84f098d936889855848ecd0295886002477062b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e279c398db12f2639a05291a66c9674e9f2d017ae2ee30f1444bffabad9990(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc35a0b2b391f67c10ccf398478e2a21616e41a5a9b0131ff009050520ee3a59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df527fba0b08f084ca4b38cbe3a53300357b82aabe47f491368f3d89e00899b8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfigurationLogType, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5bf7ff6eab484e68d2c6772e2e93dbbaaa620c81a7fcfe05e63a4b4c6faeb2d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__942edc79a5075d8b5f5ef6eae424fdc989766b786b04002232adea26690a2dc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6f8a755385b0777b17ca7ec1c1d964a5cddf96239a1b3789851c4d4e1a9255(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1142e0c3c43b19b762e51cb34d248cc4b585b8b643eee2587d561893a8a31638(
    value: typing.Optional[AthenaWorkgroupConfigurationMonitoringConfigurationCloudWatchLoggingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30cfb4c6a5c4f190f5772bc078743036a8c0a304633fed06fd332585f41ed3dd(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28040c942501f1af4bd8f079279999e8bc55464631b07a5cf51c4d55800757fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10da0b3e94714e4595f7b1eb1a29d7a898631d16c433cd4a1bfa47f77ec96f16(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88f14c8749944c7b5b2ce6bd668eab2764967e11b2f381a215b7c889c4d09ed0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c92ed12560db06f66d1a29465be7973107316d6d1548083c2a014cee01bb1ca(
    value: typing.Optional[AthenaWorkgroupConfigurationMonitoringConfigurationManagedLoggingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__743742a8ee4c985b7323388a5be13df49a6073a2a727e559a73e981f1bfcf773(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b24713bcae66df1966b1a19b8cec21cc7ff79788d0db3e3343ccdb37ca55db93(
    value: typing.Optional[AthenaWorkgroupConfigurationMonitoringConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cf93aff8c9c7fa572e0e3b85a2d9f91109df4ba25195da146534ed710cdf568(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    kms_key: typing.Optional[builtins.str] = None,
    log_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b019265d3dc5eb7a59fd9a12aa3efdf7ee0b6753bc3809be9b0cf628dae4c60a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42d49b7179fca3574d3349d49f64556657d67f62322e6c3c722fe24fce483cdc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a763a694335acbfd6bd5d1d628d16c643de194716088c231e309c5eb75e9926(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebffb4b054e807b1f425b28b48c870b6c68d0b0ec8c7ce441e761aa60a70f35a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39aff74bb8f34dc4a9bc3b998becb1176fcdee56667283754cc8494e86989b6(
    value: typing.Optional[AthenaWorkgroupConfigurationMonitoringConfigurationS3LoggingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f49dea61e9e4a75f43296b0594116add80daa058acd310447c00f19aee714414(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daa4abeb41e8c02434879be524796c5fa7113d72591b5ef46631502d23aeb9cd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0cc65a5e9ffc6a3aa0013d41dc8c69ff8562d311666232cc1523805acd67a5d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__535d998f91102efffc42d1b7d1e81cae1df82bf958deef76c00c9d3a6aed8bcf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a3eda39211d786c6f8777f4934eb06419efdf73c3ed7adb4ba640251d62608b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b5ae27e152e14b32219d276047103743bb3439bfa0323c6c18d67499b4812af(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05699ccf75eb5cb8782f745b0f38bb052f6297f6ff267f81db1fd858ff27dcd5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c38b3d08babafdf1e0be01664122660c98f14276a850f6300544973a903a143(
    value: typing.Optional[AthenaWorkgroupConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3492de4d5df5964ee6e0a2051af610e6d9ec3f537c4239c891911caa7718aeef(
    *,
    acl_configuration: typing.Optional[typing.Union[AthenaWorkgroupConfigurationResultConfigurationAclConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    encryption_configuration: typing.Optional[typing.Union[AthenaWorkgroupConfigurationResultConfigurationEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    expected_bucket_owner: typing.Optional[builtins.str] = None,
    output_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0814ccacc0f924260c4e0059dd9e57ff3beddc1c66cda05ff83664f2061b5e6(
    *,
    s3_acl_option: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df5def788f07855531f3313adc5c02a57470f3b51ec66cd56f9cd59021e1c09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce3d677801de733f9dfa18b6a1334f8429cdc170ef2aee6ea64a4474138236e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01e9266a1923ee489b5d60dc742e0356d4290bcedf665e2a4431ff35920c5b11(
    value: typing.Optional[AthenaWorkgroupConfigurationResultConfigurationAclConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a71c0e1c544df3ab0072bb98fa7730418db0f87868c1b7ef5d3803373051238(
    *,
    encryption_option: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf3e6ca2fbcb08122eea9e34e99911cbb6559df4f9b5f52c0de10646fe8a374(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76b409518ac4c1222c92d925b7a0071ba7a7a7b9b3639baf1bf7a8170b68574(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ceefa764a522f3c74b0eee33bb9a2d349517e512a4ba95bf3f4d30eccf65d03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d96aa62098b40a7a6775e2180eaa7401d9fc3b90544d640cd59f61b14cacce(
    value: typing.Optional[AthenaWorkgroupConfigurationResultConfigurationEncryptionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08e078ff998ed3c8834ebe4f2292028db5bd00a5f039302d833cceb52be83cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e6a0b80c0f51a4a53b7604a302dae8c8afddf32a3b56daa4d44cbd79cc4d6a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35d230167403c5e10061d75eb49fbfa61f52e317e84c425d8b8f3295fbe59127(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8a7a6477f3138dd34e2c25832303314fd532c72b549882adcc8ab6ccff49d4(
    value: typing.Optional[AthenaWorkgroupConfigurationResultConfiguration],
) -> None:
    """Type checking stubs"""
    pass
