r'''
# `aws_fis_experiment_template`

Refer to the Terraform Registry for docs: [`aws_fis_experiment_template`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template).
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


class FisExperimentTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template aws_fis_experiment_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateAction", typing.Dict[builtins.str, typing.Any]]]],
        description: builtins.str,
        role_arn: builtins.str,
        stop_condition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateStopCondition", typing.Dict[builtins.str, typing.Any]]]],
        experiment_options: typing.Optional[typing.Union["FisExperimentTemplateExperimentOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        experiment_report_configuration: typing.Optional[typing.Union["FisExperimentTemplateExperimentReportConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        log_configuration: typing.Optional[typing.Union["FisExperimentTemplateLogConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["FisExperimentTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template aws_fis_experiment_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#action FisExperimentTemplate#action}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#description FisExperimentTemplate#description}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#role_arn FisExperimentTemplate#role_arn}.
        :param stop_condition: stop_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#stop_condition FisExperimentTemplate#stop_condition}
        :param experiment_options: experiment_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#experiment_options FisExperimentTemplate#experiment_options}
        :param experiment_report_configuration: experiment_report_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#experiment_report_configuration FisExperimentTemplate#experiment_report_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#id FisExperimentTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_configuration: log_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#log_configuration FisExperimentTemplate#log_configuration}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#region FisExperimentTemplate#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#tags FisExperimentTemplate#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#tags_all FisExperimentTemplate#tags_all}.
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#target FisExperimentTemplate#target}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#timeouts FisExperimentTemplate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4cc33aec75247a02c09a67ec37e7287931b9a9f6ce40efec144b43fce51d47a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FisExperimentTemplateConfig(
            action=action,
            description=description,
            role_arn=role_arn,
            stop_condition=stop_condition,
            experiment_options=experiment_options,
            experiment_report_configuration=experiment_report_configuration,
            id=id,
            log_configuration=log_configuration,
            region=region,
            tags=tags,
            tags_all=tags_all,
            target=target,
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
        '''Generates CDKTF code for importing a FisExperimentTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FisExperimentTemplate to import.
        :param import_from_id: The id of the existing FisExperimentTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FisExperimentTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8afdb69386b1f59706be39a97a1eceb363bc981b2a87e598ddfa7599ca891c47)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateAction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed92adf8c6d893aafccde45e7bbf048b7979df76d3c1a7401427ce2bfc567be4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putExperimentOptions")
    def put_experiment_options(
        self,
        *,
        account_targeting: typing.Optional[builtins.str] = None,
        empty_target_resolution_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_targeting: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#account_targeting FisExperimentTemplate#account_targeting}.
        :param empty_target_resolution_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#empty_target_resolution_mode FisExperimentTemplate#empty_target_resolution_mode}.
        '''
        value = FisExperimentTemplateExperimentOptions(
            account_targeting=account_targeting,
            empty_target_resolution_mode=empty_target_resolution_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putExperimentOptions", [value]))

    @jsii.member(jsii_name="putExperimentReportConfiguration")
    def put_experiment_report_configuration(
        self,
        *,
        data_sources: typing.Optional[typing.Union["FisExperimentTemplateExperimentReportConfigurationDataSources", typing.Dict[builtins.str, typing.Any]]] = None,
        outputs: typing.Optional[typing.Union["FisExperimentTemplateExperimentReportConfigurationOutputs", typing.Dict[builtins.str, typing.Any]]] = None,
        post_experiment_duration: typing.Optional[builtins.str] = None,
        pre_experiment_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_sources: data_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#data_sources FisExperimentTemplate#data_sources}
        :param outputs: outputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#outputs FisExperimentTemplate#outputs}
        :param post_experiment_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#post_experiment_duration FisExperimentTemplate#post_experiment_duration}.
        :param pre_experiment_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#pre_experiment_duration FisExperimentTemplate#pre_experiment_duration}.
        '''
        value = FisExperimentTemplateExperimentReportConfiguration(
            data_sources=data_sources,
            outputs=outputs,
            post_experiment_duration=post_experiment_duration,
            pre_experiment_duration=pre_experiment_duration,
        )

        return typing.cast(None, jsii.invoke(self, "putExperimentReportConfiguration", [value]))

    @jsii.member(jsii_name="putLogConfiguration")
    def put_log_configuration(
        self,
        *,
        log_schema_version: jsii.Number,
        cloudwatch_logs_configuration: typing.Optional[typing.Union["FisExperimentTemplateLogConfigurationCloudwatchLogsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_configuration: typing.Optional[typing.Union["FisExperimentTemplateLogConfigurationS3Configuration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param log_schema_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#log_schema_version FisExperimentTemplate#log_schema_version}.
        :param cloudwatch_logs_configuration: cloudwatch_logs_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#cloudwatch_logs_configuration FisExperimentTemplate#cloudwatch_logs_configuration}
        :param s3_configuration: s3_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#s3_configuration FisExperimentTemplate#s3_configuration}
        '''
        value = FisExperimentTemplateLogConfiguration(
            log_schema_version=log_schema_version,
            cloudwatch_logs_configuration=cloudwatch_logs_configuration,
            s3_configuration=s3_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putLogConfiguration", [value]))

    @jsii.member(jsii_name="putStopCondition")
    def put_stop_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateStopCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc459a5667aaf1ca6e83d926f357b5208a35f6bc8bbe93be69d9bab26bfef916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStopCondition", [value]))

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b1173844cf57e23ff78fe8e703a2a2c00f19a482cd5e8698ed984d2f5617f31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTarget", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#create FisExperimentTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#delete FisExperimentTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#update FisExperimentTemplate#update}.
        '''
        value = FisExperimentTemplateTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetExperimentOptions")
    def reset_experiment_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExperimentOptions", []))

    @jsii.member(jsii_name="resetExperimentReportConfiguration")
    def reset_experiment_report_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExperimentReportConfiguration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogConfiguration")
    def reset_log_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogConfiguration", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

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
    @jsii.member(jsii_name="action")
    def action(self) -> "FisExperimentTemplateActionList":
        return typing.cast("FisExperimentTemplateActionList", jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="experimentOptions")
    def experiment_options(
        self,
    ) -> "FisExperimentTemplateExperimentOptionsOutputReference":
        return typing.cast("FisExperimentTemplateExperimentOptionsOutputReference", jsii.get(self, "experimentOptions"))

    @builtins.property
    @jsii.member(jsii_name="experimentReportConfiguration")
    def experiment_report_configuration(
        self,
    ) -> "FisExperimentTemplateExperimentReportConfigurationOutputReference":
        return typing.cast("FisExperimentTemplateExperimentReportConfigurationOutputReference", jsii.get(self, "experimentReportConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="logConfiguration")
    def log_configuration(
        self,
    ) -> "FisExperimentTemplateLogConfigurationOutputReference":
        return typing.cast("FisExperimentTemplateLogConfigurationOutputReference", jsii.get(self, "logConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="stopCondition")
    def stop_condition(self) -> "FisExperimentTemplateStopConditionList":
        return typing.cast("FisExperimentTemplateStopConditionList", jsii.get(self, "stopCondition"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "FisExperimentTemplateTargetList":
        return typing.cast("FisExperimentTemplateTargetList", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "FisExperimentTemplateTimeoutsOutputReference":
        return typing.cast("FisExperimentTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateAction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateAction"]]], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="experimentOptionsInput")
    def experiment_options_input(
        self,
    ) -> typing.Optional["FisExperimentTemplateExperimentOptions"]:
        return typing.cast(typing.Optional["FisExperimentTemplateExperimentOptions"], jsii.get(self, "experimentOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="experimentReportConfigurationInput")
    def experiment_report_configuration_input(
        self,
    ) -> typing.Optional["FisExperimentTemplateExperimentReportConfiguration"]:
        return typing.cast(typing.Optional["FisExperimentTemplateExperimentReportConfiguration"], jsii.get(self, "experimentReportConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logConfigurationInput")
    def log_configuration_input(
        self,
    ) -> typing.Optional["FisExperimentTemplateLogConfiguration"]:
        return typing.cast(typing.Optional["FisExperimentTemplateLogConfiguration"], jsii.get(self, "logConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="stopConditionInput")
    def stop_condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateStopCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateStopCondition"]]], jsii.get(self, "stopConditionInput"))

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
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateTarget"]]], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FisExperimentTemplateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FisExperimentTemplateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cb4131c9e0a56b60e960e8b0c538c195a58bfc8cf72619bcf8df135864a9194)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__686ca11f8280f9c4c42fbb7c9f20b724c1bf263b8ad84476ae31284be2c6fe86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b971c4aa70a78130204ec25717b4683947e90c95b7adfd4a19a7bcc2c08f631e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcdefddf9db74adb1e290e01b9a7c66805f725855365ed74392e73e520ca2a8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fed14b95b7bbccbb5e6438094f3bdae21ab616285b7d392fd495b5a42e1b310)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__305b82d87ead720f8365ab191baea5f5ec1d961f67d5013285e614aee6d93941)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateAction",
    jsii_struct_bases=[],
    name_mapping={
        "action_id": "actionId",
        "name": "name",
        "description": "description",
        "parameter": "parameter",
        "start_after": "startAfter",
        "target": "target",
    },
)
class FisExperimentTemplateAction:
    def __init__(
        self,
        *,
        action_id: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateActionParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        start_after: typing.Optional[typing.Sequence[builtins.str]] = None,
        target: typing.Optional[typing.Union["FisExperimentTemplateActionTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param action_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#action_id FisExperimentTemplate#action_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#name FisExperimentTemplate#name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#description FisExperimentTemplate#description}.
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#parameter FisExperimentTemplate#parameter}
        :param start_after: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#start_after FisExperimentTemplate#start_after}.
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#target FisExperimentTemplate#target}
        '''
        if isinstance(target, dict):
            target = FisExperimentTemplateActionTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c117974cb446ce0a45d20a944530e1d049a1997e96c549f3c9b25eb62cc31bb)
            check_type(argname="argument action_id", value=action_id, expected_type=type_hints["action_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
            check_type(argname="argument start_after", value=start_after, expected_type=type_hints["start_after"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_id": action_id,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if parameter is not None:
            self._values["parameter"] = parameter
        if start_after is not None:
            self._values["start_after"] = start_after
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def action_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#action_id FisExperimentTemplate#action_id}.'''
        result = self._values.get("action_id")
        assert result is not None, "Required property 'action_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#name FisExperimentTemplate#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#description FisExperimentTemplate#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateActionParameter"]]]:
        '''parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#parameter FisExperimentTemplate#parameter}
        '''
        result = self._values.get("parameter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateActionParameter"]]], result)

    @builtins.property
    def start_after(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#start_after FisExperimentTemplate#start_after}.'''
        result = self._values.get("start_after")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target(self) -> typing.Optional["FisExperimentTemplateActionTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#target FisExperimentTemplate#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["FisExperimentTemplateActionTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FisExperimentTemplateActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a9e6fffbf2dafaf51e52a9998dfbec7be097986f5daec2a30dc968a6e05986d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FisExperimentTemplateActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf49d0dc2a1f5b0a893e3cb68b8bffadc65da7f6acf164e91aeee0d5bafa358f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FisExperimentTemplateActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6fe213007dffdd5795c915314f34a8b92a7ba0d38281d9c5d3c1cf16991b295)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c96bf74e0faf0bc8faf18af30c2cce6679d11ee574d093fa24a12d05864e250c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85f368979ebe81596ceb1d67c91407d43d9570acabfe4d2a08e65fc29130f16b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__911c19bd5728a3b25537b9a27d88233351be904cf5d5bcc9daadda78a64de77f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FisExperimentTemplateActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10c8ba77f44a249c3e37a717c2b6133947729e42f7daa48020bfb0524f34d19f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putParameter")
    def put_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateActionParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afeea4eea934a936a4aa263a3c68df47a42598c8d4a94b165f4df2793aaada29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParameter", [value]))

    @jsii.member(jsii_name="putTarget")
    def put_target(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#key FisExperimentTemplate#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#value FisExperimentTemplate#value}.
        '''
        value_ = FisExperimentTemplateActionTarget(key=key, value=value)

        return typing.cast(None, jsii.invoke(self, "putTarget", [value_]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetParameter")
    def reset_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameter", []))

    @jsii.member(jsii_name="resetStartAfter")
    def reset_start_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartAfter", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @builtins.property
    @jsii.member(jsii_name="parameter")
    def parameter(self) -> "FisExperimentTemplateActionParameterList":
        return typing.cast("FisExperimentTemplateActionParameterList", jsii.get(self, "parameter"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "FisExperimentTemplateActionTargetOutputReference":
        return typing.cast("FisExperimentTemplateActionTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="actionIdInput")
    def action_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterInput")
    def parameter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateActionParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateActionParameter"]]], jsii.get(self, "parameterInput"))

    @builtins.property
    @jsii.member(jsii_name="startAfterInput")
    def start_after_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "startAfterInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional["FisExperimentTemplateActionTarget"]:
        return typing.cast(typing.Optional["FisExperimentTemplateActionTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="actionId")
    def action_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionId"))

    @action_id.setter
    def action_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc046274e502e55a06f3f01df5fd93b334e14119595d5aef03ea1714ebc47494)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2938eaf34a43f486ffdb22cd845d3b8d0fd44f9e4f19a1f637a4c214c2cfcf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f35290ad005325cf5b94f2a171154c5158f8b7829063458ae79063a787a396d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startAfter")
    def start_after(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "startAfter"))

    @start_after.setter
    def start_after(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90c3f9eeefc6c3844c54ae690c68f03ae0dec428d21fca551979d701b735e6fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startAfter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4908d12cd6334893614459be383a185b49cf28c730744c9ceb65e11e7603f61c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateActionParameter",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class FisExperimentTemplateActionParameter:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#key FisExperimentTemplate#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#value FisExperimentTemplate#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f110fbf0e104dd52593194940650cdd3603c72b9fc8155b40fe484795e2289d0)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#key FisExperimentTemplate#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#value FisExperimentTemplate#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateActionParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FisExperimentTemplateActionParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateActionParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4281ddccb2c208a418fe528e2c5c07862db25e3a11049aa883bdbb9dea3f4af9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FisExperimentTemplateActionParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9553e309382dbd3b4bb2f58f8caadf6143aa89182752499a032a3dda4d98ead)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FisExperimentTemplateActionParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f395ade77f8400925db42c499090dc8a9da5a464feb538a1c37a927ff9a7c8b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b93d989c729d76802a42e2860f2102eb68d7fcb1e1db5a5f257f34c863dcee24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9236514e4962965b7c004988b79267b37ca9e0bc686acb30a47a20d09cc8a58f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateActionParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateActionParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateActionParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__303e921edd95fd95e21143ad5d774cbae1b0b5b05418827544733a9ce79117e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FisExperimentTemplateActionParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateActionParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d8d3c9ce354b5a0a61d662e62322ebcf26f7e173de6f733b7318537e4f5948c)
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
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a17733ce143295ddea49a3c5402e4e5d98944fd6d66d41e0df5e2f6239563c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89f4ad5a9e59406fbaa000ad3f9a48314a149ba732819df456e85a47e6e80251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateActionParameter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateActionParameter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateActionParameter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cf9df78e7d1d9ecac76ec74fbf4ce3b37952178d62ec7b85baaa07dd649bcc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateActionTarget",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class FisExperimentTemplateActionTarget:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#key FisExperimentTemplate#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#value FisExperimentTemplate#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf12acc9b4a969a6bd163e1529b298ffe0eb35d02ad90ba91bb756bdfb089ac)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#key FisExperimentTemplate#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#value FisExperimentTemplate#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateActionTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FisExperimentTemplateActionTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateActionTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__613fa41c294a72d9a841f6abc1613e960307b6e4c70da60a9815c57c3f22e9d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d7a1839ffa48868c58dc20033aeaae17111c4e11e66c7982d96fc082fd4ee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f0ff252c2fbe31f7e85f681e1e360cd7df8047a228af130a03508179086526b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FisExperimentTemplateActionTarget]:
        return typing.cast(typing.Optional[FisExperimentTemplateActionTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FisExperimentTemplateActionTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__125eb2a292a105b2566cb5c99ece1abe8e3f4f11c06d98b55cdb50118bea73a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "action": "action",
        "description": "description",
        "role_arn": "roleArn",
        "stop_condition": "stopCondition",
        "experiment_options": "experimentOptions",
        "experiment_report_configuration": "experimentReportConfiguration",
        "id": "id",
        "log_configuration": "logConfiguration",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
        "target": "target",
        "timeouts": "timeouts",
    },
)
class FisExperimentTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateAction, typing.Dict[builtins.str, typing.Any]]]],
        description: builtins.str,
        role_arn: builtins.str,
        stop_condition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateStopCondition", typing.Dict[builtins.str, typing.Any]]]],
        experiment_options: typing.Optional[typing.Union["FisExperimentTemplateExperimentOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        experiment_report_configuration: typing.Optional[typing.Union["FisExperimentTemplateExperimentReportConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        log_configuration: typing.Optional[typing.Union["FisExperimentTemplateLogConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["FisExperimentTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#action FisExperimentTemplate#action}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#description FisExperimentTemplate#description}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#role_arn FisExperimentTemplate#role_arn}.
        :param stop_condition: stop_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#stop_condition FisExperimentTemplate#stop_condition}
        :param experiment_options: experiment_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#experiment_options FisExperimentTemplate#experiment_options}
        :param experiment_report_configuration: experiment_report_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#experiment_report_configuration FisExperimentTemplate#experiment_report_configuration}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#id FisExperimentTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_configuration: log_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#log_configuration FisExperimentTemplate#log_configuration}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#region FisExperimentTemplate#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#tags FisExperimentTemplate#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#tags_all FisExperimentTemplate#tags_all}.
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#target FisExperimentTemplate#target}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#timeouts FisExperimentTemplate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(experiment_options, dict):
            experiment_options = FisExperimentTemplateExperimentOptions(**experiment_options)
        if isinstance(experiment_report_configuration, dict):
            experiment_report_configuration = FisExperimentTemplateExperimentReportConfiguration(**experiment_report_configuration)
        if isinstance(log_configuration, dict):
            log_configuration = FisExperimentTemplateLogConfiguration(**log_configuration)
        if isinstance(timeouts, dict):
            timeouts = FisExperimentTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec4fc8e38ecbbce021fa89f4a4e975d8f8e228653f08591876795b1075c77653)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument stop_condition", value=stop_condition, expected_type=type_hints["stop_condition"])
            check_type(argname="argument experiment_options", value=experiment_options, expected_type=type_hints["experiment_options"])
            check_type(argname="argument experiment_report_configuration", value=experiment_report_configuration, expected_type=type_hints["experiment_report_configuration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_configuration", value=log_configuration, expected_type=type_hints["log_configuration"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "description": description,
            "role_arn": role_arn,
            "stop_condition": stop_condition,
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
        if experiment_options is not None:
            self._values["experiment_options"] = experiment_options
        if experiment_report_configuration is not None:
            self._values["experiment_report_configuration"] = experiment_report_configuration
        if id is not None:
            self._values["id"] = id
        if log_configuration is not None:
            self._values["log_configuration"] = log_configuration
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if target is not None:
            self._values["target"] = target
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
    def action(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateAction]]:
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#action FisExperimentTemplate#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateAction]], result)

    @builtins.property
    def description(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#description FisExperimentTemplate#description}.'''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#role_arn FisExperimentTemplate#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stop_condition(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateStopCondition"]]:
        '''stop_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#stop_condition FisExperimentTemplate#stop_condition}
        '''
        result = self._values.get("stop_condition")
        assert result is not None, "Required property 'stop_condition' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateStopCondition"]], result)

    @builtins.property
    def experiment_options(
        self,
    ) -> typing.Optional["FisExperimentTemplateExperimentOptions"]:
        '''experiment_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#experiment_options FisExperimentTemplate#experiment_options}
        '''
        result = self._values.get("experiment_options")
        return typing.cast(typing.Optional["FisExperimentTemplateExperimentOptions"], result)

    @builtins.property
    def experiment_report_configuration(
        self,
    ) -> typing.Optional["FisExperimentTemplateExperimentReportConfiguration"]:
        '''experiment_report_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#experiment_report_configuration FisExperimentTemplate#experiment_report_configuration}
        '''
        result = self._values.get("experiment_report_configuration")
        return typing.cast(typing.Optional["FisExperimentTemplateExperimentReportConfiguration"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#id FisExperimentTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_configuration(
        self,
    ) -> typing.Optional["FisExperimentTemplateLogConfiguration"]:
        '''log_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#log_configuration FisExperimentTemplate#log_configuration}
        '''
        result = self._values.get("log_configuration")
        return typing.cast(typing.Optional["FisExperimentTemplateLogConfiguration"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#region FisExperimentTemplate#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#tags FisExperimentTemplate#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#tags_all FisExperimentTemplate#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateTarget"]]]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#target FisExperimentTemplate#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateTarget"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["FisExperimentTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#timeouts FisExperimentTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["FisExperimentTemplateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateExperimentOptions",
    jsii_struct_bases=[],
    name_mapping={
        "account_targeting": "accountTargeting",
        "empty_target_resolution_mode": "emptyTargetResolutionMode",
    },
)
class FisExperimentTemplateExperimentOptions:
    def __init__(
        self,
        *,
        account_targeting: typing.Optional[builtins.str] = None,
        empty_target_resolution_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_targeting: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#account_targeting FisExperimentTemplate#account_targeting}.
        :param empty_target_resolution_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#empty_target_resolution_mode FisExperimentTemplate#empty_target_resolution_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69bdb5dd938df79d3555f230ae0982ebbed19f286daf4ea63d32e41b70482b67)
            check_type(argname="argument account_targeting", value=account_targeting, expected_type=type_hints["account_targeting"])
            check_type(argname="argument empty_target_resolution_mode", value=empty_target_resolution_mode, expected_type=type_hints["empty_target_resolution_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_targeting is not None:
            self._values["account_targeting"] = account_targeting
        if empty_target_resolution_mode is not None:
            self._values["empty_target_resolution_mode"] = empty_target_resolution_mode

    @builtins.property
    def account_targeting(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#account_targeting FisExperimentTemplate#account_targeting}.'''
        result = self._values.get("account_targeting")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def empty_target_resolution_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#empty_target_resolution_mode FisExperimentTemplate#empty_target_resolution_mode}.'''
        result = self._values.get("empty_target_resolution_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateExperimentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FisExperimentTemplateExperimentOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateExperimentOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cafda7bc89e3bd428e97b19822e998405a3c00cffe1cc5bdd927d4e564e3cfa1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccountTargeting")
    def reset_account_targeting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountTargeting", []))

    @jsii.member(jsii_name="resetEmptyTargetResolutionMode")
    def reset_empty_target_resolution_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmptyTargetResolutionMode", []))

    @builtins.property
    @jsii.member(jsii_name="accountTargetingInput")
    def account_targeting_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountTargetingInput"))

    @builtins.property
    @jsii.member(jsii_name="emptyTargetResolutionModeInput")
    def empty_target_resolution_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emptyTargetResolutionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="accountTargeting")
    def account_targeting(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountTargeting"))

    @account_targeting.setter
    def account_targeting(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c53de0b2017ea210f061b049efcd1361d47862f4a20b6a28c6aaacd532ba65d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountTargeting", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emptyTargetResolutionMode")
    def empty_target_resolution_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emptyTargetResolutionMode"))

    @empty_target_resolution_mode.setter
    def empty_target_resolution_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de527a799364a2348fbc623b8f46cf9f11390c8bf6292b43b98168afc29875e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emptyTargetResolutionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FisExperimentTemplateExperimentOptions]:
        return typing.cast(typing.Optional[FisExperimentTemplateExperimentOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FisExperimentTemplateExperimentOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63c022ff9180b82b159433b766a85909ae5fcc7cd3aebf6a75c7fe4a32da2b21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateExperimentReportConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "data_sources": "dataSources",
        "outputs": "outputs",
        "post_experiment_duration": "postExperimentDuration",
        "pre_experiment_duration": "preExperimentDuration",
    },
)
class FisExperimentTemplateExperimentReportConfiguration:
    def __init__(
        self,
        *,
        data_sources: typing.Optional[typing.Union["FisExperimentTemplateExperimentReportConfigurationDataSources", typing.Dict[builtins.str, typing.Any]]] = None,
        outputs: typing.Optional[typing.Union["FisExperimentTemplateExperimentReportConfigurationOutputs", typing.Dict[builtins.str, typing.Any]]] = None,
        post_experiment_duration: typing.Optional[builtins.str] = None,
        pre_experiment_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_sources: data_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#data_sources FisExperimentTemplate#data_sources}
        :param outputs: outputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#outputs FisExperimentTemplate#outputs}
        :param post_experiment_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#post_experiment_duration FisExperimentTemplate#post_experiment_duration}.
        :param pre_experiment_duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#pre_experiment_duration FisExperimentTemplate#pre_experiment_duration}.
        '''
        if isinstance(data_sources, dict):
            data_sources = FisExperimentTemplateExperimentReportConfigurationDataSources(**data_sources)
        if isinstance(outputs, dict):
            outputs = FisExperimentTemplateExperimentReportConfigurationOutputs(**outputs)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43be4301df9d38c5e0ae18e6e30557e63c35100b28b91ad6ac0620e6f1c76d2c)
            check_type(argname="argument data_sources", value=data_sources, expected_type=type_hints["data_sources"])
            check_type(argname="argument outputs", value=outputs, expected_type=type_hints["outputs"])
            check_type(argname="argument post_experiment_duration", value=post_experiment_duration, expected_type=type_hints["post_experiment_duration"])
            check_type(argname="argument pre_experiment_duration", value=pre_experiment_duration, expected_type=type_hints["pre_experiment_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_sources is not None:
            self._values["data_sources"] = data_sources
        if outputs is not None:
            self._values["outputs"] = outputs
        if post_experiment_duration is not None:
            self._values["post_experiment_duration"] = post_experiment_duration
        if pre_experiment_duration is not None:
            self._values["pre_experiment_duration"] = pre_experiment_duration

    @builtins.property
    def data_sources(
        self,
    ) -> typing.Optional["FisExperimentTemplateExperimentReportConfigurationDataSources"]:
        '''data_sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#data_sources FisExperimentTemplate#data_sources}
        '''
        result = self._values.get("data_sources")
        return typing.cast(typing.Optional["FisExperimentTemplateExperimentReportConfigurationDataSources"], result)

    @builtins.property
    def outputs(
        self,
    ) -> typing.Optional["FisExperimentTemplateExperimentReportConfigurationOutputs"]:
        '''outputs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#outputs FisExperimentTemplate#outputs}
        '''
        result = self._values.get("outputs")
        return typing.cast(typing.Optional["FisExperimentTemplateExperimentReportConfigurationOutputs"], result)

    @builtins.property
    def post_experiment_duration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#post_experiment_duration FisExperimentTemplate#post_experiment_duration}.'''
        result = self._values.get("post_experiment_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pre_experiment_duration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#pre_experiment_duration FisExperimentTemplate#pre_experiment_duration}.'''
        result = self._values.get("pre_experiment_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateExperimentReportConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateExperimentReportConfigurationDataSources",
    jsii_struct_bases=[],
    name_mapping={"cloudwatch_dashboard": "cloudwatchDashboard"},
)
class FisExperimentTemplateExperimentReportConfigurationDataSources:
    def __init__(
        self,
        *,
        cloudwatch_dashboard: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cloudwatch_dashboard: cloudwatch_dashboard block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#cloudwatch_dashboard FisExperimentTemplate#cloudwatch_dashboard}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72d754606a50bde2d533b14aaf91d4cd734c744b43d126ed45af21b413992388)
            check_type(argname="argument cloudwatch_dashboard", value=cloudwatch_dashboard, expected_type=type_hints["cloudwatch_dashboard"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloudwatch_dashboard is not None:
            self._values["cloudwatch_dashboard"] = cloudwatch_dashboard

    @builtins.property
    def cloudwatch_dashboard(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard"]]]:
        '''cloudwatch_dashboard block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#cloudwatch_dashboard FisExperimentTemplate#cloudwatch_dashboard}
        '''
        result = self._values.get("cloudwatch_dashboard")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateExperimentReportConfigurationDataSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard",
    jsii_struct_bases=[],
    name_mapping={"dashboard_arn": "dashboardArn"},
)
class FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard:
    def __init__(self, *, dashboard_arn: typing.Optional[builtins.str] = None) -> None:
        '''
        :param dashboard_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#dashboard_arn FisExperimentTemplate#dashboard_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__237df9f4f6e3962212d2de9057e317259b5cf5a868c7dce4d3514d699fd02cdf)
            check_type(argname="argument dashboard_arn", value=dashboard_arn, expected_type=type_hints["dashboard_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dashboard_arn is not None:
            self._values["dashboard_arn"] = dashboard_arn

    @builtins.property
    def dashboard_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#dashboard_arn FisExperimentTemplate#dashboard_arn}.'''
        result = self._values.get("dashboard_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboardList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboardList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97158213231121147af122936a57f7e405d1bc3f6911f4a0b02d7be6d872c8ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboardOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d69ac74d8ef4e091525a04f356f4baa716d8c48c221c8649159f239caaa04c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboardOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd0296b047ae964b4008533e4d06d8dd389b60094da6717574c48667f3fb9bad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0181de43b1fd03b3b093f3c70122323105a8fc9ddadc2e1515ab40fad9d6afc2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c535a7f31daee571ff3839f34c9f0ab9cec909ba44a4f8f53a525e7691cc121b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63d45424e32c36b43a97302bc455c5e9124c0a34ed6163616388f2695a9614f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboardOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboardOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57d1ea5e136e15c27fa892368e3302798018c7845744a2aa6fa3e955dbe9f3ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDashboardArn")
    def reset_dashboard_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDashboardArn", []))

    @builtins.property
    @jsii.member(jsii_name="dashboardArnInput")
    def dashboard_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dashboardArnInput"))

    @builtins.property
    @jsii.member(jsii_name="dashboardArn")
    def dashboard_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dashboardArn"))

    @dashboard_arn.setter
    def dashboard_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__015007b76f0b8f25b2eae31b4f9e525acb5b6bd7c8032709e40f108bb71b61ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dashboardArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__534e412862c020006cab41e3e9d3bf5d2957e8216714e37b44746988e9745831)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FisExperimentTemplateExperimentReportConfigurationDataSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateExperimentReportConfigurationDataSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80298c154ca3c5d6a5e78c18adf3e151a2d4012c3b72d7023eb93b40397f6f51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchDashboard")
    def put_cloudwatch_dashboard(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbae5ef19800c71745a04e50727c95397dd90a2ef9d2e775eb4fcf2d35f0fdec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCloudwatchDashboard", [value]))

    @jsii.member(jsii_name="resetCloudwatchDashboard")
    def reset_cloudwatch_dashboard(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchDashboard", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchDashboard")
    def cloudwatch_dashboard(
        self,
    ) -> FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboardList:
        return typing.cast(FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboardList, jsii.get(self, "cloudwatchDashboard"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchDashboardInput")
    def cloudwatch_dashboard_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard]]], jsii.get(self, "cloudwatchDashboardInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FisExperimentTemplateExperimentReportConfigurationDataSources]:
        return typing.cast(typing.Optional[FisExperimentTemplateExperimentReportConfigurationDataSources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FisExperimentTemplateExperimentReportConfigurationDataSources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27f4ac667c6904fbc8cf82e016886aa7077ab70a5dc6ff5b151ef28aca23be14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FisExperimentTemplateExperimentReportConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateExperimentReportConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__081562651047d100d16133b06915ab7fc3f106cfad898cd5993239399855973a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataSources")
    def put_data_sources(
        self,
        *,
        cloudwatch_dashboard: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cloudwatch_dashboard: cloudwatch_dashboard block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#cloudwatch_dashboard FisExperimentTemplate#cloudwatch_dashboard}
        '''
        value = FisExperimentTemplateExperimentReportConfigurationDataSources(
            cloudwatch_dashboard=cloudwatch_dashboard
        )

        return typing.cast(None, jsii.invoke(self, "putDataSources", [value]))

    @jsii.member(jsii_name="putOutputs")
    def put_outputs(
        self,
        *,
        s3_configuration: typing.Optional[typing.Union["FisExperimentTemplateExperimentReportConfigurationOutputsS3Configuration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param s3_configuration: s3_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#s3_configuration FisExperimentTemplate#s3_configuration}
        '''
        value = FisExperimentTemplateExperimentReportConfigurationOutputs(
            s3_configuration=s3_configuration
        )

        return typing.cast(None, jsii.invoke(self, "putOutputs", [value]))

    @jsii.member(jsii_name="resetDataSources")
    def reset_data_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataSources", []))

    @jsii.member(jsii_name="resetOutputs")
    def reset_outputs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputs", []))

    @jsii.member(jsii_name="resetPostExperimentDuration")
    def reset_post_experiment_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostExperimentDuration", []))

    @jsii.member(jsii_name="resetPreExperimentDuration")
    def reset_pre_experiment_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreExperimentDuration", []))

    @builtins.property
    @jsii.member(jsii_name="dataSources")
    def data_sources(
        self,
    ) -> FisExperimentTemplateExperimentReportConfigurationDataSourcesOutputReference:
        return typing.cast(FisExperimentTemplateExperimentReportConfigurationDataSourcesOutputReference, jsii.get(self, "dataSources"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(
        self,
    ) -> "FisExperimentTemplateExperimentReportConfigurationOutputsOutputReference":
        return typing.cast("FisExperimentTemplateExperimentReportConfigurationOutputsOutputReference", jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="dataSourcesInput")
    def data_sources_input(
        self,
    ) -> typing.Optional[FisExperimentTemplateExperimentReportConfigurationDataSources]:
        return typing.cast(typing.Optional[FisExperimentTemplateExperimentReportConfigurationDataSources], jsii.get(self, "dataSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="outputsInput")
    def outputs_input(
        self,
    ) -> typing.Optional["FisExperimentTemplateExperimentReportConfigurationOutputs"]:
        return typing.cast(typing.Optional["FisExperimentTemplateExperimentReportConfigurationOutputs"], jsii.get(self, "outputsInput"))

    @builtins.property
    @jsii.member(jsii_name="postExperimentDurationInput")
    def post_experiment_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postExperimentDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="preExperimentDurationInput")
    def pre_experiment_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preExperimentDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="postExperimentDuration")
    def post_experiment_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postExperimentDuration"))

    @post_experiment_duration.setter
    def post_experiment_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd3b07f1b79ae17f96e5680ba38be2cc846111b7b571a64b3597deb64d8af2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postExperimentDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preExperimentDuration")
    def pre_experiment_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preExperimentDuration"))

    @pre_experiment_duration.setter
    def pre_experiment_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb17c1ff72b945c162639e0cb0213b0eb4c0a9ce4f8150cb8e96061205ba0d12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preExperimentDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FisExperimentTemplateExperimentReportConfiguration]:
        return typing.cast(typing.Optional[FisExperimentTemplateExperimentReportConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FisExperimentTemplateExperimentReportConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baa9b4da2baa1659c1f7c7b0e3b520a9eb7d102b972e70bb7ae9770cecd06354)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateExperimentReportConfigurationOutputs",
    jsii_struct_bases=[],
    name_mapping={"s3_configuration": "s3Configuration"},
)
class FisExperimentTemplateExperimentReportConfigurationOutputs:
    def __init__(
        self,
        *,
        s3_configuration: typing.Optional[typing.Union["FisExperimentTemplateExperimentReportConfigurationOutputsS3Configuration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param s3_configuration: s3_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#s3_configuration FisExperimentTemplate#s3_configuration}
        '''
        if isinstance(s3_configuration, dict):
            s3_configuration = FisExperimentTemplateExperimentReportConfigurationOutputsS3Configuration(**s3_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__805b76c3c096267742c84302ce0fea2bb2d9ae03e903dfd86210628a2f61e485)
            check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if s3_configuration is not None:
            self._values["s3_configuration"] = s3_configuration

    @builtins.property
    def s3_configuration(
        self,
    ) -> typing.Optional["FisExperimentTemplateExperimentReportConfigurationOutputsS3Configuration"]:
        '''s3_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#s3_configuration FisExperimentTemplate#s3_configuration}
        '''
        result = self._values.get("s3_configuration")
        return typing.cast(typing.Optional["FisExperimentTemplateExperimentReportConfigurationOutputsS3Configuration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateExperimentReportConfigurationOutputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FisExperimentTemplateExperimentReportConfigurationOutputsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateExperimentReportConfigurationOutputsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfe172420274e0b0a1e941935af228ee4625adf43b64f54c6a27de7df2872f7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putS3Configuration")
    def put_s3_configuration(
        self,
        *,
        bucket_name: builtins.str,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#bucket_name FisExperimentTemplate#bucket_name}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#prefix FisExperimentTemplate#prefix}.
        '''
        value = FisExperimentTemplateExperimentReportConfigurationOutputsS3Configuration(
            bucket_name=bucket_name, prefix=prefix
        )

        return typing.cast(None, jsii.invoke(self, "putS3Configuration", [value]))

    @jsii.member(jsii_name="resetS3Configuration")
    def reset_s3_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Configuration", []))

    @builtins.property
    @jsii.member(jsii_name="s3Configuration")
    def s3_configuration(
        self,
    ) -> "FisExperimentTemplateExperimentReportConfigurationOutputsS3ConfigurationOutputReference":
        return typing.cast("FisExperimentTemplateExperimentReportConfigurationOutputsS3ConfigurationOutputReference", jsii.get(self, "s3Configuration"))

    @builtins.property
    @jsii.member(jsii_name="s3ConfigurationInput")
    def s3_configuration_input(
        self,
    ) -> typing.Optional["FisExperimentTemplateExperimentReportConfigurationOutputsS3Configuration"]:
        return typing.cast(typing.Optional["FisExperimentTemplateExperimentReportConfigurationOutputsS3Configuration"], jsii.get(self, "s3ConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FisExperimentTemplateExperimentReportConfigurationOutputs]:
        return typing.cast(typing.Optional[FisExperimentTemplateExperimentReportConfigurationOutputs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FisExperimentTemplateExperimentReportConfigurationOutputs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75638b3622673598171d85d96879ab4ebb6da85a630b7a95200b80d19cf95a39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateExperimentReportConfigurationOutputsS3Configuration",
    jsii_struct_bases=[],
    name_mapping={"bucket_name": "bucketName", "prefix": "prefix"},
)
class FisExperimentTemplateExperimentReportConfigurationOutputsS3Configuration:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#bucket_name FisExperimentTemplate#bucket_name}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#prefix FisExperimentTemplate#prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac1697c66fd2cb6cef739c7b90310776eb5bbe7ac93353fe43ed3e9813512808)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
        }
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#bucket_name FisExperimentTemplate#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#prefix FisExperimentTemplate#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateExperimentReportConfigurationOutputsS3Configuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FisExperimentTemplateExperimentReportConfigurationOutputsS3ConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateExperimentReportConfigurationOutputsS3ConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d1e5067d6b58974778d6c7319e3e6c04fbe1cbf5a31810efbd5acb8b073fc20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5d9732c8b3ce3ae5f00e870243492f47bdb6edd6e70703ee21cecf19f80c957)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d847d2bb9cd8a1e00d93329c5d1e8cae8b273b2fad0ae6327431ad5e441023e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FisExperimentTemplateExperimentReportConfigurationOutputsS3Configuration]:
        return typing.cast(typing.Optional[FisExperimentTemplateExperimentReportConfigurationOutputsS3Configuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FisExperimentTemplateExperimentReportConfigurationOutputsS3Configuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d5974a20c9eb28f26f21b5763c483982eec3239f2f1d7eeb439366e641feba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateLogConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "log_schema_version": "logSchemaVersion",
        "cloudwatch_logs_configuration": "cloudwatchLogsConfiguration",
        "s3_configuration": "s3Configuration",
    },
)
class FisExperimentTemplateLogConfiguration:
    def __init__(
        self,
        *,
        log_schema_version: jsii.Number,
        cloudwatch_logs_configuration: typing.Optional[typing.Union["FisExperimentTemplateLogConfigurationCloudwatchLogsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_configuration: typing.Optional[typing.Union["FisExperimentTemplateLogConfigurationS3Configuration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param log_schema_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#log_schema_version FisExperimentTemplate#log_schema_version}.
        :param cloudwatch_logs_configuration: cloudwatch_logs_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#cloudwatch_logs_configuration FisExperimentTemplate#cloudwatch_logs_configuration}
        :param s3_configuration: s3_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#s3_configuration FisExperimentTemplate#s3_configuration}
        '''
        if isinstance(cloudwatch_logs_configuration, dict):
            cloudwatch_logs_configuration = FisExperimentTemplateLogConfigurationCloudwatchLogsConfiguration(**cloudwatch_logs_configuration)
        if isinstance(s3_configuration, dict):
            s3_configuration = FisExperimentTemplateLogConfigurationS3Configuration(**s3_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82b7023d402acd614d02b5b7dc53ed946258967036ba08c3c1653a47b73e8307)
            check_type(argname="argument log_schema_version", value=log_schema_version, expected_type=type_hints["log_schema_version"])
            check_type(argname="argument cloudwatch_logs_configuration", value=cloudwatch_logs_configuration, expected_type=type_hints["cloudwatch_logs_configuration"])
            check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_schema_version": log_schema_version,
        }
        if cloudwatch_logs_configuration is not None:
            self._values["cloudwatch_logs_configuration"] = cloudwatch_logs_configuration
        if s3_configuration is not None:
            self._values["s3_configuration"] = s3_configuration

    @builtins.property
    def log_schema_version(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#log_schema_version FisExperimentTemplate#log_schema_version}.'''
        result = self._values.get("log_schema_version")
        assert result is not None, "Required property 'log_schema_version' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def cloudwatch_logs_configuration(
        self,
    ) -> typing.Optional["FisExperimentTemplateLogConfigurationCloudwatchLogsConfiguration"]:
        '''cloudwatch_logs_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#cloudwatch_logs_configuration FisExperimentTemplate#cloudwatch_logs_configuration}
        '''
        result = self._values.get("cloudwatch_logs_configuration")
        return typing.cast(typing.Optional["FisExperimentTemplateLogConfigurationCloudwatchLogsConfiguration"], result)

    @builtins.property
    def s3_configuration(
        self,
    ) -> typing.Optional["FisExperimentTemplateLogConfigurationS3Configuration"]:
        '''s3_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#s3_configuration FisExperimentTemplate#s3_configuration}
        '''
        result = self._values.get("s3_configuration")
        return typing.cast(typing.Optional["FisExperimentTemplateLogConfigurationS3Configuration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateLogConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateLogConfigurationCloudwatchLogsConfiguration",
    jsii_struct_bases=[],
    name_mapping={"log_group_arn": "logGroupArn"},
)
class FisExperimentTemplateLogConfigurationCloudwatchLogsConfiguration:
    def __init__(self, *, log_group_arn: builtins.str) -> None:
        '''
        :param log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#log_group_arn FisExperimentTemplate#log_group_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__584cb1c7a1a57dc8f7332a43667097216ddb105f2b12fddf600d71dbc9ade0cd)
            check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group_arn": log_group_arn,
        }

    @builtins.property
    def log_group_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#log_group_arn FisExperimentTemplate#log_group_arn}.'''
        result = self._values.get("log_group_arn")
        assert result is not None, "Required property 'log_group_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateLogConfigurationCloudwatchLogsConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FisExperimentTemplateLogConfigurationCloudwatchLogsConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateLogConfigurationCloudwatchLogsConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a2b044d3d581b28396849f4c7e7450734ce557e0201633db03e8b8f4ef4d714)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="logGroupArnInput")
    def log_group_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupArnInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupArn"))

    @log_group_arn.setter
    def log_group_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__149df848a4104bb0344e31a9f944f6bcac6d8325e3bea41e193be14ea020f9e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FisExperimentTemplateLogConfigurationCloudwatchLogsConfiguration]:
        return typing.cast(typing.Optional[FisExperimentTemplateLogConfigurationCloudwatchLogsConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FisExperimentTemplateLogConfigurationCloudwatchLogsConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e10af770bce5268344762e6fbd6c47dc620782d0a2949baa74c154b65e9ac61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FisExperimentTemplateLogConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateLogConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61bd4be35d1266b1a79b66c45adf1b6f4c30280f2b4e92d7b7ec2578204c4a91)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchLogsConfiguration")
    def put_cloudwatch_logs_configuration(self, *, log_group_arn: builtins.str) -> None:
        '''
        :param log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#log_group_arn FisExperimentTemplate#log_group_arn}.
        '''
        value = FisExperimentTemplateLogConfigurationCloudwatchLogsConfiguration(
            log_group_arn=log_group_arn
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLogsConfiguration", [value]))

    @jsii.member(jsii_name="putS3Configuration")
    def put_s3_configuration(
        self,
        *,
        bucket_name: builtins.str,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#bucket_name FisExperimentTemplate#bucket_name}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#prefix FisExperimentTemplate#prefix}.
        '''
        value = FisExperimentTemplateLogConfigurationS3Configuration(
            bucket_name=bucket_name, prefix=prefix
        )

        return typing.cast(None, jsii.invoke(self, "putS3Configuration", [value]))

    @jsii.member(jsii_name="resetCloudwatchLogsConfiguration")
    def reset_cloudwatch_logs_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLogsConfiguration", []))

    @jsii.member(jsii_name="resetS3Configuration")
    def reset_s3_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Configuration", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogsConfiguration")
    def cloudwatch_logs_configuration(
        self,
    ) -> FisExperimentTemplateLogConfigurationCloudwatchLogsConfigurationOutputReference:
        return typing.cast(FisExperimentTemplateLogConfigurationCloudwatchLogsConfigurationOutputReference, jsii.get(self, "cloudwatchLogsConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="s3Configuration")
    def s3_configuration(
        self,
    ) -> "FisExperimentTemplateLogConfigurationS3ConfigurationOutputReference":
        return typing.cast("FisExperimentTemplateLogConfigurationS3ConfigurationOutputReference", jsii.get(self, "s3Configuration"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogsConfigurationInput")
    def cloudwatch_logs_configuration_input(
        self,
    ) -> typing.Optional[FisExperimentTemplateLogConfigurationCloudwatchLogsConfiguration]:
        return typing.cast(typing.Optional[FisExperimentTemplateLogConfigurationCloudwatchLogsConfiguration], jsii.get(self, "cloudwatchLogsConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="logSchemaVersionInput")
    def log_schema_version_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "logSchemaVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="s3ConfigurationInput")
    def s3_configuration_input(
        self,
    ) -> typing.Optional["FisExperimentTemplateLogConfigurationS3Configuration"]:
        return typing.cast(typing.Optional["FisExperimentTemplateLogConfigurationS3Configuration"], jsii.get(self, "s3ConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="logSchemaVersion")
    def log_schema_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "logSchemaVersion"))

    @log_schema_version.setter
    def log_schema_version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aba61e2d82703c2aeb6791b4e2832d6a0db3e4911f57eb5505f3bc157d69b93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logSchemaVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FisExperimentTemplateLogConfiguration]:
        return typing.cast(typing.Optional[FisExperimentTemplateLogConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FisExperimentTemplateLogConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3fe12e882513dec4b605f11a1bb2c32a56a39d43ce5b296d83fd6d5f886f984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateLogConfigurationS3Configuration",
    jsii_struct_bases=[],
    name_mapping={"bucket_name": "bucketName", "prefix": "prefix"},
)
class FisExperimentTemplateLogConfigurationS3Configuration:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#bucket_name FisExperimentTemplate#bucket_name}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#prefix FisExperimentTemplate#prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__599e016baa0585251b24e9606c49dc0dd0216f3bb324b46b3b5a512486643852)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
        }
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#bucket_name FisExperimentTemplate#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#prefix FisExperimentTemplate#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateLogConfigurationS3Configuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FisExperimentTemplateLogConfigurationS3ConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateLogConfigurationS3ConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b36f9d001e21f5f911ef23b365e35dd74544aeec33abf542ac80a1778d9377d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e720e8d3c088940798f899e484427a9c572345e38b1e2110b939b4fa99704e73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3454cbb96f772d0583d7ce88c057dbc1e79700a414a77165d77eb438ecc107d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FisExperimentTemplateLogConfigurationS3Configuration]:
        return typing.cast(typing.Optional[FisExperimentTemplateLogConfigurationS3Configuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FisExperimentTemplateLogConfigurationS3Configuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ab31a50356e0553d4a6e0938696b6c1ea2ad10bc57b6b2987eb9040ad4a2c56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateStopCondition",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "value": "value"},
)
class FisExperimentTemplateStopCondition:
    def __init__(
        self,
        *,
        source: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#source FisExperimentTemplate#source}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#value FisExperimentTemplate#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b2e99e65393a3748e7099ba2660a94d049e088c3d6481b84b370fd06cde3a9)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#source FisExperimentTemplate#source}.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#value FisExperimentTemplate#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateStopCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FisExperimentTemplateStopConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateStopConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9ff3a3db767bd3aa27e354896066b6b6cca0599d4e31aee2fb924b4dad07058)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FisExperimentTemplateStopConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9edc78cc767c9e403e5afe366cfa035c40c259056fcf45ce8dc35c027577f20e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FisExperimentTemplateStopConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc9c4b4cf39e79822b00ba56ee0d72aa141340346c814a0b292dbd0dfa7179e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__169a95aca4b3a08d5471bf474dd109a644f1f392fb5530fe42f8fe82ff023c50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7652c4d84fe15021af06a583b355ff5966e964b0a791bd7b43950c8f9bf2ef44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateStopCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateStopCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateStopCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__002ba8b0c11c866569131fcfe2201d33de38eda074c4ca48d86d1c0dcb48ce81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FisExperimentTemplateStopConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateStopConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddd926182138874bb22eb00ba0813da12bfdcd8ac295655b721b05c568d269f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ade70566a5fa66695522a7df3ff658c7baec84e9d4e304cd2d494e81148de2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4627533e93e93450771df54044fc7622ae34a804509988b140d59582a7552541)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateStopCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateStopCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateStopCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d74fb1aa81ae8691e53f9e78405b5c7c86b124abf620ed71fd91605f0a61bf29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateTarget",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "resource_type": "resourceType",
        "selection_mode": "selectionMode",
        "filter": "filter",
        "parameters": "parameters",
        "resource_arns": "resourceArns",
        "resource_tag": "resourceTag",
    },
)
class FisExperimentTemplateTarget:
    def __init__(
        self,
        *,
        name: builtins.str,
        resource_type: builtins.str,
        selection_mode: builtins.str,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateTargetFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateTargetResourceTag", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#name FisExperimentTemplate#name}.
        :param resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#resource_type FisExperimentTemplate#resource_type}.
        :param selection_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#selection_mode FisExperimentTemplate#selection_mode}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#filter FisExperimentTemplate#filter}
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#parameters FisExperimentTemplate#parameters}.
        :param resource_arns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#resource_arns FisExperimentTemplate#resource_arns}.
        :param resource_tag: resource_tag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#resource_tag FisExperimentTemplate#resource_tag}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59a0a8743679fc7974ba2a7144e15517a7b2afa1a0e5ee0f4654436d00b1db74)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument selection_mode", value=selection_mode, expected_type=type_hints["selection_mode"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument resource_arns", value=resource_arns, expected_type=type_hints["resource_arns"])
            check_type(argname="argument resource_tag", value=resource_tag, expected_type=type_hints["resource_tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "resource_type": resource_type,
            "selection_mode": selection_mode,
        }
        if filter is not None:
            self._values["filter"] = filter
        if parameters is not None:
            self._values["parameters"] = parameters
        if resource_arns is not None:
            self._values["resource_arns"] = resource_arns
        if resource_tag is not None:
            self._values["resource_tag"] = resource_tag

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#name FisExperimentTemplate#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#resource_type FisExperimentTemplate#resource_type}.'''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selection_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#selection_mode FisExperimentTemplate#selection_mode}.'''
        result = self._values.get("selection_mode")
        assert result is not None, "Required property 'selection_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateTargetFilter"]]]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#filter FisExperimentTemplate#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateTargetFilter"]]], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#parameters FisExperimentTemplate#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def resource_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#resource_arns FisExperimentTemplate#resource_arns}.'''
        result = self._values.get("resource_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_tag(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateTargetResourceTag"]]]:
        '''resource_tag block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#resource_tag FisExperimentTemplate#resource_tag}
        '''
        result = self._values.get("resource_tag")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateTargetResourceTag"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateTargetFilter",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "values": "values"},
)
class FisExperimentTemplateTargetFilter:
    def __init__(
        self,
        *,
        path: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#path FisExperimentTemplate#path}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#values FisExperimentTemplate#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__285106d37e559bae735d39fc70e68965861eee58299130147d9fdd0f202e5c93)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "values": values,
        }

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#path FisExperimentTemplate#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#values FisExperimentTemplate#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateTargetFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FisExperimentTemplateTargetFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateTargetFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0602b6b6b302c8aa9f7b1ae8c2abe9e7d55a1d4f4d33f47a45d8b09e0a0f8550)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FisExperimentTemplateTargetFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ff80b2ee99e62464154edef9b2c0087a87314c62a41b39f9d9a7fca00208b8a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FisExperimentTemplateTargetFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec5552c085a2bae2fc6153433a2b440c2c1779d78570ee5f7353d70828a29ae6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8847756700ef0afc993987c4b37472e4379fcd7fbb7050f0941a5497d9344d87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__acf09a6353d5a2ac60a26f1718aba1c1c3d9db5ac90f69bdbaa343d4bd9200ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTargetFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTargetFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTargetFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13dbfaee4d87a136525cb0f20cd10f36d0ad69a3c9a5ad1b45fc0e67226b1240)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FisExperimentTemplateTargetFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateTargetFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67e69cc6abce7ab627bbed5edbb8ce381763b916b6559341d7c2eff22f2da986)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8f4900e616d0d36ec727a6ee23e3c368f7c0975dd9e92cf852d2fdbb18cdbe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__299e0c4792d536ed55eef63d6c6f93811d24a89f3a15604ffbe6d4d84676acbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateTargetFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateTargetFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateTargetFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a056aacb5433b23d669c41125be188747182b36c5a98c4e34a99eec04325309d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FisExperimentTemplateTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e7b45288562bea71c8562daab3837d9ca7ff08dc23a065fe59c4f1e322c4828)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FisExperimentTemplateTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6fb7517fbba2da5020826486068a9bf7c1c07f89d5ab86273114fc3d2801d65)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FisExperimentTemplateTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6119c0c804e3cc1631876afb6a7ac67b9900bd85a77799eb67be2d8817cf8b8a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6447ed7b145e50bf65044de879752ec3759b9cb1e57ec5ac5e67230c4bf5de1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f422be41d762d7179d677775d3ea9683ce3ab87e7061a2d806f9c94c0a85620b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd93903484131ef8ca79177c545b66d5072a090a879bddeb7dec556e234bf822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FisExperimentTemplateTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__886eee9e34a186d31cccbf3a1f4d64c266bd03e9d65639d228a03f1079ea4bed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateTargetFilter, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9703b0e32fc2836ee72e3b0ef97cb76a4fe87f06112b401ead9140a8fc9b1cbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putResourceTag")
    def put_resource_tag(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FisExperimentTemplateTargetResourceTag", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92e6d027ae90ad80b7d44396d735e8fa876c26238b1e3e2b4c0570c00dfb0185)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceTag", [value]))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetResourceArns")
    def reset_resource_arns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceArns", []))

    @jsii.member(jsii_name="resetResourceTag")
    def reset_resource_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTag", []))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> FisExperimentTemplateTargetFilterList:
        return typing.cast(FisExperimentTemplateTargetFilterList, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="resourceTag")
    def resource_tag(self) -> "FisExperimentTemplateTargetResourceTagList":
        return typing.cast("FisExperimentTemplateTargetResourceTagList", jsii.get(self, "resourceTag"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTargetFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTargetFilter]]], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceArnsInput")
    def resource_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTagInput")
    def resource_tag_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateTargetResourceTag"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FisExperimentTemplateTargetResourceTag"]]], jsii.get(self, "resourceTagInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="selectionModeInput")
    def selection_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selectionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__324e6b3823224765d39b28033c540d92c8d69ca34cdf0742f288ad6c599deae6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6403820b789793c3d4f0a7e0f452a79d4cf328f33f144ad989310abfc990895f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceArns")
    def resource_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceArns"))

    @resource_arns.setter
    def resource_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92dc06add3e2685dbd60e361c6c1ec79d736f67b91e0894212394e0c0f65aba6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad1717f4e70b98636e9d82d06fc878703515999977b4dcfccd0272beb4ad45a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="selectionMode")
    def selection_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selectionMode"))

    @selection_mode.setter
    def selection_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__218b79b91b37b842a31b5c7f4181391e544c2fb6f2c27ef34c964ad27b5918d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selectionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd83da5d7a7df1648ce731107591bc93ff701558f19b04d9a096286f5a962875)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateTargetResourceTag",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class FisExperimentTemplateTargetResourceTag:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#key FisExperimentTemplate#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#value FisExperimentTemplate#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f6cf8094a1ef6973025d5889567a6329cc26d6e286ca403c080365597c74d9d)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#key FisExperimentTemplate#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#value FisExperimentTemplate#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateTargetResourceTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FisExperimentTemplateTargetResourceTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateTargetResourceTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06ddacfa87bef3701f50048d8560ead5cd4e0f85b2a5a56b86b65ab027d20463)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FisExperimentTemplateTargetResourceTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97735699f2b0ca9db5edf6a913b42dd15190d7d676f41ad702b3557f6798becc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FisExperimentTemplateTargetResourceTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__805401d4ee8fc99ef3d9f6b336d2c7badd5ca9b2b7e3d687a666987c73e24b3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41e7aa94ae394ece18bf3ae3651d41ea80c15ca0ea83d6f80228cd9835e286ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf940b928059201b7ffb49eb6bdc7e69bcd654667880da0cdb43c76c3c489050)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTargetResourceTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTargetResourceTag]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTargetResourceTag]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b66dadbbf75f4ec39c3252177c31f767a2f695c2b050670cd65672aad570b824)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FisExperimentTemplateTargetResourceTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateTargetResourceTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a0a2700c9dba9dbc427c35e4725fe33cd6604f31e1803145b98769f14a436ce)
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
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0db0e1849a691074c63d5c6720d5bced4cfdbc4ad896105b3e05d5eac0a1fbee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ee452de27efc903ad2d8f8783d8c007a21b61afae801cca379a1436e3c6759)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateTargetResourceTag]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateTargetResourceTag]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateTargetResourceTag]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__916816891830371e6bef1f5d9febf0b2850f0dbe6aeba5016feea5ef29eed5f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class FisExperimentTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#create FisExperimentTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#delete FisExperimentTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#update FisExperimentTemplate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdedbb555f75ab4de0fc84b3a3b5ede1e135e64ae25b3d5c1e7149a6e367d12a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#create FisExperimentTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#delete FisExperimentTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fis_experiment_template#update FisExperimentTemplate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FisExperimentTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FisExperimentTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fisExperimentTemplate.FisExperimentTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__256c1b9b9d45b835ffa1dc543967c2afd7d8705ef4e84ee71d9f3d0348ba45f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64af88c711c78b209f101dc9ae90a72d8ef59ad3bd9e35cde05ddecadac2b6f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9cb34cc997b8b0c03368708d99f664bc62e8cf1f391fd8ccb3e86d0d92288a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__239723ef30afe19977513b30d1d0b1c3c6f4024a3c0863a06b5884a4bb76c17d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31863eafc8de4a3da1d80c3aaabaa07971cc093c923ef165e4f53f38e2439a0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FisExperimentTemplate",
    "FisExperimentTemplateAction",
    "FisExperimentTemplateActionList",
    "FisExperimentTemplateActionOutputReference",
    "FisExperimentTemplateActionParameter",
    "FisExperimentTemplateActionParameterList",
    "FisExperimentTemplateActionParameterOutputReference",
    "FisExperimentTemplateActionTarget",
    "FisExperimentTemplateActionTargetOutputReference",
    "FisExperimentTemplateConfig",
    "FisExperimentTemplateExperimentOptions",
    "FisExperimentTemplateExperimentOptionsOutputReference",
    "FisExperimentTemplateExperimentReportConfiguration",
    "FisExperimentTemplateExperimentReportConfigurationDataSources",
    "FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard",
    "FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboardList",
    "FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboardOutputReference",
    "FisExperimentTemplateExperimentReportConfigurationDataSourcesOutputReference",
    "FisExperimentTemplateExperimentReportConfigurationOutputReference",
    "FisExperimentTemplateExperimentReportConfigurationOutputs",
    "FisExperimentTemplateExperimentReportConfigurationOutputsOutputReference",
    "FisExperimentTemplateExperimentReportConfigurationOutputsS3Configuration",
    "FisExperimentTemplateExperimentReportConfigurationOutputsS3ConfigurationOutputReference",
    "FisExperimentTemplateLogConfiguration",
    "FisExperimentTemplateLogConfigurationCloudwatchLogsConfiguration",
    "FisExperimentTemplateLogConfigurationCloudwatchLogsConfigurationOutputReference",
    "FisExperimentTemplateLogConfigurationOutputReference",
    "FisExperimentTemplateLogConfigurationS3Configuration",
    "FisExperimentTemplateLogConfigurationS3ConfigurationOutputReference",
    "FisExperimentTemplateStopCondition",
    "FisExperimentTemplateStopConditionList",
    "FisExperimentTemplateStopConditionOutputReference",
    "FisExperimentTemplateTarget",
    "FisExperimentTemplateTargetFilter",
    "FisExperimentTemplateTargetFilterList",
    "FisExperimentTemplateTargetFilterOutputReference",
    "FisExperimentTemplateTargetList",
    "FisExperimentTemplateTargetOutputReference",
    "FisExperimentTemplateTargetResourceTag",
    "FisExperimentTemplateTargetResourceTagList",
    "FisExperimentTemplateTargetResourceTagOutputReference",
    "FisExperimentTemplateTimeouts",
    "FisExperimentTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c4cc33aec75247a02c09a67ec37e7287931b9a9f6ce40efec144b43fce51d47a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateAction, typing.Dict[builtins.str, typing.Any]]]],
    description: builtins.str,
    role_arn: builtins.str,
    stop_condition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateStopCondition, typing.Dict[builtins.str, typing.Any]]]],
    experiment_options: typing.Optional[typing.Union[FisExperimentTemplateExperimentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    experiment_report_configuration: typing.Optional[typing.Union[FisExperimentTemplateExperimentReportConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    log_configuration: typing.Optional[typing.Union[FisExperimentTemplateLogConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[FisExperimentTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8afdb69386b1f59706be39a97a1eceb363bc981b2a87e598ddfa7599ca891c47(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed92adf8c6d893aafccde45e7bbf048b7979df76d3c1a7401427ce2bfc567be4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc459a5667aaf1ca6e83d926f357b5208a35f6bc8bbe93be69d9bab26bfef916(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateStopCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b1173844cf57e23ff78fe8e703a2a2c00f19a482cd5e8698ed984d2f5617f31(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cb4131c9e0a56b60e960e8b0c538c195a58bfc8cf72619bcf8df135864a9194(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686ca11f8280f9c4c42fbb7c9f20b724c1bf263b8ad84476ae31284be2c6fe86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b971c4aa70a78130204ec25717b4683947e90c95b7adfd4a19a7bcc2c08f631e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcdefddf9db74adb1e290e01b9a7c66805f725855365ed74392e73e520ca2a8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fed14b95b7bbccbb5e6438094f3bdae21ab616285b7d392fd495b5a42e1b310(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__305b82d87ead720f8365ab191baea5f5ec1d961f67d5013285e614aee6d93941(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c117974cb446ce0a45d20a944530e1d049a1997e96c549f3c9b25eb62cc31bb(
    *,
    action_id: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateActionParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    start_after: typing.Optional[typing.Sequence[builtins.str]] = None,
    target: typing.Optional[typing.Union[FisExperimentTemplateActionTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9e6fffbf2dafaf51e52a9998dfbec7be097986f5daec2a30dc968a6e05986d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf49d0dc2a1f5b0a893e3cb68b8bffadc65da7f6acf164e91aeee0d5bafa358f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6fe213007dffdd5795c915314f34a8b92a7ba0d38281d9c5d3c1cf16991b295(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96bf74e0faf0bc8faf18af30c2cce6679d11ee574d093fa24a12d05864e250c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85f368979ebe81596ceb1d67c91407d43d9570acabfe4d2a08e65fc29130f16b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__911c19bd5728a3b25537b9a27d88233351be904cf5d5bcc9daadda78a64de77f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10c8ba77f44a249c3e37a717c2b6133947729e42f7daa48020bfb0524f34d19f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afeea4eea934a936a4aa263a3c68df47a42598c8d4a94b165f4df2793aaada29(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateActionParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc046274e502e55a06f3f01df5fd93b334e14119595d5aef03ea1714ebc47494(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2938eaf34a43f486ffdb22cd845d3b8d0fd44f9e4f19a1f637a4c214c2cfcf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f35290ad005325cf5b94f2a171154c5158f8b7829063458ae79063a787a396d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c3f9eeefc6c3844c54ae690c68f03ae0dec428d21fca551979d701b735e6fa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4908d12cd6334893614459be383a185b49cf28c730744c9ceb65e11e7603f61c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f110fbf0e104dd52593194940650cdd3603c72b9fc8155b40fe484795e2289d0(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4281ddccb2c208a418fe528e2c5c07862db25e3a11049aa883bdbb9dea3f4af9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9553e309382dbd3b4bb2f58f8caadf6143aa89182752499a032a3dda4d98ead(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f395ade77f8400925db42c499090dc8a9da5a464feb538a1c37a927ff9a7c8b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93d989c729d76802a42e2860f2102eb68d7fcb1e1db5a5f257f34c863dcee24(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9236514e4962965b7c004988b79267b37ca9e0bc686acb30a47a20d09cc8a58f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__303e921edd95fd95e21143ad5d774cbae1b0b5b05418827544733a9ce79117e0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateActionParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d8d3c9ce354b5a0a61d662e62322ebcf26f7e173de6f733b7318537e4f5948c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a17733ce143295ddea49a3c5402e4e5d98944fd6d66d41e0df5e2f6239563c99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f4ad5a9e59406fbaa000ad3f9a48314a149ba732819df456e85a47e6e80251(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf9df78e7d1d9ecac76ec74fbf4ce3b37952178d62ec7b85baaa07dd649bcc0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateActionParameter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf12acc9b4a969a6bd163e1529b298ffe0eb35d02ad90ba91bb756bdfb089ac(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__613fa41c294a72d9a841f6abc1613e960307b6e4c70da60a9815c57c3f22e9d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d7a1839ffa48868c58dc20033aeaae17111c4e11e66c7982d96fc082fd4ee7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f0ff252c2fbe31f7e85f681e1e360cd7df8047a228af130a03508179086526b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125eb2a292a105b2566cb5c99ece1abe8e3f4f11c06d98b55cdb50118bea73a7(
    value: typing.Optional[FisExperimentTemplateActionTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec4fc8e38ecbbce021fa89f4a4e975d8f8e228653f08591876795b1075c77653(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateAction, typing.Dict[builtins.str, typing.Any]]]],
    description: builtins.str,
    role_arn: builtins.str,
    stop_condition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateStopCondition, typing.Dict[builtins.str, typing.Any]]]],
    experiment_options: typing.Optional[typing.Union[FisExperimentTemplateExperimentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    experiment_report_configuration: typing.Optional[typing.Union[FisExperimentTemplateExperimentReportConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    log_configuration: typing.Optional[typing.Union[FisExperimentTemplateLogConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[FisExperimentTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69bdb5dd938df79d3555f230ae0982ebbed19f286daf4ea63d32e41b70482b67(
    *,
    account_targeting: typing.Optional[builtins.str] = None,
    empty_target_resolution_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cafda7bc89e3bd428e97b19822e998405a3c00cffe1cc5bdd927d4e564e3cfa1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c53de0b2017ea210f061b049efcd1361d47862f4a20b6a28c6aaacd532ba65d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de527a799364a2348fbc623b8f46cf9f11390c8bf6292b43b98168afc29875e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c022ff9180b82b159433b766a85909ae5fcc7cd3aebf6a75c7fe4a32da2b21(
    value: typing.Optional[FisExperimentTemplateExperimentOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43be4301df9d38c5e0ae18e6e30557e63c35100b28b91ad6ac0620e6f1c76d2c(
    *,
    data_sources: typing.Optional[typing.Union[FisExperimentTemplateExperimentReportConfigurationDataSources, typing.Dict[builtins.str, typing.Any]]] = None,
    outputs: typing.Optional[typing.Union[FisExperimentTemplateExperimentReportConfigurationOutputs, typing.Dict[builtins.str, typing.Any]]] = None,
    post_experiment_duration: typing.Optional[builtins.str] = None,
    pre_experiment_duration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d754606a50bde2d533b14aaf91d4cd734c744b43d126ed45af21b413992388(
    *,
    cloudwatch_dashboard: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__237df9f4f6e3962212d2de9057e317259b5cf5a868c7dce4d3514d699fd02cdf(
    *,
    dashboard_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97158213231121147af122936a57f7e405d1bc3f6911f4a0b02d7be6d872c8ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d69ac74d8ef4e091525a04f356f4baa716d8c48c221c8649159f239caaa04c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd0296b047ae964b4008533e4d06d8dd389b60094da6717574c48667f3fb9bad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0181de43b1fd03b3b093f3c70122323105a8fc9ddadc2e1515ab40fad9d6afc2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c535a7f31daee571ff3839f34c9f0ab9cec909ba44a4f8f53a525e7691cc121b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63d45424e32c36b43a97302bc455c5e9124c0a34ed6163616388f2695a9614f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57d1ea5e136e15c27fa892368e3302798018c7845744a2aa6fa3e955dbe9f3ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015007b76f0b8f25b2eae31b4f9e525acb5b6bd7c8032709e40f108bb71b61ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__534e412862c020006cab41e3e9d3bf5d2957e8216714e37b44746988e9745831(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80298c154ca3c5d6a5e78c18adf3e151a2d4012c3b72d7023eb93b40397f6f51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbae5ef19800c71745a04e50727c95397dd90a2ef9d2e775eb4fcf2d35f0fdec(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateExperimentReportConfigurationDataSourcesCloudwatchDashboard, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f4ac667c6904fbc8cf82e016886aa7077ab70a5dc6ff5b151ef28aca23be14(
    value: typing.Optional[FisExperimentTemplateExperimentReportConfigurationDataSources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081562651047d100d16133b06915ab7fc3f106cfad898cd5993239399855973a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd3b07f1b79ae17f96e5680ba38be2cc846111b7b571a64b3597deb64d8af2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb17c1ff72b945c162639e0cb0213b0eb4c0a9ce4f8150cb8e96061205ba0d12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baa9b4da2baa1659c1f7c7b0e3b520a9eb7d102b972e70bb7ae9770cecd06354(
    value: typing.Optional[FisExperimentTemplateExperimentReportConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__805b76c3c096267742c84302ce0fea2bb2d9ae03e903dfd86210628a2f61e485(
    *,
    s3_configuration: typing.Optional[typing.Union[FisExperimentTemplateExperimentReportConfigurationOutputsS3Configuration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe172420274e0b0a1e941935af228ee4625adf43b64f54c6a27de7df2872f7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75638b3622673598171d85d96879ab4ebb6da85a630b7a95200b80d19cf95a39(
    value: typing.Optional[FisExperimentTemplateExperimentReportConfigurationOutputs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac1697c66fd2cb6cef739c7b90310776eb5bbe7ac93353fe43ed3e9813512808(
    *,
    bucket_name: builtins.str,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d1e5067d6b58974778d6c7319e3e6c04fbe1cbf5a31810efbd5acb8b073fc20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5d9732c8b3ce3ae5f00e870243492f47bdb6edd6e70703ee21cecf19f80c957(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d847d2bb9cd8a1e00d93329c5d1e8cae8b273b2fad0ae6327431ad5e441023e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d5974a20c9eb28f26f21b5763c483982eec3239f2f1d7eeb439366e641feba(
    value: typing.Optional[FisExperimentTemplateExperimentReportConfigurationOutputsS3Configuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b7023d402acd614d02b5b7dc53ed946258967036ba08c3c1653a47b73e8307(
    *,
    log_schema_version: jsii.Number,
    cloudwatch_logs_configuration: typing.Optional[typing.Union[FisExperimentTemplateLogConfigurationCloudwatchLogsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_configuration: typing.Optional[typing.Union[FisExperimentTemplateLogConfigurationS3Configuration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__584cb1c7a1a57dc8f7332a43667097216ddb105f2b12fddf600d71dbc9ade0cd(
    *,
    log_group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2b044d3d581b28396849f4c7e7450734ce557e0201633db03e8b8f4ef4d714(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__149df848a4104bb0344e31a9f944f6bcac6d8325e3bea41e193be14ea020f9e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e10af770bce5268344762e6fbd6c47dc620782d0a2949baa74c154b65e9ac61(
    value: typing.Optional[FisExperimentTemplateLogConfigurationCloudwatchLogsConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61bd4be35d1266b1a79b66c45adf1b6f4c30280f2b4e92d7b7ec2578204c4a91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aba61e2d82703c2aeb6791b4e2832d6a0db3e4911f57eb5505f3bc157d69b93(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3fe12e882513dec4b605f11a1bb2c32a56a39d43ce5b296d83fd6d5f886f984(
    value: typing.Optional[FisExperimentTemplateLogConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__599e016baa0585251b24e9606c49dc0dd0216f3bb324b46b3b5a512486643852(
    *,
    bucket_name: builtins.str,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b36f9d001e21f5f911ef23b365e35dd74544aeec33abf542ac80a1778d9377d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e720e8d3c088940798f899e484427a9c572345e38b1e2110b939b4fa99704e73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3454cbb96f772d0583d7ce88c057dbc1e79700a414a77165d77eb438ecc107d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab31a50356e0553d4a6e0938696b6c1ea2ad10bc57b6b2987eb9040ad4a2c56(
    value: typing.Optional[FisExperimentTemplateLogConfigurationS3Configuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b2e99e65393a3748e7099ba2660a94d049e088c3d6481b84b370fd06cde3a9(
    *,
    source: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9ff3a3db767bd3aa27e354896066b6b6cca0599d4e31aee2fb924b4dad07058(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9edc78cc767c9e403e5afe366cfa035c40c259056fcf45ce8dc35c027577f20e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc9c4b4cf39e79822b00ba56ee0d72aa141340346c814a0b292dbd0dfa7179e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__169a95aca4b3a08d5471bf474dd109a644f1f392fb5530fe42f8fe82ff023c50(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7652c4d84fe15021af06a583b355ff5966e964b0a791bd7b43950c8f9bf2ef44(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002ba8b0c11c866569131fcfe2201d33de38eda074c4ca48d86d1c0dcb48ce81(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateStopCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd926182138874bb22eb00ba0813da12bfdcd8ac295655b721b05c568d269f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ade70566a5fa66695522a7df3ff658c7baec84e9d4e304cd2d494e81148de2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4627533e93e93450771df54044fc7622ae34a804509988b140d59582a7552541(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d74fb1aa81ae8691e53f9e78405b5c7c86b124abf620ed71fd91605f0a61bf29(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateStopCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a0a8743679fc7974ba2a7144e15517a7b2afa1a0e5ee0f4654436d00b1db74(
    *,
    name: builtins.str,
    resource_type: builtins.str,
    selection_mode: builtins.str,
    filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateTargetFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateTargetResourceTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__285106d37e559bae735d39fc70e68965861eee58299130147d9fdd0f202e5c93(
    *,
    path: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0602b6b6b302c8aa9f7b1ae8c2abe9e7d55a1d4f4d33f47a45d8b09e0a0f8550(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff80b2ee99e62464154edef9b2c0087a87314c62a41b39f9d9a7fca00208b8a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec5552c085a2bae2fc6153433a2b440c2c1779d78570ee5f7353d70828a29ae6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8847756700ef0afc993987c4b37472e4379fcd7fbb7050f0941a5497d9344d87(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf09a6353d5a2ac60a26f1718aba1c1c3d9db5ac90f69bdbaa343d4bd9200ee(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13dbfaee4d87a136525cb0f20cd10f36d0ad69a3c9a5ad1b45fc0e67226b1240(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTargetFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67e69cc6abce7ab627bbed5edbb8ce381763b916b6559341d7c2eff22f2da986(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f4900e616d0d36ec727a6ee23e3c368f7c0975dd9e92cf852d2fdbb18cdbe6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299e0c4792d536ed55eef63d6c6f93811d24a89f3a15604ffbe6d4d84676acbb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a056aacb5433b23d669c41125be188747182b36c5a98c4e34a99eec04325309d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateTargetFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e7b45288562bea71c8562daab3837d9ca7ff08dc23a065fe59c4f1e322c4828(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6fb7517fbba2da5020826486068a9bf7c1c07f89d5ab86273114fc3d2801d65(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6119c0c804e3cc1631876afb6a7ac67b9900bd85a77799eb67be2d8817cf8b8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6447ed7b145e50bf65044de879752ec3759b9cb1e57ec5ac5e67230c4bf5de1e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f422be41d762d7179d677775d3ea9683ce3ab87e7061a2d806f9c94c0a85620b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd93903484131ef8ca79177c545b66d5072a090a879bddeb7dec556e234bf822(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__886eee9e34a186d31cccbf3a1f4d64c266bd03e9d65639d228a03f1079ea4bed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9703b0e32fc2836ee72e3b0ef97cb76a4fe87f06112b401ead9140a8fc9b1cbc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateTargetFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e6d027ae90ad80b7d44396d735e8fa876c26238b1e3e2b4c0570c00dfb0185(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FisExperimentTemplateTargetResourceTag, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__324e6b3823224765d39b28033c540d92c8d69ca34cdf0742f288ad6c599deae6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6403820b789793c3d4f0a7e0f452a79d4cf328f33f144ad989310abfc990895f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92dc06add3e2685dbd60e361c6c1ec79d736f67b91e0894212394e0c0f65aba6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad1717f4e70b98636e9d82d06fc878703515999977b4dcfccd0272beb4ad45a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__218b79b91b37b842a31b5c7f4181391e544c2fb6f2c27ef34c964ad27b5918d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd83da5d7a7df1648ce731107591bc93ff701558f19b04d9a096286f5a962875(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f6cf8094a1ef6973025d5889567a6329cc26d6e286ca403c080365597c74d9d(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ddacfa87bef3701f50048d8560ead5cd4e0f85b2a5a56b86b65ab027d20463(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97735699f2b0ca9db5edf6a913b42dd15190d7d676f41ad702b3557f6798becc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__805401d4ee8fc99ef3d9f6b336d2c7badd5ca9b2b7e3d687a666987c73e24b3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e7aa94ae394ece18bf3ae3651d41ea80c15ca0ea83d6f80228cd9835e286ad(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf940b928059201b7ffb49eb6bdc7e69bcd654667880da0cdb43c76c3c489050(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66dadbbf75f4ec39c3252177c31f767a2f695c2b050670cd65672aad570b824(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FisExperimentTemplateTargetResourceTag]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a0a2700c9dba9dbc427c35e4725fe33cd6604f31e1803145b98769f14a436ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db0e1849a691074c63d5c6720d5bced4cfdbc4ad896105b3e05d5eac0a1fbee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ee452de27efc903ad2d8f8783d8c007a21b61afae801cca379a1436e3c6759(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__916816891830371e6bef1f5d9febf0b2850f0dbe6aeba5016feea5ef29eed5f0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateTargetResourceTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdedbb555f75ab4de0fc84b3a3b5ede1e135e64ae25b3d5c1e7149a6e367d12a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__256c1b9b9d45b835ffa1dc543967c2afd7d8705ef4e84ee71d9f3d0348ba45f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64af88c711c78b209f101dc9ae90a72d8ef59ad3bd9e35cde05ddecadac2b6f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9cb34cc997b8b0c03368708d99f664bc62e8cf1f391fd8ccb3e86d0d92288a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__239723ef30afe19977513b30d1d0b1c3c6f4024a3c0863a06b5884a4bb76c17d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31863eafc8de4a3da1d80c3aaabaa07971cc093c923ef165e4f53f38e2439a0d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FisExperimentTemplateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
