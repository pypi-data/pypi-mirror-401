r'''
# `aws_macie2_classification_job`

Refer to the Terraform Registry for docs: [`aws_macie2_classification_job`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job).
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


class Macie2ClassificationJob(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJob",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job aws_macie2_classification_job}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        job_type: builtins.str,
        s3_job_definition: typing.Union["Macie2ClassificationJobS3JobDefinition", typing.Dict[builtins.str, typing.Any]],
        custom_data_identifier_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        initial_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        job_status: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        sampling_percentage: typing.Optional[jsii.Number] = None,
        schedule_frequency: typing.Optional[typing.Union["Macie2ClassificationJobScheduleFrequency", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["Macie2ClassificationJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job aws_macie2_classification_job} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param job_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#job_type Macie2ClassificationJob#job_type}.
        :param s3_job_definition: s3_job_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#s3_job_definition Macie2ClassificationJob#s3_job_definition}
        :param custom_data_identifier_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#custom_data_identifier_ids Macie2ClassificationJob#custom_data_identifier_ids}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#description Macie2ClassificationJob#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#id Macie2ClassificationJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_run: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#initial_run Macie2ClassificationJob#initial_run}.
        :param job_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#job_status Macie2ClassificationJob#job_status}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#name Macie2ClassificationJob#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#name_prefix Macie2ClassificationJob#name_prefix}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#region Macie2ClassificationJob#region}
        :param sampling_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#sampling_percentage Macie2ClassificationJob#sampling_percentage}.
        :param schedule_frequency: schedule_frequency block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#schedule_frequency Macie2ClassificationJob#schedule_frequency}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tags Macie2ClassificationJob#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tags_all Macie2ClassificationJob#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#timeouts Macie2ClassificationJob#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b27f646cb589918b6833577cd0c1cffa029ba870c44bb9892b8a8f930553f3c3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = Macie2ClassificationJobConfig(
            job_type=job_type,
            s3_job_definition=s3_job_definition,
            custom_data_identifier_ids=custom_data_identifier_ids,
            description=description,
            id=id,
            initial_run=initial_run,
            job_status=job_status,
            name=name,
            name_prefix=name_prefix,
            region=region,
            sampling_percentage=sampling_percentage,
            schedule_frequency=schedule_frequency,
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
        '''Generates CDKTF code for importing a Macie2ClassificationJob resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Macie2ClassificationJob to import.
        :param import_from_id: The id of the existing Macie2ClassificationJob that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Macie2ClassificationJob to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee968fc8518efb0bfb702808348328c88b175644c6b55b644f4df9ee04b05f5f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putS3JobDefinition")
    def put_s3_job_definition(
        self,
        *,
        bucket_criteria: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteria", typing.Dict[builtins.str, typing.Any]]] = None,
        bucket_definitions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketDefinitions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scoping: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionScoping", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket_criteria: bucket_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#bucket_criteria Macie2ClassificationJob#bucket_criteria}
        :param bucket_definitions: bucket_definitions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#bucket_definitions Macie2ClassificationJob#bucket_definitions}
        :param scoping: scoping block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#scoping Macie2ClassificationJob#scoping}
        '''
        value = Macie2ClassificationJobS3JobDefinition(
            bucket_criteria=bucket_criteria,
            bucket_definitions=bucket_definitions,
            scoping=scoping,
        )

        return typing.cast(None, jsii.invoke(self, "putS3JobDefinition", [value]))

    @jsii.member(jsii_name="putScheduleFrequency")
    def put_schedule_frequency(
        self,
        *,
        daily_schedule: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monthly_schedule: typing.Optional[jsii.Number] = None,
        weekly_schedule: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param daily_schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#daily_schedule Macie2ClassificationJob#daily_schedule}.
        :param monthly_schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#monthly_schedule Macie2ClassificationJob#monthly_schedule}.
        :param weekly_schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#weekly_schedule Macie2ClassificationJob#weekly_schedule}.
        '''
        value = Macie2ClassificationJobScheduleFrequency(
            daily_schedule=daily_schedule,
            monthly_schedule=monthly_schedule,
            weekly_schedule=weekly_schedule,
        )

        return typing.cast(None, jsii.invoke(self, "putScheduleFrequency", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#create Macie2ClassificationJob#create}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#update Macie2ClassificationJob#update}.
        '''
        value = Macie2ClassificationJobTimeouts(create=create, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCustomDataIdentifierIds")
    def reset_custom_data_identifier_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomDataIdentifierIds", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInitialRun")
    def reset_initial_run(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialRun", []))

    @jsii.member(jsii_name="resetJobStatus")
    def reset_job_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJobStatus", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamePrefix")
    def reset_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamePrefix", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSamplingPercentage")
    def reset_sampling_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSamplingPercentage", []))

    @jsii.member(jsii_name="resetScheduleFrequency")
    def reset_schedule_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduleFrequency", []))

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
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="jobArn")
    def job_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobArn"))

    @builtins.property
    @jsii.member(jsii_name="jobId")
    def job_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobId"))

    @builtins.property
    @jsii.member(jsii_name="s3JobDefinition")
    def s3_job_definition(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionOutputReference":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionOutputReference", jsii.get(self, "s3JobDefinition"))

    @builtins.property
    @jsii.member(jsii_name="scheduleFrequency")
    def schedule_frequency(
        self,
    ) -> "Macie2ClassificationJobScheduleFrequencyOutputReference":
        return typing.cast("Macie2ClassificationJobScheduleFrequencyOutputReference", jsii.get(self, "scheduleFrequency"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "Macie2ClassificationJobTimeoutsOutputReference":
        return typing.cast("Macie2ClassificationJobTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="userPausedDetails")
    def user_paused_details(self) -> "Macie2ClassificationJobUserPausedDetailsList":
        return typing.cast("Macie2ClassificationJobUserPausedDetailsList", jsii.get(self, "userPausedDetails"))

    @builtins.property
    @jsii.member(jsii_name="customDataIdentifierIdsInput")
    def custom_data_identifier_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "customDataIdentifierIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="initialRunInput")
    def initial_run_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "initialRunInput"))

    @builtins.property
    @jsii.member(jsii_name="jobStatusInput")
    def job_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="jobTypeInput")
    def job_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namePrefixInput")
    def name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="s3JobDefinitionInput")
    def s3_job_definition_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinition"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinition"], jsii.get(self, "s3JobDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="samplingPercentageInput")
    def sampling_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "samplingPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleFrequencyInput")
    def schedule_frequency_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobScheduleFrequency"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobScheduleFrequency"], jsii.get(self, "scheduleFrequencyInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "Macie2ClassificationJobTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "Macie2ClassificationJobTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="customDataIdentifierIds")
    def custom_data_identifier_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customDataIdentifierIds"))

    @custom_data_identifier_ids.setter
    def custom_data_identifier_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48d3fa0d5f073d8e270dcc359bff406524e968d8ef8367364bee18a08bf5bc9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDataIdentifierIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__946a2681566b2ba68ab0e3727c0ae8a824fcb855080dfd7c57542184c0c8a71b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12bc6d950649773961ad0f657735083157c13907cb0a60c6e1b57bcd2e9d9d9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialRun")
    def initial_run(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "initialRun"))

    @initial_run.setter
    def initial_run(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99c96bbb9909ab64aca2483c08cc670636af1c84dd1fcc5230929f9a74ec30fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialRun", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobStatus")
    def job_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobStatus"))

    @job_status.setter
    def job_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b0abbbd5b09b6aa0a6ea3877d8134d0236e8037669faa836175612871837a39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jobType")
    def job_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobType"))

    @job_type.setter
    def job_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd28aeaf3713887db444206fb52d1db628ffa28406fed85800848c750e73c73a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e22622ef4a1839b088bfcef31c0e8f29355c5a36ea807df2cdcc55c8c975e56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @name_prefix.setter
    def name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b34928322c3fe215fb861f7ce0c2ff6b6f7a0029d7ebaca4094b176bcced0f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1eaf5e00cf44ac41b4381a4daa6c327a348a7bff9ecb14e6d3175e6b7049c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="samplingPercentage")
    def sampling_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "samplingPercentage"))

    @sampling_percentage.setter
    def sampling_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5e1385fb628fd33039b4ccf5381ef3e07c685f8e62f16dacd1d0743ba90cec1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samplingPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bcf59dd846b84e07781154169bd835fcffb22aa3ba570059c7f62efcb29aa0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbd30dbb71172e184f4db88e7d6dff089bf5b6d0db7688a3423b5c39d419196b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "job_type": "jobType",
        "s3_job_definition": "s3JobDefinition",
        "custom_data_identifier_ids": "customDataIdentifierIds",
        "description": "description",
        "id": "id",
        "initial_run": "initialRun",
        "job_status": "jobStatus",
        "name": "name",
        "name_prefix": "namePrefix",
        "region": "region",
        "sampling_percentage": "samplingPercentage",
        "schedule_frequency": "scheduleFrequency",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
    },
)
class Macie2ClassificationJobConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        job_type: builtins.str,
        s3_job_definition: typing.Union["Macie2ClassificationJobS3JobDefinition", typing.Dict[builtins.str, typing.Any]],
        custom_data_identifier_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        initial_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        job_status: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        sampling_percentage: typing.Optional[jsii.Number] = None,
        schedule_frequency: typing.Optional[typing.Union["Macie2ClassificationJobScheduleFrequency", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["Macie2ClassificationJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param job_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#job_type Macie2ClassificationJob#job_type}.
        :param s3_job_definition: s3_job_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#s3_job_definition Macie2ClassificationJob#s3_job_definition}
        :param custom_data_identifier_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#custom_data_identifier_ids Macie2ClassificationJob#custom_data_identifier_ids}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#description Macie2ClassificationJob#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#id Macie2ClassificationJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_run: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#initial_run Macie2ClassificationJob#initial_run}.
        :param job_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#job_status Macie2ClassificationJob#job_status}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#name Macie2ClassificationJob#name}.
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#name_prefix Macie2ClassificationJob#name_prefix}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#region Macie2ClassificationJob#region}
        :param sampling_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#sampling_percentage Macie2ClassificationJob#sampling_percentage}.
        :param schedule_frequency: schedule_frequency block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#schedule_frequency Macie2ClassificationJob#schedule_frequency}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tags Macie2ClassificationJob#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tags_all Macie2ClassificationJob#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#timeouts Macie2ClassificationJob#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(s3_job_definition, dict):
            s3_job_definition = Macie2ClassificationJobS3JobDefinition(**s3_job_definition)
        if isinstance(schedule_frequency, dict):
            schedule_frequency = Macie2ClassificationJobScheduleFrequency(**schedule_frequency)
        if isinstance(timeouts, dict):
            timeouts = Macie2ClassificationJobTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7134d153c1af478cc168b2a9e6b9247e70ff92ed4fb8df1ab1c7b3a5d9b77580)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument job_type", value=job_type, expected_type=type_hints["job_type"])
            check_type(argname="argument s3_job_definition", value=s3_job_definition, expected_type=type_hints["s3_job_definition"])
            check_type(argname="argument custom_data_identifier_ids", value=custom_data_identifier_ids, expected_type=type_hints["custom_data_identifier_ids"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument initial_run", value=initial_run, expected_type=type_hints["initial_run"])
            check_type(argname="argument job_status", value=job_status, expected_type=type_hints["job_status"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument name_prefix", value=name_prefix, expected_type=type_hints["name_prefix"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument sampling_percentage", value=sampling_percentage, expected_type=type_hints["sampling_percentage"])
            check_type(argname="argument schedule_frequency", value=schedule_frequency, expected_type=type_hints["schedule_frequency"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "job_type": job_type,
            "s3_job_definition": s3_job_definition,
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
        if custom_data_identifier_ids is not None:
            self._values["custom_data_identifier_ids"] = custom_data_identifier_ids
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if initial_run is not None:
            self._values["initial_run"] = initial_run
        if job_status is not None:
            self._values["job_status"] = job_status
        if name is not None:
            self._values["name"] = name
        if name_prefix is not None:
            self._values["name_prefix"] = name_prefix
        if region is not None:
            self._values["region"] = region
        if sampling_percentage is not None:
            self._values["sampling_percentage"] = sampling_percentage
        if schedule_frequency is not None:
            self._values["schedule_frequency"] = schedule_frequency
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
    def job_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#job_type Macie2ClassificationJob#job_type}.'''
        result = self._values.get("job_type")
        assert result is not None, "Required property 'job_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_job_definition(self) -> "Macie2ClassificationJobS3JobDefinition":
        '''s3_job_definition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#s3_job_definition Macie2ClassificationJob#s3_job_definition}
        '''
        result = self._values.get("s3_job_definition")
        assert result is not None, "Required property 's3_job_definition' is missing"
        return typing.cast("Macie2ClassificationJobS3JobDefinition", result)

    @builtins.property
    def custom_data_identifier_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#custom_data_identifier_ids Macie2ClassificationJob#custom_data_identifier_ids}.'''
        result = self._values.get("custom_data_identifier_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#description Macie2ClassificationJob#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#id Macie2ClassificationJob#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_run(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#initial_run Macie2ClassificationJob#initial_run}.'''
        result = self._values.get("initial_run")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def job_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#job_status Macie2ClassificationJob#job_status}.'''
        result = self._values.get("job_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#name Macie2ClassificationJob#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#name_prefix Macie2ClassificationJob#name_prefix}.'''
        result = self._values.get("name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#region Macie2ClassificationJob#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sampling_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#sampling_percentage Macie2ClassificationJob#sampling_percentage}.'''
        result = self._values.get("sampling_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def schedule_frequency(
        self,
    ) -> typing.Optional["Macie2ClassificationJobScheduleFrequency"]:
        '''schedule_frequency block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#schedule_frequency Macie2ClassificationJob#schedule_frequency}
        '''
        result = self._values.get("schedule_frequency")
        return typing.cast(typing.Optional["Macie2ClassificationJobScheduleFrequency"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tags Macie2ClassificationJob#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tags_all Macie2ClassificationJob#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["Macie2ClassificationJobTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#timeouts Macie2ClassificationJob#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["Macie2ClassificationJobTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinition",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_criteria": "bucketCriteria",
        "bucket_definitions": "bucketDefinitions",
        "scoping": "scoping",
    },
)
class Macie2ClassificationJobS3JobDefinition:
    def __init__(
        self,
        *,
        bucket_criteria: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteria", typing.Dict[builtins.str, typing.Any]]] = None,
        bucket_definitions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketDefinitions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scoping: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionScoping", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param bucket_criteria: bucket_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#bucket_criteria Macie2ClassificationJob#bucket_criteria}
        :param bucket_definitions: bucket_definitions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#bucket_definitions Macie2ClassificationJob#bucket_definitions}
        :param scoping: scoping block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#scoping Macie2ClassificationJob#scoping}
        '''
        if isinstance(bucket_criteria, dict):
            bucket_criteria = Macie2ClassificationJobS3JobDefinitionBucketCriteria(**bucket_criteria)
        if isinstance(scoping, dict):
            scoping = Macie2ClassificationJobS3JobDefinitionScoping(**scoping)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fddc2ab6187bd44df4e3fe36277b708a25e6ef608d6f5f71dda94af67159d5f8)
            check_type(argname="argument bucket_criteria", value=bucket_criteria, expected_type=type_hints["bucket_criteria"])
            check_type(argname="argument bucket_definitions", value=bucket_definitions, expected_type=type_hints["bucket_definitions"])
            check_type(argname="argument scoping", value=scoping, expected_type=type_hints["scoping"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_criteria is not None:
            self._values["bucket_criteria"] = bucket_criteria
        if bucket_definitions is not None:
            self._values["bucket_definitions"] = bucket_definitions
        if scoping is not None:
            self._values["scoping"] = scoping

    @builtins.property
    def bucket_criteria(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteria"]:
        '''bucket_criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#bucket_criteria Macie2ClassificationJob#bucket_criteria}
        '''
        result = self._values.get("bucket_criteria")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteria"], result)

    @builtins.property
    def bucket_definitions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketDefinitions"]]]:
        '''bucket_definitions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#bucket_definitions Macie2ClassificationJob#bucket_definitions}
        '''
        result = self._values.get("bucket_definitions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketDefinitions"]]], result)

    @builtins.property
    def scoping(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScoping"]:
        '''scoping block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#scoping Macie2ClassificationJob#scoping}
        '''
        result = self._values.get("scoping")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScoping"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteria",
    jsii_struct_bases=[],
    name_mapping={"excludes": "excludes", "includes": "includes"},
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteria:
    def __init__(
        self,
        *,
        excludes: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes", typing.Dict[builtins.str, typing.Any]]] = None,
        includes: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param excludes: excludes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#excludes Macie2ClassificationJob#excludes}
        :param includes: includes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#includes Macie2ClassificationJob#includes}
        '''
        if isinstance(excludes, dict):
            excludes = Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes(**excludes)
        if isinstance(includes, dict):
            includes = Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes(**includes)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4486295bac77b06d2bf31169c8fa1976f6a28b327287fb1174e0adb9be1ba138)
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
            check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if excludes is not None:
            self._values["excludes"] = excludes
        if includes is not None:
            self._values["includes"] = includes

    @builtins.property
    def excludes(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes"]:
        '''excludes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#excludes Macie2ClassificationJob#excludes}
        '''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes"], result)

    @builtins.property
    def includes(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes"]:
        '''includes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#includes Macie2ClassificationJob#includes}
        '''
        result = self._values.get("includes")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes",
    jsii_struct_bases=[],
    name_mapping={"and_": "and"},
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes:
    def __init__(
        self,
        *,
        and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param and_: and block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21332f9c258d95f2293c79b5597ebdf255840c2b050cfb5c86afd7e3ebf85ff9)
            check_type(argname="argument and_", value=and_, expected_type=type_hints["and_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if and_ is not None:
            self._values["and_"] = and_

    @builtins.property
    def and_(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd"]]]:
        '''and block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        result = self._values.get("and_")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd",
    jsii_struct_bases=[],
    name_mapping={
        "simple_criterion": "simpleCriterion",
        "tag_criterion": "tagCriterion",
    },
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd:
    def __init__(
        self,
        *,
        simple_criterion: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_criterion: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param simple_criterion: simple_criterion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#simple_criterion Macie2ClassificationJob#simple_criterion}
        :param tag_criterion: tag_criterion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tag_criterion Macie2ClassificationJob#tag_criterion}
        '''
        if isinstance(simple_criterion, dict):
            simple_criterion = Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion(**simple_criterion)
        if isinstance(tag_criterion, dict):
            tag_criterion = Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion(**tag_criterion)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8732ca1e9d2d77f09f760b86fedb652428e9d22a57601e615618e68caea6bc9a)
            check_type(argname="argument simple_criterion", value=simple_criterion, expected_type=type_hints["simple_criterion"])
            check_type(argname="argument tag_criterion", value=tag_criterion, expected_type=type_hints["tag_criterion"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if simple_criterion is not None:
            self._values["simple_criterion"] = simple_criterion
        if tag_criterion is not None:
            self._values["tag_criterion"] = tag_criterion

    @builtins.property
    def simple_criterion(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion"]:
        '''simple_criterion block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#simple_criterion Macie2ClassificationJob#simple_criterion}
        '''
        result = self._values.get("simple_criterion")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion"], result)

    @builtins.property
    def tag_criterion(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion"]:
        '''tag_criterion block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tag_criterion Macie2ClassificationJob#tag_criterion}
        '''
        result = self._values.get("tag_criterion")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72abf350195283ccbac23fb4bf99d93bc07c135687acac03005419c374a0c3ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5072880ec83ad3e3d07d9c4bb41b18f27602e397e27c7bed26ae57d3cf76647)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ad23fc40e14bfe99353de98b0ba8f1fa800e09345478eaf5ec7184de091ca0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af2e7dc66bd87eb3dbc57147b6928000eca6c115be76fa055705b0ed44d336d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__029eedb082600072be4f926b998f05df70af1cbafe16fda4acfd639d16232aa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b61aabc18c85211cc0ab3276cc21f719c267fc6c04e8fca9e449940e2289b1f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb2d85aa656d7d2ef1c2d04c690188913bfbaff71613aa6f257e98604173e7eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSimpleCriterion")
    def put_simple_criterion(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.
        '''
        value = Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion(
            comparator=comparator, key=key, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putSimpleCriterion", [value]))

    @jsii.member(jsii_name="putTagCriterion")
    def put_tag_criterion(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param tag_values: tag_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        '''
        value = Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion(
            comparator=comparator, tag_values=tag_values
        )

        return typing.cast(None, jsii.invoke(self, "putTagCriterion", [value]))

    @jsii.member(jsii_name="resetSimpleCriterion")
    def reset_simple_criterion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSimpleCriterion", []))

    @jsii.member(jsii_name="resetTagCriterion")
    def reset_tag_criterion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagCriterion", []))

    @builtins.property
    @jsii.member(jsii_name="simpleCriterion")
    def simple_criterion(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterionOutputReference":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterionOutputReference", jsii.get(self, "simpleCriterion"))

    @builtins.property
    @jsii.member(jsii_name="tagCriterion")
    def tag_criterion(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionOutputReference":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionOutputReference", jsii.get(self, "tagCriterion"))

    @builtins.property
    @jsii.member(jsii_name="simpleCriterionInput")
    def simple_criterion_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion"], jsii.get(self, "simpleCriterionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagCriterionInput")
    def tag_criterion_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion"], jsii.get(self, "tagCriterionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c2d20f058b107eb8e170b64274bcdbee1dccf071bc0fe2bd515beacef3d0bc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion",
    jsii_struct_bases=[],
    name_mapping={"comparator": "comparator", "key": "key", "values": "values"},
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion:
    def __init__(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34034d8cc44ccb3fd875957df4e298f9b5cc2fd8ebc19f48261052a338f1a64e)
            check_type(argname="argument comparator", value=comparator, expected_type=type_hints["comparator"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comparator is not None:
            self._values["comparator"] = comparator
        if key is not None:
            self._values["key"] = key
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def comparator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.'''
        result = self._values.get("comparator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83ac5076706a3aa529f1ee346de0cde586c1942aeb2e7b1c01a026259af887bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetComparator")
    def reset_comparator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComparator", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="comparatorInput")
    def comparator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparatorInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="comparator")
    def comparator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparator"))

    @comparator.setter
    def comparator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e189a3b5b91e89de5db9163bb40c148fded84dbe9d2979587720bd36cdb6684)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d3cfa4220d1b2720484b64e9c48f14e44cb64a831ded24e620b26a6c63eee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf5f4e41a8e9a8b999735f60c93ac9bb987df8184715522b7151a5559a0d8d14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e13626784cbd3018d74d8176bdc75a64578a322e7443b9643f63c1da4cf37271)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion",
    jsii_struct_bases=[],
    name_mapping={"comparator": "comparator", "tag_values": "tagValues"},
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion:
    def __init__(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param tag_values: tag_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d065a383fbad797a9516b0d9a6ce27b9f3dfa145321fd5dc354c66b2869dbc)
            check_type(argname="argument comparator", value=comparator, expected_type=type_hints["comparator"])
            check_type(argname="argument tag_values", value=tag_values, expected_type=type_hints["tag_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comparator is not None:
            self._values["comparator"] = comparator
        if tag_values is not None:
            self._values["tag_values"] = tag_values

    @builtins.property
    def comparator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.'''
        result = self._values.get("comparator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_values(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues"]]]:
        '''tag_values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        '''
        result = self._values.get("tag_values")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3328325bd672cd376b7879f40442525778d1a684d4a849c0f6299244960ca0d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTagValues")
    def put_tag_values(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8914ff064df8631c13e121fb3f48ececfa8c7484ca154e9aff057f6b5b54837)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTagValues", [value]))

    @jsii.member(jsii_name="resetComparator")
    def reset_comparator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComparator", []))

    @jsii.member(jsii_name="resetTagValues")
    def reset_tag_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValues", []))

    @builtins.property
    @jsii.member(jsii_name="tagValues")
    def tag_values(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValuesList":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValuesList", jsii.get(self, "tagValues"))

    @builtins.property
    @jsii.member(jsii_name="comparatorInput")
    def comparator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparatorInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValuesInput")
    def tag_values_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues"]]], jsii.get(self, "tagValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="comparator")
    def comparator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparator"))

    @comparator.setter
    def comparator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b6dcd7b544e14293aa0885e52ef4ad3fa0750dff9f149c59a4bc88559debcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a05d31f4a63f62acbdd56bac6491225bbd52bdce9c73f5ebaa6bf4041c212303)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#value Macie2ClassificationJob#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d452374651ba5886aa559560d4a5cfc69acd4eec355fa0604cf944a0487e2e07)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#value Macie2ClassificationJob#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValuesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValuesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5885c06b610cb52e8509868b2c7005d5094b43215978570a286c509abf51881f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValuesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1374265b08364c705996f5b603bd1a61e1518a39f082317690bc85f5532f8dda)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValuesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eead6ac4717b489d80009ab63cc1670a9f0ab7e7ccc099ed71a935be6078415)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d438fcf138c2bfa81344a9d3686729bda882dbf628581beca31ef8e41b470238)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9794e203274bc451e18e90370925d8f907a06e22676759bc3b493b26dbb39fd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__821445a23b608965605deaab5c3ef85a4d2523879fba20abe6d6d6bead77dcb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c2fd39eb8c3311233d61faa74df3295ed9a1083844e88c63f8335cc53aa69f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__14b838fcdf6f2d0795368fea4267ba0a2b4486418049eeb53ee9a5a770d4301e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31cabe064aefc7ac864acc8f239a117cb7384296ccc6f7316392670a49c9d129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4159680af750fe2b1c66121abbcc6b55746bc6ccc86bb2497737ee89b08feb8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b9005a7f294a4d59089d69114d06e5ca1336ef953cc2415cd90aa70f27b8563)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAnd")
    def put_and(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27b2b623b07cb0d716f7976c74eb3c1c8cf984d89bb94ed32ff46c5c766a882c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAnd", [value]))

    @jsii.member(jsii_name="resetAnd")
    def reset_and(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnd", []))

    @builtins.property
    @jsii.member(jsii_name="and")
    def and_(
        self,
    ) -> Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndList:
        return typing.cast(Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndList, jsii.get(self, "and"))

    @builtins.property
    @jsii.member(jsii_name="andInput")
    def and_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd]]], jsii.get(self, "andInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fc6f5f11294da5733b7df5e7db479ef281dbfa52318921f852ad15186089746)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes",
    jsii_struct_bases=[],
    name_mapping={"and_": "and"},
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes:
    def __init__(
        self,
        *,
        and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param and_: and block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e42c09cd3fb8662ee299b944c5fa5552574adb7f3a2c74a8d922d476aa01e005)
            check_type(argname="argument and_", value=and_, expected_type=type_hints["and_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if and_ is not None:
            self._values["and_"] = and_

    @builtins.property
    def and_(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd"]]]:
        '''and block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        result = self._values.get("and_")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd",
    jsii_struct_bases=[],
    name_mapping={
        "simple_criterion": "simpleCriterion",
        "tag_criterion": "tagCriterion",
    },
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd:
    def __init__(
        self,
        *,
        simple_criterion: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_criterion: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param simple_criterion: simple_criterion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#simple_criterion Macie2ClassificationJob#simple_criterion}
        :param tag_criterion: tag_criterion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tag_criterion Macie2ClassificationJob#tag_criterion}
        '''
        if isinstance(simple_criterion, dict):
            simple_criterion = Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion(**simple_criterion)
        if isinstance(tag_criterion, dict):
            tag_criterion = Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion(**tag_criterion)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c880900b8891ef4a29f8e8dee12e1f27fb615d97b31052e70beb1d1ebabc8e16)
            check_type(argname="argument simple_criterion", value=simple_criterion, expected_type=type_hints["simple_criterion"])
            check_type(argname="argument tag_criterion", value=tag_criterion, expected_type=type_hints["tag_criterion"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if simple_criterion is not None:
            self._values["simple_criterion"] = simple_criterion
        if tag_criterion is not None:
            self._values["tag_criterion"] = tag_criterion

    @builtins.property
    def simple_criterion(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion"]:
        '''simple_criterion block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#simple_criterion Macie2ClassificationJob#simple_criterion}
        '''
        result = self._values.get("simple_criterion")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion"], result)

    @builtins.property
    def tag_criterion(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion"]:
        '''tag_criterion block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tag_criterion Macie2ClassificationJob#tag_criterion}
        '''
        result = self._values.get("tag_criterion")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6ffcb3856dfcf7b25d517db7d4186249414549d12a353ae2d1f826c2de52d19)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a2b0ce6d60e26830b3f90e7df0baf7b55e2873f8ebf1774cf640f2bc8fb3c80)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a0195a59b5b397d9c75cafaa87ed647a9968f06c9501ffb94383b8fd0bfa026)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be70c22dd592e112a423378a35c8a6c7f17173656f82a259c1ac8a5bc1e7b5e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__769554752155139a7895248053d0556dafbbbe85d82f9a74bffddcf4630d3d8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a5474b66362cf25f0380f2c382ded76ffdec3fd289248622b0adbde818bf8bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__882c777b91be818a835e26b18fa25875adc2fa1a63f47cc327df3154e2ab46c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSimpleCriterion")
    def put_simple_criterion(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.
        '''
        value = Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion(
            comparator=comparator, key=key, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putSimpleCriterion", [value]))

    @jsii.member(jsii_name="putTagCriterion")
    def put_tag_criterion(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param tag_values: tag_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        '''
        value = Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion(
            comparator=comparator, tag_values=tag_values
        )

        return typing.cast(None, jsii.invoke(self, "putTagCriterion", [value]))

    @jsii.member(jsii_name="resetSimpleCriterion")
    def reset_simple_criterion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSimpleCriterion", []))

    @jsii.member(jsii_name="resetTagCriterion")
    def reset_tag_criterion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagCriterion", []))

    @builtins.property
    @jsii.member(jsii_name="simpleCriterion")
    def simple_criterion(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterionOutputReference":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterionOutputReference", jsii.get(self, "simpleCriterion"))

    @builtins.property
    @jsii.member(jsii_name="tagCriterion")
    def tag_criterion(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionOutputReference":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionOutputReference", jsii.get(self, "tagCriterion"))

    @builtins.property
    @jsii.member(jsii_name="simpleCriterionInput")
    def simple_criterion_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion"], jsii.get(self, "simpleCriterionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagCriterionInput")
    def tag_criterion_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion"], jsii.get(self, "tagCriterionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acd417a172971dadc2913c0c78328674fb4df98a97e832755a155803d3fd50ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion",
    jsii_struct_bases=[],
    name_mapping={"comparator": "comparator", "key": "key", "values": "values"},
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion:
    def __init__(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4cee1d343af150f8a94cb3f29dae693916dea0f6a3e76c61d56561ab668ec26)
            check_type(argname="argument comparator", value=comparator, expected_type=type_hints["comparator"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comparator is not None:
            self._values["comparator"] = comparator
        if key is not None:
            self._values["key"] = key
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def comparator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.'''
        result = self._values.get("comparator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3dcd9b9e3e17df15c6993ee993e899af24da5c2538d927726cc3479c0797060f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetComparator")
    def reset_comparator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComparator", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="comparatorInput")
    def comparator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparatorInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="comparator")
    def comparator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparator"))

    @comparator.setter
    def comparator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c75414f43368f80e65a2ec4e9115fddb18780f1d4aabc0b0097ddee3040ed424)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83b45e5e181baa036fd40b155133e6d3f1a4481360ea75d37083cc02395f6bfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ab66e4899aed98edab7912127357c60480c5f08846bcde3e65a5facaba39d32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__862419614876fede75cf4a45da89ddc8428a5821369706c317074658a38d35bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion",
    jsii_struct_bases=[],
    name_mapping={"comparator": "comparator", "tag_values": "tagValues"},
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion:
    def __init__(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param tag_values: tag_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__348a366c7ebfc3ff333310fc1ac2b9ef23fe19027aa306f492b6e5b265ae9847)
            check_type(argname="argument comparator", value=comparator, expected_type=type_hints["comparator"])
            check_type(argname="argument tag_values", value=tag_values, expected_type=type_hints["tag_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comparator is not None:
            self._values["comparator"] = comparator
        if tag_values is not None:
            self._values["tag_values"] = tag_values

    @builtins.property
    def comparator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.'''
        result = self._values.get("comparator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_values(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues"]]]:
        '''tag_values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        '''
        result = self._values.get("tag_values")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eee36ea70d41a3ab47e9c9c695ef8896696e75b81801f037bb8c4aaf1b53dd7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTagValues")
    def put_tag_values(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f81d78766299651d8a679fefb8fd875af0374ec031a1d551035657f941bc876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTagValues", [value]))

    @jsii.member(jsii_name="resetComparator")
    def reset_comparator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComparator", []))

    @jsii.member(jsii_name="resetTagValues")
    def reset_tag_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValues", []))

    @builtins.property
    @jsii.member(jsii_name="tagValues")
    def tag_values(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValuesList":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValuesList", jsii.get(self, "tagValues"))

    @builtins.property
    @jsii.member(jsii_name="comparatorInput")
    def comparator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparatorInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValuesInput")
    def tag_values_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues"]]], jsii.get(self, "tagValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="comparator")
    def comparator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparator"))

    @comparator.setter
    def comparator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbfa3550da35846dd0455207e48fdee2e47e35fa43eaf3d3b7816dc367ef4701)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__256415c1b91af62f23f3e9b9dcf6d3d1b5bb448e90860ae7deca7b826709fdd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#value Macie2ClassificationJob#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c9fd0c60d7d2f2e2352187c22861346538b7d1946757891b5f977211e55c959)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#value Macie2ClassificationJob#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValuesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValuesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a30c6148170568dbf5ce38855fbaba35b20a2559797114d59adbdbf3b147b7db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValuesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0af012fead3f28cca100b14addd7087bb7dac2d1034df4e07167877ba0c8678a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValuesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a56ffe148c33c7a6811f538889f3e16bcf706500d711d175fc25d91aa9855a8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__795d872cfc729c96867dfeeadce7db3069014fc8c94e4798a69845e7d70f542d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__428d6ee28e88d3f4a2a6f0306bb67aa695e810a965eb941979b8eafc08984ed2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff62e08f6c4ee8373e2505dc11ae47a212f67fae92e484ff1edba914c8f504c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__954ff9d361ae1746c949c8f33598abd361d47a6548cf4bfeff5b6ffe5576c6c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d256fe8ece847260d929c310db677e625a7b7ff0212cd62173806e6cfc67fec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ea78167932fd89cb29ea1ecea2d79ea24929c17a610ecf62d86b256250e1a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ca86171edd2ff405c2cd82aded6d14861c823c67d0d61cacd40be4c4db63cc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b11f87961d623856d068ab64eb65d1b537031df629b53a29c8ef3d985d0b39b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAnd")
    def put_and(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6de0e5f81cf65bffbf078183e23f40c4e4e2cbcc5189cb3e22f53cb4cc7c29b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAnd", [value]))

    @jsii.member(jsii_name="resetAnd")
    def reset_and(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnd", []))

    @builtins.property
    @jsii.member(jsii_name="and")
    def and_(
        self,
    ) -> Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndList:
        return typing.cast(Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndList, jsii.get(self, "and"))

    @builtins.property
    @jsii.member(jsii_name="andInput")
    def and_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd]]], jsii.get(self, "andInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a00a0fd356899e15feb398fc0ef8a1057b090de4638cb32b494cdd0471d82d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionBucketCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec8ca8247fa5679e146542cbcc57cae115440609b024d77aa326e92be998e577)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExcludes")
    def put_excludes(
        self,
        *,
        and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param and_: and block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        value = Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes(and_=and_)

        return typing.cast(None, jsii.invoke(self, "putExcludes", [value]))

    @jsii.member(jsii_name="putIncludes")
    def put_includes(
        self,
        *,
        and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param and_: and block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        value = Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes(and_=and_)

        return typing.cast(None, jsii.invoke(self, "putIncludes", [value]))

    @jsii.member(jsii_name="resetExcludes")
    def reset_excludes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludes", []))

    @jsii.member(jsii_name="resetIncludes")
    def reset_includes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludes", []))

    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(
        self,
    ) -> Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesOutputReference:
        return typing.cast(Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesOutputReference, jsii.get(self, "excludes"))

    @builtins.property
    @jsii.member(jsii_name="includes")
    def includes(
        self,
    ) -> Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesOutputReference:
        return typing.cast(Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesOutputReference, jsii.get(self, "includes"))

    @builtins.property
    @jsii.member(jsii_name="excludesInput")
    def excludes_input(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes], jsii.get(self, "excludesInput"))

    @builtins.property
    @jsii.member(jsii_name="includesInput")
    def includes_input(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes], jsii.get(self, "includesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteria]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteria],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a02ec066ec6b6553865bc8b3533676419c34b7f6e8bd5c729aba68c3a853a24f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketDefinitions",
    jsii_struct_bases=[],
    name_mapping={"account_id": "accountId", "buckets": "buckets"},
)
class Macie2ClassificationJobS3JobDefinitionBucketDefinitions:
    def __init__(
        self,
        *,
        account_id: builtins.str,
        buckets: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#account_id Macie2ClassificationJob#account_id}.
        :param buckets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#buckets Macie2ClassificationJob#buckets}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__409b30772acdc69220c9f3cca065295ece32dce52346813f88780db53eb20a0f)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument buckets", value=buckets, expected_type=type_hints["buckets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "buckets": buckets,
        }

    @builtins.property
    def account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#account_id Macie2ClassificationJob#account_id}.'''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def buckets(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#buckets Macie2ClassificationJob#buckets}.'''
        result = self._values.get("buckets")
        assert result is not None, "Required property 'buckets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionBucketDefinitions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionBucketDefinitionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketDefinitionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09194a64252d9a0f72532ba21fd000847024950be18aa824466669816e6fd1ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Macie2ClassificationJobS3JobDefinitionBucketDefinitionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da0d49a03bcbd70c9e09b41754f3beea83a5ca0ed63787f001d7cc3c24034122)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Macie2ClassificationJobS3JobDefinitionBucketDefinitionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579317fc44c6cfa343863b0f0eac269c72392c878532ca1443eae2d5b5476b99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb21d6fc896a8135dd299a14eac779e30878db8fa16966809839a666190a712b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24ce8cdccb84e690c2490d51586feeb6bace5a5bcba43216539b3418efcf5c22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketDefinitions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketDefinitions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketDefinitions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ae790b3191ccecf0387ad7c43ebe8f21601c8931cd418c87c2c397bac60ab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionBucketDefinitionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionBucketDefinitionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c70da27c62dea45aa4cbd5434618cb5112879be3664a9d1c42120a7d9e9348bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketsInput")
    def buckets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "bucketsInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae36595933435e168428d7d36fde393d702c67e9a94e4f082d533ad0dc269430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="buckets")
    def buckets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "buckets"))

    @buckets.setter
    def buckets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ba508f29bd858625aa7d01e3b383d6c740793c0535e1b11df309d72cbd31eb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buckets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketDefinitions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketDefinitions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketDefinitions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a59c22900ed845da673bb063c0011704343906fd26fc8ae501644f47195b189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa48591774648c837499a846c90dc954c5c09424a8ee9acc4c753c95fb8df96b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBucketCriteria")
    def put_bucket_criteria(
        self,
        *,
        excludes: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes, typing.Dict[builtins.str, typing.Any]]] = None,
        includes: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param excludes: excludes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#excludes Macie2ClassificationJob#excludes}
        :param includes: includes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#includes Macie2ClassificationJob#includes}
        '''
        value = Macie2ClassificationJobS3JobDefinitionBucketCriteria(
            excludes=excludes, includes=includes
        )

        return typing.cast(None, jsii.invoke(self, "putBucketCriteria", [value]))

    @jsii.member(jsii_name="putBucketDefinitions")
    def put_bucket_definitions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketDefinitions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebcd0db9458285e9b01df165ad3a31103c4389fcdd4b34ee2726b56ee88ac9f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBucketDefinitions", [value]))

    @jsii.member(jsii_name="putScoping")
    def put_scoping(
        self,
        *,
        excludes: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingExcludes", typing.Dict[builtins.str, typing.Any]]] = None,
        includes: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingIncludes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param excludes: excludes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#excludes Macie2ClassificationJob#excludes}
        :param includes: includes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#includes Macie2ClassificationJob#includes}
        '''
        value = Macie2ClassificationJobS3JobDefinitionScoping(
            excludes=excludes, includes=includes
        )

        return typing.cast(None, jsii.invoke(self, "putScoping", [value]))

    @jsii.member(jsii_name="resetBucketCriteria")
    def reset_bucket_criteria(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketCriteria", []))

    @jsii.member(jsii_name="resetBucketDefinitions")
    def reset_bucket_definitions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketDefinitions", []))

    @jsii.member(jsii_name="resetScoping")
    def reset_scoping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScoping", []))

    @builtins.property
    @jsii.member(jsii_name="bucketCriteria")
    def bucket_criteria(
        self,
    ) -> Macie2ClassificationJobS3JobDefinitionBucketCriteriaOutputReference:
        return typing.cast(Macie2ClassificationJobS3JobDefinitionBucketCriteriaOutputReference, jsii.get(self, "bucketCriteria"))

    @builtins.property
    @jsii.member(jsii_name="bucketDefinitions")
    def bucket_definitions(
        self,
    ) -> Macie2ClassificationJobS3JobDefinitionBucketDefinitionsList:
        return typing.cast(Macie2ClassificationJobS3JobDefinitionBucketDefinitionsList, jsii.get(self, "bucketDefinitions"))

    @builtins.property
    @jsii.member(jsii_name="scoping")
    def scoping(self) -> "Macie2ClassificationJobS3JobDefinitionScopingOutputReference":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingOutputReference", jsii.get(self, "scoping"))

    @builtins.property
    @jsii.member(jsii_name="bucketCriteriaInput")
    def bucket_criteria_input(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteria]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteria], jsii.get(self, "bucketCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketDefinitionsInput")
    def bucket_definitions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketDefinitions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketDefinitions]]], jsii.get(self, "bucketDefinitionsInput"))

    @builtins.property
    @jsii.member(jsii_name="scopingInput")
    def scoping_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScoping"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScoping"], jsii.get(self, "scopingInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[Macie2ClassificationJobS3JobDefinition]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__028783e26cce2cc1b3c120d7fba4a48c1d33654f319fa673a47ab78539090e5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScoping",
    jsii_struct_bases=[],
    name_mapping={"excludes": "excludes", "includes": "includes"},
)
class Macie2ClassificationJobS3JobDefinitionScoping:
    def __init__(
        self,
        *,
        excludes: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingExcludes", typing.Dict[builtins.str, typing.Any]]] = None,
        includes: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingIncludes", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param excludes: excludes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#excludes Macie2ClassificationJob#excludes}
        :param includes: includes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#includes Macie2ClassificationJob#includes}
        '''
        if isinstance(excludes, dict):
            excludes = Macie2ClassificationJobS3JobDefinitionScopingExcludes(**excludes)
        if isinstance(includes, dict):
            includes = Macie2ClassificationJobS3JobDefinitionScopingIncludes(**includes)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdd4e97e8f54cdbacb025b4a71616a663a684da718b3b3847fe3f0eda5b7e8b6)
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
            check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if excludes is not None:
            self._values["excludes"] = excludes
        if includes is not None:
            self._values["includes"] = includes

    @builtins.property
    def excludes(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingExcludes"]:
        '''excludes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#excludes Macie2ClassificationJob#excludes}
        '''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingExcludes"], result)

    @builtins.property
    def includes(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingIncludes"]:
        '''includes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#includes Macie2ClassificationJob#includes}
        '''
        result = self._values.get("includes")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingIncludes"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScoping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludes",
    jsii_struct_bases=[],
    name_mapping={"and_": "and"},
)
class Macie2ClassificationJobS3JobDefinitionScopingExcludes:
    def __init__(
        self,
        *,
        and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param and_: and block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22e57fd95443a6295598f0e07b80c4106bd31692e7d3c67ba924bc3e3c273028)
            check_type(argname="argument and_", value=and_, expected_type=type_hints["and_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if and_ is not None:
            self._values["and_"] = and_

    @builtins.property
    def and_(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd"]]]:
        '''and block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        result = self._values.get("and_")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScopingExcludes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd",
    jsii_struct_bases=[],
    name_mapping={
        "simple_scope_term": "simpleScopeTerm",
        "tag_scope_term": "tagScopeTerm",
    },
)
class Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd:
    def __init__(
        self,
        *,
        simple_scope_term: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_scope_term: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param simple_scope_term: simple_scope_term block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#simple_scope_term Macie2ClassificationJob#simple_scope_term}
        :param tag_scope_term: tag_scope_term block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tag_scope_term Macie2ClassificationJob#tag_scope_term}
        '''
        if isinstance(simple_scope_term, dict):
            simple_scope_term = Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm(**simple_scope_term)
        if isinstance(tag_scope_term, dict):
            tag_scope_term = Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm(**tag_scope_term)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a70fd8f7eb021cbfed4b36b9515bd0234ab69e7dfcf453807c494ec4fb1bd47)
            check_type(argname="argument simple_scope_term", value=simple_scope_term, expected_type=type_hints["simple_scope_term"])
            check_type(argname="argument tag_scope_term", value=tag_scope_term, expected_type=type_hints["tag_scope_term"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if simple_scope_term is not None:
            self._values["simple_scope_term"] = simple_scope_term
        if tag_scope_term is not None:
            self._values["tag_scope_term"] = tag_scope_term

    @builtins.property
    def simple_scope_term(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm"]:
        '''simple_scope_term block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#simple_scope_term Macie2ClassificationJob#simple_scope_term}
        '''
        result = self._values.get("simple_scope_term")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm"], result)

    @builtins.property
    def tag_scope_term(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm"]:
        '''tag_scope_term block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tag_scope_term Macie2ClassificationJob#tag_scope_term}
        '''
        result = self._values.get("tag_scope_term")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionScopingExcludesAndList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesAndList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1fd60e7c1b1fa948065e5ea3c547b46f0670e38ef51088d023c4f373018f4b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9c60e0b3fa6128e50f75647463263d0eabb195edfc793a41f9326009b32be2c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingExcludesAndOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4a99aec9dec3b6d0c69f2cb84ccdf9c8e364be1fe842b371c62a57c4ce4923e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12d4f13e0066da291bb6b67efb39fb85dcc56e4db281207058430b76a6264a8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a89a45026aa35435b1068c6bc179a708ee8ba472cfffff498e627a6c681af5cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d43dc3e2bce2f77a815eeaace7654d10e90b8184e2a782fec7f84b54b0422e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionScopingExcludesAndOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesAndOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__338d6d5ac8efe596a90be318e71541a642b23d7e9dd96bdc31b4205cc34e972c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSimpleScopeTerm")
    def put_simple_scope_term(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.
        '''
        value = Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm(
            comparator=comparator, key=key, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putSimpleScopeTerm", [value]))

    @jsii.member(jsii_name="putTagScopeTerm")
    def put_tag_scope_term(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param tag_values: tag_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#target Macie2ClassificationJob#target}.
        '''
        value = Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm(
            comparator=comparator, key=key, tag_values=tag_values, target=target
        )

        return typing.cast(None, jsii.invoke(self, "putTagScopeTerm", [value]))

    @jsii.member(jsii_name="resetSimpleScopeTerm")
    def reset_simple_scope_term(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSimpleScopeTerm", []))

    @jsii.member(jsii_name="resetTagScopeTerm")
    def reset_tag_scope_term(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagScopeTerm", []))

    @builtins.property
    @jsii.member(jsii_name="simpleScopeTerm")
    def simple_scope_term(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTermOutputReference":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTermOutputReference", jsii.get(self, "simpleScopeTerm"))

    @builtins.property
    @jsii.member(jsii_name="tagScopeTerm")
    def tag_scope_term(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermOutputReference":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermOutputReference", jsii.get(self, "tagScopeTerm"))

    @builtins.property
    @jsii.member(jsii_name="simpleScopeTermInput")
    def simple_scope_term_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm"], jsii.get(self, "simpleScopeTermInput"))

    @builtins.property
    @jsii.member(jsii_name="tagScopeTermInput")
    def tag_scope_term_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm"], jsii.get(self, "tagScopeTermInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f231c11dca68d7cce3956e01623300211abac99bf7bc624ff78922a88548c19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm",
    jsii_struct_bases=[],
    name_mapping={"comparator": "comparator", "key": "key", "values": "values"},
)
class Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm:
    def __init__(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9abc41e0bff51507e28a5ef637a514574424d0f50b2f61df8a4741697ffb1a29)
            check_type(argname="argument comparator", value=comparator, expected_type=type_hints["comparator"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comparator is not None:
            self._values["comparator"] = comparator
        if key is not None:
            self._values["key"] = key
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def comparator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.'''
        result = self._values.get("comparator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTermOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTermOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb9debac8573dfee8c836cb8a138890ab4c83198affe21bf42e81ea65f661e1e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetComparator")
    def reset_comparator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComparator", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="comparatorInput")
    def comparator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparatorInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="comparator")
    def comparator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparator"))

    @comparator.setter
    def comparator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__441c9131141f1604431bc8d92f4438813f7fc17037ce07a27d85f30c8c97a8a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__766b8f65631e70c4be68ec81dad41a2060b53a09f625b0d62be1b7e71086e5fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f58a8ec3e4c6da66d5ad7b790e6bfdc91a955f98101febfd6ad0371af44e53d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a0f1c9b911dbdf9daef53ab8c629c4fd1b3e3d7bc2a94e811ebcf453cea9245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm",
    jsii_struct_bases=[],
    name_mapping={
        "comparator": "comparator",
        "key": "key",
        "tag_values": "tagValues",
        "target": "target",
    },
)
class Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm:
    def __init__(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param tag_values: tag_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#target Macie2ClassificationJob#target}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7824722e8b6931eb380b850f3574534afaed1c8154d54776a779ff70a16a8ca7)
            check_type(argname="argument comparator", value=comparator, expected_type=type_hints["comparator"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument tag_values", value=tag_values, expected_type=type_hints["tag_values"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comparator is not None:
            self._values["comparator"] = comparator
        if key is not None:
            self._values["key"] = key
        if tag_values is not None:
            self._values["tag_values"] = tag_values
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def comparator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.'''
        result = self._values.get("comparator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_values(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues"]]]:
        '''tag_values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        '''
        result = self._values.get("tag_values")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues"]]], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#target Macie2ClassificationJob#target}.'''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ef6ab5f3d2b5b6b1122fe92c9d680db40a32de77381f2c9b6bab275b020ee22)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTagValues")
    def put_tag_values(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__049d3887bf29643c870b91dcb5d70ee0168ccbc06a0fce9970c5287726876b42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTagValues", [value]))

    @jsii.member(jsii_name="resetComparator")
    def reset_comparator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComparator", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetTagValues")
    def reset_tag_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValues", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @builtins.property
    @jsii.member(jsii_name="tagValues")
    def tag_values(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValuesList":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValuesList", jsii.get(self, "tagValues"))

    @builtins.property
    @jsii.member(jsii_name="comparatorInput")
    def comparator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparatorInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValuesInput")
    def tag_values_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues"]]], jsii.get(self, "tagValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="comparator")
    def comparator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparator"))

    @comparator.setter
    def comparator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b407154648b02ef960553b9bccf5ea4f77fe3c9b01638fdd20b35600eae756e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7454d8a934926917c8c21aa8f01d43f35c1d19c7aa52b0c4e1eb957aa174047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d4195cc5e09b46fb481b49c4a10b5ffc332b6a8f21157a71b279e8c9c14887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3187badc173a0943a01d5ccaa7b18ddd6630f898fb3e45e1720c94506ad449d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#value Macie2ClassificationJob#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__341b5c6b4a87587ac38d99f5acbf9224429dfd3ffc1a0c4009d09e9157a24133)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#value Macie2ClassificationJob#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValuesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValuesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c6c156d58834fcd13303abdcbd8e889a84a3728810707917352da305dc44218)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValuesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6ad6bbe5826f0811bfc67080ff231c6f9b6b500b770b41b9e73eff06e573b20)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValuesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65349b525e4e3c1d383adeb71d2814a9a53848385cbe4898b7821ddf05f579c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11a5feb6b095b0e16049ed469796fddda0a7d7b4485ed1556cb3f6ac3b487663)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac4af6f6f838f1cb6514daa9c0a3213bb0078132dc1dc9ce3dfe882fa990c221)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c10b9e44e895fe6bbe617a7d175af76cca9fb1627ad0f87324521cefc642f98b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a98e67a78c586c23992fd044613cce7ce03061455168770fcbea4e7ec5178ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2ae123321cd58568ca0ec6285008041a902d1a3dfb9cf471a408ab3e47178a33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af61b8a4442328f553180aac383798639e7d6db0d0ff7399951dd4578c4b6b28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89d97920f3e8105b35d341668734b9dd0ba99114a515c8c282cc9af214d8adb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionScopingExcludesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingExcludesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81b4dcb47d4702df619d0f548acdb02e5e5977a6c0bce036984522673dfdfd2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAnd")
    def put_and(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9f7558decb3ec607352f6d29464a94aa92e1e8c714e64a2944c5aeeada12a01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAnd", [value]))

    @jsii.member(jsii_name="resetAnd")
    def reset_and(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnd", []))

    @builtins.property
    @jsii.member(jsii_name="and")
    def and_(self) -> Macie2ClassificationJobS3JobDefinitionScopingExcludesAndList:
        return typing.cast(Macie2ClassificationJobS3JobDefinitionScopingExcludesAndList, jsii.get(self, "and"))

    @builtins.property
    @jsii.member(jsii_name="andInput")
    def and_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd]]], jsii.get(self, "andInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludes]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a3b51b0e857d6353902d5a19320b77ee162a85e1519402f388e542892a52907)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludes",
    jsii_struct_bases=[],
    name_mapping={"and_": "and"},
)
class Macie2ClassificationJobS3JobDefinitionScopingIncludes:
    def __init__(
        self,
        *,
        and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param and_: and block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e570e602da9bfa96244e6b7587fc2b7e377e5889b031a843a92dfa348aed2332)
            check_type(argname="argument and_", value=and_, expected_type=type_hints["and_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if and_ is not None:
            self._values["and_"] = and_

    @builtins.property
    def and_(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd"]]]:
        '''and block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        result = self._values.get("and_")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScopingIncludes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd",
    jsii_struct_bases=[],
    name_mapping={
        "simple_scope_term": "simpleScopeTerm",
        "tag_scope_term": "tagScopeTerm",
    },
)
class Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd:
    def __init__(
        self,
        *,
        simple_scope_term: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_scope_term: typing.Optional[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param simple_scope_term: simple_scope_term block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#simple_scope_term Macie2ClassificationJob#simple_scope_term}
        :param tag_scope_term: tag_scope_term block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tag_scope_term Macie2ClassificationJob#tag_scope_term}
        '''
        if isinstance(simple_scope_term, dict):
            simple_scope_term = Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm(**simple_scope_term)
        if isinstance(tag_scope_term, dict):
            tag_scope_term = Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm(**tag_scope_term)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aafc145857dad48702129c23480793c5549d2463d50cc5c713dc80eb4518721)
            check_type(argname="argument simple_scope_term", value=simple_scope_term, expected_type=type_hints["simple_scope_term"])
            check_type(argname="argument tag_scope_term", value=tag_scope_term, expected_type=type_hints["tag_scope_term"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if simple_scope_term is not None:
            self._values["simple_scope_term"] = simple_scope_term
        if tag_scope_term is not None:
            self._values["tag_scope_term"] = tag_scope_term

    @builtins.property
    def simple_scope_term(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm"]:
        '''simple_scope_term block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#simple_scope_term Macie2ClassificationJob#simple_scope_term}
        '''
        result = self._values.get("simple_scope_term")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm"], result)

    @builtins.property
    def tag_scope_term(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm"]:
        '''tag_scope_term block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tag_scope_term Macie2ClassificationJob#tag_scope_term}
        '''
        result = self._values.get("tag_scope_term")
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionScopingIncludesAndList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesAndList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57f796291b92b64911e2f0c213a1ca067bba1d52d0cc5247e514dddd47dd5f61)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50f780d03c689004a2817db17b6e25851525339eb43af7219cfef519d83d9886)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingIncludesAndOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67df3d0a990e743b71ca9dce0ec586f9db4b56894a9d62717ee2c5de4969b3c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f3803e0546802c68f8a9d8ef756c707e05cb267279d26fae6cf926c310efb58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6f58a2cd07469087fbed346d85db46387fb23c5450bc7642fffa7b65464f2ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88fe88009aea1d9c50acd3ff7f930913c33dc537c156577097954ff1d419bd01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionScopingIncludesAndOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesAndOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90c731f97e402910d32e824cb46b2ea83e2b4edc5711d0c731ba9941fc3b565e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSimpleScopeTerm")
    def put_simple_scope_term(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.
        '''
        value = Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm(
            comparator=comparator, key=key, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putSimpleScopeTerm", [value]))

    @jsii.member(jsii_name="putTagScopeTerm")
    def put_tag_scope_term(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param tag_values: tag_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#target Macie2ClassificationJob#target}.
        '''
        value = Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm(
            comparator=comparator, key=key, tag_values=tag_values, target=target
        )

        return typing.cast(None, jsii.invoke(self, "putTagScopeTerm", [value]))

    @jsii.member(jsii_name="resetSimpleScopeTerm")
    def reset_simple_scope_term(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSimpleScopeTerm", []))

    @jsii.member(jsii_name="resetTagScopeTerm")
    def reset_tag_scope_term(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagScopeTerm", []))

    @builtins.property
    @jsii.member(jsii_name="simpleScopeTerm")
    def simple_scope_term(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTermOutputReference":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTermOutputReference", jsii.get(self, "simpleScopeTerm"))

    @builtins.property
    @jsii.member(jsii_name="tagScopeTerm")
    def tag_scope_term(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermOutputReference":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermOutputReference", jsii.get(self, "tagScopeTerm"))

    @builtins.property
    @jsii.member(jsii_name="simpleScopeTermInput")
    def simple_scope_term_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm"], jsii.get(self, "simpleScopeTermInput"))

    @builtins.property
    @jsii.member(jsii_name="tagScopeTermInput")
    def tag_scope_term_input(
        self,
    ) -> typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm"]:
        return typing.cast(typing.Optional["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm"], jsii.get(self, "tagScopeTermInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__479acd3284e689e34f54033fc5895cecc887e674101ed254b98a278a45b07e57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm",
    jsii_struct_bases=[],
    name_mapping={"comparator": "comparator", "key": "key", "values": "values"},
)
class Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm:
    def __init__(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdfd4b334a9735aa5ef66631fc27969a04d8769bed66af1107d4ad6eb719db07)
            check_type(argname="argument comparator", value=comparator, expected_type=type_hints["comparator"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comparator is not None:
            self._values["comparator"] = comparator
        if key is not None:
            self._values["key"] = key
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def comparator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.'''
        result = self._values.get("comparator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#values Macie2ClassificationJob#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTermOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTermOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__419d3c327a7df54c511afc0fac10d31e30880d9888a92d7ecb861b2f1eb94c77)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetComparator")
    def reset_comparator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComparator", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="comparatorInput")
    def comparator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparatorInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="comparator")
    def comparator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparator"))

    @comparator.setter
    def comparator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdc6e3ffa5714c90e9aef24ee0b9d95486253ab7d7492d8130aa2471e49d4791)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97f0f3215509de64f149fc2ac23488e6e1d280ac6c71db0f1cfb13f2a49e9989)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc8ed7db72cf2952995a96aeb8368d82432dbcaa8df56ebd09be0f0cecb0dbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05c91c1c8c4e8f99592e61fe2da364c94713566b079da8ad087879643a689ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm",
    jsii_struct_bases=[],
    name_mapping={
        "comparator": "comparator",
        "key": "key",
        "tag_values": "tagValues",
        "target": "target",
    },
)
class Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm:
    def __init__(
        self,
        *,
        comparator: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param comparator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param tag_values: tag_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#target Macie2ClassificationJob#target}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e511e0b0fe9aa49f853afa0e8464e3107b838fc255ca1042bed9886876ac372c)
            check_type(argname="argument comparator", value=comparator, expected_type=type_hints["comparator"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument tag_values", value=tag_values, expected_type=type_hints["tag_values"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comparator is not None:
            self._values["comparator"] = comparator
        if key is not None:
            self._values["key"] = key
        if tag_values is not None:
            self._values["tag_values"] = tag_values
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def comparator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#comparator Macie2ClassificationJob#comparator}.'''
        result = self._values.get("comparator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_values(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues"]]]:
        '''tag_values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#tag_values Macie2ClassificationJob#tag_values}
        '''
        result = self._values.get("tag_values")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues"]]], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#target Macie2ClassificationJob#target}.'''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd55c79244422501e395c8b754a7d0523dc4037e8a395594e431a60646562acd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTagValues")
    def put_tag_values(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0012d15f998a9e1078f2f004d4474a1f5f362f62b902b9f7b735926890b389e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTagValues", [value]))

    @jsii.member(jsii_name="resetComparator")
    def reset_comparator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComparator", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetTagValues")
    def reset_tag_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValues", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @builtins.property
    @jsii.member(jsii_name="tagValues")
    def tag_values(
        self,
    ) -> "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValuesList":
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValuesList", jsii.get(self, "tagValues"))

    @builtins.property
    @jsii.member(jsii_name="comparatorInput")
    def comparator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparatorInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValuesInput")
    def tag_values_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues"]]], jsii.get(self, "tagValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="comparator")
    def comparator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparator"))

    @comparator.setter
    def comparator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fb85f874bf2e2c01ddaf1eb95630ceadc01353b9478e5f7eba470efadce8768)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e57e176b34b5755766d5b469457e38c5d476f7e6b6b0362634eafdd4b36dd1ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b74fec6fbd1e6431afea4ab7e1d4f25cd8a3b3c09e2bfb0c7316d7b7d5441d4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbc9448e249c5f6989d0a224dc6db876009d7698dd213b1a65c3a0d71dad613c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#value Macie2ClassificationJob#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dcbc6d85fe2ccc6d0027b81c8ec06d5c81da64a50705ad09b8c414240bf3d5a)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#key Macie2ClassificationJob#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#value Macie2ClassificationJob#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValuesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValuesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7717275e8a333e495b2c1267080cb7a9774ed35bf3ec460f9f3a8f5204303cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValuesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6db56ebe2d2ccc20eb26d76223b3c707e58d94fba058c77470c71f3dc8b81ec2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValuesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e3ed5595655ca51394826f6a6fd9e062935be840230427099169ba7ed0093a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dc3a055741ec9f990ab6f2d682c63e03a56917be61dc56e85cb936420de8d73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aaddede93f096f6d32bb96741c9a8c4210f2d20bf8d9c4a1b3be6987f0473ac0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0d02c9112fe6f91d529b437f3527a478512eb17f036c9d88e49a82fe9604107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15e1f24e30e210b95e9037da090412e2f808ac7325b1c108ed4fec8330c47922)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3520fcbbef175d1c8ae09099a8aa2c2fabdefaef807dab2ee52a403ecc1095fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe45d341167064b499bc56732b205b59120b7ad58a27cd099cb84dc5ec9fe2b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f56d1290096d6835a645fa7ef2b41431b6867892f5174d01ceef3536a3012394)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionScopingIncludesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingIncludesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__672f3263e3a5cbb903a9e163636e0c5daa9c6ff1df7a15b3fc10a23cff497a3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAnd")
    def put_and(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebf9b346a4f8e26e4aeefbaa30344fe624f2db59986ad3ed223ebdb3aa3bc2d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAnd", [value]))

    @jsii.member(jsii_name="resetAnd")
    def reset_and(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnd", []))

    @builtins.property
    @jsii.member(jsii_name="and")
    def and_(self) -> Macie2ClassificationJobS3JobDefinitionScopingIncludesAndList:
        return typing.cast(Macie2ClassificationJobS3JobDefinitionScopingIncludesAndList, jsii.get(self, "and"))

    @builtins.property
    @jsii.member(jsii_name="andInput")
    def and_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd]]], jsii.get(self, "andInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludes]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35ff79c3b6435155ce07785dbe3a1977fc06718267e61b6887277e79bdb520b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobS3JobDefinitionScopingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobS3JobDefinitionScopingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2246622b485798148df8249ba80f782c1b5b3bcf3f31728843f61e099ccb660d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExcludes")
    def put_excludes(
        self,
        *,
        and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param and_: and block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        value = Macie2ClassificationJobS3JobDefinitionScopingExcludes(and_=and_)

        return typing.cast(None, jsii.invoke(self, "putExcludes", [value]))

    @jsii.member(jsii_name="putIncludes")
    def put_includes(
        self,
        *,
        and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param and_: and block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#and Macie2ClassificationJob#and}
        '''
        value = Macie2ClassificationJobS3JobDefinitionScopingIncludes(and_=and_)

        return typing.cast(None, jsii.invoke(self, "putIncludes", [value]))

    @jsii.member(jsii_name="resetExcludes")
    def reset_excludes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludes", []))

    @jsii.member(jsii_name="resetIncludes")
    def reset_includes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludes", []))

    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(
        self,
    ) -> Macie2ClassificationJobS3JobDefinitionScopingExcludesOutputReference:
        return typing.cast(Macie2ClassificationJobS3JobDefinitionScopingExcludesOutputReference, jsii.get(self, "excludes"))

    @builtins.property
    @jsii.member(jsii_name="includes")
    def includes(
        self,
    ) -> Macie2ClassificationJobS3JobDefinitionScopingIncludesOutputReference:
        return typing.cast(Macie2ClassificationJobS3JobDefinitionScopingIncludesOutputReference, jsii.get(self, "includes"))

    @builtins.property
    @jsii.member(jsii_name="excludesInput")
    def excludes_input(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludes]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludes], jsii.get(self, "excludesInput"))

    @builtins.property
    @jsii.member(jsii_name="includesInput")
    def includes_input(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludes]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludes], jsii.get(self, "includesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobS3JobDefinitionScoping]:
        return typing.cast(typing.Optional[Macie2ClassificationJobS3JobDefinitionScoping], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScoping],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a7941fdc1a81bb158959e4271df889a10e2c2fb44658d555c674d92dfd63808)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobScheduleFrequency",
    jsii_struct_bases=[],
    name_mapping={
        "daily_schedule": "dailySchedule",
        "monthly_schedule": "monthlySchedule",
        "weekly_schedule": "weeklySchedule",
    },
)
class Macie2ClassificationJobScheduleFrequency:
    def __init__(
        self,
        *,
        daily_schedule: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monthly_schedule: typing.Optional[jsii.Number] = None,
        weekly_schedule: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param daily_schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#daily_schedule Macie2ClassificationJob#daily_schedule}.
        :param monthly_schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#monthly_schedule Macie2ClassificationJob#monthly_schedule}.
        :param weekly_schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#weekly_schedule Macie2ClassificationJob#weekly_schedule}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c7000a6ef7658ee246f9c28cfcac4395951ff404bcb9a1fa06b2b0e6e62b7be)
            check_type(argname="argument daily_schedule", value=daily_schedule, expected_type=type_hints["daily_schedule"])
            check_type(argname="argument monthly_schedule", value=monthly_schedule, expected_type=type_hints["monthly_schedule"])
            check_type(argname="argument weekly_schedule", value=weekly_schedule, expected_type=type_hints["weekly_schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if daily_schedule is not None:
            self._values["daily_schedule"] = daily_schedule
        if monthly_schedule is not None:
            self._values["monthly_schedule"] = monthly_schedule
        if weekly_schedule is not None:
            self._values["weekly_schedule"] = weekly_schedule

    @builtins.property
    def daily_schedule(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#daily_schedule Macie2ClassificationJob#daily_schedule}.'''
        result = self._values.get("daily_schedule")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def monthly_schedule(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#monthly_schedule Macie2ClassificationJob#monthly_schedule}.'''
        result = self._values.get("monthly_schedule")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def weekly_schedule(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#weekly_schedule Macie2ClassificationJob#weekly_schedule}.'''
        result = self._values.get("weekly_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobScheduleFrequency(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobScheduleFrequencyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobScheduleFrequencyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd09d8f826c064f44a07c120814a8a042e54547a929afacce23e8629908adaeb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDailySchedule")
    def reset_daily_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDailySchedule", []))

    @jsii.member(jsii_name="resetMonthlySchedule")
    def reset_monthly_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthlySchedule", []))

    @jsii.member(jsii_name="resetWeeklySchedule")
    def reset_weekly_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeklySchedule", []))

    @builtins.property
    @jsii.member(jsii_name="dailyScheduleInput")
    def daily_schedule_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dailyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="monthlyScheduleInput")
    def monthly_schedule_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthlyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyScheduleInput")
    def weekly_schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "weeklyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="dailySchedule")
    def daily_schedule(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dailySchedule"))

    @daily_schedule.setter
    def daily_schedule(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dffbcd6b8c212458b79f448243ac044679e4ef75fd9032aab5fd7fc6adf42525)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dailySchedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monthlySchedule")
    def monthly_schedule(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "monthlySchedule"))

    @monthly_schedule.setter
    def monthly_schedule(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9e3d77a2eacd57796953aeed006f2a1c1037042eb6dc6518045f6c8d84934d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monthlySchedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weeklySchedule")
    def weekly_schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "weeklySchedule"))

    @weekly_schedule.setter
    def weekly_schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02028eb798545f6da970872515bb77321901d840be2a3e4869caf2bf84a91ee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weeklySchedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobScheduleFrequency]:
        return typing.cast(typing.Optional[Macie2ClassificationJobScheduleFrequency], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobScheduleFrequency],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bde9c37c1d02484be84ca250f8a83bb7b70be7ecf5eea5fb6125f957efb2ddc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "update": "update"},
)
class Macie2ClassificationJobTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#create Macie2ClassificationJob#create}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#update Macie2ClassificationJob#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15eba9f9a3c0b1e21cab611ec24b38951e6a9ea048adb8719134f40f96b7dad3)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#create Macie2ClassificationJob#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/macie2_classification_job#update Macie2ClassificationJob#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc1c40a13eba05ea2de886c5cc72013a3d8bd67fb9c035fe3ca508e3592f803d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__49aea812b3bac028d24548e206af73ad84c5cee314ab30fade5bbd921fe7f262)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49e0c6deb702c01361abb3437c3b6080b10635d332a6b70aeb7a12aee1571c6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4446b0c30d284941011114d9116674189201679c78fb441aff8db58ae321d083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobUserPausedDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class Macie2ClassificationJobUserPausedDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Macie2ClassificationJobUserPausedDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Macie2ClassificationJobUserPausedDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobUserPausedDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfc45528ad24b6863aa0c0a9d2aa6faf2cbe95affb8a7533732970ebf2af685c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Macie2ClassificationJobUserPausedDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df19ed37f43bb25f39495f8582ecadbb9f1953ea10b99071e86f85edc55b94c8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Macie2ClassificationJobUserPausedDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b623519a1a6c12e26210e2163cfad597a38440dabbed0fc6b73982c9819c382e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85b858fcce77b782f9134850c8c60fb49ab05cbc77133b4a8aed84a4d6cb7066)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3885555be49299d8eea7af21a733248ea80d5418e10ea68dfb6dbbafe5ec0946)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class Macie2ClassificationJobUserPausedDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.macie2ClassificationJob.Macie2ClassificationJobUserPausedDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c39c40ea99599593d5c372dd3353d881f7c7ad8c38d481390cca9cd03b8c74c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="jobExpiresAt")
    def job_expires_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobExpiresAt"))

    @builtins.property
    @jsii.member(jsii_name="jobImminentExpirationHealthEventArn")
    def job_imminent_expiration_health_event_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobImminentExpirationHealthEventArn"))

    @builtins.property
    @jsii.member(jsii_name="jobPausedAt")
    def job_paused_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobPausedAt"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Macie2ClassificationJobUserPausedDetails]:
        return typing.cast(typing.Optional[Macie2ClassificationJobUserPausedDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Macie2ClassificationJobUserPausedDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79cf163330655818d0a85f5c5557654375ad97855094fd0973989ebf25fb01c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Macie2ClassificationJob",
    "Macie2ClassificationJobConfig",
    "Macie2ClassificationJobS3JobDefinition",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteria",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndList",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterionOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValuesList",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValuesOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndList",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterionOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValuesList",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValuesOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketCriteriaOutputReference",
    "Macie2ClassificationJobS3JobDefinitionBucketDefinitions",
    "Macie2ClassificationJobS3JobDefinitionBucketDefinitionsList",
    "Macie2ClassificationJobS3JobDefinitionBucketDefinitionsOutputReference",
    "Macie2ClassificationJobS3JobDefinitionOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScoping",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludes",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndList",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTermOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValuesList",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValuesOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScopingExcludesOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludes",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndList",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTermOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValuesList",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValuesOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScopingIncludesOutputReference",
    "Macie2ClassificationJobS3JobDefinitionScopingOutputReference",
    "Macie2ClassificationJobScheduleFrequency",
    "Macie2ClassificationJobScheduleFrequencyOutputReference",
    "Macie2ClassificationJobTimeouts",
    "Macie2ClassificationJobTimeoutsOutputReference",
    "Macie2ClassificationJobUserPausedDetails",
    "Macie2ClassificationJobUserPausedDetailsList",
    "Macie2ClassificationJobUserPausedDetailsOutputReference",
]

publication.publish()

def _typecheckingstub__b27f646cb589918b6833577cd0c1cffa029ba870c44bb9892b8a8f930553f3c3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    job_type: builtins.str,
    s3_job_definition: typing.Union[Macie2ClassificationJobS3JobDefinition, typing.Dict[builtins.str, typing.Any]],
    custom_data_identifier_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    initial_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    job_status: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    sampling_percentage: typing.Optional[jsii.Number] = None,
    schedule_frequency: typing.Optional[typing.Union[Macie2ClassificationJobScheduleFrequency, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[Macie2ClassificationJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ee968fc8518efb0bfb702808348328c88b175644c6b55b644f4df9ee04b05f5f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d3fa0d5f073d8e270dcc359bff406524e968d8ef8367364bee18a08bf5bc9a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__946a2681566b2ba68ab0e3727c0ae8a824fcb855080dfd7c57542184c0c8a71b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12bc6d950649773961ad0f657735083157c13907cb0a60c6e1b57bcd2e9d9d9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c96bbb9909ab64aca2483c08cc670636af1c84dd1fcc5230929f9a74ec30fb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b0abbbd5b09b6aa0a6ea3877d8134d0236e8037669faa836175612871837a39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd28aeaf3713887db444206fb52d1db628ffa28406fed85800848c750e73c73a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e22622ef4a1839b088bfcef31c0e8f29355c5a36ea807df2cdcc55c8c975e56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b34928322c3fe215fb861f7ce0c2ff6b6f7a0029d7ebaca4094b176bcced0f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1eaf5e00cf44ac41b4381a4daa6c327a348a7bff9ecb14e6d3175e6b7049c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5e1385fb628fd33039b4ccf5381ef3e07c685f8e62f16dacd1d0743ba90cec1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bcf59dd846b84e07781154169bd835fcffb22aa3ba570059c7f62efcb29aa0a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd30dbb71172e184f4db88e7d6dff089bf5b6d0db7688a3423b5c39d419196b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7134d153c1af478cc168b2a9e6b9247e70ff92ed4fb8df1ab1c7b3a5d9b77580(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    job_type: builtins.str,
    s3_job_definition: typing.Union[Macie2ClassificationJobS3JobDefinition, typing.Dict[builtins.str, typing.Any]],
    custom_data_identifier_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    initial_run: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    job_status: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    sampling_percentage: typing.Optional[jsii.Number] = None,
    schedule_frequency: typing.Optional[typing.Union[Macie2ClassificationJobScheduleFrequency, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[Macie2ClassificationJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fddc2ab6187bd44df4e3fe36277b708a25e6ef608d6f5f71dda94af67159d5f8(
    *,
    bucket_criteria: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteria, typing.Dict[builtins.str, typing.Any]]] = None,
    bucket_definitions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketDefinitions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scoping: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionScoping, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4486295bac77b06d2bf31169c8fa1976f6a28b327287fb1174e0adb9be1ba138(
    *,
    excludes: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes, typing.Dict[builtins.str, typing.Any]]] = None,
    includes: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21332f9c258d95f2293c79b5597ebdf255840c2b050cfb5c86afd7e3ebf85ff9(
    *,
    and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8732ca1e9d2d77f09f760b86fedb652428e9d22a57601e615618e68caea6bc9a(
    *,
    simple_criterion: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_criterion: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72abf350195283ccbac23fb4bf99d93bc07c135687acac03005419c374a0c3ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5072880ec83ad3e3d07d9c4bb41b18f27602e397e27c7bed26ae57d3cf76647(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ad23fc40e14bfe99353de98b0ba8f1fa800e09345478eaf5ec7184de091ca0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2e7dc66bd87eb3dbc57147b6928000eca6c115be76fa055705b0ed44d336d5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029eedb082600072be4f926b998f05df70af1cbafe16fda4acfd639d16232aa7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61aabc18c85211cc0ab3276cc21f719c267fc6c04e8fca9e449940e2289b1f4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2d85aa656d7d2ef1c2d04c690188913bfbaff71613aa6f257e98604173e7eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2d20f058b107eb8e170b64274bcdbee1dccf071bc0fe2bd515beacef3d0bc7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34034d8cc44ccb3fd875957df4e298f9b5cc2fd8ebc19f48261052a338f1a64e(
    *,
    comparator: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ac5076706a3aa529f1ee346de0cde586c1942aeb2e7b1c01a026259af887bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e189a3b5b91e89de5db9163bb40c148fded84dbe9d2979587720bd36cdb6684(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d3cfa4220d1b2720484b64e9c48f14e44cb64a831ded24e620b26a6c63eee0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf5f4e41a8e9a8b999735f60c93ac9bb987df8184715522b7151a5559a0d8d14(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e13626784cbd3018d74d8176bdc75a64578a322e7443b9643f63c1da4cf37271(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndSimpleCriterion],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d065a383fbad797a9516b0d9a6ce27b9f3dfa145321fd5dc354c66b2869dbc(
    *,
    comparator: typing.Optional[builtins.str] = None,
    tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3328325bd672cd376b7879f40442525778d1a684d4a849c0f6299244960ca0d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8914ff064df8631c13e121fb3f48ececfa8c7484ca154e9aff057f6b5b54837(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b6dcd7b544e14293aa0885e52ef4ad3fa0750dff9f149c59a4bc88559debcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a05d31f4a63f62acbdd56bac6491225bbd52bdce9c73f5ebaa6bf4041c212303(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterion],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d452374651ba5886aa559560d4a5cfc69acd4eec355fa0604cf944a0487e2e07(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5885c06b610cb52e8509868b2c7005d5094b43215978570a286c509abf51881f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1374265b08364c705996f5b603bd1a61e1518a39f082317690bc85f5532f8dda(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eead6ac4717b489d80009ab63cc1670a9f0ab7e7ccc099ed71a935be6078415(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d438fcf138c2bfa81344a9d3686729bda882dbf628581beca31ef8e41b470238(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9794e203274bc451e18e90370925d8f907a06e22676759bc3b493b26dbb39fd9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821445a23b608965605deaab5c3ef85a4d2523879fba20abe6d6d6bead77dcb4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c2fd39eb8c3311233d61faa74df3295ed9a1083844e88c63f8335cc53aa69f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b838fcdf6f2d0795368fea4267ba0a2b4486418049eeb53ee9a5a770d4301e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31cabe064aefc7ac864acc8f239a117cb7384296ccc6f7316392670a49c9d129(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4159680af750fe2b1c66121abbcc6b55746bc6ccc86bb2497737ee89b08feb8d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAndTagCriterionTagValues]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9005a7f294a4d59089d69114d06e5ca1336ef953cc2415cd90aa70f27b8563(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b2b623b07cb0d716f7976c74eb3c1c8cf984d89bb94ed32ff46c5c766a882c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludesAnd, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc6f5f11294da5733b7df5e7db479ef281dbfa52318921f852ad15186089746(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaExcludes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e42c09cd3fb8662ee299b944c5fa5552574adb7f3a2c74a8d922d476aa01e005(
    *,
    and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c880900b8891ef4a29f8e8dee12e1f27fb615d97b31052e70beb1d1ebabc8e16(
    *,
    simple_criterion: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_criterion: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ffcb3856dfcf7b25d517db7d4186249414549d12a353ae2d1f826c2de52d19(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2b0ce6d60e26830b3f90e7df0baf7b55e2873f8ebf1774cf640f2bc8fb3c80(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a0195a59b5b397d9c75cafaa87ed647a9968f06c9501ffb94383b8fd0bfa026(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be70c22dd592e112a423378a35c8a6c7f17173656f82a259c1ac8a5bc1e7b5e7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__769554752155139a7895248053d0556dafbbbe85d82f9a74bffddcf4630d3d8d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a5474b66362cf25f0380f2c382ded76ffdec3fd289248622b0adbde818bf8bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882c777b91be818a835e26b18fa25875adc2fa1a63f47cc327df3154e2ab46c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd417a172971dadc2913c0c78328674fb4df98a97e832755a155803d3fd50ab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4cee1d343af150f8a94cb3f29dae693916dea0f6a3e76c61d56561ab668ec26(
    *,
    comparator: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dcd9b9e3e17df15c6993ee993e899af24da5c2538d927726cc3479c0797060f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75414f43368f80e65a2ec4e9115fddb18780f1d4aabc0b0097ddee3040ed424(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b45e5e181baa036fd40b155133e6d3f1a4481360ea75d37083cc02395f6bfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab66e4899aed98edab7912127357c60480c5f08846bcde3e65a5facaba39d32(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862419614876fede75cf4a45da89ddc8428a5821369706c317074658a38d35bb(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndSimpleCriterion],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348a366c7ebfc3ff333310fc1ac2b9ef23fe19027aa306f492b6e5b265ae9847(
    *,
    comparator: typing.Optional[builtins.str] = None,
    tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eee36ea70d41a3ab47e9c9c695ef8896696e75b81801f037bb8c4aaf1b53dd7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f81d78766299651d8a679fefb8fd875af0374ec031a1d551035657f941bc876(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbfa3550da35846dd0455207e48fdee2e47e35fa43eaf3d3b7816dc367ef4701(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__256415c1b91af62f23f3e9b9dcf6d3d1b5bb448e90860ae7deca7b826709fdd4(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterion],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c9fd0c60d7d2f2e2352187c22861346538b7d1946757891b5f977211e55c959(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a30c6148170568dbf5ce38855fbaba35b20a2559797114d59adbdbf3b147b7db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0af012fead3f28cca100b14addd7087bb7dac2d1034df4e07167877ba0c8678a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a56ffe148c33c7a6811f538889f3e16bcf706500d711d175fc25d91aa9855a8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795d872cfc729c96867dfeeadce7db3069014fc8c94e4798a69845e7d70f542d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428d6ee28e88d3f4a2a6f0306bb67aa695e810a965eb941979b8eafc08984ed2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff62e08f6c4ee8373e2505dc11ae47a212f67fae92e484ff1edba914c8f504c6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__954ff9d361ae1746c949c8f33598abd361d47a6548cf4bfeff5b6ffe5576c6c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d256fe8ece847260d929c310db677e625a7b7ff0212cd62173806e6cfc67fec7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ea78167932fd89cb29ea1ecea2d79ea24929c17a610ecf62d86b256250e1a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca86171edd2ff405c2cd82aded6d14861c823c67d0d61cacd40be4c4db63cc2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAndTagCriterionTagValues]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11f87961d623856d068ab64eb65d1b537031df629b53a29c8ef3d985d0b39b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de0e5f81cf65bffbf078183e23f40c4e4e2cbcc5189cb3e22f53cb4cc7c29b6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludesAnd, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a00a0fd356899e15feb398fc0ef8a1057b090de4638cb32b494cdd0471d82d2(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteriaIncludes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec8ca8247fa5679e146542cbcc57cae115440609b024d77aa326e92be998e577(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02ec066ec6b6553865bc8b3533676419c34b7f6e8bd5c729aba68c3a853a24f(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionBucketCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__409b30772acdc69220c9f3cca065295ece32dce52346813f88780db53eb20a0f(
    *,
    account_id: builtins.str,
    buckets: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09194a64252d9a0f72532ba21fd000847024950be18aa824466669816e6fd1ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da0d49a03bcbd70c9e09b41754f3beea83a5ca0ed63787f001d7cc3c24034122(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579317fc44c6cfa343863b0f0eac269c72392c878532ca1443eae2d5b5476b99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb21d6fc896a8135dd299a14eac779e30878db8fa16966809839a666190a712b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ce8cdccb84e690c2490d51586feeb6bace5a5bcba43216539b3418efcf5c22(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ae790b3191ccecf0387ad7c43ebe8f21601c8931cd418c87c2c397bac60ab3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionBucketDefinitions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c70da27c62dea45aa4cbd5434618cb5112879be3664a9d1c42120a7d9e9348bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae36595933435e168428d7d36fde393d702c67e9a94e4f082d533ad0dc269430(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba508f29bd858625aa7d01e3b383d6c740793c0535e1b11df309d72cbd31eb4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a59c22900ed845da673bb063c0011704343906fd26fc8ae501644f47195b189(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionBucketDefinitions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa48591774648c837499a846c90dc954c5c09424a8ee9acc4c753c95fb8df96b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebcd0db9458285e9b01df165ad3a31103c4389fcdd4b34ee2726b56ee88ac9f9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionBucketDefinitions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028783e26cce2cc1b3c120d7fba4a48c1d33654f319fa673a47ab78539090e5b(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdd4e97e8f54cdbacb025b4a71616a663a684da718b3b3847fe3f0eda5b7e8b6(
    *,
    excludes: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingExcludes, typing.Dict[builtins.str, typing.Any]]] = None,
    includes: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingIncludes, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e57fd95443a6295598f0e07b80c4106bd31692e7d3c67ba924bc3e3c273028(
    *,
    and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a70fd8f7eb021cbfed4b36b9515bd0234ab69e7dfcf453807c494ec4fb1bd47(
    *,
    simple_scope_term: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_scope_term: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1fd60e7c1b1fa948065e5ea3c547b46f0670e38ef51088d023c4f373018f4b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c60e0b3fa6128e50f75647463263d0eabb195edfc793a41f9326009b32be2c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4a99aec9dec3b6d0c69f2cb84ccdf9c8e364be1fe842b371c62a57c4ce4923e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d4f13e0066da291bb6b67efb39fb85dcc56e4db281207058430b76a6264a8f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89a45026aa35435b1068c6bc179a708ee8ba472cfffff498e627a6c681af5cd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d43dc3e2bce2f77a815eeaace7654d10e90b8184e2a782fec7f84b54b0422e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__338d6d5ac8efe596a90be318e71541a642b23d7e9dd96bdc31b4205cc34e972c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f231c11dca68d7cce3956e01623300211abac99bf7bc624ff78922a88548c19(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9abc41e0bff51507e28a5ef637a514574424d0f50b2f61df8a4741697ffb1a29(
    *,
    comparator: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb9debac8573dfee8c836cb8a138890ab4c83198affe21bf42e81ea65f661e1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441c9131141f1604431bc8d92f4438813f7fc17037ce07a27d85f30c8c97a8a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__766b8f65631e70c4be68ec81dad41a2060b53a09f625b0d62be1b7e71086e5fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f58a8ec3e4c6da66d5ad7b790e6bfdc91a955f98101febfd6ad0371af44e53d3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a0f1c9b911dbdf9daef53ab8c629c4fd1b3e3d7bc2a94e811ebcf453cea9245(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndSimpleScopeTerm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7824722e8b6931eb380b850f3574534afaed1c8154d54776a779ff70a16a8ca7(
    *,
    comparator: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ef6ab5f3d2b5b6b1122fe92c9d680db40a32de77381f2c9b6bab275b020ee22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__049d3887bf29643c870b91dcb5d70ee0168ccbc06a0fce9970c5287726876b42(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b407154648b02ef960553b9bccf5ea4f77fe3c9b01638fdd20b35600eae756e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7454d8a934926917c8c21aa8f01d43f35c1d19c7aa52b0c4e1eb957aa174047(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d4195cc5e09b46fb481b49c4a10b5ffc332b6a8f21157a71b279e8c9c14887(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3187badc173a0943a01d5ccaa7b18ddd6630f898fb3e45e1720c94506ad449d(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTerm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__341b5c6b4a87587ac38d99f5acbf9224429dfd3ffc1a0c4009d09e9157a24133(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c6c156d58834fcd13303abdcbd8e889a84a3728810707917352da305dc44218(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ad6bbe5826f0811bfc67080ff231c6f9b6b500b770b41b9e73eff06e573b20(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65349b525e4e3c1d383adeb71d2814a9a53848385cbe4898b7821ddf05f579c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a5feb6b095b0e16049ed469796fddda0a7d7b4485ed1556cb3f6ac3b487663(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac4af6f6f838f1cb6514daa9c0a3213bb0078132dc1dc9ce3dfe882fa990c221(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c10b9e44e895fe6bbe617a7d175af76cca9fb1627ad0f87324521cefc642f98b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a98e67a78c586c23992fd044613cce7ce03061455168770fcbea4e7ec5178ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae123321cd58568ca0ec6285008041a902d1a3dfb9cf471a408ab3e47178a33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af61b8a4442328f553180aac383798639e7d6db0d0ff7399951dd4578c4b6b28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89d97920f3e8105b35d341668734b9dd0ba99114a515c8c282cc9af214d8adb4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingExcludesAndTagScopeTermTagValues]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b4dcb47d4702df619d0f548acdb02e5e5977a6c0bce036984522673dfdfd2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f7558decb3ec607352f6d29464a94aa92e1e8c714e64a2944c5aeeada12a01(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingExcludesAnd, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3b51b0e857d6353902d5a19320b77ee162a85e1519402f388e542892a52907(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingExcludes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e570e602da9bfa96244e6b7587fc2b7e377e5889b031a843a92dfa348aed2332(
    *,
    and_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aafc145857dad48702129c23480793c5549d2463d50cc5c713dc80eb4518721(
    *,
    simple_scope_term: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_scope_term: typing.Optional[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f796291b92b64911e2f0c213a1ca067bba1d52d0cc5247e514dddd47dd5f61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50f780d03c689004a2817db17b6e25851525339eb43af7219cfef519d83d9886(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67df3d0a990e743b71ca9dce0ec586f9db4b56894a9d62717ee2c5de4969b3c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3803e0546802c68f8a9d8ef756c707e05cb267279d26fae6cf926c310efb58(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f58a2cd07469087fbed346d85db46387fb23c5450bc7642fffa7b65464f2ea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88fe88009aea1d9c50acd3ff7f930913c33dc537c156577097954ff1d419bd01(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c731f97e402910d32e824cb46b2ea83e2b4edc5711d0c731ba9941fc3b565e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__479acd3284e689e34f54033fc5895cecc887e674101ed254b98a278a45b07e57(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdfd4b334a9735aa5ef66631fc27969a04d8769bed66af1107d4ad6eb719db07(
    *,
    comparator: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__419d3c327a7df54c511afc0fac10d31e30880d9888a92d7ecb861b2f1eb94c77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc6e3ffa5714c90e9aef24ee0b9d95486253ab7d7492d8130aa2471e49d4791(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f0f3215509de64f149fc2ac23488e6e1d280ac6c71db0f1cfb13f2a49e9989(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc8ed7db72cf2952995a96aeb8368d82432dbcaa8df56ebd09be0f0cecb0dbc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05c91c1c8c4e8f99592e61fe2da364c94713566b079da8ad087879643a689ef(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndSimpleScopeTerm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e511e0b0fe9aa49f853afa0e8464e3107b838fc255ca1042bed9886876ac372c(
    *,
    comparator: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    tag_values: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd55c79244422501e395c8b754a7d0523dc4037e8a395594e431a60646562acd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0012d15f998a9e1078f2f004d4474a1f5f362f62b902b9f7b735926890b389e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb85f874bf2e2c01ddaf1eb95630ceadc01353b9478e5f7eba470efadce8768(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e57e176b34b5755766d5b469457e38c5d476f7e6b6b0362634eafdd4b36dd1ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74fec6fbd1e6431afea4ab7e1d4f25cd8a3b3c09e2bfb0c7316d7b7d5441d4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc9448e249c5f6989d0a224dc6db876009d7698dd213b1a65c3a0d71dad613c(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTerm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dcbc6d85fe2ccc6d0027b81c8ec06d5c81da64a50705ad09b8c414240bf3d5a(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7717275e8a333e495b2c1267080cb7a9774ed35bf3ec460f9f3a8f5204303cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db56ebe2d2ccc20eb26d76223b3c707e58d94fba058c77470c71f3dc8b81ec2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3ed5595655ca51394826f6a6fd9e062935be840230427099169ba7ed0093a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc3a055741ec9f990ab6f2d682c63e03a56917be61dc56e85cb936420de8d73(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaddede93f096f6d32bb96741c9a8c4210f2d20bf8d9c4a1b3be6987f0473ac0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0d02c9112fe6f91d529b437f3527a478512eb17f036c9d88e49a82fe9604107(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e1f24e30e210b95e9037da090412e2f808ac7325b1c108ed4fec8330c47922(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3520fcbbef175d1c8ae09099a8aa2c2fabdefaef807dab2ee52a403ecc1095fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe45d341167064b499bc56732b205b59120b7ad58a27cd099cb84dc5ec9fe2b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f56d1290096d6835a645fa7ef2b41431b6867892f5174d01ceef3536a3012394(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobS3JobDefinitionScopingIncludesAndTagScopeTermTagValues]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__672f3263e3a5cbb903a9e163636e0c5daa9c6ff1df7a15b3fc10a23cff497a3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebf9b346a4f8e26e4aeefbaa30344fe624f2db59986ad3ed223ebdb3aa3bc2d7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Macie2ClassificationJobS3JobDefinitionScopingIncludesAnd, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ff79c3b6435155ce07785dbe3a1977fc06718267e61b6887277e79bdb520b2(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScopingIncludes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2246622b485798148df8249ba80f782c1b5b3bcf3f31728843f61e099ccb660d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a7941fdc1a81bb158959e4271df889a10e2c2fb44658d555c674d92dfd63808(
    value: typing.Optional[Macie2ClassificationJobS3JobDefinitionScoping],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c7000a6ef7658ee246f9c28cfcac4395951ff404bcb9a1fa06b2b0e6e62b7be(
    *,
    daily_schedule: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    monthly_schedule: typing.Optional[jsii.Number] = None,
    weekly_schedule: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd09d8f826c064f44a07c120814a8a042e54547a929afacce23e8629908adaeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dffbcd6b8c212458b79f448243ac044679e4ef75fd9032aab5fd7fc6adf42525(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9e3d77a2eacd57796953aeed006f2a1c1037042eb6dc6518045f6c8d84934d6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02028eb798545f6da970872515bb77321901d840be2a3e4869caf2bf84a91ee0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bde9c37c1d02484be84ca250f8a83bb7b70be7ecf5eea5fb6125f957efb2ddc(
    value: typing.Optional[Macie2ClassificationJobScheduleFrequency],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15eba9f9a3c0b1e21cab611ec24b38951e6a9ea048adb8719134f40f96b7dad3(
    *,
    create: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1c40a13eba05ea2de886c5cc72013a3d8bd67fb9c035fe3ca508e3592f803d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49aea812b3bac028d24548e206af73ad84c5cee314ab30fade5bbd921fe7f262(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e0c6deb702c01361abb3437c3b6080b10635d332a6b70aeb7a12aee1571c6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4446b0c30d284941011114d9116674189201679c78fb441aff8db58ae321d083(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Macie2ClassificationJobTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc45528ad24b6863aa0c0a9d2aa6faf2cbe95affb8a7533732970ebf2af685c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df19ed37f43bb25f39495f8582ecadbb9f1953ea10b99071e86f85edc55b94c8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b623519a1a6c12e26210e2163cfad597a38440dabbed0fc6b73982c9819c382e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b858fcce77b782f9134850c8c60fb49ab05cbc77133b4a8aed84a4d6cb7066(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3885555be49299d8eea7af21a733248ea80d5418e10ea68dfb6dbbafe5ec0946(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c39c40ea99599593d5c372dd3353d881f7c7ad8c38d481390cca9cd03b8c74c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79cf163330655818d0a85f5c5557654375ad97855094fd0973989ebf25fb01c8(
    value: typing.Optional[Macie2ClassificationJobUserPausedDetails],
) -> None:
    """Type checking stubs"""
    pass
