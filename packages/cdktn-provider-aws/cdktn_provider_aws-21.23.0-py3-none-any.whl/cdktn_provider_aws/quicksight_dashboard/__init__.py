r'''
# `aws_quicksight_dashboard`

Refer to the Terraform Registry for docs: [`aws_quicksight_dashboard`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard).
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


class QuicksightDashboard(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboard",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard aws_quicksight_dashboard}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dashboard_id: builtins.str,
        name: builtins.str,
        version_description: builtins.str,
        aws_account_id: typing.Optional[builtins.str] = None,
        dashboard_publish_options: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        definition: typing.Any = None,
        id: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union["QuicksightDashboardParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardPermissions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        source_entity: typing.Optional[typing.Union["QuicksightDashboardSourceEntity", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        theme_arn: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["QuicksightDashboardTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard aws_quicksight_dashboard} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dashboard_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#dashboard_id QuicksightDashboard#dashboard_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.
        :param version_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#version_description QuicksightDashboard#version_description}.
        :param aws_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#aws_account_id QuicksightDashboard#aws_account_id}.
        :param dashboard_publish_options: dashboard_publish_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#dashboard_publish_options QuicksightDashboard#dashboard_publish_options}
        :param definition: definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#definition QuicksightDashboard#definition}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#id QuicksightDashboard#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#parameters QuicksightDashboard#parameters}
        :param permissions: permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#permissions QuicksightDashboard#permissions}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#region QuicksightDashboard#region}
        :param source_entity: source_entity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#source_entity QuicksightDashboard#source_entity}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#tags QuicksightDashboard#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#tags_all QuicksightDashboard#tags_all}.
        :param theme_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#theme_arn QuicksightDashboard#theme_arn}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#timeouts QuicksightDashboard#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6f945749e8425615e0d56466b5a27bd905354edc5bd3fa97c48ff2802cabdf7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = QuicksightDashboardConfig(
            dashboard_id=dashboard_id,
            name=name,
            version_description=version_description,
            aws_account_id=aws_account_id,
            dashboard_publish_options=dashboard_publish_options,
            definition=definition,
            id=id,
            parameters=parameters,
            permissions=permissions,
            region=region,
            source_entity=source_entity,
            tags=tags,
            tags_all=tags_all,
            theme_arn=theme_arn,
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
        '''Generates CDKTF code for importing a QuicksightDashboard resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the QuicksightDashboard to import.
        :param import_from_id: The id of the existing QuicksightDashboard that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the QuicksightDashboard to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f95c4456a0fc1e34e194ab79d38ae74cf0131248438256f90c07b838cbe04a6f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDashboardPublishOptions")
    def put_dashboard_publish_options(
        self,
        *,
        ad_hoc_filtering_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption", typing.Dict[builtins.str, typing.Any]]] = None,
        data_point_drill_up_down_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption", typing.Dict[builtins.str, typing.Any]]] = None,
        data_point_menu_label_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption", typing.Dict[builtins.str, typing.Any]]] = None,
        data_point_tooltip_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption", typing.Dict[builtins.str, typing.Any]]] = None,
        export_to_csv_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsExportToCsvOption", typing.Dict[builtins.str, typing.Any]]] = None,
        export_with_hidden_fields_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption", typing.Dict[builtins.str, typing.Any]]] = None,
        sheet_controls_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsSheetControlsOption", typing.Dict[builtins.str, typing.Any]]] = None,
        sheet_layout_element_maximization_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption", typing.Dict[builtins.str, typing.Any]]] = None,
        visual_axis_sort_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption", typing.Dict[builtins.str, typing.Any]]] = None,
        visual_menu_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsVisualMenuOption", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ad_hoc_filtering_option: ad_hoc_filtering_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#ad_hoc_filtering_option QuicksightDashboard#ad_hoc_filtering_option}
        :param data_point_drill_up_down_option: data_point_drill_up_down_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#data_point_drill_up_down_option QuicksightDashboard#data_point_drill_up_down_option}
        :param data_point_menu_label_option: data_point_menu_label_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#data_point_menu_label_option QuicksightDashboard#data_point_menu_label_option}
        :param data_point_tooltip_option: data_point_tooltip_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#data_point_tooltip_option QuicksightDashboard#data_point_tooltip_option}
        :param export_to_csv_option: export_to_csv_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#export_to_csv_option QuicksightDashboard#export_to_csv_option}
        :param export_with_hidden_fields_option: export_with_hidden_fields_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#export_with_hidden_fields_option QuicksightDashboard#export_with_hidden_fields_option}
        :param sheet_controls_option: sheet_controls_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#sheet_controls_option QuicksightDashboard#sheet_controls_option}
        :param sheet_layout_element_maximization_option: sheet_layout_element_maximization_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#sheet_layout_element_maximization_option QuicksightDashboard#sheet_layout_element_maximization_option}
        :param visual_axis_sort_option: visual_axis_sort_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#visual_axis_sort_option QuicksightDashboard#visual_axis_sort_option}
        :param visual_menu_option: visual_menu_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#visual_menu_option QuicksightDashboard#visual_menu_option}
        '''
        value = QuicksightDashboardDashboardPublishOptions(
            ad_hoc_filtering_option=ad_hoc_filtering_option,
            data_point_drill_up_down_option=data_point_drill_up_down_option,
            data_point_menu_label_option=data_point_menu_label_option,
            data_point_tooltip_option=data_point_tooltip_option,
            export_to_csv_option=export_to_csv_option,
            export_with_hidden_fields_option=export_with_hidden_fields_option,
            sheet_controls_option=sheet_controls_option,
            sheet_layout_element_maximization_option=sheet_layout_element_maximization_option,
            visual_axis_sort_option=visual_axis_sort_option,
            visual_menu_option=visual_menu_option,
        )

        return typing.cast(None, jsii.invoke(self, "putDashboardPublishOptions", [value]))

    @jsii.member(jsii_name="putParameters")
    def put_parameters(
        self,
        *,
        date_time_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardParametersDateTimeParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        decimal_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardParametersDecimalParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        integer_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardParametersIntegerParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardParametersStringParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param date_time_parameters: date_time_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#date_time_parameters QuicksightDashboard#date_time_parameters}
        :param decimal_parameters: decimal_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#decimal_parameters QuicksightDashboard#decimal_parameters}
        :param integer_parameters: integer_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#integer_parameters QuicksightDashboard#integer_parameters}
        :param string_parameters: string_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#string_parameters QuicksightDashboard#string_parameters}
        '''
        value = QuicksightDashboardParameters(
            date_time_parameters=date_time_parameters,
            decimal_parameters=decimal_parameters,
            integer_parameters=integer_parameters,
            string_parameters=string_parameters,
        )

        return typing.cast(None, jsii.invoke(self, "putParameters", [value]))

    @jsii.member(jsii_name="putPermissions")
    def put_permissions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardPermissions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5558401553e68c841440c625c4271d0e8463b4ca33f52d079fd31c908b15cc57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPermissions", [value]))

    @jsii.member(jsii_name="putSourceEntity")
    def put_source_entity(
        self,
        *,
        source_template: typing.Optional[typing.Union["QuicksightDashboardSourceEntitySourceTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param source_template: source_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#source_template QuicksightDashboard#source_template}
        '''
        value = QuicksightDashboardSourceEntity(source_template=source_template)

        return typing.cast(None, jsii.invoke(self, "putSourceEntity", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#create QuicksightDashboard#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#delete QuicksightDashboard#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#update QuicksightDashboard#update}.
        '''
        value = QuicksightDashboardTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAwsAccountId")
    def reset_aws_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAccountId", []))

    @jsii.member(jsii_name="resetDashboardPublishOptions")
    def reset_dashboard_publish_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDashboardPublishOptions", []))

    @jsii.member(jsii_name="resetDefinition")
    def reset_definition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefinition", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetPermissions")
    def reset_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissions", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSourceEntity")
    def reset_source_entity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceEntity", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetThemeArn")
    def reset_theme_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThemeArn", []))

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
    @jsii.member(jsii_name="createdTime")
    def created_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdTime"))

    @builtins.property
    @jsii.member(jsii_name="dashboardPublishOptions")
    def dashboard_publish_options(
        self,
    ) -> "QuicksightDashboardDashboardPublishOptionsOutputReference":
        return typing.cast("QuicksightDashboardDashboardPublishOptionsOutputReference", jsii.get(self, "dashboardPublishOptions"))

    @builtins.property
    @jsii.member(jsii_name="definitionInput")
    def definition_input(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "definitionInput"))

    @builtins.property
    @jsii.member(jsii_name="lastPublishedTime")
    def last_published_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastPublishedTime"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdatedTime")
    def last_updated_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdatedTime"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> "QuicksightDashboardParametersOutputReference":
        return typing.cast("QuicksightDashboardParametersOutputReference", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> "QuicksightDashboardPermissionsList":
        return typing.cast("QuicksightDashboardPermissionsList", jsii.get(self, "permissions"))

    @builtins.property
    @jsii.member(jsii_name="sourceEntity")
    def source_entity(self) -> "QuicksightDashboardSourceEntityOutputReference":
        return typing.cast("QuicksightDashboardSourceEntityOutputReference", jsii.get(self, "sourceEntity"))

    @builtins.property
    @jsii.member(jsii_name="sourceEntityArn")
    def source_entity_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceEntityArn"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "QuicksightDashboardTimeoutsOutputReference":
        return typing.cast("QuicksightDashboardTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="versionNumber")
    def version_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "versionNumber"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountIdInput")
    def aws_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dashboardIdInput")
    def dashboard_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dashboardIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dashboardPublishOptionsInput")
    def dashboard_publish_options_input(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptions"]:
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptions"], jsii.get(self, "dashboardPublishOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(self) -> typing.Optional["QuicksightDashboardParameters"]:
        return typing.cast(typing.Optional["QuicksightDashboardParameters"], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionsInput")
    def permissions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardPermissions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardPermissions"]]], jsii.get(self, "permissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceEntityInput")
    def source_entity_input(self) -> typing.Optional["QuicksightDashboardSourceEntity"]:
        return typing.cast(typing.Optional["QuicksightDashboardSourceEntity"], jsii.get(self, "sourceEntityInput"))

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
    @jsii.member(jsii_name="themeArnInput")
    def theme_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "themeArnInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "QuicksightDashboardTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "QuicksightDashboardTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionDescriptionInput")
    def version_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @aws_account_id.setter
    def aws_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88daa4a3894808dfeab6fd2b715e89587844fee573a94f80d822ac54a38ab189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dashboardId")
    def dashboard_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dashboardId"))

    @dashboard_id.setter
    def dashboard_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c3b86db15463bc5f99a415a0d1a047cc99664c9fc2e2df0bbbc2cffa9bc79a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dashboardId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "definition"))

    @definition.setter
    def definition(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf5d52eccd044659707364ea67529c84f9e7484edb7f400a770cf8f10ad9b45c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b47105c41cdaee8dbef531111e185f482d33816697310e38baa89e9c66a1c73d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaeaf071b8610df5ce70dfaf3e2cdf7c85ec01ee68746870874728014e641887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6907869bf5801dfdfefece023d7a95c8f7fe15c917f8bafc3379c7acaea34c22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c057beb2e3537a0c72ad8ccff361f553de9693266a3da18baf3a61d2669744e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c73f163cc688087243afa2dcba49f544fecabd643bd2af86815d3fda908aac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="themeArn")
    def theme_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "themeArn"))

    @theme_arn.setter
    def theme_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47536d7fe72c65c98c3d4875f1dad303c96311c44fcb55647214723451a9d5d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "themeArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionDescription")
    def version_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionDescription"))

    @version_description.setter
    def version_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05b55e8cb97c182d1e81c0d80073a4736d79c3a234fd6891f924d9a618abad43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionDescription", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "dashboard_id": "dashboardId",
        "name": "name",
        "version_description": "versionDescription",
        "aws_account_id": "awsAccountId",
        "dashboard_publish_options": "dashboardPublishOptions",
        "definition": "definition",
        "id": "id",
        "parameters": "parameters",
        "permissions": "permissions",
        "region": "region",
        "source_entity": "sourceEntity",
        "tags": "tags",
        "tags_all": "tagsAll",
        "theme_arn": "themeArn",
        "timeouts": "timeouts",
    },
)
class QuicksightDashboardConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dashboard_id: builtins.str,
        name: builtins.str,
        version_description: builtins.str,
        aws_account_id: typing.Optional[builtins.str] = None,
        dashboard_publish_options: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        definition: typing.Any = None,
        id: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union["QuicksightDashboardParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardPermissions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        source_entity: typing.Optional[typing.Union["QuicksightDashboardSourceEntity", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        theme_arn: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["QuicksightDashboardTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dashboard_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#dashboard_id QuicksightDashboard#dashboard_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.
        :param version_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#version_description QuicksightDashboard#version_description}.
        :param aws_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#aws_account_id QuicksightDashboard#aws_account_id}.
        :param dashboard_publish_options: dashboard_publish_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#dashboard_publish_options QuicksightDashboard#dashboard_publish_options}
        :param definition: definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#definition QuicksightDashboard#definition}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#id QuicksightDashboard#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#parameters QuicksightDashboard#parameters}
        :param permissions: permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#permissions QuicksightDashboard#permissions}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#region QuicksightDashboard#region}
        :param source_entity: source_entity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#source_entity QuicksightDashboard#source_entity}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#tags QuicksightDashboard#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#tags_all QuicksightDashboard#tags_all}.
        :param theme_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#theme_arn QuicksightDashboard#theme_arn}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#timeouts QuicksightDashboard#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(dashboard_publish_options, dict):
            dashboard_publish_options = QuicksightDashboardDashboardPublishOptions(**dashboard_publish_options)
        if isinstance(parameters, dict):
            parameters = QuicksightDashboardParameters(**parameters)
        if isinstance(source_entity, dict):
            source_entity = QuicksightDashboardSourceEntity(**source_entity)
        if isinstance(timeouts, dict):
            timeouts = QuicksightDashboardTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2afde40d98d11c03fc5664c2400b67700b374156be5ca5d9601310eb62a049e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument dashboard_id", value=dashboard_id, expected_type=type_hints["dashboard_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument version_description", value=version_description, expected_type=type_hints["version_description"])
            check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
            check_type(argname="argument dashboard_publish_options", value=dashboard_publish_options, expected_type=type_hints["dashboard_publish_options"])
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument source_entity", value=source_entity, expected_type=type_hints["source_entity"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument theme_arn", value=theme_arn, expected_type=type_hints["theme_arn"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dashboard_id": dashboard_id,
            "name": name,
            "version_description": version_description,
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
        if aws_account_id is not None:
            self._values["aws_account_id"] = aws_account_id
        if dashboard_publish_options is not None:
            self._values["dashboard_publish_options"] = dashboard_publish_options
        if definition is not None:
            self._values["definition"] = definition
        if id is not None:
            self._values["id"] = id
        if parameters is not None:
            self._values["parameters"] = parameters
        if permissions is not None:
            self._values["permissions"] = permissions
        if region is not None:
            self._values["region"] = region
        if source_entity is not None:
            self._values["source_entity"] = source_entity
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if theme_arn is not None:
            self._values["theme_arn"] = theme_arn
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
    def dashboard_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#dashboard_id QuicksightDashboard#dashboard_id}.'''
        result = self._values.get("dashboard_id")
        assert result is not None, "Required property 'dashboard_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version_description(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#version_description QuicksightDashboard#version_description}.'''
        result = self._values.get("version_description")
        assert result is not None, "Required property 'version_description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#aws_account_id QuicksightDashboard#aws_account_id}.'''
        result = self._values.get("aws_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dashboard_publish_options(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptions"]:
        '''dashboard_publish_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#dashboard_publish_options QuicksightDashboard#dashboard_publish_options}
        '''
        result = self._values.get("dashboard_publish_options")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptions"], result)

    @builtins.property
    def definition(self) -> typing.Any:
        '''definition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#definition QuicksightDashboard#definition}
        '''
        result = self._values.get("definition")
        return typing.cast(typing.Any, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#id QuicksightDashboard#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional["QuicksightDashboardParameters"]:
        '''parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#parameters QuicksightDashboard#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional["QuicksightDashboardParameters"], result)

    @builtins.property
    def permissions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardPermissions"]]]:
        '''permissions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#permissions QuicksightDashboard#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardPermissions"]]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#region QuicksightDashboard#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_entity(self) -> typing.Optional["QuicksightDashboardSourceEntity"]:
        '''source_entity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#source_entity QuicksightDashboard#source_entity}
        '''
        result = self._values.get("source_entity")
        return typing.cast(typing.Optional["QuicksightDashboardSourceEntity"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#tags QuicksightDashboard#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#tags_all QuicksightDashboard#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def theme_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#theme_arn QuicksightDashboard#theme_arn}.'''
        result = self._values.get("theme_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["QuicksightDashboardTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#timeouts QuicksightDashboard#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["QuicksightDashboardTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptions",
    jsii_struct_bases=[],
    name_mapping={
        "ad_hoc_filtering_option": "adHocFilteringOption",
        "data_point_drill_up_down_option": "dataPointDrillUpDownOption",
        "data_point_menu_label_option": "dataPointMenuLabelOption",
        "data_point_tooltip_option": "dataPointTooltipOption",
        "export_to_csv_option": "exportToCsvOption",
        "export_with_hidden_fields_option": "exportWithHiddenFieldsOption",
        "sheet_controls_option": "sheetControlsOption",
        "sheet_layout_element_maximization_option": "sheetLayoutElementMaximizationOption",
        "visual_axis_sort_option": "visualAxisSortOption",
        "visual_menu_option": "visualMenuOption",
    },
)
class QuicksightDashboardDashboardPublishOptions:
    def __init__(
        self,
        *,
        ad_hoc_filtering_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption", typing.Dict[builtins.str, typing.Any]]] = None,
        data_point_drill_up_down_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption", typing.Dict[builtins.str, typing.Any]]] = None,
        data_point_menu_label_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption", typing.Dict[builtins.str, typing.Any]]] = None,
        data_point_tooltip_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption", typing.Dict[builtins.str, typing.Any]]] = None,
        export_to_csv_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsExportToCsvOption", typing.Dict[builtins.str, typing.Any]]] = None,
        export_with_hidden_fields_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption", typing.Dict[builtins.str, typing.Any]]] = None,
        sheet_controls_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsSheetControlsOption", typing.Dict[builtins.str, typing.Any]]] = None,
        sheet_layout_element_maximization_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption", typing.Dict[builtins.str, typing.Any]]] = None,
        visual_axis_sort_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption", typing.Dict[builtins.str, typing.Any]]] = None,
        visual_menu_option: typing.Optional[typing.Union["QuicksightDashboardDashboardPublishOptionsVisualMenuOption", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ad_hoc_filtering_option: ad_hoc_filtering_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#ad_hoc_filtering_option QuicksightDashboard#ad_hoc_filtering_option}
        :param data_point_drill_up_down_option: data_point_drill_up_down_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#data_point_drill_up_down_option QuicksightDashboard#data_point_drill_up_down_option}
        :param data_point_menu_label_option: data_point_menu_label_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#data_point_menu_label_option QuicksightDashboard#data_point_menu_label_option}
        :param data_point_tooltip_option: data_point_tooltip_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#data_point_tooltip_option QuicksightDashboard#data_point_tooltip_option}
        :param export_to_csv_option: export_to_csv_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#export_to_csv_option QuicksightDashboard#export_to_csv_option}
        :param export_with_hidden_fields_option: export_with_hidden_fields_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#export_with_hidden_fields_option QuicksightDashboard#export_with_hidden_fields_option}
        :param sheet_controls_option: sheet_controls_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#sheet_controls_option QuicksightDashboard#sheet_controls_option}
        :param sheet_layout_element_maximization_option: sheet_layout_element_maximization_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#sheet_layout_element_maximization_option QuicksightDashboard#sheet_layout_element_maximization_option}
        :param visual_axis_sort_option: visual_axis_sort_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#visual_axis_sort_option QuicksightDashboard#visual_axis_sort_option}
        :param visual_menu_option: visual_menu_option block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#visual_menu_option QuicksightDashboard#visual_menu_option}
        '''
        if isinstance(ad_hoc_filtering_option, dict):
            ad_hoc_filtering_option = QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption(**ad_hoc_filtering_option)
        if isinstance(data_point_drill_up_down_option, dict):
            data_point_drill_up_down_option = QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption(**data_point_drill_up_down_option)
        if isinstance(data_point_menu_label_option, dict):
            data_point_menu_label_option = QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption(**data_point_menu_label_option)
        if isinstance(data_point_tooltip_option, dict):
            data_point_tooltip_option = QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption(**data_point_tooltip_option)
        if isinstance(export_to_csv_option, dict):
            export_to_csv_option = QuicksightDashboardDashboardPublishOptionsExportToCsvOption(**export_to_csv_option)
        if isinstance(export_with_hidden_fields_option, dict):
            export_with_hidden_fields_option = QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption(**export_with_hidden_fields_option)
        if isinstance(sheet_controls_option, dict):
            sheet_controls_option = QuicksightDashboardDashboardPublishOptionsSheetControlsOption(**sheet_controls_option)
        if isinstance(sheet_layout_element_maximization_option, dict):
            sheet_layout_element_maximization_option = QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption(**sheet_layout_element_maximization_option)
        if isinstance(visual_axis_sort_option, dict):
            visual_axis_sort_option = QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption(**visual_axis_sort_option)
        if isinstance(visual_menu_option, dict):
            visual_menu_option = QuicksightDashboardDashboardPublishOptionsVisualMenuOption(**visual_menu_option)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccb893b99528dda9a987ec9186e87705e3d6af3978025b890f9edf52a9beaff2)
            check_type(argname="argument ad_hoc_filtering_option", value=ad_hoc_filtering_option, expected_type=type_hints["ad_hoc_filtering_option"])
            check_type(argname="argument data_point_drill_up_down_option", value=data_point_drill_up_down_option, expected_type=type_hints["data_point_drill_up_down_option"])
            check_type(argname="argument data_point_menu_label_option", value=data_point_menu_label_option, expected_type=type_hints["data_point_menu_label_option"])
            check_type(argname="argument data_point_tooltip_option", value=data_point_tooltip_option, expected_type=type_hints["data_point_tooltip_option"])
            check_type(argname="argument export_to_csv_option", value=export_to_csv_option, expected_type=type_hints["export_to_csv_option"])
            check_type(argname="argument export_with_hidden_fields_option", value=export_with_hidden_fields_option, expected_type=type_hints["export_with_hidden_fields_option"])
            check_type(argname="argument sheet_controls_option", value=sheet_controls_option, expected_type=type_hints["sheet_controls_option"])
            check_type(argname="argument sheet_layout_element_maximization_option", value=sheet_layout_element_maximization_option, expected_type=type_hints["sheet_layout_element_maximization_option"])
            check_type(argname="argument visual_axis_sort_option", value=visual_axis_sort_option, expected_type=type_hints["visual_axis_sort_option"])
            check_type(argname="argument visual_menu_option", value=visual_menu_option, expected_type=type_hints["visual_menu_option"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ad_hoc_filtering_option is not None:
            self._values["ad_hoc_filtering_option"] = ad_hoc_filtering_option
        if data_point_drill_up_down_option is not None:
            self._values["data_point_drill_up_down_option"] = data_point_drill_up_down_option
        if data_point_menu_label_option is not None:
            self._values["data_point_menu_label_option"] = data_point_menu_label_option
        if data_point_tooltip_option is not None:
            self._values["data_point_tooltip_option"] = data_point_tooltip_option
        if export_to_csv_option is not None:
            self._values["export_to_csv_option"] = export_to_csv_option
        if export_with_hidden_fields_option is not None:
            self._values["export_with_hidden_fields_option"] = export_with_hidden_fields_option
        if sheet_controls_option is not None:
            self._values["sheet_controls_option"] = sheet_controls_option
        if sheet_layout_element_maximization_option is not None:
            self._values["sheet_layout_element_maximization_option"] = sheet_layout_element_maximization_option
        if visual_axis_sort_option is not None:
            self._values["visual_axis_sort_option"] = visual_axis_sort_option
        if visual_menu_option is not None:
            self._values["visual_menu_option"] = visual_menu_option

    @builtins.property
    def ad_hoc_filtering_option(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption"]:
        '''ad_hoc_filtering_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#ad_hoc_filtering_option QuicksightDashboard#ad_hoc_filtering_option}
        '''
        result = self._values.get("ad_hoc_filtering_option")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption"], result)

    @builtins.property
    def data_point_drill_up_down_option(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption"]:
        '''data_point_drill_up_down_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#data_point_drill_up_down_option QuicksightDashboard#data_point_drill_up_down_option}
        '''
        result = self._values.get("data_point_drill_up_down_option")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption"], result)

    @builtins.property
    def data_point_menu_label_option(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption"]:
        '''data_point_menu_label_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#data_point_menu_label_option QuicksightDashboard#data_point_menu_label_option}
        '''
        result = self._values.get("data_point_menu_label_option")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption"], result)

    @builtins.property
    def data_point_tooltip_option(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption"]:
        '''data_point_tooltip_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#data_point_tooltip_option QuicksightDashboard#data_point_tooltip_option}
        '''
        result = self._values.get("data_point_tooltip_option")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption"], result)

    @builtins.property
    def export_to_csv_option(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsExportToCsvOption"]:
        '''export_to_csv_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#export_to_csv_option QuicksightDashboard#export_to_csv_option}
        '''
        result = self._values.get("export_to_csv_option")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsExportToCsvOption"], result)

    @builtins.property
    def export_with_hidden_fields_option(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption"]:
        '''export_with_hidden_fields_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#export_with_hidden_fields_option QuicksightDashboard#export_with_hidden_fields_option}
        '''
        result = self._values.get("export_with_hidden_fields_option")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption"], result)

    @builtins.property
    def sheet_controls_option(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsSheetControlsOption"]:
        '''sheet_controls_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#sheet_controls_option QuicksightDashboard#sheet_controls_option}
        '''
        result = self._values.get("sheet_controls_option")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsSheetControlsOption"], result)

    @builtins.property
    def sheet_layout_element_maximization_option(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption"]:
        '''sheet_layout_element_maximization_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#sheet_layout_element_maximization_option QuicksightDashboard#sheet_layout_element_maximization_option}
        '''
        result = self._values.get("sheet_layout_element_maximization_option")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption"], result)

    @builtins.property
    def visual_axis_sort_option(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption"]:
        '''visual_axis_sort_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#visual_axis_sort_option QuicksightDashboard#visual_axis_sort_option}
        '''
        result = self._values.get("visual_axis_sort_option")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption"], result)

    @builtins.property
    def visual_menu_option(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsVisualMenuOption"]:
        '''visual_menu_option block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#visual_menu_option QuicksightDashboard#visual_menu_option}
        '''
        result = self._values.get("visual_menu_option")
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsVisualMenuOption"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption",
    jsii_struct_bases=[],
    name_mapping={"availability_status": "availabilityStatus"},
)
class QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption:
    def __init__(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b1922c457c52618e87d6258b5e5b0bde126da7e468b3ef476d73744df36c91)
            check_type(argname="argument availability_status", value=availability_status, expected_type=type_hints["availability_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_status is not None:
            self._values["availability_status"] = availability_status

    @builtins.property
    def availability_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.'''
        result = self._values.get("availability_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardDashboardPublishOptionsAdHocFilteringOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsAdHocFilteringOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c752c4fed1cf0f5fa265fd6d37fbdb1f9d4d0791a6ffc48fecd949d7537ab29)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailabilityStatus")
    def reset_availability_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityStatus", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatusInput")
    def availability_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatus")
    def availability_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityStatus"))

    @availability_status.setter
    def availability_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__affd758886b5dd4db1b4b51bbb7aaa248d798258cf8ed4b04d26db8dcb5e86b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75bba562c66fc61539b61cbabd53031ef9a527a62f8fa41d59450ef580199f9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption",
    jsii_struct_bases=[],
    name_mapping={"availability_status": "availabilityStatus"},
)
class QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption:
    def __init__(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edc263f94817ac647820355d8235c9accccdf542207c053d4d8b3cb8a5b5fe3c)
            check_type(argname="argument availability_status", value=availability_status, expected_type=type_hints["availability_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_status is not None:
            self._values["availability_status"] = availability_status

    @builtins.property
    def availability_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.'''
        result = self._values.get("availability_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c05640e1665dcb5491d77cea5f6dffe0da1542aad3e9f57e5d011d5527b1a02)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailabilityStatus")
    def reset_availability_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityStatus", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatusInput")
    def availability_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatus")
    def availability_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityStatus"))

    @availability_status.setter
    def availability_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c5c74e5999d56468fba26d69215c0d5f76b72fe8a33249822843f287513d3de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7663b8b45f7ad0a4e8ac893b17c5d2f3d8d76a28e3a467ba24cc7bb61fce91c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption",
    jsii_struct_bases=[],
    name_mapping={"availability_status": "availabilityStatus"},
)
class QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption:
    def __init__(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceccd7aa7602bfbe72243fbc02699342a07ac515d6252ee4c62b14fc3636bd5e)
            check_type(argname="argument availability_status", value=availability_status, expected_type=type_hints["availability_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_status is not None:
            self._values["availability_status"] = availability_status

    @builtins.property
    def availability_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.'''
        result = self._values.get("availability_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bc88b26802f8118ab5a4408e4fb98a79b8c08bfdca2d6231a0fe5b7112a0133)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailabilityStatus")
    def reset_availability_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityStatus", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatusInput")
    def availability_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatus")
    def availability_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityStatus"))

    @availability_status.setter
    def availability_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30842c1e61cb71171c4a1ddda55c37dc62844d55bfbd9c6bafb839daf1352778)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__446d941292da420c72ee8942c6dd49d5409f8579268016baa0ddfd1520585342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption",
    jsii_struct_bases=[],
    name_mapping={"availability_status": "availabilityStatus"},
)
class QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption:
    def __init__(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572ecfa7cb01c32f83e0f0027842293b86a990a870a77e09854c5282cffb48ac)
            check_type(argname="argument availability_status", value=availability_status, expected_type=type_hints["availability_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_status is not None:
            self._values["availability_status"] = availability_status

    @builtins.property
    def availability_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.'''
        result = self._values.get("availability_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardDashboardPublishOptionsDataPointTooltipOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsDataPointTooltipOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e7052a273d26c3c57bbbacba116d712227bfab297f9f5c6f25cceed50ae4eb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailabilityStatus")
    def reset_availability_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityStatus", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatusInput")
    def availability_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatus")
    def availability_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityStatus"))

    @availability_status.setter
    def availability_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d11ab6c6a92f9cf94d3bc3cce73e8e14c8295c0cb6bb2f574613bc2a53cc6450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c11702d21886567d1a113a7e0d896446702adaa987e1f0290549e9ce290431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsExportToCsvOption",
    jsii_struct_bases=[],
    name_mapping={"availability_status": "availabilityStatus"},
)
class QuicksightDashboardDashboardPublishOptionsExportToCsvOption:
    def __init__(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5c7c3bccb7eabd54d6030242608ca2317e98a597779244aa642173ca2c9ddc)
            check_type(argname="argument availability_status", value=availability_status, expected_type=type_hints["availability_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_status is not None:
            self._values["availability_status"] = availability_status

    @builtins.property
    def availability_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.'''
        result = self._values.get("availability_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptionsExportToCsvOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardDashboardPublishOptionsExportToCsvOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsExportToCsvOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fddb319a999cb82b045e693975ea0529801014475e185f40010934ed2227efd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailabilityStatus")
    def reset_availability_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityStatus", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatusInput")
    def availability_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatus")
    def availability_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityStatus"))

    @availability_status.setter
    def availability_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e67ebf0cf34b5da1b0e53b86722995a53998e804e940b4d5ffe6efd529d30eba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsExportToCsvOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsExportToCsvOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptionsExportToCsvOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f248d110b7767bb74de8e065c7bd753026a06e90bba68ca3b659484dda919d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption",
    jsii_struct_bases=[],
    name_mapping={"availability_status": "availabilityStatus"},
)
class QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption:
    def __init__(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dc81a978f10e7926365637e9740158ddee70a1f49b25418bd4d85603e794992)
            check_type(argname="argument availability_status", value=availability_status, expected_type=type_hints["availability_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_status is not None:
            self._values["availability_status"] = availability_status

    @builtins.property
    def availability_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.'''
        result = self._values.get("availability_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2734972f592ece1da8c64519828e849e5463fafafb9b39dce79e9749a8758dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailabilityStatus")
    def reset_availability_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityStatus", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatusInput")
    def availability_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatus")
    def availability_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityStatus"))

    @availability_status.setter
    def availability_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a636829de24beef305dc9dbddb4443626cdcf3688de66dc9775fd52f518f040f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c209b65e423ca7ff8f86596bd44536c48bd80a4bc6655dcc41ff7573ec45adf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDashboardDashboardPublishOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6edcb4130fbda57ec2e91632d158cda7b1b523e33c9ad7b00388e00ebdf8de4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdHocFilteringOption")
    def put_ad_hoc_filtering_option(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        value = QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption(
            availability_status=availability_status
        )

        return typing.cast(None, jsii.invoke(self, "putAdHocFilteringOption", [value]))

    @jsii.member(jsii_name="putDataPointDrillUpDownOption")
    def put_data_point_drill_up_down_option(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        value = QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption(
            availability_status=availability_status
        )

        return typing.cast(None, jsii.invoke(self, "putDataPointDrillUpDownOption", [value]))

    @jsii.member(jsii_name="putDataPointMenuLabelOption")
    def put_data_point_menu_label_option(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        value = QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption(
            availability_status=availability_status
        )

        return typing.cast(None, jsii.invoke(self, "putDataPointMenuLabelOption", [value]))

    @jsii.member(jsii_name="putDataPointTooltipOption")
    def put_data_point_tooltip_option(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        value = QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption(
            availability_status=availability_status
        )

        return typing.cast(None, jsii.invoke(self, "putDataPointTooltipOption", [value]))

    @jsii.member(jsii_name="putExportToCsvOption")
    def put_export_to_csv_option(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        value = QuicksightDashboardDashboardPublishOptionsExportToCsvOption(
            availability_status=availability_status
        )

        return typing.cast(None, jsii.invoke(self, "putExportToCsvOption", [value]))

    @jsii.member(jsii_name="putExportWithHiddenFieldsOption")
    def put_export_with_hidden_fields_option(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        value = QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption(
            availability_status=availability_status
        )

        return typing.cast(None, jsii.invoke(self, "putExportWithHiddenFieldsOption", [value]))

    @jsii.member(jsii_name="putSheetControlsOption")
    def put_sheet_controls_option(
        self,
        *,
        visibility_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param visibility_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#visibility_state QuicksightDashboard#visibility_state}.
        '''
        value = QuicksightDashboardDashboardPublishOptionsSheetControlsOption(
            visibility_state=visibility_state
        )

        return typing.cast(None, jsii.invoke(self, "putSheetControlsOption", [value]))

    @jsii.member(jsii_name="putSheetLayoutElementMaximizationOption")
    def put_sheet_layout_element_maximization_option(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        value = QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption(
            availability_status=availability_status
        )

        return typing.cast(None, jsii.invoke(self, "putSheetLayoutElementMaximizationOption", [value]))

    @jsii.member(jsii_name="putVisualAxisSortOption")
    def put_visual_axis_sort_option(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        value = QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption(
            availability_status=availability_status
        )

        return typing.cast(None, jsii.invoke(self, "putVisualAxisSortOption", [value]))

    @jsii.member(jsii_name="putVisualMenuOption")
    def put_visual_menu_option(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        value = QuicksightDashboardDashboardPublishOptionsVisualMenuOption(
            availability_status=availability_status
        )

        return typing.cast(None, jsii.invoke(self, "putVisualMenuOption", [value]))

    @jsii.member(jsii_name="resetAdHocFilteringOption")
    def reset_ad_hoc_filtering_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdHocFilteringOption", []))

    @jsii.member(jsii_name="resetDataPointDrillUpDownOption")
    def reset_data_point_drill_up_down_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataPointDrillUpDownOption", []))

    @jsii.member(jsii_name="resetDataPointMenuLabelOption")
    def reset_data_point_menu_label_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataPointMenuLabelOption", []))

    @jsii.member(jsii_name="resetDataPointTooltipOption")
    def reset_data_point_tooltip_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataPointTooltipOption", []))

    @jsii.member(jsii_name="resetExportToCsvOption")
    def reset_export_to_csv_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportToCsvOption", []))

    @jsii.member(jsii_name="resetExportWithHiddenFieldsOption")
    def reset_export_with_hidden_fields_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportWithHiddenFieldsOption", []))

    @jsii.member(jsii_name="resetSheetControlsOption")
    def reset_sheet_controls_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSheetControlsOption", []))

    @jsii.member(jsii_name="resetSheetLayoutElementMaximizationOption")
    def reset_sheet_layout_element_maximization_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSheetLayoutElementMaximizationOption", []))

    @jsii.member(jsii_name="resetVisualAxisSortOption")
    def reset_visual_axis_sort_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisualAxisSortOption", []))

    @jsii.member(jsii_name="resetVisualMenuOption")
    def reset_visual_menu_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisualMenuOption", []))

    @builtins.property
    @jsii.member(jsii_name="adHocFilteringOption")
    def ad_hoc_filtering_option(
        self,
    ) -> QuicksightDashboardDashboardPublishOptionsAdHocFilteringOptionOutputReference:
        return typing.cast(QuicksightDashboardDashboardPublishOptionsAdHocFilteringOptionOutputReference, jsii.get(self, "adHocFilteringOption"))

    @builtins.property
    @jsii.member(jsii_name="dataPointDrillUpDownOption")
    def data_point_drill_up_down_option(
        self,
    ) -> QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOptionOutputReference:
        return typing.cast(QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOptionOutputReference, jsii.get(self, "dataPointDrillUpDownOption"))

    @builtins.property
    @jsii.member(jsii_name="dataPointMenuLabelOption")
    def data_point_menu_label_option(
        self,
    ) -> QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOptionOutputReference:
        return typing.cast(QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOptionOutputReference, jsii.get(self, "dataPointMenuLabelOption"))

    @builtins.property
    @jsii.member(jsii_name="dataPointTooltipOption")
    def data_point_tooltip_option(
        self,
    ) -> QuicksightDashboardDashboardPublishOptionsDataPointTooltipOptionOutputReference:
        return typing.cast(QuicksightDashboardDashboardPublishOptionsDataPointTooltipOptionOutputReference, jsii.get(self, "dataPointTooltipOption"))

    @builtins.property
    @jsii.member(jsii_name="exportToCsvOption")
    def export_to_csv_option(
        self,
    ) -> QuicksightDashboardDashboardPublishOptionsExportToCsvOptionOutputReference:
        return typing.cast(QuicksightDashboardDashboardPublishOptionsExportToCsvOptionOutputReference, jsii.get(self, "exportToCsvOption"))

    @builtins.property
    @jsii.member(jsii_name="exportWithHiddenFieldsOption")
    def export_with_hidden_fields_option(
        self,
    ) -> QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOptionOutputReference:
        return typing.cast(QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOptionOutputReference, jsii.get(self, "exportWithHiddenFieldsOption"))

    @builtins.property
    @jsii.member(jsii_name="sheetControlsOption")
    def sheet_controls_option(
        self,
    ) -> "QuicksightDashboardDashboardPublishOptionsSheetControlsOptionOutputReference":
        return typing.cast("QuicksightDashboardDashboardPublishOptionsSheetControlsOptionOutputReference", jsii.get(self, "sheetControlsOption"))

    @builtins.property
    @jsii.member(jsii_name="sheetLayoutElementMaximizationOption")
    def sheet_layout_element_maximization_option(
        self,
    ) -> "QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOptionOutputReference":
        return typing.cast("QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOptionOutputReference", jsii.get(self, "sheetLayoutElementMaximizationOption"))

    @builtins.property
    @jsii.member(jsii_name="visualAxisSortOption")
    def visual_axis_sort_option(
        self,
    ) -> "QuicksightDashboardDashboardPublishOptionsVisualAxisSortOptionOutputReference":
        return typing.cast("QuicksightDashboardDashboardPublishOptionsVisualAxisSortOptionOutputReference", jsii.get(self, "visualAxisSortOption"))

    @builtins.property
    @jsii.member(jsii_name="visualMenuOption")
    def visual_menu_option(
        self,
    ) -> "QuicksightDashboardDashboardPublishOptionsVisualMenuOptionOutputReference":
        return typing.cast("QuicksightDashboardDashboardPublishOptionsVisualMenuOptionOutputReference", jsii.get(self, "visualMenuOption"))

    @builtins.property
    @jsii.member(jsii_name="adHocFilteringOptionInput")
    def ad_hoc_filtering_option_input(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption], jsii.get(self, "adHocFilteringOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dataPointDrillUpDownOptionInput")
    def data_point_drill_up_down_option_input(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption], jsii.get(self, "dataPointDrillUpDownOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dataPointMenuLabelOptionInput")
    def data_point_menu_label_option_input(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption], jsii.get(self, "dataPointMenuLabelOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dataPointTooltipOptionInput")
    def data_point_tooltip_option_input(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption], jsii.get(self, "dataPointTooltipOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="exportToCsvOptionInput")
    def export_to_csv_option_input(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsExportToCsvOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsExportToCsvOption], jsii.get(self, "exportToCsvOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="exportWithHiddenFieldsOptionInput")
    def export_with_hidden_fields_option_input(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption], jsii.get(self, "exportWithHiddenFieldsOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="sheetControlsOptionInput")
    def sheet_controls_option_input(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsSheetControlsOption"]:
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsSheetControlsOption"], jsii.get(self, "sheetControlsOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="sheetLayoutElementMaximizationOptionInput")
    def sheet_layout_element_maximization_option_input(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption"]:
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption"], jsii.get(self, "sheetLayoutElementMaximizationOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="visualAxisSortOptionInput")
    def visual_axis_sort_option_input(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption"]:
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption"], jsii.get(self, "visualAxisSortOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="visualMenuOptionInput")
    def visual_menu_option_input(
        self,
    ) -> typing.Optional["QuicksightDashboardDashboardPublishOptionsVisualMenuOption"]:
        return typing.cast(typing.Optional["QuicksightDashboardDashboardPublishOptionsVisualMenuOption"], jsii.get(self, "visualMenuOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptions]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9008c973ca360e532c537a55ed0673c96aa8aadae3790e9d82d5933763915fd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsSheetControlsOption",
    jsii_struct_bases=[],
    name_mapping={"visibility_state": "visibilityState"},
)
class QuicksightDashboardDashboardPublishOptionsSheetControlsOption:
    def __init__(
        self,
        *,
        visibility_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param visibility_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#visibility_state QuicksightDashboard#visibility_state}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dcb46c516daa186c69ce4561d103db60068a047b9946382e8a4bbd19b3e883b)
            check_type(argname="argument visibility_state", value=visibility_state, expected_type=type_hints["visibility_state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if visibility_state is not None:
            self._values["visibility_state"] = visibility_state

    @builtins.property
    def visibility_state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#visibility_state QuicksightDashboard#visibility_state}.'''
        result = self._values.get("visibility_state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptionsSheetControlsOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardDashboardPublishOptionsSheetControlsOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsSheetControlsOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31914e301ca46ace29bd8f6dd526f4073c5957c7c84c32a6e238dcf202eb296a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetVisibilityState")
    def reset_visibility_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisibilityState", []))

    @builtins.property
    @jsii.member(jsii_name="visibilityStateInput")
    def visibility_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visibilityStateInput"))

    @builtins.property
    @jsii.member(jsii_name="visibilityState")
    def visibility_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibilityState"))

    @visibility_state.setter
    def visibility_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e4d39e749c35c977cffb4baef31c96bcc6612c335a07964db49eabd4145404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibilityState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsSheetControlsOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsSheetControlsOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptionsSheetControlsOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71bfb2fca6ef73d3b7d24e569cec6e8060f52f69394ea7e65067f47f156a48a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption",
    jsii_struct_bases=[],
    name_mapping={"availability_status": "availabilityStatus"},
)
class QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption:
    def __init__(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63c5874f10d12669ef411d931aca5b883b1e55665d8ef55f588824d7dabde3f0)
            check_type(argname="argument availability_status", value=availability_status, expected_type=type_hints["availability_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_status is not None:
            self._values["availability_status"] = availability_status

    @builtins.property
    def availability_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.'''
        result = self._values.get("availability_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6958b43f89a4ddce37a8ce6aad5bab4ae970963464244bc50e11052e6390d341)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailabilityStatus")
    def reset_availability_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityStatus", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatusInput")
    def availability_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatus")
    def availability_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityStatus"))

    @availability_status.setter
    def availability_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f522ca086cdd42ec0acd329c1427b9dab0ac7f306936ed2816e095f049570876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a05e0769b1bd54f93c22387e0e7cd69b75ef048d7d6f44b5f4421b66c3a9871b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption",
    jsii_struct_bases=[],
    name_mapping={"availability_status": "availabilityStatus"},
)
class QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption:
    def __init__(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d3e32e741f89d9f3020709fb3f804fde9b57855538dbd16dc7ddf5e8b269073)
            check_type(argname="argument availability_status", value=availability_status, expected_type=type_hints["availability_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_status is not None:
            self._values["availability_status"] = availability_status

    @builtins.property
    def availability_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.'''
        result = self._values.get("availability_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardDashboardPublishOptionsVisualAxisSortOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsVisualAxisSortOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cd94ce2acca64df61c20073f3ecf5aa06ad50dc9e113f59d4c1d61b774e0680)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailabilityStatus")
    def reset_availability_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityStatus", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatusInput")
    def availability_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatus")
    def availability_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityStatus"))

    @availability_status.setter
    def availability_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__582732287a00261c4a633173a560c33ac425f7420e69f77fd7b68ed1e5c6be22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b22c5887146d885be80ca9ce2816a1562985d198c68f230375282e2f884f22f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsVisualMenuOption",
    jsii_struct_bases=[],
    name_mapping={"availability_status": "availabilityStatus"},
)
class QuicksightDashboardDashboardPublishOptionsVisualMenuOption:
    def __init__(
        self,
        *,
        availability_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__763e6a814c3e309b45a74b82a5872d5474e0085879de0844214f3adf5f7cc31b)
            check_type(argname="argument availability_status", value=availability_status, expected_type=type_hints["availability_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_status is not None:
            self._values["availability_status"] = availability_status

    @builtins.property
    def availability_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#availability_status QuicksightDashboard#availability_status}.'''
        result = self._values.get("availability_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardDashboardPublishOptionsVisualMenuOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardDashboardPublishOptionsVisualMenuOptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardDashboardPublishOptionsVisualMenuOptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be54c00abe2aab912942d79e764ae5d51313e0f37a1fb6c1b3f4fbff5720dfe4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailabilityStatus")
    def reset_availability_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityStatus", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatusInput")
    def availability_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityStatus")
    def availability_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityStatus"))

    @availability_status.setter
    def availability_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9409717badbf70101e5e0573c27b5809f8ed59e968c6960350db12e86d4aab9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardDashboardPublishOptionsVisualMenuOption]:
        return typing.cast(typing.Optional[QuicksightDashboardDashboardPublishOptionsVisualMenuOption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardDashboardPublishOptionsVisualMenuOption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c42d3407dfb71dac4ab6bb72279ab67628f5a0bb773c3696be9e08798c9a9875)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardParameters",
    jsii_struct_bases=[],
    name_mapping={
        "date_time_parameters": "dateTimeParameters",
        "decimal_parameters": "decimalParameters",
        "integer_parameters": "integerParameters",
        "string_parameters": "stringParameters",
    },
)
class QuicksightDashboardParameters:
    def __init__(
        self,
        *,
        date_time_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardParametersDateTimeParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        decimal_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardParametersDecimalParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        integer_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardParametersIntegerParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        string_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardParametersStringParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param date_time_parameters: date_time_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#date_time_parameters QuicksightDashboard#date_time_parameters}
        :param decimal_parameters: decimal_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#decimal_parameters QuicksightDashboard#decimal_parameters}
        :param integer_parameters: integer_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#integer_parameters QuicksightDashboard#integer_parameters}
        :param string_parameters: string_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#string_parameters QuicksightDashboard#string_parameters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9425f93544d344bb5dfe7a539d2bfc4b5645a8f04909676999c943a3ec896904)
            check_type(argname="argument date_time_parameters", value=date_time_parameters, expected_type=type_hints["date_time_parameters"])
            check_type(argname="argument decimal_parameters", value=decimal_parameters, expected_type=type_hints["decimal_parameters"])
            check_type(argname="argument integer_parameters", value=integer_parameters, expected_type=type_hints["integer_parameters"])
            check_type(argname="argument string_parameters", value=string_parameters, expected_type=type_hints["string_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if date_time_parameters is not None:
            self._values["date_time_parameters"] = date_time_parameters
        if decimal_parameters is not None:
            self._values["decimal_parameters"] = decimal_parameters
        if integer_parameters is not None:
            self._values["integer_parameters"] = integer_parameters
        if string_parameters is not None:
            self._values["string_parameters"] = string_parameters

    @builtins.property
    def date_time_parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardParametersDateTimeParameters"]]]:
        '''date_time_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#date_time_parameters QuicksightDashboard#date_time_parameters}
        '''
        result = self._values.get("date_time_parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardParametersDateTimeParameters"]]], result)

    @builtins.property
    def decimal_parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardParametersDecimalParameters"]]]:
        '''decimal_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#decimal_parameters QuicksightDashboard#decimal_parameters}
        '''
        result = self._values.get("decimal_parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardParametersDecimalParameters"]]], result)

    @builtins.property
    def integer_parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardParametersIntegerParameters"]]]:
        '''integer_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#integer_parameters QuicksightDashboard#integer_parameters}
        '''
        result = self._values.get("integer_parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardParametersIntegerParameters"]]], result)

    @builtins.property
    def string_parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardParametersStringParameters"]]]:
        '''string_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#string_parameters QuicksightDashboard#string_parameters}
        '''
        result = self._values.get("string_parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardParametersStringParameters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardParametersDateTimeParameters",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class QuicksightDashboardParametersDateTimeParameters:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#values QuicksightDashboard#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35cbe14c4e14e482b27937dcedb0fb431c4a618e1b9678fc1e2d37bc3897c79f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#values QuicksightDashboard#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardParametersDateTimeParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardParametersDateTimeParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardParametersDateTimeParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ea7de1cd0213a59e70fff4aa838d8439be020691e7cdc3c4b719f75d2d15ee5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDashboardParametersDateTimeParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc7930a4436119e34b0d4b5a099a6d00fda938fdd313f048583f17763bb3c767)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDashboardParametersDateTimeParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__621896ea7938d77a488d0460d924c1e5c44fe08077e24610c755242985efb31e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f1979175c621dafe08953031e5d68ea58d2cfec6bd38618fce261b9dc46304d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__037fb141d7ce6cdbcca72028bdf2d0cf834bf0522e4fcbaf741b18303ecb6141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDateTimeParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDateTimeParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDateTimeParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fbb42f294a44f63415f3e9c645c7171e3c52c387107eec68138477b84405763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDashboardParametersDateTimeParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardParametersDateTimeParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e67a15562833374412e2516824d214759f753355eee3c4998c270407d2892833)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ca4c294e648fd31c9d7ee6106d5bdb40f9d091dc8c9fd08014a2f408f7deef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75dda0f59bbcd4d065f99670172e0776c8a04ea5275d14b0cafd4fb8acefec98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersDateTimeParameters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersDateTimeParameters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersDateTimeParameters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65d89f708fb3530ac19e293f65033c3cf0dc5ca47ae5803633ddd2daf817c1c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardParametersDecimalParameters",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class QuicksightDashboardParametersDecimalParameters:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#values QuicksightDashboard#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__083e90a9066bed7391575720ac1ee0a9946946222e470a88af7017302b3ad69c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#values QuicksightDashboard#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardParametersDecimalParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardParametersDecimalParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardParametersDecimalParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__517ee98c380fc93fc32efbea65e93a171bccc54f62ce31aacf5bf5d37dd28faf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDashboardParametersDecimalParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a6e87d0224973aad2d543ba04724c090a395b190654775d62e8bf406f5cd3e5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDashboardParametersDecimalParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63bc7b60935e05c41a801a0158b675491296b164acc7dfb8391dfde80375a7ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a55f4c9603417724981a86a8728545d4e169ddfc75b12723e93703aa696e5ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5db16d7855f5a4b651441ea4f9cac3d655c2d20f89bac0e42c0cfc2a895f03d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDecimalParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDecimalParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDecimalParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68565e4d4ae7de638ecd0d7510d87e33a4380407be38f36e30bdbef096b535b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDashboardParametersDecimalParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardParametersDecimalParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d69d203a13c221ab0a540f0f15e67b9ea7625e63ead6ab38cda9ff0c75859c8f)
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
    def values_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7f7aa0cb82f681bdf892ed4d12c9a6a17f85f1d9e5bca0b7a05698d4332e03d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__698f35d3b172e70659ee17ba427967920e2f973dc57ce8cad080b5e7b0ffa92b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersDecimalParameters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersDecimalParameters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersDecimalParameters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a54f75462c7d272cbee801e1e34f06a4b3568a0180a379f6b47bfc8d95a0959)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardParametersIntegerParameters",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class QuicksightDashboardParametersIntegerParameters:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#values QuicksightDashboard#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b13bf606d416db34421e65879cdb0c12bab2a3775fdbfb7efe9f3bf0b6a205e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#values QuicksightDashboard#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardParametersIntegerParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardParametersIntegerParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardParametersIntegerParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f10075c98f92028e91cecfd364c8dc8924a5eaa4c7801c92c8c1aec9ca004f45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDashboardParametersIntegerParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4de0231641e1e8128326a61e62b51a77e04317f465f0cc19d1b46bd1f5162d41)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDashboardParametersIntegerParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5766842307494b10bb92187c9469828d65ae77989ed86f2629725d499f9afa9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b571e826dd75e5325775564b8cda704fd3796f204bdac55a9e395d477ed8f78e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d1fb87b64d05822a1270a4558966f339ec675954b131d5c75ef745456eb9a06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersIntegerParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersIntegerParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersIntegerParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eec865cf717f948622c483af6671a2d1d86f4f5b0b5cee62f37992b880e97270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDashboardParametersIntegerParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardParametersIntegerParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__350843606116db0b7e78ea24d355abf198d11979465d493f2d904b338e365682)
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
    def values_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f890d3e2d08c0e5acdf9594cfd5bb2822a8f3721276343718f81da2b4820bb98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2f49a48c8e56fb978e9bd15f31e6fccfc7317fc091ad7c87544912fc531dda7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersIntegerParameters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersIntegerParameters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersIntegerParameters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc3d43ad84e9c73a5b6f3d1c35aa2767db0af6ab824590b8f9bc7c15a16671f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDashboardParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__038d9c892cb47efb80c59bdcca490eddb6c9db7365b2e6874c80bc9776eaeb22)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDateTimeParameters")
    def put_date_time_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersDateTimeParameters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__500314a4ac2125bb057c3664022049f69be2031f60d2b0aaa0d17780b06b3148)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDateTimeParameters", [value]))

    @jsii.member(jsii_name="putDecimalParameters")
    def put_decimal_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersDecimalParameters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d33694ba0aa952debe1f58530524c8fb02dcd0c1366427189cf462486dfdfc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDecimalParameters", [value]))

    @jsii.member(jsii_name="putIntegerParameters")
    def put_integer_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersIntegerParameters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98cf32363eb5cd1f8142d4858ebac7880b929a3cdb7fb989fcfe708b4c687737)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIntegerParameters", [value]))

    @jsii.member(jsii_name="putStringParameters")
    def put_string_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardParametersStringParameters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e8bef1ebcaa41ef058564563a75bcf9be6951fb8cf159d0bf92a66646f6a9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStringParameters", [value]))

    @jsii.member(jsii_name="resetDateTimeParameters")
    def reset_date_time_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateTimeParameters", []))

    @jsii.member(jsii_name="resetDecimalParameters")
    def reset_decimal_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDecimalParameters", []))

    @jsii.member(jsii_name="resetIntegerParameters")
    def reset_integer_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegerParameters", []))

    @jsii.member(jsii_name="resetStringParameters")
    def reset_string_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringParameters", []))

    @builtins.property
    @jsii.member(jsii_name="dateTimeParameters")
    def date_time_parameters(
        self,
    ) -> QuicksightDashboardParametersDateTimeParametersList:
        return typing.cast(QuicksightDashboardParametersDateTimeParametersList, jsii.get(self, "dateTimeParameters"))

    @builtins.property
    @jsii.member(jsii_name="decimalParameters")
    def decimal_parameters(self) -> QuicksightDashboardParametersDecimalParametersList:
        return typing.cast(QuicksightDashboardParametersDecimalParametersList, jsii.get(self, "decimalParameters"))

    @builtins.property
    @jsii.member(jsii_name="integerParameters")
    def integer_parameters(self) -> QuicksightDashboardParametersIntegerParametersList:
        return typing.cast(QuicksightDashboardParametersIntegerParametersList, jsii.get(self, "integerParameters"))

    @builtins.property
    @jsii.member(jsii_name="stringParameters")
    def string_parameters(self) -> "QuicksightDashboardParametersStringParametersList":
        return typing.cast("QuicksightDashboardParametersStringParametersList", jsii.get(self, "stringParameters"))

    @builtins.property
    @jsii.member(jsii_name="dateTimeParametersInput")
    def date_time_parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDateTimeParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDateTimeParameters]]], jsii.get(self, "dateTimeParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="decimalParametersInput")
    def decimal_parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDecimalParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDecimalParameters]]], jsii.get(self, "decimalParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="integerParametersInput")
    def integer_parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersIntegerParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersIntegerParameters]]], jsii.get(self, "integerParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="stringParametersInput")
    def string_parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardParametersStringParameters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardParametersStringParameters"]]], jsii.get(self, "stringParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDashboardParameters]:
        return typing.cast(typing.Optional[QuicksightDashboardParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a5ec08d9c5318d087b2a194a81f3c23266274e85e1712ff41a30fda16e241f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardParametersStringParameters",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class QuicksightDashboardParametersStringParameters:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#values QuicksightDashboard#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e03d27ef566e798845ab6e27a7aa920cb18dd1a57a34789dc4d8cc51e9e75a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#name QuicksightDashboard#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#values QuicksightDashboard#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardParametersStringParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardParametersStringParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardParametersStringParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31ecf6308390013f732b6f5c215063f5568c0409075840001abeb3a83c590e69)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDashboardParametersStringParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6be2a92bf0befbf9d251b2eadefc4b961fccafe9202d14de361fc3dd79805a5e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDashboardParametersStringParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b9ed4357df6ee97ff76dcb846455ec5930a37e1b2c9847e6e05f51972275d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4731f589ad8b0c917e4a14b2d697db9d6ce802d4275ebcc9f21c51da1ec87394)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec014a6b20ac67004f1426b40d492e32af18afa0c44b05c17b1c9810c5026ac2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersStringParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersStringParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersStringParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f5b85e257711b8a72a9608397c1391d8d8a96d7d5a23b1100cd93653e7ecdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDashboardParametersStringParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardParametersStringParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40695655b867ff255f6d76f6adf354cbd90ecf57a8ce647a94ab6f49e355310d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f52f4db777aef10b8f8d87210632851a64851aa51ba4ce59fc0c71d76900bd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b4563b0f7d794bf055c99d0ad372de683e12a8c90cd408c413dc08a305f44b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersStringParameters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersStringParameters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersStringParameters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a913d6eb2be54e9f1b21469adabefc42b1edfdd0efc01c937a9f5b593c0a3985)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardPermissions",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions", "principal": "principal"},
)
class QuicksightDashboardPermissions:
    def __init__(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        principal: builtins.str,
    ) -> None:
        '''
        :param actions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#actions QuicksightDashboard#actions}.
        :param principal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#principal QuicksightDashboard#principal}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e8e66d4a46575b60b5f5cad7079bc11e39efcb18f86fda70b8b040c8cd1ae4d)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "principal": principal,
        }

    @builtins.property
    def actions(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#actions QuicksightDashboard#actions}.'''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def principal(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#principal QuicksightDashboard#principal}.'''
        result = self._values.get("principal")
        assert result is not None, "Required property 'principal' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardPermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardPermissionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardPermissionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df94e836ee874090d8019f2dffe3391c8deebe7d35f24968b6c01cbb2baee937)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDashboardPermissionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da99ff1a9cbb37294f8e02ee6c5e769a0041577855f818fe6245f3175dae53aa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDashboardPermissionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4516a04b5cc7d12d48ee5a86327285db211a089178a964af9c89b41cdd7c63f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6929e9ac0d28cf6c89cf5c576f13faef461dd24b9e50be19266de1899c963811)
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
            type_hints = typing.get_type_hints(_typecheckingstub__919f855eff42eee640676933fda517e202121606be671808b00243994702b116)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardPermissions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardPermissions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardPermissions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fe020350585a537a61a4115a00cf6ab76e2918d76168136f34e55442ca3c234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDashboardPermissionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardPermissionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7959424328cf65b74ffb8e6687181aed1523f0693502099f12a6649f5dd6bd0a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="principalInput")
    def principal_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalInput"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @actions.setter
    def actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7682a76fb4b65fb23ff20f65a9a9093710b3954f157dc90823b0bba12f10748c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principal"))

    @principal.setter
    def principal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__356aa0e2d23c4b33e885eb2585b2fb4a73de74e960324a2387d8e6ddc591284e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardPermissions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardPermissions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardPermissions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dbec55a699585e385e4cff74089f4a42e38fefd7946aff5008e00c598143e32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardSourceEntity",
    jsii_struct_bases=[],
    name_mapping={"source_template": "sourceTemplate"},
)
class QuicksightDashboardSourceEntity:
    def __init__(
        self,
        *,
        source_template: typing.Optional[typing.Union["QuicksightDashboardSourceEntitySourceTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param source_template: source_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#source_template QuicksightDashboard#source_template}
        '''
        if isinstance(source_template, dict):
            source_template = QuicksightDashboardSourceEntitySourceTemplate(**source_template)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ca352f76f0bd739944159150e3f8e75218b5077373288c73e5c9d4ad0eaad3f)
            check_type(argname="argument source_template", value=source_template, expected_type=type_hints["source_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if source_template is not None:
            self._values["source_template"] = source_template

    @builtins.property
    def source_template(
        self,
    ) -> typing.Optional["QuicksightDashboardSourceEntitySourceTemplate"]:
        '''source_template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#source_template QuicksightDashboard#source_template}
        '''
        result = self._values.get("source_template")
        return typing.cast(typing.Optional["QuicksightDashboardSourceEntitySourceTemplate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardSourceEntity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardSourceEntityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardSourceEntityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de8c9974933c926403542afba62780d3b8ce7faf084d60952c9a90bfe107452d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSourceTemplate")
    def put_source_template(
        self,
        *,
        arn: builtins.str,
        data_set_references: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardSourceEntitySourceTemplateDataSetReferences", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#arn QuicksightDashboard#arn}.
        :param data_set_references: data_set_references block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#data_set_references QuicksightDashboard#data_set_references}
        '''
        value = QuicksightDashboardSourceEntitySourceTemplate(
            arn=arn, data_set_references=data_set_references
        )

        return typing.cast(None, jsii.invoke(self, "putSourceTemplate", [value]))

    @jsii.member(jsii_name="resetSourceTemplate")
    def reset_source_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceTemplate", []))

    @builtins.property
    @jsii.member(jsii_name="sourceTemplate")
    def source_template(
        self,
    ) -> "QuicksightDashboardSourceEntitySourceTemplateOutputReference":
        return typing.cast("QuicksightDashboardSourceEntitySourceTemplateOutputReference", jsii.get(self, "sourceTemplate"))

    @builtins.property
    @jsii.member(jsii_name="sourceTemplateInput")
    def source_template_input(
        self,
    ) -> typing.Optional["QuicksightDashboardSourceEntitySourceTemplate"]:
        return typing.cast(typing.Optional["QuicksightDashboardSourceEntitySourceTemplate"], jsii.get(self, "sourceTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDashboardSourceEntity]:
        return typing.cast(typing.Optional[QuicksightDashboardSourceEntity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardSourceEntity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f6ef5fcf350708ef2adf6113c05c95b6a5b84d8408795b11e1b7fadb356a3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardSourceEntitySourceTemplate",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn", "data_set_references": "dataSetReferences"},
)
class QuicksightDashboardSourceEntitySourceTemplate:
    def __init__(
        self,
        *,
        arn: builtins.str,
        data_set_references: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDashboardSourceEntitySourceTemplateDataSetReferences", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#arn QuicksightDashboard#arn}.
        :param data_set_references: data_set_references block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#data_set_references QuicksightDashboard#data_set_references}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a27da7e9a27c33a0efa0e4ff6a134ad285ffd581d9e85dd0c856e008a472236)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument data_set_references", value=data_set_references, expected_type=type_hints["data_set_references"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arn": arn,
            "data_set_references": data_set_references,
        }

    @builtins.property
    def arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#arn QuicksightDashboard#arn}.'''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_set_references(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardSourceEntitySourceTemplateDataSetReferences"]]:
        '''data_set_references block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#data_set_references QuicksightDashboard#data_set_references}
        '''
        result = self._values.get("data_set_references")
        assert result is not None, "Required property 'data_set_references' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDashboardSourceEntitySourceTemplateDataSetReferences"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardSourceEntitySourceTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardSourceEntitySourceTemplateDataSetReferences",
    jsii_struct_bases=[],
    name_mapping={
        "data_set_arn": "dataSetArn",
        "data_set_placeholder": "dataSetPlaceholder",
    },
)
class QuicksightDashboardSourceEntitySourceTemplateDataSetReferences:
    def __init__(
        self,
        *,
        data_set_arn: builtins.str,
        data_set_placeholder: builtins.str,
    ) -> None:
        '''
        :param data_set_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#data_set_arn QuicksightDashboard#data_set_arn}.
        :param data_set_placeholder: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#data_set_placeholder QuicksightDashboard#data_set_placeholder}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9b241abc932032cf22b34ce77c1eb21e053646e9c0d7f2d8c8fb3209134be3e)
            check_type(argname="argument data_set_arn", value=data_set_arn, expected_type=type_hints["data_set_arn"])
            check_type(argname="argument data_set_placeholder", value=data_set_placeholder, expected_type=type_hints["data_set_placeholder"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_set_arn": data_set_arn,
            "data_set_placeholder": data_set_placeholder,
        }

    @builtins.property
    def data_set_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#data_set_arn QuicksightDashboard#data_set_arn}.'''
        result = self._values.get("data_set_arn")
        assert result is not None, "Required property 'data_set_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_set_placeholder(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#data_set_placeholder QuicksightDashboard#data_set_placeholder}.'''
        result = self._values.get("data_set_placeholder")
        assert result is not None, "Required property 'data_set_placeholder' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardSourceEntitySourceTemplateDataSetReferences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardSourceEntitySourceTemplateDataSetReferencesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardSourceEntitySourceTemplateDataSetReferencesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ded5b41635afe959e4dddb4994d911681775f578481184dcc1e2f3c359755f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDashboardSourceEntitySourceTemplateDataSetReferencesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b697c5dbfedce095e06f333c3bf219b043365e085c357fc354b70791cd25453)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDashboardSourceEntitySourceTemplateDataSetReferencesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1f72509488e66b43612c2c1f5e292489273f7e4c9855f7887bac214349e2360)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f06c4149ac3ce4791707f6142f1710a59e04be527c32396522eb5b8a62c6ac7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70ee1e25177a0e19d55ba4e34a8e8f9b8e8ce24760848889f47cae99e80324a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardSourceEntitySourceTemplateDataSetReferences]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardSourceEntitySourceTemplateDataSetReferences]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardSourceEntitySourceTemplateDataSetReferences]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58f9804649ad9c08aafd9d86b051af47e6d93e6b58149ee8799cf54cfe5a9196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDashboardSourceEntitySourceTemplateDataSetReferencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardSourceEntitySourceTemplateDataSetReferencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__718d3c5d9ae8f77b2aa8aa676f56069b6390f41a5a950403e7dc2f36379d157d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dataSetArnInput")
    def data_set_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSetArnInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSetPlaceholderInput")
    def data_set_placeholder_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSetPlaceholderInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSetArn")
    def data_set_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSetArn"))

    @data_set_arn.setter
    def data_set_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3844412d2e3136ff2bf05ec1b535edc75c3d8a9dd2ed348c27399de4092378e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSetArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataSetPlaceholder")
    def data_set_placeholder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSetPlaceholder"))

    @data_set_placeholder.setter
    def data_set_placeholder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a11479e88956303ec94ba097703bde038fe76ec22194280f21033403e4da41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSetPlaceholder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardSourceEntitySourceTemplateDataSetReferences]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardSourceEntitySourceTemplateDataSetReferences]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardSourceEntitySourceTemplateDataSetReferences]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ce0b089e22cb34b49cce16b872c4a14de4b115f95da194e7a07c04ffe62140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDashboardSourceEntitySourceTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardSourceEntitySourceTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__626e7de29f183cf4e17f997cf216348f3d2ec538683daa6f46bca5185b1b1266)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataSetReferences")
    def put_data_set_references(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardSourceEntitySourceTemplateDataSetReferences, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42bf81fb9212b1f26f3b710333db5bf040aea231ea2a83046f554c6804bec533)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataSetReferences", [value]))

    @builtins.property
    @jsii.member(jsii_name="dataSetReferences")
    def data_set_references(
        self,
    ) -> QuicksightDashboardSourceEntitySourceTemplateDataSetReferencesList:
        return typing.cast(QuicksightDashboardSourceEntitySourceTemplateDataSetReferencesList, jsii.get(self, "dataSetReferences"))

    @builtins.property
    @jsii.member(jsii_name="arnInput")
    def arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arnInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSetReferencesInput")
    def data_set_references_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardSourceEntitySourceTemplateDataSetReferences]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardSourceEntitySourceTemplateDataSetReferences]]], jsii.get(self, "dataSetReferencesInput"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1256044661f2dc9a39bc7791168c58a09acf728a2d43b3d9985fa4037263fb4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDashboardSourceEntitySourceTemplate]:
        return typing.cast(typing.Optional[QuicksightDashboardSourceEntitySourceTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDashboardSourceEntitySourceTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f790a07ca91820c04383ca9dd5f2647999237abad8665454918a1af3ea4b9b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class QuicksightDashboardTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#create QuicksightDashboard#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#delete QuicksightDashboard#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#update QuicksightDashboard#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cdf55f751f7306acd9f37b6be963f0913e7ca34af22fd42927da2cb2c311a11)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#create QuicksightDashboard#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#delete QuicksightDashboard#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/quicksight_dashboard#update QuicksightDashboard#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDashboardTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDashboardTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.quicksightDashboard.QuicksightDashboardTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5b089ed98b01801ffd1889176b73ff6990a853e6e34fd978f6e7cabafe8c3d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aafdc25dd2b389a4d000a00494b1b0cb8f4ee34379f7b59d74a10ac4ee4c1b61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba1dc28aa95ee554531e7286f490de847c964f2b485843336f44520a6a26cc95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a54b6e6e49da9dfe365d5ab934fc13575321885e9c566677008ce92618044431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90ec314eda13c23ce7edf66ddd04f8fcefebbec854bed397d3a4ce1a0e98da04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "QuicksightDashboard",
    "QuicksightDashboardConfig",
    "QuicksightDashboardDashboardPublishOptions",
    "QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption",
    "QuicksightDashboardDashboardPublishOptionsAdHocFilteringOptionOutputReference",
    "QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption",
    "QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOptionOutputReference",
    "QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption",
    "QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOptionOutputReference",
    "QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption",
    "QuicksightDashboardDashboardPublishOptionsDataPointTooltipOptionOutputReference",
    "QuicksightDashboardDashboardPublishOptionsExportToCsvOption",
    "QuicksightDashboardDashboardPublishOptionsExportToCsvOptionOutputReference",
    "QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption",
    "QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOptionOutputReference",
    "QuicksightDashboardDashboardPublishOptionsOutputReference",
    "QuicksightDashboardDashboardPublishOptionsSheetControlsOption",
    "QuicksightDashboardDashboardPublishOptionsSheetControlsOptionOutputReference",
    "QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption",
    "QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOptionOutputReference",
    "QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption",
    "QuicksightDashboardDashboardPublishOptionsVisualAxisSortOptionOutputReference",
    "QuicksightDashboardDashboardPublishOptionsVisualMenuOption",
    "QuicksightDashboardDashboardPublishOptionsVisualMenuOptionOutputReference",
    "QuicksightDashboardParameters",
    "QuicksightDashboardParametersDateTimeParameters",
    "QuicksightDashboardParametersDateTimeParametersList",
    "QuicksightDashboardParametersDateTimeParametersOutputReference",
    "QuicksightDashboardParametersDecimalParameters",
    "QuicksightDashboardParametersDecimalParametersList",
    "QuicksightDashboardParametersDecimalParametersOutputReference",
    "QuicksightDashboardParametersIntegerParameters",
    "QuicksightDashboardParametersIntegerParametersList",
    "QuicksightDashboardParametersIntegerParametersOutputReference",
    "QuicksightDashboardParametersOutputReference",
    "QuicksightDashboardParametersStringParameters",
    "QuicksightDashboardParametersStringParametersList",
    "QuicksightDashboardParametersStringParametersOutputReference",
    "QuicksightDashboardPermissions",
    "QuicksightDashboardPermissionsList",
    "QuicksightDashboardPermissionsOutputReference",
    "QuicksightDashboardSourceEntity",
    "QuicksightDashboardSourceEntityOutputReference",
    "QuicksightDashboardSourceEntitySourceTemplate",
    "QuicksightDashboardSourceEntitySourceTemplateDataSetReferences",
    "QuicksightDashboardSourceEntitySourceTemplateDataSetReferencesList",
    "QuicksightDashboardSourceEntitySourceTemplateDataSetReferencesOutputReference",
    "QuicksightDashboardSourceEntitySourceTemplateOutputReference",
    "QuicksightDashboardTimeouts",
    "QuicksightDashboardTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a6f945749e8425615e0d56466b5a27bd905354edc5bd3fa97c48ff2802cabdf7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dashboard_id: builtins.str,
    name: builtins.str,
    version_description: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    dashboard_publish_options: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    definition: typing.Any = None,
    id: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[QuicksightDashboardParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardPermissions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    source_entity: typing.Optional[typing.Union[QuicksightDashboardSourceEntity, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    theme_arn: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[QuicksightDashboardTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f95c4456a0fc1e34e194ab79d38ae74cf0131248438256f90c07b838cbe04a6f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5558401553e68c841440c625c4271d0e8463b4ca33f52d079fd31c908b15cc57(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardPermissions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88daa4a3894808dfeab6fd2b715e89587844fee573a94f80d822ac54a38ab189(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c3b86db15463bc5f99a415a0d1a047cc99664c9fc2e2df0bbbc2cffa9bc79a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf5d52eccd044659707364ea67529c84f9e7484edb7f400a770cf8f10ad9b45c(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47105c41cdaee8dbef531111e185f482d33816697310e38baa89e9c66a1c73d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaeaf071b8610df5ce70dfaf3e2cdf7c85ec01ee68746870874728014e641887(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6907869bf5801dfdfefece023d7a95c8f7fe15c917f8bafc3379c7acaea34c22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c057beb2e3537a0c72ad8ccff361f553de9693266a3da18baf3a61d2669744e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c73f163cc688087243afa2dcba49f544fecabd643bd2af86815d3fda908aac3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47536d7fe72c65c98c3d4875f1dad303c96311c44fcb55647214723451a9d5d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05b55e8cb97c182d1e81c0d80073a4736d79c3a234fd6891f924d9a618abad43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2afde40d98d11c03fc5664c2400b67700b374156be5ca5d9601310eb62a049e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dashboard_id: builtins.str,
    name: builtins.str,
    version_description: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    dashboard_publish_options: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    definition: typing.Any = None,
    id: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[QuicksightDashboardParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardPermissions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    source_entity: typing.Optional[typing.Union[QuicksightDashboardSourceEntity, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    theme_arn: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[QuicksightDashboardTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb893b99528dda9a987ec9186e87705e3d6af3978025b890f9edf52a9beaff2(
    *,
    ad_hoc_filtering_option: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption, typing.Dict[builtins.str, typing.Any]]] = None,
    data_point_drill_up_down_option: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption, typing.Dict[builtins.str, typing.Any]]] = None,
    data_point_menu_label_option: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption, typing.Dict[builtins.str, typing.Any]]] = None,
    data_point_tooltip_option: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption, typing.Dict[builtins.str, typing.Any]]] = None,
    export_to_csv_option: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptionsExportToCsvOption, typing.Dict[builtins.str, typing.Any]]] = None,
    export_with_hidden_fields_option: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption, typing.Dict[builtins.str, typing.Any]]] = None,
    sheet_controls_option: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptionsSheetControlsOption, typing.Dict[builtins.str, typing.Any]]] = None,
    sheet_layout_element_maximization_option: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption, typing.Dict[builtins.str, typing.Any]]] = None,
    visual_axis_sort_option: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption, typing.Dict[builtins.str, typing.Any]]] = None,
    visual_menu_option: typing.Optional[typing.Union[QuicksightDashboardDashboardPublishOptionsVisualMenuOption, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b1922c457c52618e87d6258b5e5b0bde126da7e468b3ef476d73744df36c91(
    *,
    availability_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c752c4fed1cf0f5fa265fd6d37fbdb1f9d4d0791a6ffc48fecd949d7537ab29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__affd758886b5dd4db1b4b51bbb7aaa248d798258cf8ed4b04d26db8dcb5e86b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75bba562c66fc61539b61cbabd53031ef9a527a62f8fa41d59450ef580199f9e(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptionsAdHocFilteringOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edc263f94817ac647820355d8235c9accccdf542207c053d4d8b3cb8a5b5fe3c(
    *,
    availability_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c05640e1665dcb5491d77cea5f6dffe0da1542aad3e9f57e5d011d5527b1a02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c5c74e5999d56468fba26d69215c0d5f76b72fe8a33249822843f287513d3de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7663b8b45f7ad0a4e8ac893b17c5d2f3d8d76a28e3a467ba24cc7bb61fce91c7(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointDrillUpDownOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceccd7aa7602bfbe72243fbc02699342a07ac515d6252ee4c62b14fc3636bd5e(
    *,
    availability_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc88b26802f8118ab5a4408e4fb98a79b8c08bfdca2d6231a0fe5b7112a0133(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30842c1e61cb71171c4a1ddda55c37dc62844d55bfbd9c6bafb839daf1352778(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__446d941292da420c72ee8942c6dd49d5409f8579268016baa0ddfd1520585342(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointMenuLabelOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572ecfa7cb01c32f83e0f0027842293b86a990a870a77e09854c5282cffb48ac(
    *,
    availability_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7052a273d26c3c57bbbacba116d712227bfab297f9f5c6f25cceed50ae4eb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d11ab6c6a92f9cf94d3bc3cce73e8e14c8295c0cb6bb2f574613bc2a53cc6450(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c11702d21886567d1a113a7e0d896446702adaa987e1f0290549e9ce290431(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptionsDataPointTooltipOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5c7c3bccb7eabd54d6030242608ca2317e98a597779244aa642173ca2c9ddc(
    *,
    availability_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fddb319a999cb82b045e693975ea0529801014475e185f40010934ed2227efd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67ebf0cf34b5da1b0e53b86722995a53998e804e940b4d5ffe6efd529d30eba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f248d110b7767bb74de8e065c7bd753026a06e90bba68ca3b659484dda919d0(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptionsExportToCsvOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc81a978f10e7926365637e9740158ddee70a1f49b25418bd4d85603e794992(
    *,
    availability_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2734972f592ece1da8c64519828e849e5463fafafb9b39dce79e9749a8758dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a636829de24beef305dc9dbddb4443626cdcf3688de66dc9775fd52f518f040f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c209b65e423ca7ff8f86596bd44536c48bd80a4bc6655dcc41ff7573ec45adf(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptionsExportWithHiddenFieldsOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6edcb4130fbda57ec2e91632d158cda7b1b523e33c9ad7b00388e00ebdf8de4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9008c973ca360e532c537a55ed0673c96aa8aadae3790e9d82d5933763915fd3(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dcb46c516daa186c69ce4561d103db60068a047b9946382e8a4bbd19b3e883b(
    *,
    visibility_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31914e301ca46ace29bd8f6dd526f4073c5957c7c84c32a6e238dcf202eb296a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e4d39e749c35c977cffb4baef31c96bcc6612c335a07964db49eabd4145404(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71bfb2fca6ef73d3b7d24e569cec6e8060f52f69394ea7e65067f47f156a48a6(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptionsSheetControlsOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c5874f10d12669ef411d931aca5b883b1e55665d8ef55f588824d7dabde3f0(
    *,
    availability_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6958b43f89a4ddce37a8ce6aad5bab4ae970963464244bc50e11052e6390d341(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f522ca086cdd42ec0acd329c1427b9dab0ac7f306936ed2816e095f049570876(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a05e0769b1bd54f93c22387e0e7cd69b75ef048d7d6f44b5f4421b66c3a9871b(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptionsSheetLayoutElementMaximizationOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3e32e741f89d9f3020709fb3f804fde9b57855538dbd16dc7ddf5e8b269073(
    *,
    availability_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd94ce2acca64df61c20073f3ecf5aa06ad50dc9e113f59d4c1d61b774e0680(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__582732287a00261c4a633173a560c33ac425f7420e69f77fd7b68ed1e5c6be22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b22c5887146d885be80ca9ce2816a1562985d198c68f230375282e2f884f22f(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptionsVisualAxisSortOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__763e6a814c3e309b45a74b82a5872d5474e0085879de0844214f3adf5f7cc31b(
    *,
    availability_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be54c00abe2aab912942d79e764ae5d51313e0f37a1fb6c1b3f4fbff5720dfe4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9409717badbf70101e5e0573c27b5809f8ed59e968c6960350db12e86d4aab9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c42d3407dfb71dac4ab6bb72279ab67628f5a0bb773c3696be9e08798c9a9875(
    value: typing.Optional[QuicksightDashboardDashboardPublishOptionsVisualMenuOption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9425f93544d344bb5dfe7a539d2bfc4b5645a8f04909676999c943a3ec896904(
    *,
    date_time_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersDateTimeParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    decimal_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersDecimalParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    integer_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersIntegerParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    string_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersStringParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35cbe14c4e14e482b27937dcedb0fb431c4a618e1b9678fc1e2d37bc3897c79f(
    *,
    name: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ea7de1cd0213a59e70fff4aa838d8439be020691e7cdc3c4b719f75d2d15ee5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7930a4436119e34b0d4b5a099a6d00fda938fdd313f048583f17763bb3c767(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__621896ea7938d77a488d0460d924c1e5c44fe08077e24610c755242985efb31e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1979175c621dafe08953031e5d68ea58d2cfec6bd38618fce261b9dc46304d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037fb141d7ce6cdbcca72028bdf2d0cf834bf0522e4fcbaf741b18303ecb6141(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fbb42f294a44f63415f3e9c645c7171e3c52c387107eec68138477b84405763(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDateTimeParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67a15562833374412e2516824d214759f753355eee3c4998c270407d2892833(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca4c294e648fd31c9d7ee6106d5bdb40f9d091dc8c9fd08014a2f408f7deef5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75dda0f59bbcd4d065f99670172e0776c8a04ea5275d14b0cafd4fb8acefec98(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d89f708fb3530ac19e293f65033c3cf0dc5ca47ae5803633ddd2daf817c1c4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersDateTimeParameters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083e90a9066bed7391575720ac1ee0a9946946222e470a88af7017302b3ad69c(
    *,
    name: builtins.str,
    values: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__517ee98c380fc93fc32efbea65e93a171bccc54f62ce31aacf5bf5d37dd28faf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a6e87d0224973aad2d543ba04724c090a395b190654775d62e8bf406f5cd3e5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63bc7b60935e05c41a801a0158b675491296b164acc7dfb8391dfde80375a7ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a55f4c9603417724981a86a8728545d4e169ddfc75b12723e93703aa696e5ca(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5db16d7855f5a4b651441ea4f9cac3d655c2d20f89bac0e42c0cfc2a895f03d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68565e4d4ae7de638ecd0d7510d87e33a4380407be38f36e30bdbef096b535b1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersDecimalParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d69d203a13c221ab0a540f0f15e67b9ea7625e63ead6ab38cda9ff0c75859c8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f7aa0cb82f681bdf892ed4d12c9a6a17f85f1d9e5bca0b7a05698d4332e03d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698f35d3b172e70659ee17ba427967920e2f973dc57ce8cad080b5e7b0ffa92b(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a54f75462c7d272cbee801e1e34f06a4b3568a0180a379f6b47bfc8d95a0959(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersDecimalParameters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b13bf606d416db34421e65879cdb0c12bab2a3775fdbfb7efe9f3bf0b6a205e(
    *,
    name: builtins.str,
    values: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10075c98f92028e91cecfd364c8dc8924a5eaa4c7801c92c8c1aec9ca004f45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de0231641e1e8128326a61e62b51a77e04317f465f0cc19d1b46bd1f5162d41(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5766842307494b10bb92187c9469828d65ae77989ed86f2629725d499f9afa9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b571e826dd75e5325775564b8cda704fd3796f204bdac55a9e395d477ed8f78e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d1fb87b64d05822a1270a4558966f339ec675954b131d5c75ef745456eb9a06(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec865cf717f948622c483af6671a2d1d86f4f5b0b5cee62f37992b880e97270(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersIntegerParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__350843606116db0b7e78ea24d355abf198d11979465d493f2d904b338e365682(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f890d3e2d08c0e5acdf9594cfd5bb2822a8f3721276343718f81da2b4820bb98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2f49a48c8e56fb978e9bd15f31e6fccfc7317fc091ad7c87544912fc531dda7(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc3d43ad84e9c73a5b6f3d1c35aa2767db0af6ab824590b8f9bc7c15a16671f1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersIntegerParameters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__038d9c892cb47efb80c59bdcca490eddb6c9db7365b2e6874c80bc9776eaeb22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__500314a4ac2125bb057c3664022049f69be2031f60d2b0aaa0d17780b06b3148(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersDateTimeParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d33694ba0aa952debe1f58530524c8fb02dcd0c1366427189cf462486dfdfc9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersDecimalParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98cf32363eb5cd1f8142d4858ebac7880b929a3cdb7fb989fcfe708b4c687737(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersIntegerParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e8bef1ebcaa41ef058564563a75bcf9be6951fb8cf159d0bf92a66646f6a9d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardParametersStringParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a5ec08d9c5318d087b2a194a81f3c23266274e85e1712ff41a30fda16e241f2(
    value: typing.Optional[QuicksightDashboardParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e03d27ef566e798845ab6e27a7aa920cb18dd1a57a34789dc4d8cc51e9e75a(
    *,
    name: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ecf6308390013f732b6f5c215063f5568c0409075840001abeb3a83c590e69(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be2a92bf0befbf9d251b2eadefc4b961fccafe9202d14de361fc3dd79805a5e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b9ed4357df6ee97ff76dcb846455ec5930a37e1b2c9847e6e05f51972275d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4731f589ad8b0c917e4a14b2d697db9d6ce802d4275ebcc9f21c51da1ec87394(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec014a6b20ac67004f1426b40d492e32af18afa0c44b05c17b1c9810c5026ac2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f5b85e257711b8a72a9608397c1391d8d8a96d7d5a23b1100cd93653e7ecdf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardParametersStringParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40695655b867ff255f6d76f6adf354cbd90ecf57a8ce647a94ab6f49e355310d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f52f4db777aef10b8f8d87210632851a64851aa51ba4ce59fc0c71d76900bd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4563b0f7d794bf055c99d0ad372de683e12a8c90cd408c413dc08a305f44b4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a913d6eb2be54e9f1b21469adabefc42b1edfdd0efc01c937a9f5b593c0a3985(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardParametersStringParameters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e8e66d4a46575b60b5f5cad7079bc11e39efcb18f86fda70b8b040c8cd1ae4d(
    *,
    actions: typing.Sequence[builtins.str],
    principal: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df94e836ee874090d8019f2dffe3391c8deebe7d35f24968b6c01cbb2baee937(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da99ff1a9cbb37294f8e02ee6c5e769a0041577855f818fe6245f3175dae53aa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4516a04b5cc7d12d48ee5a86327285db211a089178a964af9c89b41cdd7c63f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6929e9ac0d28cf6c89cf5c576f13faef461dd24b9e50be19266de1899c963811(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__919f855eff42eee640676933fda517e202121606be671808b00243994702b116(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fe020350585a537a61a4115a00cf6ab76e2918d76168136f34e55442ca3c234(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardPermissions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7959424328cf65b74ffb8e6687181aed1523f0693502099f12a6649f5dd6bd0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7682a76fb4b65fb23ff20f65a9a9093710b3954f157dc90823b0bba12f10748c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__356aa0e2d23c4b33e885eb2585b2fb4a73de74e960324a2387d8e6ddc591284e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dbec55a699585e385e4cff74089f4a42e38fefd7946aff5008e00c598143e32(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardPermissions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca352f76f0bd739944159150e3f8e75218b5077373288c73e5c9d4ad0eaad3f(
    *,
    source_template: typing.Optional[typing.Union[QuicksightDashboardSourceEntitySourceTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8c9974933c926403542afba62780d3b8ce7faf084d60952c9a90bfe107452d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f6ef5fcf350708ef2adf6113c05c95b6a5b84d8408795b11e1b7fadb356a3b(
    value: typing.Optional[QuicksightDashboardSourceEntity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a27da7e9a27c33a0efa0e4ff6a134ad285ffd581d9e85dd0c856e008a472236(
    *,
    arn: builtins.str,
    data_set_references: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardSourceEntitySourceTemplateDataSetReferences, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9b241abc932032cf22b34ce77c1eb21e053646e9c0d7f2d8c8fb3209134be3e(
    *,
    data_set_arn: builtins.str,
    data_set_placeholder: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ded5b41635afe959e4dddb4994d911681775f578481184dcc1e2f3c359755f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b697c5dbfedce095e06f333c3bf219b043365e085c357fc354b70791cd25453(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f72509488e66b43612c2c1f5e292489273f7e4c9855f7887bac214349e2360(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06c4149ac3ce4791707f6142f1710a59e04be527c32396522eb5b8a62c6ac7d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ee1e25177a0e19d55ba4e34a8e8f9b8e8ce24760848889f47cae99e80324a4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58f9804649ad9c08aafd9d86b051af47e6d93e6b58149ee8799cf54cfe5a9196(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDashboardSourceEntitySourceTemplateDataSetReferences]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718d3c5d9ae8f77b2aa8aa676f56069b6390f41a5a950403e7dc2f36379d157d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3844412d2e3136ff2bf05ec1b535edc75c3d8a9dd2ed348c27399de4092378e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a11479e88956303ec94ba097703bde038fe76ec22194280f21033403e4da41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ce0b089e22cb34b49cce16b872c4a14de4b115f95da194e7a07c04ffe62140(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardSourceEntitySourceTemplateDataSetReferences]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__626e7de29f183cf4e17f997cf216348f3d2ec538683daa6f46bca5185b1b1266(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42bf81fb9212b1f26f3b710333db5bf040aea231ea2a83046f554c6804bec533(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDashboardSourceEntitySourceTemplateDataSetReferences, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1256044661f2dc9a39bc7791168c58a09acf728a2d43b3d9985fa4037263fb4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f790a07ca91820c04383ca9dd5f2647999237abad8665454918a1af3ea4b9b6(
    value: typing.Optional[QuicksightDashboardSourceEntitySourceTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cdf55f751f7306acd9f37b6be963f0913e7ca34af22fd42927da2cb2c311a11(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b089ed98b01801ffd1889176b73ff6990a853e6e34fd978f6e7cabafe8c3d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aafdc25dd2b389a4d000a00494b1b0cb8f4ee34379f7b59d74a10ac4ee4c1b61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba1dc28aa95ee554531e7286f490de847c964f2b485843336f44520a6a26cc95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54b6e6e49da9dfe365d5ab934fc13575321885e9c566677008ce92618044431(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ec314eda13c23ce7edf66ddd04f8fcefebbec854bed397d3a4ce1a0e98da04(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDashboardTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
