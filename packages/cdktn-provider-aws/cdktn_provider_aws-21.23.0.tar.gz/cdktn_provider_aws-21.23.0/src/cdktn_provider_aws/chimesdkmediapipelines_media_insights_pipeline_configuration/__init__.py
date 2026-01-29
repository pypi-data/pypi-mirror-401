r'''
# `aws_chimesdkmediapipelines_media_insights_pipeline_configuration`

Refer to the Terraform Registry for docs: [`aws_chimesdkmediapipelines_media_insights_pipeline_configuration`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration).
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


class ChimesdkmediapipelinesMediaInsightsPipelineConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration aws_chimesdkmediapipelines_media_insights_pipeline_configuration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        elements: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        resource_access_role_arn: builtins.str,
        real_time_alert_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration aws_chimesdkmediapipelines_media_insights_pipeline_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param elements: elements block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#elements ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#elements}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#name}.
        :param resource_access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#resource_access_role_arn ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#resource_access_role_arn}.
        :param real_time_alert_configuration: real_time_alert_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#real_time_alert_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#real_time_alert_configuration}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#region ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#tags ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#tags_all ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#timeouts ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c88a8e89419d3fdb08bbb28715bc9e29ea3bc158479ae5be4e6737ed19ca31f5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationConfig(
            elements=elements,
            name=name,
            resource_access_role_arn=resource_access_role_arn,
            real_time_alert_configuration=real_time_alert_configuration,
            region=region,
            tags=tags,
            tags_all=tags_all,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a ChimesdkmediapipelinesMediaInsightsPipelineConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ChimesdkmediapipelinesMediaInsightsPipelineConfiguration to import.
        :param import_from_id: The id of the existing ChimesdkmediapipelinesMediaInsightsPipelineConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ChimesdkmediapipelinesMediaInsightsPipelineConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__982d5f8a707f2bff552afa7b3cfa3f4ba9c09c9a842f5e2efbbb26a713986876)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putElements")
    def put_elements(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6ae99019e9cc1c7aef67a5763069fd970e7e46c20a16bfb0b97619e47a9fdcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putElements", [value]))

    @jsii.member(jsii_name="putRealTimeAlertConfiguration")
    def put_real_time_alert_configuration(
        self,
        *,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules", typing.Dict[builtins.str, typing.Any]]]],
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rules ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rules}
        :param disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#disabled ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#disabled}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration(
            rules=rules, disabled=disabled
        )

        return typing.cast(None, jsii.invoke(self, "putRealTimeAlertConfiguration", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#create ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#delete ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#update ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#update}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetRealTimeAlertConfiguration")
    def reset_real_time_alert_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRealTimeAlertConfiguration", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="elements")
    def elements(
        self,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsList":
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsList", jsii.get(self, "elements"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="realTimeAlertConfiguration")
    def real_time_alert_configuration(
        self,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationOutputReference":
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationOutputReference", jsii.get(self, "realTimeAlertConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeoutsOutputReference":
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="elementsInput")
    def elements_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements"]]], jsii.get(self, "elementsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="realTimeAlertConfigurationInput")
    def real_time_alert_configuration_input(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration"]:
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration"], jsii.get(self, "realTimeAlertConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceAccessRoleArnInput")
    def resource_access_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceAccessRoleArnInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc3c2206d9887ebf7783e178c47a4c56da80159e11e4c7ce427bc908a48ce9ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69104bef5831e3eeae897f7cd14efe1178443e14dbd04a1f4ebb39c881ba2089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceAccessRoleArn")
    def resource_access_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceAccessRoleArn"))

    @resource_access_role_arn.setter
    def resource_access_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c12458a083d55483da97e6551f20ec36329d823654ab452e46ab6be1a98fae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceAccessRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b44e9b46c1c48bb67dce8422362d6b71151acc745f75390aec934371923c4af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5533a2b646e6d1f5df4e277e5306e7c0f8aaaea3223d9f5037899820a7e1d486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "elements": "elements",
        "name": "name",
        "resource_access_role_arn": "resourceAccessRoleArn",
        "real_time_alert_configuration": "realTimeAlertConfiguration",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
    },
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        elements: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        resource_access_role_arn: builtins.str,
        real_time_alert_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param elements: elements block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#elements ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#elements}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#name}.
        :param resource_access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#resource_access_role_arn ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#resource_access_role_arn}.
        :param real_time_alert_configuration: real_time_alert_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#real_time_alert_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#real_time_alert_configuration}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#region ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#tags ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#tags_all ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#timeouts ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(real_time_alert_configuration, dict):
            real_time_alert_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration(**real_time_alert_configuration)
        if isinstance(timeouts, dict):
            timeouts = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ef64faccc404724f25b42e33c4aa968fb92c70c4baa8a9a22f9212fd4868e40)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument elements", value=elements, expected_type=type_hints["elements"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_access_role_arn", value=resource_access_role_arn, expected_type=type_hints["resource_access_role_arn"])
            check_type(argname="argument real_time_alert_configuration", value=real_time_alert_configuration, expected_type=type_hints["real_time_alert_configuration"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "elements": elements,
            "name": name,
            "resource_access_role_arn": resource_access_role_arn,
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
        if real_time_alert_configuration is not None:
            self._values["real_time_alert_configuration"] = real_time_alert_configuration
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
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
    def elements(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements"]]:
        '''elements block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#elements ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#elements}
        '''
        result = self._values.get("elements")
        assert result is not None, "Required property 'elements' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_access_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#resource_access_role_arn ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#resource_access_role_arn}.'''
        result = self._values.get("resource_access_role_arn")
        assert result is not None, "Required property 'resource_access_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def real_time_alert_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration"]:
        '''real_time_alert_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#real_time_alert_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#real_time_alert_configuration}
        '''
        result = self._values.get("real_time_alert_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#region ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#tags ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#tags_all ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#timeouts ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "amazon_transcribe_call_analytics_processor_configuration": "amazonTranscribeCallAnalyticsProcessorConfiguration",
        "amazon_transcribe_processor_configuration": "amazonTranscribeProcessorConfiguration",
        "kinesis_data_stream_sink_configuration": "kinesisDataStreamSinkConfiguration",
        "lambda_function_sink_configuration": "lambdaFunctionSinkConfiguration",
        "s3_recording_sink_configuration": "s3RecordingSinkConfiguration",
        "sns_topic_sink_configuration": "snsTopicSinkConfiguration",
        "sqs_queue_sink_configuration": "sqsQueueSinkConfiguration",
        "voice_analytics_processor_configuration": "voiceAnalyticsProcessorConfiguration",
    },
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements:
    def __init__(
        self,
        *,
        type: builtins.str,
        amazon_transcribe_call_analytics_processor_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        amazon_transcribe_processor_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_data_stream_sink_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_function_sink_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_recording_sink_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        sns_topic_sink_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        sqs_queue_sink_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        voice_analytics_processor_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#type}.
        :param amazon_transcribe_call_analytics_processor_configuration: amazon_transcribe_call_analytics_processor_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#amazon_transcribe_call_analytics_processor_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#amazon_transcribe_call_analytics_processor_configuration}
        :param amazon_transcribe_processor_configuration: amazon_transcribe_processor_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#amazon_transcribe_processor_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#amazon_transcribe_processor_configuration}
        :param kinesis_data_stream_sink_configuration: kinesis_data_stream_sink_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#kinesis_data_stream_sink_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#kinesis_data_stream_sink_configuration}
        :param lambda_function_sink_configuration: lambda_function_sink_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#lambda_function_sink_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#lambda_function_sink_configuration}
        :param s3_recording_sink_configuration: s3_recording_sink_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#s3_recording_sink_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#s3_recording_sink_configuration}
        :param sns_topic_sink_configuration: sns_topic_sink_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#sns_topic_sink_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#sns_topic_sink_configuration}
        :param sqs_queue_sink_configuration: sqs_queue_sink_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#sqs_queue_sink_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#sqs_queue_sink_configuration}
        :param voice_analytics_processor_configuration: voice_analytics_processor_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#voice_analytics_processor_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#voice_analytics_processor_configuration}
        '''
        if isinstance(amazon_transcribe_call_analytics_processor_configuration, dict):
            amazon_transcribe_call_analytics_processor_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration(**amazon_transcribe_call_analytics_processor_configuration)
        if isinstance(amazon_transcribe_processor_configuration, dict):
            amazon_transcribe_processor_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration(**amazon_transcribe_processor_configuration)
        if isinstance(kinesis_data_stream_sink_configuration, dict):
            kinesis_data_stream_sink_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration(**kinesis_data_stream_sink_configuration)
        if isinstance(lambda_function_sink_configuration, dict):
            lambda_function_sink_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration(**lambda_function_sink_configuration)
        if isinstance(s3_recording_sink_configuration, dict):
            s3_recording_sink_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration(**s3_recording_sink_configuration)
        if isinstance(sns_topic_sink_configuration, dict):
            sns_topic_sink_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration(**sns_topic_sink_configuration)
        if isinstance(sqs_queue_sink_configuration, dict):
            sqs_queue_sink_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration(**sqs_queue_sink_configuration)
        if isinstance(voice_analytics_processor_configuration, dict):
            voice_analytics_processor_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration(**voice_analytics_processor_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1a60bdbda06dbe937f00f600d4d1e9b9e758895dcbc610014315035bbc34d83)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument amazon_transcribe_call_analytics_processor_configuration", value=amazon_transcribe_call_analytics_processor_configuration, expected_type=type_hints["amazon_transcribe_call_analytics_processor_configuration"])
            check_type(argname="argument amazon_transcribe_processor_configuration", value=amazon_transcribe_processor_configuration, expected_type=type_hints["amazon_transcribe_processor_configuration"])
            check_type(argname="argument kinesis_data_stream_sink_configuration", value=kinesis_data_stream_sink_configuration, expected_type=type_hints["kinesis_data_stream_sink_configuration"])
            check_type(argname="argument lambda_function_sink_configuration", value=lambda_function_sink_configuration, expected_type=type_hints["lambda_function_sink_configuration"])
            check_type(argname="argument s3_recording_sink_configuration", value=s3_recording_sink_configuration, expected_type=type_hints["s3_recording_sink_configuration"])
            check_type(argname="argument sns_topic_sink_configuration", value=sns_topic_sink_configuration, expected_type=type_hints["sns_topic_sink_configuration"])
            check_type(argname="argument sqs_queue_sink_configuration", value=sqs_queue_sink_configuration, expected_type=type_hints["sqs_queue_sink_configuration"])
            check_type(argname="argument voice_analytics_processor_configuration", value=voice_analytics_processor_configuration, expected_type=type_hints["voice_analytics_processor_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if amazon_transcribe_call_analytics_processor_configuration is not None:
            self._values["amazon_transcribe_call_analytics_processor_configuration"] = amazon_transcribe_call_analytics_processor_configuration
        if amazon_transcribe_processor_configuration is not None:
            self._values["amazon_transcribe_processor_configuration"] = amazon_transcribe_processor_configuration
        if kinesis_data_stream_sink_configuration is not None:
            self._values["kinesis_data_stream_sink_configuration"] = kinesis_data_stream_sink_configuration
        if lambda_function_sink_configuration is not None:
            self._values["lambda_function_sink_configuration"] = lambda_function_sink_configuration
        if s3_recording_sink_configuration is not None:
            self._values["s3_recording_sink_configuration"] = s3_recording_sink_configuration
        if sns_topic_sink_configuration is not None:
            self._values["sns_topic_sink_configuration"] = sns_topic_sink_configuration
        if sqs_queue_sink_configuration is not None:
            self._values["sqs_queue_sink_configuration"] = sqs_queue_sink_configuration
        if voice_analytics_processor_configuration is not None:
            self._values["voice_analytics_processor_configuration"] = voice_analytics_processor_configuration

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def amazon_transcribe_call_analytics_processor_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration"]:
        '''amazon_transcribe_call_analytics_processor_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#amazon_transcribe_call_analytics_processor_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#amazon_transcribe_call_analytics_processor_configuration}
        '''
        result = self._values.get("amazon_transcribe_call_analytics_processor_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration"], result)

    @builtins.property
    def amazon_transcribe_processor_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration"]:
        '''amazon_transcribe_processor_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#amazon_transcribe_processor_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#amazon_transcribe_processor_configuration}
        '''
        result = self._values.get("amazon_transcribe_processor_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration"], result)

    @builtins.property
    def kinesis_data_stream_sink_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration"]:
        '''kinesis_data_stream_sink_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#kinesis_data_stream_sink_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#kinesis_data_stream_sink_configuration}
        '''
        result = self._values.get("kinesis_data_stream_sink_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration"], result)

    @builtins.property
    def lambda_function_sink_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration"]:
        '''lambda_function_sink_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#lambda_function_sink_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#lambda_function_sink_configuration}
        '''
        result = self._values.get("lambda_function_sink_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration"], result)

    @builtins.property
    def s3_recording_sink_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration"]:
        '''s3_recording_sink_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#s3_recording_sink_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#s3_recording_sink_configuration}
        '''
        result = self._values.get("s3_recording_sink_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration"], result)

    @builtins.property
    def sns_topic_sink_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration"]:
        '''sns_topic_sink_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#sns_topic_sink_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#sns_topic_sink_configuration}
        '''
        result = self._values.get("sns_topic_sink_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration"], result)

    @builtins.property
    def sqs_queue_sink_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration"]:
        '''sqs_queue_sink_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#sqs_queue_sink_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#sqs_queue_sink_configuration}
        '''
        result = self._values.get("sqs_queue_sink_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration"], result)

    @builtins.property
    def voice_analytics_processor_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration"]:
        '''voice_analytics_processor_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#voice_analytics_processor_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#voice_analytics_processor_configuration}
        '''
        result = self._values.get("voice_analytics_processor_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "language_code": "languageCode",
        "call_analytics_stream_categories": "callAnalyticsStreamCategories",
        "content_identification_type": "contentIdentificationType",
        "content_redaction_type": "contentRedactionType",
        "enable_partial_results_stabilization": "enablePartialResultsStabilization",
        "filter_partial_results": "filterPartialResults",
        "language_model_name": "languageModelName",
        "partial_results_stability": "partialResultsStability",
        "pii_entity_types": "piiEntityTypes",
        "post_call_analytics_settings": "postCallAnalyticsSettings",
        "vocabulary_filter_method": "vocabularyFilterMethod",
        "vocabulary_filter_name": "vocabularyFilterName",
        "vocabulary_name": "vocabularyName",
    },
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration:
    def __init__(
        self,
        *,
        language_code: builtins.str,
        call_analytics_stream_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        content_identification_type: typing.Optional[builtins.str] = None,
        content_redaction_type: typing.Optional[builtins.str] = None,
        enable_partial_results_stabilization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filter_partial_results: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        language_model_name: typing.Optional[builtins.str] = None,
        partial_results_stability: typing.Optional[builtins.str] = None,
        pii_entity_types: typing.Optional[builtins.str] = None,
        post_call_analytics_settings: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        vocabulary_filter_method: typing.Optional[builtins.str] = None,
        vocabulary_filter_name: typing.Optional[builtins.str] = None,
        vocabulary_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param language_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_code ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_code}.
        :param call_analytics_stream_categories: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#call_analytics_stream_categories ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#call_analytics_stream_categories}.
        :param content_identification_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_identification_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_identification_type}.
        :param content_redaction_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_redaction_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_redaction_type}.
        :param enable_partial_results_stabilization: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#enable_partial_results_stabilization ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#enable_partial_results_stabilization}.
        :param filter_partial_results: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#filter_partial_results ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#filter_partial_results}.
        :param language_model_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_model_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_model_name}.
        :param partial_results_stability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#partial_results_stability ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#partial_results_stability}.
        :param pii_entity_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#pii_entity_types ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#pii_entity_types}.
        :param post_call_analytics_settings: post_call_analytics_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#post_call_analytics_settings ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#post_call_analytics_settings}
        :param vocabulary_filter_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_method ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_method}.
        :param vocabulary_filter_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_name}.
        :param vocabulary_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_name}.
        '''
        if isinstance(post_call_analytics_settings, dict):
            post_call_analytics_settings = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings(**post_call_analytics_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d207b87f5daa59c74728636a3f4ffe948ba3bb9c5b9b0b1fc399f78fbdbc138c)
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            check_type(argname="argument call_analytics_stream_categories", value=call_analytics_stream_categories, expected_type=type_hints["call_analytics_stream_categories"])
            check_type(argname="argument content_identification_type", value=content_identification_type, expected_type=type_hints["content_identification_type"])
            check_type(argname="argument content_redaction_type", value=content_redaction_type, expected_type=type_hints["content_redaction_type"])
            check_type(argname="argument enable_partial_results_stabilization", value=enable_partial_results_stabilization, expected_type=type_hints["enable_partial_results_stabilization"])
            check_type(argname="argument filter_partial_results", value=filter_partial_results, expected_type=type_hints["filter_partial_results"])
            check_type(argname="argument language_model_name", value=language_model_name, expected_type=type_hints["language_model_name"])
            check_type(argname="argument partial_results_stability", value=partial_results_stability, expected_type=type_hints["partial_results_stability"])
            check_type(argname="argument pii_entity_types", value=pii_entity_types, expected_type=type_hints["pii_entity_types"])
            check_type(argname="argument post_call_analytics_settings", value=post_call_analytics_settings, expected_type=type_hints["post_call_analytics_settings"])
            check_type(argname="argument vocabulary_filter_method", value=vocabulary_filter_method, expected_type=type_hints["vocabulary_filter_method"])
            check_type(argname="argument vocabulary_filter_name", value=vocabulary_filter_name, expected_type=type_hints["vocabulary_filter_name"])
            check_type(argname="argument vocabulary_name", value=vocabulary_name, expected_type=type_hints["vocabulary_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "language_code": language_code,
        }
        if call_analytics_stream_categories is not None:
            self._values["call_analytics_stream_categories"] = call_analytics_stream_categories
        if content_identification_type is not None:
            self._values["content_identification_type"] = content_identification_type
        if content_redaction_type is not None:
            self._values["content_redaction_type"] = content_redaction_type
        if enable_partial_results_stabilization is not None:
            self._values["enable_partial_results_stabilization"] = enable_partial_results_stabilization
        if filter_partial_results is not None:
            self._values["filter_partial_results"] = filter_partial_results
        if language_model_name is not None:
            self._values["language_model_name"] = language_model_name
        if partial_results_stability is not None:
            self._values["partial_results_stability"] = partial_results_stability
        if pii_entity_types is not None:
            self._values["pii_entity_types"] = pii_entity_types
        if post_call_analytics_settings is not None:
            self._values["post_call_analytics_settings"] = post_call_analytics_settings
        if vocabulary_filter_method is not None:
            self._values["vocabulary_filter_method"] = vocabulary_filter_method
        if vocabulary_filter_name is not None:
            self._values["vocabulary_filter_name"] = vocabulary_filter_name
        if vocabulary_name is not None:
            self._values["vocabulary_name"] = vocabulary_name

    @builtins.property
    def language_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_code ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_code}.'''
        result = self._values.get("language_code")
        assert result is not None, "Required property 'language_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def call_analytics_stream_categories(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#call_analytics_stream_categories ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#call_analytics_stream_categories}.'''
        result = self._values.get("call_analytics_stream_categories")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def content_identification_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_identification_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_identification_type}.'''
        result = self._values.get("content_identification_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_redaction_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_redaction_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_redaction_type}.'''
        result = self._values.get("content_redaction_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_partial_results_stabilization(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#enable_partial_results_stabilization ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#enable_partial_results_stabilization}.'''
        result = self._values.get("enable_partial_results_stabilization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def filter_partial_results(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#filter_partial_results ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#filter_partial_results}.'''
        result = self._values.get("filter_partial_results")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def language_model_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_model_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_model_name}.'''
        result = self._values.get("language_model_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partial_results_stability(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#partial_results_stability ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#partial_results_stability}.'''
        result = self._values.get("partial_results_stability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pii_entity_types(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#pii_entity_types ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#pii_entity_types}.'''
        result = self._values.get("pii_entity_types")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_call_analytics_settings(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings"]:
        '''post_call_analytics_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#post_call_analytics_settings ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#post_call_analytics_settings}
        '''
        result = self._values.get("post_call_analytics_settings")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings"], result)

    @builtins.property
    def vocabulary_filter_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_method ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_method}.'''
        result = self._values.get("vocabulary_filter_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vocabulary_filter_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_name}.'''
        result = self._values.get("vocabulary_filter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vocabulary_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_name}.'''
        result = self._values.get("vocabulary_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d59a3d25e3b9416d473ca1f98f81cbcae8f069e25d60c03b88a15750f072c42)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPostCallAnalyticsSettings")
    def put_post_call_analytics_settings(
        self,
        *,
        data_access_role_arn: builtins.str,
        output_location: builtins.str,
        content_redaction_output: typing.Optional[builtins.str] = None,
        output_encryption_kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#data_access_role_arn ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#data_access_role_arn}.
        :param output_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#output_location ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#output_location}.
        :param content_redaction_output: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_redaction_output ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_redaction_output}.
        :param output_encryption_kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#output_encryption_kms_key_id ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#output_encryption_kms_key_id}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings(
            data_access_role_arn=data_access_role_arn,
            output_location=output_location,
            content_redaction_output=content_redaction_output,
            output_encryption_kms_key_id=output_encryption_kms_key_id,
        )

        return typing.cast(None, jsii.invoke(self, "putPostCallAnalyticsSettings", [value]))

    @jsii.member(jsii_name="resetCallAnalyticsStreamCategories")
    def reset_call_analytics_stream_categories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCallAnalyticsStreamCategories", []))

    @jsii.member(jsii_name="resetContentIdentificationType")
    def reset_content_identification_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentIdentificationType", []))

    @jsii.member(jsii_name="resetContentRedactionType")
    def reset_content_redaction_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentRedactionType", []))

    @jsii.member(jsii_name="resetEnablePartialResultsStabilization")
    def reset_enable_partial_results_stabilization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablePartialResultsStabilization", []))

    @jsii.member(jsii_name="resetFilterPartialResults")
    def reset_filter_partial_results(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterPartialResults", []))

    @jsii.member(jsii_name="resetLanguageModelName")
    def reset_language_model_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLanguageModelName", []))

    @jsii.member(jsii_name="resetPartialResultsStability")
    def reset_partial_results_stability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartialResultsStability", []))

    @jsii.member(jsii_name="resetPiiEntityTypes")
    def reset_pii_entity_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPiiEntityTypes", []))

    @jsii.member(jsii_name="resetPostCallAnalyticsSettings")
    def reset_post_call_analytics_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostCallAnalyticsSettings", []))

    @jsii.member(jsii_name="resetVocabularyFilterMethod")
    def reset_vocabulary_filter_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVocabularyFilterMethod", []))

    @jsii.member(jsii_name="resetVocabularyFilterName")
    def reset_vocabulary_filter_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVocabularyFilterName", []))

    @jsii.member(jsii_name="resetVocabularyName")
    def reset_vocabulary_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVocabularyName", []))

    @builtins.property
    @jsii.member(jsii_name="postCallAnalyticsSettings")
    def post_call_analytics_settings(
        self,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettingsOutputReference":
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettingsOutputReference", jsii.get(self, "postCallAnalyticsSettings"))

    @builtins.property
    @jsii.member(jsii_name="callAnalyticsStreamCategoriesInput")
    def call_analytics_stream_categories_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "callAnalyticsStreamCategoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="contentIdentificationTypeInput")
    def content_identification_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentIdentificationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="contentRedactionTypeInput")
    def content_redaction_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentRedactionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePartialResultsStabilizationInput")
    def enable_partial_results_stabilization_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePartialResultsStabilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="filterPartialResultsInput")
    def filter_partial_results_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "filterPartialResultsInput"))

    @builtins.property
    @jsii.member(jsii_name="languageCodeInput")
    def language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="languageModelNameInput")
    def language_model_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageModelNameInput"))

    @builtins.property
    @jsii.member(jsii_name="partialResultsStabilityInput")
    def partial_results_stability_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partialResultsStabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="piiEntityTypesInput")
    def pii_entity_types_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "piiEntityTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="postCallAnalyticsSettingsInput")
    def post_call_analytics_settings_input(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings"]:
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings"], jsii.get(self, "postCallAnalyticsSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="vocabularyFilterMethodInput")
    def vocabulary_filter_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vocabularyFilterMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="vocabularyFilterNameInput")
    def vocabulary_filter_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vocabularyFilterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="vocabularyNameInput")
    def vocabulary_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vocabularyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="callAnalyticsStreamCategories")
    def call_analytics_stream_categories(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "callAnalyticsStreamCategories"))

    @call_analytics_stream_categories.setter
    def call_analytics_stream_categories(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37040717169f7a79945e895d16763d1020b249906e6a11393ba927ef4ab8468a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "callAnalyticsStreamCategories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentIdentificationType")
    def content_identification_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentIdentificationType"))

    @content_identification_type.setter
    def content_identification_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89bcf7d63c33351e79107f58b459c90b3f65ee533d383166f6f8d88c3d0ff0a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentIdentificationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentRedactionType")
    def content_redaction_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentRedactionType"))

    @content_redaction_type.setter
    def content_redaction_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c49a59a67d1405eb5895e84fb048c067c35ef449058c2ddab484fc51f4c0f25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentRedactionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enablePartialResultsStabilization")
    def enable_partial_results_stabilization(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePartialResultsStabilization"))

    @enable_partial_results_stabilization.setter
    def enable_partial_results_stabilization(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e49851a3196b05a8a79d36442519e11386155abd69c284df8a7f0d8f960a7f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePartialResultsStabilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterPartialResults")
    def filter_partial_results(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "filterPartialResults"))

    @filter_partial_results.setter
    def filter_partial_results(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e720432cf1d4e2a163f56f400a11ab33a3b39a5666742ff34ab8b60b34996248)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterPartialResults", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e90379c8f7073123bbc59fc9e383c96e097a9030ea50dd18bb035db9e8861b2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageModelName")
    def language_model_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageModelName"))

    @language_model_name.setter
    def language_model_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cbb1d6903ab0cd7a16573794c1d97b55cb79eceda5c488074d8ea73e9204c46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageModelName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partialResultsStability")
    def partial_results_stability(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partialResultsStability"))

    @partial_results_stability.setter
    def partial_results_stability(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9786a3e39cdbabba543954457d96de6f9a5f6e91e143a438c24a9d0453ba333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partialResultsStability", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="piiEntityTypes")
    def pii_entity_types(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "piiEntityTypes"))

    @pii_entity_types.setter
    def pii_entity_types(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc7ec64d8cd482f4f379adf6df08ba321c1a603f0b41ea5c3fa313bc3ede2293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "piiEntityTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vocabularyFilterMethod")
    def vocabulary_filter_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vocabularyFilterMethod"))

    @vocabulary_filter_method.setter
    def vocabulary_filter_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51b58abbb6ad89bce23b564748798b8374c740f593b06c25b6443c7c7d4327e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vocabularyFilterMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vocabularyFilterName")
    def vocabulary_filter_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vocabularyFilterName"))

    @vocabulary_filter_name.setter
    def vocabulary_filter_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08b0c53c623c98eae002b4a52fdf5d3fd27342f25e823b61f63b89a2cf755346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vocabularyFilterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vocabularyName")
    def vocabulary_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vocabularyName"))

    @vocabulary_name.setter
    def vocabulary_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba18c5b6422fc3771c67d774f296871ed7d686fdc695341f12bac9bd4a5eecc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vocabularyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__299f1de7e187b2f8bbc8f5d6540675b83f7733d46e8f835e9b281ca2f91a69c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings",
    jsii_struct_bases=[],
    name_mapping={
        "data_access_role_arn": "dataAccessRoleArn",
        "output_location": "outputLocation",
        "content_redaction_output": "contentRedactionOutput",
        "output_encryption_kms_key_id": "outputEncryptionKmsKeyId",
    },
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings:
    def __init__(
        self,
        *,
        data_access_role_arn: builtins.str,
        output_location: builtins.str,
        content_redaction_output: typing.Optional[builtins.str] = None,
        output_encryption_kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_access_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#data_access_role_arn ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#data_access_role_arn}.
        :param output_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#output_location ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#output_location}.
        :param content_redaction_output: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_redaction_output ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_redaction_output}.
        :param output_encryption_kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#output_encryption_kms_key_id ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#output_encryption_kms_key_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1265805d5c09354c9371718ba7ccd4376c30d100869019d92f9fac18e3f86ee1)
            check_type(argname="argument data_access_role_arn", value=data_access_role_arn, expected_type=type_hints["data_access_role_arn"])
            check_type(argname="argument output_location", value=output_location, expected_type=type_hints["output_location"])
            check_type(argname="argument content_redaction_output", value=content_redaction_output, expected_type=type_hints["content_redaction_output"])
            check_type(argname="argument output_encryption_kms_key_id", value=output_encryption_kms_key_id, expected_type=type_hints["output_encryption_kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_access_role_arn": data_access_role_arn,
            "output_location": output_location,
        }
        if content_redaction_output is not None:
            self._values["content_redaction_output"] = content_redaction_output
        if output_encryption_kms_key_id is not None:
            self._values["output_encryption_kms_key_id"] = output_encryption_kms_key_id

    @builtins.property
    def data_access_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#data_access_role_arn ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#data_access_role_arn}.'''
        result = self._values.get("data_access_role_arn")
        assert result is not None, "Required property 'data_access_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def output_location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#output_location ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#output_location}.'''
        result = self._values.get("output_location")
        assert result is not None, "Required property 'output_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_redaction_output(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_redaction_output ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_redaction_output}.'''
        result = self._values.get("content_redaction_output")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_encryption_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#output_encryption_kms_key_id ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#output_encryption_kms_key_id}.'''
        result = self._values.get("output_encryption_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc3a391aed0cad8381f400ff67ddd8aff05a2dbc1271ca998ba503c8285393b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContentRedactionOutput")
    def reset_content_redaction_output(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentRedactionOutput", []))

    @jsii.member(jsii_name="resetOutputEncryptionKmsKeyId")
    def reset_output_encryption_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputEncryptionKmsKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="contentRedactionOutputInput")
    def content_redaction_output_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentRedactionOutputInput"))

    @builtins.property
    @jsii.member(jsii_name="dataAccessRoleArnInput")
    def data_access_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataAccessRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="outputEncryptionKmsKeyIdInput")
    def output_encryption_kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputEncryptionKmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="outputLocationInput")
    def output_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="contentRedactionOutput")
    def content_redaction_output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentRedactionOutput"))

    @content_redaction_output.setter
    def content_redaction_output(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd74ecad20c92eabd05e509c7b7be415c757ecdf66414be1c063f3d0e5dacc07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentRedactionOutput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataAccessRoleArn")
    def data_access_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataAccessRoleArn"))

    @data_access_role_arn.setter
    def data_access_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1d54862aeedd03e788402c6a2837a4801890a8daa83e55397844cc1e89ce9ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataAccessRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputEncryptionKmsKeyId")
    def output_encryption_kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputEncryptionKmsKeyId"))

    @output_encryption_kms_key_id.setter
    def output_encryption_kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__210f1091ebb9bba86ac3efe0a15a84f471377e1bdc83039b3d3ed3f6f88b62c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputEncryptionKmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputLocation")
    def output_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputLocation"))

    @output_location.setter
    def output_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3555a10ff34442c237ba9d8a862a598117da6dd80d162a5edb238967bd87d2d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baa947982d055498b38b6fff7eccbd560405cdf1fcca430b172b15489a9cc836)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "language_code": "languageCode",
        "content_identification_type": "contentIdentificationType",
        "content_redaction_type": "contentRedactionType",
        "enable_partial_results_stabilization": "enablePartialResultsStabilization",
        "filter_partial_results": "filterPartialResults",
        "language_model_name": "languageModelName",
        "partial_results_stability": "partialResultsStability",
        "pii_entity_types": "piiEntityTypes",
        "show_speaker_label": "showSpeakerLabel",
        "vocabulary_filter_method": "vocabularyFilterMethod",
        "vocabulary_filter_name": "vocabularyFilterName",
        "vocabulary_name": "vocabularyName",
    },
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration:
    def __init__(
        self,
        *,
        language_code: builtins.str,
        content_identification_type: typing.Optional[builtins.str] = None,
        content_redaction_type: typing.Optional[builtins.str] = None,
        enable_partial_results_stabilization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filter_partial_results: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        language_model_name: typing.Optional[builtins.str] = None,
        partial_results_stability: typing.Optional[builtins.str] = None,
        pii_entity_types: typing.Optional[builtins.str] = None,
        show_speaker_label: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vocabulary_filter_method: typing.Optional[builtins.str] = None,
        vocabulary_filter_name: typing.Optional[builtins.str] = None,
        vocabulary_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param language_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_code ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_code}.
        :param content_identification_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_identification_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_identification_type}.
        :param content_redaction_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_redaction_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_redaction_type}.
        :param enable_partial_results_stabilization: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#enable_partial_results_stabilization ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#enable_partial_results_stabilization}.
        :param filter_partial_results: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#filter_partial_results ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#filter_partial_results}.
        :param language_model_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_model_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_model_name}.
        :param partial_results_stability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#partial_results_stability ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#partial_results_stability}.
        :param pii_entity_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#pii_entity_types ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#pii_entity_types}.
        :param show_speaker_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#show_speaker_label ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#show_speaker_label}.
        :param vocabulary_filter_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_method ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_method}.
        :param vocabulary_filter_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_name}.
        :param vocabulary_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32390edf6b17672bef4937d42f74a871e623a37d0ea98dc73e9aa60bf3833f84)
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            check_type(argname="argument content_identification_type", value=content_identification_type, expected_type=type_hints["content_identification_type"])
            check_type(argname="argument content_redaction_type", value=content_redaction_type, expected_type=type_hints["content_redaction_type"])
            check_type(argname="argument enable_partial_results_stabilization", value=enable_partial_results_stabilization, expected_type=type_hints["enable_partial_results_stabilization"])
            check_type(argname="argument filter_partial_results", value=filter_partial_results, expected_type=type_hints["filter_partial_results"])
            check_type(argname="argument language_model_name", value=language_model_name, expected_type=type_hints["language_model_name"])
            check_type(argname="argument partial_results_stability", value=partial_results_stability, expected_type=type_hints["partial_results_stability"])
            check_type(argname="argument pii_entity_types", value=pii_entity_types, expected_type=type_hints["pii_entity_types"])
            check_type(argname="argument show_speaker_label", value=show_speaker_label, expected_type=type_hints["show_speaker_label"])
            check_type(argname="argument vocabulary_filter_method", value=vocabulary_filter_method, expected_type=type_hints["vocabulary_filter_method"])
            check_type(argname="argument vocabulary_filter_name", value=vocabulary_filter_name, expected_type=type_hints["vocabulary_filter_name"])
            check_type(argname="argument vocabulary_name", value=vocabulary_name, expected_type=type_hints["vocabulary_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "language_code": language_code,
        }
        if content_identification_type is not None:
            self._values["content_identification_type"] = content_identification_type
        if content_redaction_type is not None:
            self._values["content_redaction_type"] = content_redaction_type
        if enable_partial_results_stabilization is not None:
            self._values["enable_partial_results_stabilization"] = enable_partial_results_stabilization
        if filter_partial_results is not None:
            self._values["filter_partial_results"] = filter_partial_results
        if language_model_name is not None:
            self._values["language_model_name"] = language_model_name
        if partial_results_stability is not None:
            self._values["partial_results_stability"] = partial_results_stability
        if pii_entity_types is not None:
            self._values["pii_entity_types"] = pii_entity_types
        if show_speaker_label is not None:
            self._values["show_speaker_label"] = show_speaker_label
        if vocabulary_filter_method is not None:
            self._values["vocabulary_filter_method"] = vocabulary_filter_method
        if vocabulary_filter_name is not None:
            self._values["vocabulary_filter_name"] = vocabulary_filter_name
        if vocabulary_name is not None:
            self._values["vocabulary_name"] = vocabulary_name

    @builtins.property
    def language_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_code ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_code}.'''
        result = self._values.get("language_code")
        assert result is not None, "Required property 'language_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_identification_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_identification_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_identification_type}.'''
        result = self._values.get("content_identification_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_redaction_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_redaction_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_redaction_type}.'''
        result = self._values.get("content_redaction_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_partial_results_stabilization(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#enable_partial_results_stabilization ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#enable_partial_results_stabilization}.'''
        result = self._values.get("enable_partial_results_stabilization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def filter_partial_results(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#filter_partial_results ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#filter_partial_results}.'''
        result = self._values.get("filter_partial_results")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def language_model_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_model_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_model_name}.'''
        result = self._values.get("language_model_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partial_results_stability(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#partial_results_stability ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#partial_results_stability}.'''
        result = self._values.get("partial_results_stability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pii_entity_types(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#pii_entity_types ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#pii_entity_types}.'''
        result = self._values.get("pii_entity_types")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def show_speaker_label(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#show_speaker_label ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#show_speaker_label}.'''
        result = self._values.get("show_speaker_label")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vocabulary_filter_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_method ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_method}.'''
        result = self._values.get("vocabulary_filter_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vocabulary_filter_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_name}.'''
        result = self._values.get("vocabulary_filter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vocabulary_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_name}.'''
        result = self._values.get("vocabulary_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e81fab263e43334cad722dfb0c1e2d78b9180f2bf45467533318bc6c18720e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContentIdentificationType")
    def reset_content_identification_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentIdentificationType", []))

    @jsii.member(jsii_name="resetContentRedactionType")
    def reset_content_redaction_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentRedactionType", []))

    @jsii.member(jsii_name="resetEnablePartialResultsStabilization")
    def reset_enable_partial_results_stabilization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablePartialResultsStabilization", []))

    @jsii.member(jsii_name="resetFilterPartialResults")
    def reset_filter_partial_results(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterPartialResults", []))

    @jsii.member(jsii_name="resetLanguageModelName")
    def reset_language_model_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLanguageModelName", []))

    @jsii.member(jsii_name="resetPartialResultsStability")
    def reset_partial_results_stability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartialResultsStability", []))

    @jsii.member(jsii_name="resetPiiEntityTypes")
    def reset_pii_entity_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPiiEntityTypes", []))

    @jsii.member(jsii_name="resetShowSpeakerLabel")
    def reset_show_speaker_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShowSpeakerLabel", []))

    @jsii.member(jsii_name="resetVocabularyFilterMethod")
    def reset_vocabulary_filter_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVocabularyFilterMethod", []))

    @jsii.member(jsii_name="resetVocabularyFilterName")
    def reset_vocabulary_filter_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVocabularyFilterName", []))

    @jsii.member(jsii_name="resetVocabularyName")
    def reset_vocabulary_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVocabularyName", []))

    @builtins.property
    @jsii.member(jsii_name="contentIdentificationTypeInput")
    def content_identification_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentIdentificationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="contentRedactionTypeInput")
    def content_redaction_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentRedactionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePartialResultsStabilizationInput")
    def enable_partial_results_stabilization_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePartialResultsStabilizationInput"))

    @builtins.property
    @jsii.member(jsii_name="filterPartialResultsInput")
    def filter_partial_results_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "filterPartialResultsInput"))

    @builtins.property
    @jsii.member(jsii_name="languageCodeInput")
    def language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="languageModelNameInput")
    def language_model_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageModelNameInput"))

    @builtins.property
    @jsii.member(jsii_name="partialResultsStabilityInput")
    def partial_results_stability_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partialResultsStabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="piiEntityTypesInput")
    def pii_entity_types_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "piiEntityTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="showSpeakerLabelInput")
    def show_speaker_label_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "showSpeakerLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="vocabularyFilterMethodInput")
    def vocabulary_filter_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vocabularyFilterMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="vocabularyFilterNameInput")
    def vocabulary_filter_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vocabularyFilterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="vocabularyNameInput")
    def vocabulary_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vocabularyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="contentIdentificationType")
    def content_identification_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentIdentificationType"))

    @content_identification_type.setter
    def content_identification_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcb5506b7d492179475e3df44d048189da980fb8a4bd5074273545ab6525f6f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentIdentificationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentRedactionType")
    def content_redaction_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentRedactionType"))

    @content_redaction_type.setter
    def content_redaction_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ee97291823384d7b23449d38d1f9535271426c971aa05735bf7fc2dc35bb872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentRedactionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enablePartialResultsStabilization")
    def enable_partial_results_stabilization(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePartialResultsStabilization"))

    @enable_partial_results_stabilization.setter
    def enable_partial_results_stabilization(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08b1becbd0e782542238c745fdfe52bcad5422ab288f3e8f5d116f07526e382b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePartialResultsStabilization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterPartialResults")
    def filter_partial_results(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "filterPartialResults"))

    @filter_partial_results.setter
    def filter_partial_results(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ed5b7d6455140e637b6065d35243e68401b5bb6d95501c1087b37650f9ff196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterPartialResults", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a66a8c53b1885ce13f7b1f818a8e395c9044e3e09723463bd08980184901e2ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageModelName")
    def language_model_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageModelName"))

    @language_model_name.setter
    def language_model_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b6d874b38dc81bcfa68f45e882109f7f6b3d4c990ad316cf01e895daf1e7ce8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageModelName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partialResultsStability")
    def partial_results_stability(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partialResultsStability"))

    @partial_results_stability.setter
    def partial_results_stability(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7606b8afceb0fc0f683a68d9e47570203c38563d5a123e792b9dc24481ecae9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partialResultsStability", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="piiEntityTypes")
    def pii_entity_types(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "piiEntityTypes"))

    @pii_entity_types.setter
    def pii_entity_types(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1678e407d27a2dc57769644ff90e7b3493469228283c9b8f831254722abb94c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "piiEntityTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="showSpeakerLabel")
    def show_speaker_label(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "showSpeakerLabel"))

    @show_speaker_label.setter
    def show_speaker_label(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e258736aa05553acb4c0fb03d652c2c01b866c4fac6fb2ae1e0a85ea634602)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "showSpeakerLabel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vocabularyFilterMethod")
    def vocabulary_filter_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vocabularyFilterMethod"))

    @vocabulary_filter_method.setter
    def vocabulary_filter_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82984e6b98f0d7dde5c78e57a289cf96f35e13379167b017475c227f71a088ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vocabularyFilterMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vocabularyFilterName")
    def vocabulary_filter_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vocabularyFilterName"))

    @vocabulary_filter_name.setter
    def vocabulary_filter_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__686f76f4b82f1d0413456f1ba4987b4be500202f6b8ed569a39f841d5d5c1789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vocabularyFilterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vocabularyName")
    def vocabulary_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vocabularyName"))

    @vocabulary_name.setter
    def vocabulary_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__001617af4039e6b4431784541bbe320c103aff4364973804983fb5ef3e751af1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vocabularyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23a7dc4f61b94c98b999f0bf5f40f45291f17d3f90c99e94a6230a1a7e9712a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"insights_target": "insightsTarget"},
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration:
    def __init__(self, *, insights_target: builtins.str) -> None:
        '''
        :param insights_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__751048f3718a427cc5284c173f6e16017fcde6e298a88c017fb97bbea063ae1a)
            check_type(argname="argument insights_target", value=insights_target, expected_type=type_hints["insights_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "insights_target": insights_target,
        }

    @builtins.property
    def insights_target(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.'''
        result = self._values.get("insights_target")
        assert result is not None, "Required property 'insights_target' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c37acde92649a71adf63e26eb0e1f084c746d8ec2db52941dd9d1b0b37c5c97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="insightsTargetInput")
    def insights_target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insightsTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="insightsTarget")
    def insights_target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "insightsTarget"))

    @insights_target.setter
    def insights_target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eb889c5f5e2a41fc7e373e92a9941436ea0eb3996de9778993d48d59c09213e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insightsTarget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2a903cb2a9dceda7177c4dc551e9f692bfb339cc45179d1fe6460e6468220c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"insights_target": "insightsTarget"},
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration:
    def __init__(self, *, insights_target: builtins.str) -> None:
        '''
        :param insights_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8c35a4ebec34d50565a404c9e50e61c87148ce07c01f071135f85b98c98f390)
            check_type(argname="argument insights_target", value=insights_target, expected_type=type_hints["insights_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "insights_target": insights_target,
        }

    @builtins.property
    def insights_target(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.'''
        result = self._values.get("insights_target")
        assert result is not None, "Required property 'insights_target' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5e87cb01376d4c1418d2e4168f71010ffda69ab50ddfa2f342d6f72719ddff8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="insightsTargetInput")
    def insights_target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insightsTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="insightsTarget")
    def insights_target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "insightsTarget"))

    @insights_target.setter
    def insights_target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8139780c191e6c07604a26b61a7d5a5550bcf6c0b2b97d574fbb3fc678d48bff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insightsTarget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4b8ec89e8a18eafa1751f61b8ecf304a9c8471ef99124c085d9206d286bb166)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdda68c53740751661cf4b5bc36ec366c72dd2916ab4964c36d4162f5f01d5e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa419ad2da120d0e68d21aefe689f855dfda592e78ec938ce5db3bd6edebaad4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1913beb2c61afac6d74a7531004c52b4b3ae26ff0d1dcb6e41d4c54b0e7c775)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9057ca5ce6b91f2910ba7ff9061a9d7fa6252ab015d386b24b530c211e6a8dbf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30681516e12970b0e9022120890bf024e699077b33955a3cfec39fd7b46a2e6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ba9a78c3cb3b768de01e6dd04cf174f1aa6aa3f7eb58deff2cb3c646cffb0e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7bd932e15932c5f8917f2597f76b492e86bb15598ed190ddb7a41da6628dda6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAmazonTranscribeCallAnalyticsProcessorConfiguration")
    def put_amazon_transcribe_call_analytics_processor_configuration(
        self,
        *,
        language_code: builtins.str,
        call_analytics_stream_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        content_identification_type: typing.Optional[builtins.str] = None,
        content_redaction_type: typing.Optional[builtins.str] = None,
        enable_partial_results_stabilization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filter_partial_results: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        language_model_name: typing.Optional[builtins.str] = None,
        partial_results_stability: typing.Optional[builtins.str] = None,
        pii_entity_types: typing.Optional[builtins.str] = None,
        post_call_analytics_settings: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        vocabulary_filter_method: typing.Optional[builtins.str] = None,
        vocabulary_filter_name: typing.Optional[builtins.str] = None,
        vocabulary_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param language_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_code ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_code}.
        :param call_analytics_stream_categories: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#call_analytics_stream_categories ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#call_analytics_stream_categories}.
        :param content_identification_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_identification_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_identification_type}.
        :param content_redaction_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_redaction_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_redaction_type}.
        :param enable_partial_results_stabilization: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#enable_partial_results_stabilization ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#enable_partial_results_stabilization}.
        :param filter_partial_results: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#filter_partial_results ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#filter_partial_results}.
        :param language_model_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_model_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_model_name}.
        :param partial_results_stability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#partial_results_stability ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#partial_results_stability}.
        :param pii_entity_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#pii_entity_types ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#pii_entity_types}.
        :param post_call_analytics_settings: post_call_analytics_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#post_call_analytics_settings ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#post_call_analytics_settings}
        :param vocabulary_filter_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_method ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_method}.
        :param vocabulary_filter_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_name}.
        :param vocabulary_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_name}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration(
            language_code=language_code,
            call_analytics_stream_categories=call_analytics_stream_categories,
            content_identification_type=content_identification_type,
            content_redaction_type=content_redaction_type,
            enable_partial_results_stabilization=enable_partial_results_stabilization,
            filter_partial_results=filter_partial_results,
            language_model_name=language_model_name,
            partial_results_stability=partial_results_stability,
            pii_entity_types=pii_entity_types,
            post_call_analytics_settings=post_call_analytics_settings,
            vocabulary_filter_method=vocabulary_filter_method,
            vocabulary_filter_name=vocabulary_filter_name,
            vocabulary_name=vocabulary_name,
        )

        return typing.cast(None, jsii.invoke(self, "putAmazonTranscribeCallAnalyticsProcessorConfiguration", [value]))

    @jsii.member(jsii_name="putAmazonTranscribeProcessorConfiguration")
    def put_amazon_transcribe_processor_configuration(
        self,
        *,
        language_code: builtins.str,
        content_identification_type: typing.Optional[builtins.str] = None,
        content_redaction_type: typing.Optional[builtins.str] = None,
        enable_partial_results_stabilization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filter_partial_results: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        language_model_name: typing.Optional[builtins.str] = None,
        partial_results_stability: typing.Optional[builtins.str] = None,
        pii_entity_types: typing.Optional[builtins.str] = None,
        show_speaker_label: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vocabulary_filter_method: typing.Optional[builtins.str] = None,
        vocabulary_filter_name: typing.Optional[builtins.str] = None,
        vocabulary_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param language_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_code ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_code}.
        :param content_identification_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_identification_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_identification_type}.
        :param content_redaction_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#content_redaction_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#content_redaction_type}.
        :param enable_partial_results_stabilization: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#enable_partial_results_stabilization ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#enable_partial_results_stabilization}.
        :param filter_partial_results: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#filter_partial_results ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#filter_partial_results}.
        :param language_model_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#language_model_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#language_model_name}.
        :param partial_results_stability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#partial_results_stability ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#partial_results_stability}.
        :param pii_entity_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#pii_entity_types ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#pii_entity_types}.
        :param show_speaker_label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#show_speaker_label ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#show_speaker_label}.
        :param vocabulary_filter_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_method ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_method}.
        :param vocabulary_filter_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_filter_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_filter_name}.
        :param vocabulary_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#vocabulary_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#vocabulary_name}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration(
            language_code=language_code,
            content_identification_type=content_identification_type,
            content_redaction_type=content_redaction_type,
            enable_partial_results_stabilization=enable_partial_results_stabilization,
            filter_partial_results=filter_partial_results,
            language_model_name=language_model_name,
            partial_results_stability=partial_results_stability,
            pii_entity_types=pii_entity_types,
            show_speaker_label=show_speaker_label,
            vocabulary_filter_method=vocabulary_filter_method,
            vocabulary_filter_name=vocabulary_filter_name,
            vocabulary_name=vocabulary_name,
        )

        return typing.cast(None, jsii.invoke(self, "putAmazonTranscribeProcessorConfiguration", [value]))

    @jsii.member(jsii_name="putKinesisDataStreamSinkConfiguration")
    def put_kinesis_data_stream_sink_configuration(
        self,
        *,
        insights_target: builtins.str,
    ) -> None:
        '''
        :param insights_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration(
            insights_target=insights_target
        )

        return typing.cast(None, jsii.invoke(self, "putKinesisDataStreamSinkConfiguration", [value]))

    @jsii.member(jsii_name="putLambdaFunctionSinkConfiguration")
    def put_lambda_function_sink_configuration(
        self,
        *,
        insights_target: builtins.str,
    ) -> None:
        '''
        :param insights_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration(
            insights_target=insights_target
        )

        return typing.cast(None, jsii.invoke(self, "putLambdaFunctionSinkConfiguration", [value]))

    @jsii.member(jsii_name="putS3RecordingSinkConfiguration")
    def put_s3_recording_sink_configuration(
        self,
        *,
        destination: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#destination ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#destination}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration(
            destination=destination
        )

        return typing.cast(None, jsii.invoke(self, "putS3RecordingSinkConfiguration", [value]))

    @jsii.member(jsii_name="putSnsTopicSinkConfiguration")
    def put_sns_topic_sink_configuration(
        self,
        *,
        insights_target: builtins.str,
    ) -> None:
        '''
        :param insights_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration(
            insights_target=insights_target
        )

        return typing.cast(None, jsii.invoke(self, "putSnsTopicSinkConfiguration", [value]))

    @jsii.member(jsii_name="putSqsQueueSinkConfiguration")
    def put_sqs_queue_sink_configuration(
        self,
        *,
        insights_target: builtins.str,
    ) -> None:
        '''
        :param insights_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration(
            insights_target=insights_target
        )

        return typing.cast(None, jsii.invoke(self, "putSqsQueueSinkConfiguration", [value]))

    @jsii.member(jsii_name="putVoiceAnalyticsProcessorConfiguration")
    def put_voice_analytics_processor_configuration(
        self,
        *,
        speaker_search_status: builtins.str,
        voice_tone_analysis_status: builtins.str,
    ) -> None:
        '''
        :param speaker_search_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#speaker_search_status ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#speaker_search_status}.
        :param voice_tone_analysis_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#voice_tone_analysis_status ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#voice_tone_analysis_status}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration(
            speaker_search_status=speaker_search_status,
            voice_tone_analysis_status=voice_tone_analysis_status,
        )

        return typing.cast(None, jsii.invoke(self, "putVoiceAnalyticsProcessorConfiguration", [value]))

    @jsii.member(jsii_name="resetAmazonTranscribeCallAnalyticsProcessorConfiguration")
    def reset_amazon_transcribe_call_analytics_processor_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmazonTranscribeCallAnalyticsProcessorConfiguration", []))

    @jsii.member(jsii_name="resetAmazonTranscribeProcessorConfiguration")
    def reset_amazon_transcribe_processor_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmazonTranscribeProcessorConfiguration", []))

    @jsii.member(jsii_name="resetKinesisDataStreamSinkConfiguration")
    def reset_kinesis_data_stream_sink_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisDataStreamSinkConfiguration", []))

    @jsii.member(jsii_name="resetLambdaFunctionSinkConfiguration")
    def reset_lambda_function_sink_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaFunctionSinkConfiguration", []))

    @jsii.member(jsii_name="resetS3RecordingSinkConfiguration")
    def reset_s3_recording_sink_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3RecordingSinkConfiguration", []))

    @jsii.member(jsii_name="resetSnsTopicSinkConfiguration")
    def reset_sns_topic_sink_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnsTopicSinkConfiguration", []))

    @jsii.member(jsii_name="resetSqsQueueSinkConfiguration")
    def reset_sqs_queue_sink_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqsQueueSinkConfiguration", []))

    @jsii.member(jsii_name="resetVoiceAnalyticsProcessorConfiguration")
    def reset_voice_analytics_processor_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVoiceAnalyticsProcessorConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="amazonTranscribeCallAnalyticsProcessorConfiguration")
    def amazon_transcribe_call_analytics_processor_configuration(
        self,
    ) -> ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationOutputReference:
        return typing.cast(ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationOutputReference, jsii.get(self, "amazonTranscribeCallAnalyticsProcessorConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="amazonTranscribeProcessorConfiguration")
    def amazon_transcribe_processor_configuration(
        self,
    ) -> ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfigurationOutputReference:
        return typing.cast(ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfigurationOutputReference, jsii.get(self, "amazonTranscribeProcessorConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="kinesisDataStreamSinkConfiguration")
    def kinesis_data_stream_sink_configuration(
        self,
    ) -> ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfigurationOutputReference:
        return typing.cast(ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfigurationOutputReference, jsii.get(self, "kinesisDataStreamSinkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionSinkConfiguration")
    def lambda_function_sink_configuration(
        self,
    ) -> ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfigurationOutputReference:
        return typing.cast(ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfigurationOutputReference, jsii.get(self, "lambdaFunctionSinkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="s3RecordingSinkConfiguration")
    def s3_recording_sink_configuration(
        self,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfigurationOutputReference":
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfigurationOutputReference", jsii.get(self, "s3RecordingSinkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="snsTopicSinkConfiguration")
    def sns_topic_sink_configuration(
        self,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfigurationOutputReference":
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfigurationOutputReference", jsii.get(self, "snsTopicSinkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="sqsQueueSinkConfiguration")
    def sqs_queue_sink_configuration(
        self,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfigurationOutputReference":
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfigurationOutputReference", jsii.get(self, "sqsQueueSinkConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="voiceAnalyticsProcessorConfiguration")
    def voice_analytics_processor_configuration(
        self,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfigurationOutputReference":
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfigurationOutputReference", jsii.get(self, "voiceAnalyticsProcessorConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="amazonTranscribeCallAnalyticsProcessorConfigurationInput")
    def amazon_transcribe_call_analytics_processor_configuration_input(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration], jsii.get(self, "amazonTranscribeCallAnalyticsProcessorConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="amazonTranscribeProcessorConfigurationInput")
    def amazon_transcribe_processor_configuration_input(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration], jsii.get(self, "amazonTranscribeProcessorConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisDataStreamSinkConfigurationInput")
    def kinesis_data_stream_sink_configuration_input(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration], jsii.get(self, "kinesisDataStreamSinkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionSinkConfigurationInput")
    def lambda_function_sink_configuration_input(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration], jsii.get(self, "lambdaFunctionSinkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="s3RecordingSinkConfigurationInput")
    def s3_recording_sink_configuration_input(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration"]:
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration"], jsii.get(self, "s3RecordingSinkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="snsTopicSinkConfigurationInput")
    def sns_topic_sink_configuration_input(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration"]:
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration"], jsii.get(self, "snsTopicSinkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="sqsQueueSinkConfigurationInput")
    def sqs_queue_sink_configuration_input(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration"]:
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration"], jsii.get(self, "sqsQueueSinkConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="voiceAnalyticsProcessorConfigurationInput")
    def voice_analytics_processor_configuration_input(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration"]:
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration"], jsii.get(self, "voiceAnalyticsProcessorConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98d5c14625444af031e0ecb8e05e6ce8ab3c24a918742fdf7adc9932586cdd6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de57e66bc49beb9fc12b32b49c5e183dfb95eb5b03192e7816216ca8009c1765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination"},
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration:
    def __init__(self, *, destination: typing.Optional[builtins.str] = None) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#destination ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#destination}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cbeb47775efdf0b4059f1be7286a05e457667effce3ed2f47bf3fc4cf2d9014)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination is not None:
            self._values["destination"] = destination

    @builtins.property
    def destination(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#destination ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#destination}.'''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ff33cd75d7cfcd514c0038fcfb63cb7a3bf7e1445a644b5599a26b8fa4f3c6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDestination")
    def reset_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestination", []))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec3efca339d08c10d1c69970154968e6c6f95cb9aea909ca068458a1acc69f35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d1f8ff050fec5fd6a6f83728731fb538dd69295da950144d256837f56a92289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"insights_target": "insightsTarget"},
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration:
    def __init__(self, *, insights_target: builtins.str) -> None:
        '''
        :param insights_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afbfe642c65720a52e24fc1c8f39fefe128386d7945910bf639d893ecb912399)
            check_type(argname="argument insights_target", value=insights_target, expected_type=type_hints["insights_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "insights_target": insights_target,
        }

    @builtins.property
    def insights_target(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.'''
        result = self._values.get("insights_target")
        assert result is not None, "Required property 'insights_target' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f1fc328f5a7a7ac3c812f6acdee6b09c5255aae6cd5b07f07b4956cdbb7103a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="insightsTargetInput")
    def insights_target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insightsTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="insightsTarget")
    def insights_target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "insightsTarget"))

    @insights_target.setter
    def insights_target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f85103d30c66aebdf9c1dd43eeb3f4dfed941359470c5753631fdd77de2bc363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insightsTarget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bd35068f102e45dacd7d824b7c0076121317cbea3c41db43646277f68d5cf30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration",
    jsii_struct_bases=[],
    name_mapping={"insights_target": "insightsTarget"},
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration:
    def __init__(self, *, insights_target: builtins.str) -> None:
        '''
        :param insights_target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a48460539f5782e9b030d03e41478387f7e1dad18d7bf5cab75612db2e2eaf11)
            check_type(argname="argument insights_target", value=insights_target, expected_type=type_hints["insights_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "insights_target": insights_target,
        }

    @builtins.property
    def insights_target(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#insights_target ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#insights_target}.'''
        result = self._values.get("insights_target")
        assert result is not None, "Required property 'insights_target' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46f7f440c729fc910555189248367a9ac1563c9f3dcd26acf0a5fa87ac70b124)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="insightsTargetInput")
    def insights_target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insightsTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="insightsTarget")
    def insights_target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "insightsTarget"))

    @insights_target.setter
    def insights_target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0a380fd0b712028851ee928d6d27b58957d18fbeb24d784b241ed870f8eead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insightsTarget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b2316a63e8e33093cbaba1296cdec93c21e185bc7feb9ba6d76cf1505aebc27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "speaker_search_status": "speakerSearchStatus",
        "voice_tone_analysis_status": "voiceToneAnalysisStatus",
    },
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration:
    def __init__(
        self,
        *,
        speaker_search_status: builtins.str,
        voice_tone_analysis_status: builtins.str,
    ) -> None:
        '''
        :param speaker_search_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#speaker_search_status ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#speaker_search_status}.
        :param voice_tone_analysis_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#voice_tone_analysis_status ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#voice_tone_analysis_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__791d6f88fc366542074bae6abb0c42e4f1c6873d4133517453ab0d68ebdc66f3)
            check_type(argname="argument speaker_search_status", value=speaker_search_status, expected_type=type_hints["speaker_search_status"])
            check_type(argname="argument voice_tone_analysis_status", value=voice_tone_analysis_status, expected_type=type_hints["voice_tone_analysis_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "speaker_search_status": speaker_search_status,
            "voice_tone_analysis_status": voice_tone_analysis_status,
        }

    @builtins.property
    def speaker_search_status(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#speaker_search_status ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#speaker_search_status}.'''
        result = self._values.get("speaker_search_status")
        assert result is not None, "Required property 'speaker_search_status' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def voice_tone_analysis_status(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#voice_tone_analysis_status ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#voice_tone_analysis_status}.'''
        result = self._values.get("voice_tone_analysis_status")
        assert result is not None, "Required property 'voice_tone_analysis_status' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c22eed96808edb2c809d67e5ba1eae32b164d1f259489ae38d9f2393e13ddad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="speakerSearchStatusInput")
    def speaker_search_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "speakerSearchStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="voiceToneAnalysisStatusInput")
    def voice_tone_analysis_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "voiceToneAnalysisStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="speakerSearchStatus")
    def speaker_search_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "speakerSearchStatus"))

    @speaker_search_status.setter
    def speaker_search_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b8250f7a253bac92407536479a9c559b7490db4fabc41ea8e21098879783cfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "speakerSearchStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="voiceToneAnalysisStatus")
    def voice_tone_analysis_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "voiceToneAnalysisStatus"))

    @voice_tone_analysis_status.setter
    def voice_tone_analysis_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b984dd3019d9ad3e8fb02e838d1867f49c3b9599c042a5026dc1e754745a7756)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "voiceToneAnalysisStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33c43577d478a60fcf033f3b706929d15b965e5607f0bf40ca4eb0b0a60fa1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration",
    jsii_struct_bases=[],
    name_mapping={"rules": "rules", "disabled": "disabled"},
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration:
    def __init__(
        self,
        *,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules", typing.Dict[builtins.str, typing.Any]]]],
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rules ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rules}
        :param disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#disabled ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#disabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e32375d66c73ac69ef906c836ebee33130e4b1e277f34a5ac6d66892c72e78)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rules": rules,
        }
        if disabled is not None:
            self._values["disabled"] = disabled

    @builtins.property
    def rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules"]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rules ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rules}
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules"]], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#disabled ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#disabled}.'''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5c42f3cdaea0dd45fbff78086f2bb93a6853dfc234d45a7951eef5c30e6c10f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b464cb9921882237cd0d72f2a68b787111c299a6c1784e180083888b7b92bfb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(
        self,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesList":
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__479a057eca5b06cc77cc5117f6feb3a753c65235c459cfcd75cdb33e73acb5d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e057c0aa1b2c1b360db59f720658d6edd1cab2d3c6f50a57053983b3deb077)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "issue_detection_configuration": "issueDetectionConfiguration",
        "keyword_match_configuration": "keywordMatchConfiguration",
        "sentiment_configuration": "sentimentConfiguration",
    },
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules:
    def __init__(
        self,
        *,
        type: builtins.str,
        issue_detection_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        keyword_match_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        sentiment_configuration: typing.Optional[typing.Union["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#type}.
        :param issue_detection_configuration: issue_detection_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#issue_detection_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#issue_detection_configuration}
        :param keyword_match_configuration: keyword_match_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#keyword_match_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#keyword_match_configuration}
        :param sentiment_configuration: sentiment_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#sentiment_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#sentiment_configuration}
        '''
        if isinstance(issue_detection_configuration, dict):
            issue_detection_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration(**issue_detection_configuration)
        if isinstance(keyword_match_configuration, dict):
            keyword_match_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration(**keyword_match_configuration)
        if isinstance(sentiment_configuration, dict):
            sentiment_configuration = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration(**sentiment_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce589fd888b694be0f4a1d83843287103e9a26755bfb0e685732efa4f99d8471)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument issue_detection_configuration", value=issue_detection_configuration, expected_type=type_hints["issue_detection_configuration"])
            check_type(argname="argument keyword_match_configuration", value=keyword_match_configuration, expected_type=type_hints["keyword_match_configuration"])
            check_type(argname="argument sentiment_configuration", value=sentiment_configuration, expected_type=type_hints["sentiment_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if issue_detection_configuration is not None:
            self._values["issue_detection_configuration"] = issue_detection_configuration
        if keyword_match_configuration is not None:
            self._values["keyword_match_configuration"] = keyword_match_configuration
        if sentiment_configuration is not None:
            self._values["sentiment_configuration"] = sentiment_configuration

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def issue_detection_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration"]:
        '''issue_detection_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#issue_detection_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#issue_detection_configuration}
        '''
        result = self._values.get("issue_detection_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration"], result)

    @builtins.property
    def keyword_match_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration"]:
        '''keyword_match_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#keyword_match_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#keyword_match_configuration}
        '''
        result = self._values.get("keyword_match_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration"], result)

    @builtins.property
    def sentiment_configuration(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration"]:
        '''sentiment_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#sentiment_configuration ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#sentiment_configuration}
        '''
        result = self._values.get("sentiment_configuration")
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"rule_name": "ruleName"},
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration:
    def __init__(self, *, rule_name: builtins.str) -> None:
        '''
        :param rule_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rule_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rule_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f96bf4cfd9f16b237e254813476e38d6f1e84aa0e98cd0afaefcbb7694306a01)
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_name": rule_name,
        }

    @builtins.property
    def rule_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rule_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rule_name}.'''
        result = self._values.get("rule_name")
        assert result is not None, "Required property 'rule_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aeb5814052e1ee1570954c0b1c2d877f3735f642feb0fff05f8e3d9bed476b65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="ruleNameInput")
    def rule_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleName"))

    @rule_name.setter
    def rule_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2153080ee1ec66c1caf9d89e8b51d37c88d588e7180ed37ad6d02ff7c869398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c9ecce3affebea0b8631c3a9db407927e9be403010b728e2e01a4453de30030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration",
    jsii_struct_bases=[],
    name_mapping={"keywords": "keywords", "rule_name": "ruleName", "negate": "negate"},
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration:
    def __init__(
        self,
        *,
        keywords: typing.Sequence[builtins.str],
        rule_name: builtins.str,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param keywords: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#keywords ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#keywords}.
        :param rule_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rule_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rule_name}.
        :param negate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#negate ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#negate}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf83791d84c9686dc970e335692c22bdc1d056d03810d15b9162a744986e3d50)
            check_type(argname="argument keywords", value=keywords, expected_type=type_hints["keywords"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument negate", value=negate, expected_type=type_hints["negate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "keywords": keywords,
            "rule_name": rule_name,
        }
        if negate is not None:
            self._values["negate"] = negate

    @builtins.property
    def keywords(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#keywords ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#keywords}.'''
        result = self._values.get("keywords")
        assert result is not None, "Required property 'keywords' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def rule_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rule_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rule_name}.'''
        result = self._values.get("rule_name")
        assert result is not None, "Required property 'rule_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def negate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#negate ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#negate}.'''
        result = self._values.get("negate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7de5e5d18f6fbf9fee5712fe6e8f4b9bcb8bd7f48e6c73339bc36e4db31145a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNegate")
    def reset_negate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegate", []))

    @builtins.property
    @jsii.member(jsii_name="keywordsInput")
    def keywords_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "keywordsInput"))

    @builtins.property
    @jsii.member(jsii_name="negateInput")
    def negate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleNameInput")
    def rule_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keywords")
    def keywords(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "keywords"))

    @keywords.setter
    def keywords(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4422663062029ac60a0bde3018852add96ba50daed9e635361bb0a759a5e697c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keywords", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negate")
    def negate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negate"))

    @negate.setter
    def negate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a00000e24922bbda822d0d5784ab4c1d301212b4f146e73d88c98d135b59a86d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleName"))

    @rule_name.setter
    def rule_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc6e69369d2d1ebcd17d633286526ef4c30f5e6c17adc43231be1526513fc6f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53454a43443ccdc4dc38cc97484d2ac3f36505d7bd9a23b716e9decdd548a064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9329876cde72fbba39d21b2268156ba714b6f7c9fab0b496bef910b9423c13e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3788fffa615ba92058d6e549f40d25140f5ed0490e7eb9b2797fa1d493b99ddc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb461c61ab7ecda261192d21a27446fe587e9ada52173d2210a2105d54b18b6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__915c0f0ccf26d40341dfb9103d76c0f24dcc39293bd20854c3d0671fb56f063f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0d58e8780a932082c7bfe28f8dc6d24cd4bb60fa2389e4d27adafedf7207b76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d54be760666bb5fb9f077da2817c56907de6b1c3fe5b7b844a333d4f69519ed7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f92e305dfde8219461d6198861520a57a5761c3f350156a79a9bab7bf4dba8b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIssueDetectionConfiguration")
    def put_issue_detection_configuration(self, *, rule_name: builtins.str) -> None:
        '''
        :param rule_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rule_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rule_name}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration(
            rule_name=rule_name
        )

        return typing.cast(None, jsii.invoke(self, "putIssueDetectionConfiguration", [value]))

    @jsii.member(jsii_name="putKeywordMatchConfiguration")
    def put_keyword_match_configuration(
        self,
        *,
        keywords: typing.Sequence[builtins.str],
        rule_name: builtins.str,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param keywords: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#keywords ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#keywords}.
        :param rule_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rule_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rule_name}.
        :param negate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#negate ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#negate}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration(
            keywords=keywords, rule_name=rule_name, negate=negate
        )

        return typing.cast(None, jsii.invoke(self, "putKeywordMatchConfiguration", [value]))

    @jsii.member(jsii_name="putSentimentConfiguration")
    def put_sentiment_configuration(
        self,
        *,
        rule_name: builtins.str,
        sentiment_type: builtins.str,
        time_period: jsii.Number,
    ) -> None:
        '''
        :param rule_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rule_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rule_name}.
        :param sentiment_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#sentiment_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#sentiment_type}.
        :param time_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#time_period ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#time_period}.
        '''
        value = ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration(
            rule_name=rule_name, sentiment_type=sentiment_type, time_period=time_period
        )

        return typing.cast(None, jsii.invoke(self, "putSentimentConfiguration", [value]))

    @jsii.member(jsii_name="resetIssueDetectionConfiguration")
    def reset_issue_detection_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssueDetectionConfiguration", []))

    @jsii.member(jsii_name="resetKeywordMatchConfiguration")
    def reset_keyword_match_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeywordMatchConfiguration", []))

    @jsii.member(jsii_name="resetSentimentConfiguration")
    def reset_sentiment_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSentimentConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="issueDetectionConfiguration")
    def issue_detection_configuration(
        self,
    ) -> ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfigurationOutputReference:
        return typing.cast(ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfigurationOutputReference, jsii.get(self, "issueDetectionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="keywordMatchConfiguration")
    def keyword_match_configuration(
        self,
    ) -> ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfigurationOutputReference:
        return typing.cast(ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfigurationOutputReference, jsii.get(self, "keywordMatchConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="sentimentConfiguration")
    def sentiment_configuration(
        self,
    ) -> "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfigurationOutputReference":
        return typing.cast("ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfigurationOutputReference", jsii.get(self, "sentimentConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="issueDetectionConfigurationInput")
    def issue_detection_configuration_input(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration], jsii.get(self, "issueDetectionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="keywordMatchConfigurationInput")
    def keyword_match_configuration_input(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration], jsii.get(self, "keywordMatchConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="sentimentConfigurationInput")
    def sentiment_configuration_input(
        self,
    ) -> typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration"]:
        return typing.cast(typing.Optional["ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration"], jsii.get(self, "sentimentConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4e66077854273b145c0b683a27ba275de0b53831efe4d5293c4e775ef0f0097)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b8b9b0367b2cd4bc472ccc1d66bd1ee4391c4b872efcc2a3eb45984d0c9e301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "rule_name": "ruleName",
        "sentiment_type": "sentimentType",
        "time_period": "timePeriod",
    },
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration:
    def __init__(
        self,
        *,
        rule_name: builtins.str,
        sentiment_type: builtins.str,
        time_period: jsii.Number,
    ) -> None:
        '''
        :param rule_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rule_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rule_name}.
        :param sentiment_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#sentiment_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#sentiment_type}.
        :param time_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#time_period ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#time_period}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b11aa407e33e27258d278f7bec1cc9345c9c3ccfc5f2d4b7a8a727cd4af645eb)
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument sentiment_type", value=sentiment_type, expected_type=type_hints["sentiment_type"])
            check_type(argname="argument time_period", value=time_period, expected_type=type_hints["time_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_name": rule_name,
            "sentiment_type": sentiment_type,
            "time_period": time_period,
        }

    @builtins.property
    def rule_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#rule_name ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#rule_name}.'''
        result = self._values.get("rule_name")
        assert result is not None, "Required property 'rule_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sentiment_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#sentiment_type ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#sentiment_type}.'''
        result = self._values.get("sentiment_type")
        assert result is not None, "Required property 'sentiment_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_period(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#time_period ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#time_period}.'''
        result = self._values.get("time_period")
        assert result is not None, "Required property 'time_period' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a8389d3052cb414cd604fc5ccba5db474afc145ef7e7e22546525c28e2a4bb8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="ruleNameInput")
    def rule_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sentimentTypeInput")
    def sentiment_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sentimentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timePeriodInput")
    def time_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timePeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleName"))

    @rule_name.setter
    def rule_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d99c757ba71dbba497d8474dab47efaa5dd0bf76d9921a2dc02b16a29e8609e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sentimentType")
    def sentiment_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sentimentType"))

    @sentiment_type.setter
    def sentiment_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d043ac1619750cf4a8ab45aac594a34155cb2be63c0854ecf3226b0357bc056)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sentimentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timePeriod")
    def time_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timePeriod"))

    @time_period.setter
    def time_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09f2bb140db073a0250cc60b5ba0e10daa14869048d20227fc32692b0954b035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timePeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration]:
        return typing.cast(typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b246c41671c7308b5c104738a7033c3504ca4aac2011a810ebc22a47af6f913c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#create ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#delete ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#update ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__357618473aa0ebcb481f496c9f60fb2f107dd518c6cee70b54823a63f32da897)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#create ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#delete ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/chimesdkmediapipelines_media_insights_pipeline_configuration#update ChimesdkmediapipelinesMediaInsightsPipelineConfiguration#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.chimesdkmediapipelinesMediaInsightsPipelineConfiguration.ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__058fc2bac9179064ae9ad2d268fb96cc25e839126a18eb412f67e30fad29fbaf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb28452d84024ffc74c3f5bd90ba3dbe79956186fde6743a7a1400eb52925c75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cca68a7e590ce63dc93943610a79fef32186eb88fc4ff1be169886870a843745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f62a8e021d25fe4783aa5158d15e5d427bc3c94c8f96be5dac3f38a01cf4b31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce02310ee6fa70b7378ed1f73b39542a268a165c6a9f7fd3a9b28e4b02d9cde0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ChimesdkmediapipelinesMediaInsightsPipelineConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationConfig",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettingsOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsList",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesList",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfigurationOutputReference",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts",
    "ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c88a8e89419d3fdb08bbb28715bc9e29ea3bc158479ae5be4e6737ed19ca31f5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    elements: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    resource_access_role_arn: builtins.str,
    real_time_alert_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__982d5f8a707f2bff552afa7b3cfa3f4ba9c09c9a842f5e2efbbb26a713986876(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6ae99019e9cc1c7aef67a5763069fd970e7e46c20a16bfb0b97619e47a9fdcb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3c2206d9887ebf7783e178c47a4c56da80159e11e4c7ce427bc908a48ce9ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69104bef5831e3eeae897f7cd14efe1178443e14dbd04a1f4ebb39c881ba2089(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c12458a083d55483da97e6551f20ec36329d823654ab452e46ab6be1a98fae4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b44e9b46c1c48bb67dce8422362d6b71151acc745f75390aec934371923c4af(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5533a2b646e6d1f5df4e277e5306e7c0f8aaaea3223d9f5037899820a7e1d486(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef64faccc404724f25b42e33c4aa968fb92c70c4baa8a9a22f9212fd4868e40(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    elements: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    resource_access_role_arn: builtins.str,
    real_time_alert_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a60bdbda06dbe937f00f600d4d1e9b9e758895dcbc610014315035bbc34d83(
    *,
    type: builtins.str,
    amazon_transcribe_call_analytics_processor_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    amazon_transcribe_processor_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    kinesis_data_stream_sink_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    lambda_function_sink_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_recording_sink_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    sns_topic_sink_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    sqs_queue_sink_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    voice_analytics_processor_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d207b87f5daa59c74728636a3f4ffe948ba3bb9c5b9b0b1fc399f78fbdbc138c(
    *,
    language_code: builtins.str,
    call_analytics_stream_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
    content_identification_type: typing.Optional[builtins.str] = None,
    content_redaction_type: typing.Optional[builtins.str] = None,
    enable_partial_results_stabilization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    filter_partial_results: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    language_model_name: typing.Optional[builtins.str] = None,
    partial_results_stability: typing.Optional[builtins.str] = None,
    pii_entity_types: typing.Optional[builtins.str] = None,
    post_call_analytics_settings: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    vocabulary_filter_method: typing.Optional[builtins.str] = None,
    vocabulary_filter_name: typing.Optional[builtins.str] = None,
    vocabulary_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d59a3d25e3b9416d473ca1f98f81cbcae8f069e25d60c03b88a15750f072c42(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37040717169f7a79945e895d16763d1020b249906e6a11393ba927ef4ab8468a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89bcf7d63c33351e79107f58b459c90b3f65ee533d383166f6f8d88c3d0ff0a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c49a59a67d1405eb5895e84fb048c067c35ef449058c2ddab484fc51f4c0f25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e49851a3196b05a8a79d36442519e11386155abd69c284df8a7f0d8f960a7f7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e720432cf1d4e2a163f56f400a11ab33a3b39a5666742ff34ab8b60b34996248(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e90379c8f7073123bbc59fc9e383c96e097a9030ea50dd18bb035db9e8861b2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cbb1d6903ab0cd7a16573794c1d97b55cb79eceda5c488074d8ea73e9204c46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9786a3e39cdbabba543954457d96de6f9a5f6e91e143a438c24a9d0453ba333(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7ec64d8cd482f4f379adf6df08ba321c1a603f0b41ea5c3fa313bc3ede2293(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51b58abbb6ad89bce23b564748798b8374c740f593b06c25b6443c7c7d4327e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b0c53c623c98eae002b4a52fdf5d3fd27342f25e823b61f63b89a2cf755346(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba18c5b6422fc3771c67d774f296871ed7d686fdc695341f12bac9bd4a5eecc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299f1de7e187b2f8bbc8f5d6540675b83f7733d46e8f835e9b281ca2f91a69c8(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1265805d5c09354c9371718ba7ccd4376c30d100869019d92f9fac18e3f86ee1(
    *,
    data_access_role_arn: builtins.str,
    output_location: builtins.str,
    content_redaction_output: typing.Optional[builtins.str] = None,
    output_encryption_kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc3a391aed0cad8381f400ff67ddd8aff05a2dbc1271ca998ba503c8285393b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd74ecad20c92eabd05e509c7b7be415c757ecdf66414be1c063f3d0e5dacc07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d54862aeedd03e788402c6a2837a4801890a8daa83e55397844cc1e89ce9ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__210f1091ebb9bba86ac3efe0a15a84f471377e1bdc83039b3d3ed3f6f88b62c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3555a10ff34442c237ba9d8a862a598117da6dd80d162a5edb238967bd87d2d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baa947982d055498b38b6fff7eccbd560405cdf1fcca430b172b15489a9cc836(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeCallAnalyticsProcessorConfigurationPostCallAnalyticsSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32390edf6b17672bef4937d42f74a871e623a37d0ea98dc73e9aa60bf3833f84(
    *,
    language_code: builtins.str,
    content_identification_type: typing.Optional[builtins.str] = None,
    content_redaction_type: typing.Optional[builtins.str] = None,
    enable_partial_results_stabilization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    filter_partial_results: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    language_model_name: typing.Optional[builtins.str] = None,
    partial_results_stability: typing.Optional[builtins.str] = None,
    pii_entity_types: typing.Optional[builtins.str] = None,
    show_speaker_label: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vocabulary_filter_method: typing.Optional[builtins.str] = None,
    vocabulary_filter_name: typing.Optional[builtins.str] = None,
    vocabulary_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e81fab263e43334cad722dfb0c1e2d78b9180f2bf45467533318bc6c18720e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb5506b7d492179475e3df44d048189da980fb8a4bd5074273545ab6525f6f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee97291823384d7b23449d38d1f9535271426c971aa05735bf7fc2dc35bb872(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b1becbd0e782542238c745fdfe52bcad5422ab288f3e8f5d116f07526e382b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed5b7d6455140e637b6065d35243e68401b5bb6d95501c1087b37650f9ff196(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66a8c53b1885ce13f7b1f818a8e395c9044e3e09723463bd08980184901e2ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6d874b38dc81bcfa68f45e882109f7f6b3d4c990ad316cf01e895daf1e7ce8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7606b8afceb0fc0f683a68d9e47570203c38563d5a123e792b9dc24481ecae9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1678e407d27a2dc57769644ff90e7b3493469228283c9b8f831254722abb94c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e258736aa05553acb4c0fb03d652c2c01b866c4fac6fb2ae1e0a85ea634602(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82984e6b98f0d7dde5c78e57a289cf96f35e13379167b017475c227f71a088ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686f76f4b82f1d0413456f1ba4987b4be500202f6b8ed569a39f841d5d5c1789(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__001617af4039e6b4431784541bbe320c103aff4364973804983fb5ef3e751af1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a7dc4f61b94c98b999f0bf5f40f45291f17d3f90c99e94a6230a1a7e9712a8(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsAmazonTranscribeProcessorConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__751048f3718a427cc5284c173f6e16017fcde6e298a88c017fb97bbea063ae1a(
    *,
    insights_target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c37acde92649a71adf63e26eb0e1f084c746d8ec2db52941dd9d1b0b37c5c97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eb889c5f5e2a41fc7e373e92a9941436ea0eb3996de9778993d48d59c09213e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a903cb2a9dceda7177c4dc551e9f692bfb339cc45179d1fe6460e6468220c1(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsKinesisDataStreamSinkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c35a4ebec34d50565a404c9e50e61c87148ce07c01f071135f85b98c98f390(
    *,
    insights_target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e87cb01376d4c1418d2e4168f71010ffda69ab50ddfa2f342d6f72719ddff8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8139780c191e6c07604a26b61a7d5a5550bcf6c0b2b97d574fbb3fc678d48bff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b8ec89e8a18eafa1751f61b8ecf304a9c8471ef99124c085d9206d286bb166(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsLambdaFunctionSinkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdda68c53740751661cf4b5bc36ec366c72dd2916ab4964c36d4162f5f01d5e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa419ad2da120d0e68d21aefe689f855dfda592e78ec938ce5db3bd6edebaad4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1913beb2c61afac6d74a7531004c52b4b3ae26ff0d1dcb6e41d4c54b0e7c775(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9057ca5ce6b91f2910ba7ff9061a9d7fa6252ab015d386b24b530c211e6a8dbf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30681516e12970b0e9022120890bf024e699077b33955a3cfec39fd7b46a2e6f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba9a78c3cb3b768de01e6dd04cf174f1aa6aa3f7eb58deff2cb3c646cffb0e4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7bd932e15932c5f8917f2597f76b492e86bb15598ed190ddb7a41da6628dda6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d5c14625444af031e0ecb8e05e6ce8ab3c24a918742fdf7adc9932586cdd6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de57e66bc49beb9fc12b32b49c5e183dfb95eb5b03192e7816216ca8009c1765(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElements]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cbeb47775efdf0b4059f1be7286a05e457667effce3ed2f47bf3fc4cf2d9014(
    *,
    destination: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff33cd75d7cfcd514c0038fcfb63cb7a3bf7e1445a644b5599a26b8fa4f3c6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec3efca339d08c10d1c69970154968e6c6f95cb9aea909ca068458a1acc69f35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1f8ff050fec5fd6a6f83728731fb538dd69295da950144d256837f56a92289(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsS3RecordingSinkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afbfe642c65720a52e24fc1c8f39fefe128386d7945910bf639d893ecb912399(
    *,
    insights_target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f1fc328f5a7a7ac3c812f6acdee6b09c5255aae6cd5b07f07b4956cdbb7103a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f85103d30c66aebdf9c1dd43eeb3f4dfed941359470c5753631fdd77de2bc363(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd35068f102e45dacd7d824b7c0076121317cbea3c41db43646277f68d5cf30(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSnsTopicSinkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a48460539f5782e9b030d03e41478387f7e1dad18d7bf5cab75612db2e2eaf11(
    *,
    insights_target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f7f440c729fc910555189248367a9ac1563c9f3dcd26acf0a5fa87ac70b124(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0a380fd0b712028851ee928d6d27b58957d18fbeb24d784b241ed870f8eead(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b2316a63e8e33093cbaba1296cdec93c21e185bc7feb9ba6d76cf1505aebc27(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsSqsQueueSinkConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791d6f88fc366542074bae6abb0c42e4f1c6873d4133517453ab0d68ebdc66f3(
    *,
    speaker_search_status: builtins.str,
    voice_tone_analysis_status: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c22eed96808edb2c809d67e5ba1eae32b164d1f259489ae38d9f2393e13ddad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8250f7a253bac92407536479a9c559b7490db4fabc41ea8e21098879783cfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b984dd3019d9ad3e8fb02e838d1867f49c3b9599c042a5026dc1e754745a7756(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33c43577d478a60fcf033f3b706929d15b965e5607f0bf40ca4eb0b0a60fa1a(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationElementsVoiceAnalyticsProcessorConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e32375d66c73ac69ef906c836ebee33130e4b1e277f34a5ac6d66892c72e78(
    *,
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules, typing.Dict[builtins.str, typing.Any]]]],
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c42f3cdaea0dd45fbff78086f2bb93a6853dfc234d45a7951eef5c30e6c10f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b464cb9921882237cd0d72f2a68b787111c299a6c1784e180083888b7b92bfb8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__479a057eca5b06cc77cc5117f6feb3a753c65235c459cfcd75cdb33e73acb5d5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e057c0aa1b2c1b360db59f720658d6edd1cab2d3c6f50a57053983b3deb077(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce589fd888b694be0f4a1d83843287103e9a26755bfb0e685732efa4f99d8471(
    *,
    type: builtins.str,
    issue_detection_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    keyword_match_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    sentiment_configuration: typing.Optional[typing.Union[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f96bf4cfd9f16b237e254813476e38d6f1e84aa0e98cd0afaefcbb7694306a01(
    *,
    rule_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb5814052e1ee1570954c0b1c2d877f3735f642feb0fff05f8e3d9bed476b65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2153080ee1ec66c1caf9d89e8b51d37c88d588e7180ed37ad6d02ff7c869398(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c9ecce3affebea0b8631c3a9db407927e9be403010b728e2e01a4453de30030(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesIssueDetectionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf83791d84c9686dc970e335692c22bdc1d056d03810d15b9162a744986e3d50(
    *,
    keywords: typing.Sequence[builtins.str],
    rule_name: builtins.str,
    negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de5e5d18f6fbf9fee5712fe6e8f4b9bcb8bd7f48e6c73339bc36e4db31145a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4422663062029ac60a0bde3018852add96ba50daed9e635361bb0a759a5e697c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a00000e24922bbda822d0d5784ab4c1d301212b4f146e73d88c98d135b59a86d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6e69369d2d1ebcd17d633286526ef4c30f5e6c17adc43231be1526513fc6f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53454a43443ccdc4dc38cc97484d2ac3f36505d7bd9a23b716e9decdd548a064(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesKeywordMatchConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9329876cde72fbba39d21b2268156ba714b6f7c9fab0b496bef910b9423c13e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3788fffa615ba92058d6e549f40d25140f5ed0490e7eb9b2797fa1d493b99ddc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb461c61ab7ecda261192d21a27446fe587e9ada52173d2210a2105d54b18b6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__915c0f0ccf26d40341dfb9103d76c0f24dcc39293bd20854c3d0671fb56f063f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d58e8780a932082c7bfe28f8dc6d24cd4bb60fa2389e4d27adafedf7207b76(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d54be760666bb5fb9f077da2817c56907de6b1c3fe5b7b844a333d4f69519ed7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f92e305dfde8219461d6198861520a57a5761c3f350156a79a9bab7bf4dba8b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4e66077854273b145c0b683a27ba275de0b53831efe4d5293c4e775ef0f0097(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b8b9b0367b2cd4bc472ccc1d66bd1ee4391c4b872efcc2a3eb45984d0c9e301(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11aa407e33e27258d278f7bec1cc9345c9c3ccfc5f2d4b7a8a727cd4af645eb(
    *,
    rule_name: builtins.str,
    sentiment_type: builtins.str,
    time_period: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a8389d3052cb414cd604fc5ccba5db474afc145ef7e7e22546525c28e2a4bb8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d99c757ba71dbba497d8474dab47efaa5dd0bf76d9921a2dc02b16a29e8609e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d043ac1619750cf4a8ab45aac594a34155cb2be63c0854ecf3226b0357bc056(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09f2bb140db073a0250cc60b5ba0e10daa14869048d20227fc32692b0954b035(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b246c41671c7308b5c104738a7033c3504ca4aac2011a810ebc22a47af6f913c(
    value: typing.Optional[ChimesdkmediapipelinesMediaInsightsPipelineConfigurationRealTimeAlertConfigurationRulesSentimentConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__357618473aa0ebcb481f496c9f60fb2f107dd518c6cee70b54823a63f32da897(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__058fc2bac9179064ae9ad2d268fb96cc25e839126a18eb412f67e30fad29fbaf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb28452d84024ffc74c3f5bd90ba3dbe79956186fde6743a7a1400eb52925c75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cca68a7e590ce63dc93943610a79fef32186eb88fc4ff1be169886870a843745(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f62a8e021d25fe4783aa5158d15e5d427bc3c94c8f96be5dac3f38a01cf4b31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce02310ee6fa70b7378ed1f73b39542a268a165c6a9f7fd3a9b28e4b02d9cde0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ChimesdkmediapipelinesMediaInsightsPipelineConfigurationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
