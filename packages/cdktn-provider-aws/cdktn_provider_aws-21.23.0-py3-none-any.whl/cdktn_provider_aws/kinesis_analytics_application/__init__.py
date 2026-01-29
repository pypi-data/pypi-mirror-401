r'''
# `aws_kinesis_analytics_application`

Refer to the Terraform Registry for docs: [`aws_kinesis_analytics_application`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application).
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


class KinesisAnalyticsApplication(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplication",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application aws_kinesis_analytics_application}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        cloudwatch_logging_options: typing.Optional[typing.Union["KinesisAnalyticsApplicationCloudwatchLoggingOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        code: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        inputs: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputs", typing.Dict[builtins.str, typing.Any]]] = None,
        outputs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationOutputs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        reference_data_sources: typing.Optional[typing.Union["KinesisAnalyticsApplicationReferenceDataSources", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        start_application: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application aws_kinesis_analytics_application} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#name KinesisAnalyticsApplication#name}.
        :param cloudwatch_logging_options: cloudwatch_logging_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#cloudwatch_logging_options KinesisAnalyticsApplication#cloudwatch_logging_options}
        :param code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#code KinesisAnalyticsApplication#code}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#description KinesisAnalyticsApplication#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#id KinesisAnalyticsApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inputs: inputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#inputs KinesisAnalyticsApplication#inputs}
        :param outputs: outputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#outputs KinesisAnalyticsApplication#outputs}
        :param reference_data_sources: reference_data_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#reference_data_sources KinesisAnalyticsApplication#reference_data_sources}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#region KinesisAnalyticsApplication#region}
        :param start_application: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#start_application KinesisAnalyticsApplication#start_application}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#tags KinesisAnalyticsApplication#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#tags_all KinesisAnalyticsApplication#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbdb1b7e2478c60d662f69643f3a17c3257094d8bffa0da9bda03347edf70ace)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KinesisAnalyticsApplicationConfig(
            name=name,
            cloudwatch_logging_options=cloudwatch_logging_options,
            code=code,
            description=description,
            id=id,
            inputs=inputs,
            outputs=outputs,
            reference_data_sources=reference_data_sources,
            region=region,
            start_application=start_application,
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
        '''Generates CDKTF code for importing a KinesisAnalyticsApplication resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the KinesisAnalyticsApplication to import.
        :param import_from_id: The id of the existing KinesisAnalyticsApplication that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the KinesisAnalyticsApplication to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fab4b856a6f82fc332c765a13902780abc0c52c5bb73ca88cec73b3a2b664226)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCloudwatchLoggingOptions")
    def put_cloudwatch_logging_options(
        self,
        *,
        log_stream_arn: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''
        :param log_stream_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#log_stream_arn KinesisAnalyticsApplication#log_stream_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        value = KinesisAnalyticsApplicationCloudwatchLoggingOptions(
            log_stream_arn=log_stream_arn, role_arn=role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLoggingOptions", [value]))

    @jsii.member(jsii_name="putInputs")
    def put_inputs(
        self,
        *,
        name_prefix: builtins.str,
        schema: typing.Union["KinesisAnalyticsApplicationInputsSchema", typing.Dict[builtins.str, typing.Any]],
        kinesis_firehose: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsKinesisFirehose", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_stream: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsKinesisStream", typing.Dict[builtins.str, typing.Any]]] = None,
        parallelism: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsParallelism", typing.Dict[builtins.str, typing.Any]]] = None,
        processing_configuration: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsProcessingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        starting_position_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationInputsStartingPositionConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#name_prefix KinesisAnalyticsApplication#name_prefix}.
        :param schema: schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#schema KinesisAnalyticsApplication#schema}
        :param kinesis_firehose: kinesis_firehose block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#kinesis_firehose KinesisAnalyticsApplication#kinesis_firehose}
        :param kinesis_stream: kinesis_stream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#kinesis_stream KinesisAnalyticsApplication#kinesis_stream}
        :param parallelism: parallelism block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#parallelism KinesisAnalyticsApplication#parallelism}
        :param processing_configuration: processing_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#processing_configuration KinesisAnalyticsApplication#processing_configuration}
        :param starting_position_configuration: starting_position_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#starting_position_configuration KinesisAnalyticsApplication#starting_position_configuration}
        '''
        value = KinesisAnalyticsApplicationInputs(
            name_prefix=name_prefix,
            schema=schema,
            kinesis_firehose=kinesis_firehose,
            kinesis_stream=kinesis_stream,
            parallelism=parallelism,
            processing_configuration=processing_configuration,
            starting_position_configuration=starting_position_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putInputs", [value]))

    @jsii.member(jsii_name="putOutputs")
    def put_outputs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationOutputs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1be5781422e93b2c175aaeda9f040d4e2acb6dfe0551b567f03162776dffded1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOutputs", [value]))

    @jsii.member(jsii_name="putReferenceDataSources")
    def put_reference_data_sources(
        self,
        *,
        s3: typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesS3", typing.Dict[builtins.str, typing.Any]],
        schema: typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchema", typing.Dict[builtins.str, typing.Any]],
        table_name: builtins.str,
    ) -> None:
        '''
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#s3 KinesisAnalyticsApplication#s3}
        :param schema: schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#schema KinesisAnalyticsApplication#schema}
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#table_name KinesisAnalyticsApplication#table_name}.
        '''
        value = KinesisAnalyticsApplicationReferenceDataSources(
            s3=s3, schema=schema, table_name=table_name
        )

        return typing.cast(None, jsii.invoke(self, "putReferenceDataSources", [value]))

    @jsii.member(jsii_name="resetCloudwatchLoggingOptions")
    def reset_cloudwatch_logging_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLoggingOptions", []))

    @jsii.member(jsii_name="resetCode")
    def reset_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCode", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInputs")
    def reset_inputs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputs", []))

    @jsii.member(jsii_name="resetOutputs")
    def reset_outputs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputs", []))

    @jsii.member(jsii_name="resetReferenceDataSources")
    def reset_reference_data_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReferenceDataSources", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetStartApplication")
    def reset_start_application(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartApplication", []))

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
    @jsii.member(jsii_name="cloudwatchLoggingOptions")
    def cloudwatch_logging_options(
        self,
    ) -> "KinesisAnalyticsApplicationCloudwatchLoggingOptionsOutputReference":
        return typing.cast("KinesisAnalyticsApplicationCloudwatchLoggingOptionsOutputReference", jsii.get(self, "cloudwatchLoggingOptions"))

    @builtins.property
    @jsii.member(jsii_name="createTimestamp")
    def create_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="inputs")
    def inputs(self) -> "KinesisAnalyticsApplicationInputsOutputReference":
        return typing.cast("KinesisAnalyticsApplicationInputsOutputReference", jsii.get(self, "inputs"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdateTimestamp")
    def last_update_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdateTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> "KinesisAnalyticsApplicationOutputsList":
        return typing.cast("KinesisAnalyticsApplicationOutputsList", jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="referenceDataSources")
    def reference_data_sources(
        self,
    ) -> "KinesisAnalyticsApplicationReferenceDataSourcesOutputReference":
        return typing.cast("KinesisAnalyticsApplicationReferenceDataSourcesOutputReference", jsii.get(self, "referenceDataSources"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLoggingOptionsInput")
    def cloudwatch_logging_options_input(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationCloudwatchLoggingOptions"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationCloudwatchLoggingOptions"], jsii.get(self, "cloudwatchLoggingOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="codeInput")
    def code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inputsInput")
    def inputs_input(self) -> typing.Optional["KinesisAnalyticsApplicationInputs"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputs"], jsii.get(self, "inputsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="outputsInput")
    def outputs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationOutputs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationOutputs"]]], jsii.get(self, "outputsInput"))

    @builtins.property
    @jsii.member(jsii_name="referenceDataSourcesInput")
    def reference_data_sources_input(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationReferenceDataSources"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationReferenceDataSources"], jsii.get(self, "referenceDataSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="startApplicationInput")
    def start_application_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "startApplicationInput"))

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
    @jsii.member(jsii_name="code")
    def code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "code"))

    @code.setter
    def code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c1e1fa66af70c1f7998b2f4cdb594267718ccb0ad367779af80406d3a12f844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "code", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95e7b334a486fd8137c5259d2e22b1da2659d8acbaa4db0177c53e0824a85a7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a30c5cd63f854eec0ed8454a3a0f9b5b184a694b8c07d7c6cf218aa932eb7e93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd8703faa968668acfb77f460fb653bc0d9e4e5224861e53ac84c1034504fd3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10de9e6613cd88d53df5e7badcbb219d7bcfac10d8613f7428a6f56fb67e9820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startApplication")
    def start_application(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "startApplication"))

    @start_application.setter
    def start_application(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__063947a72049b6797791e2036c6fdcf2bf108e4a7c77badedb8d9ea21a64b3a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startApplication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8739f8f7b66eeb0ba29fa1ea39103ddd293ad86b6d75ed9f22a690a1b4fcd210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c3363f93296933a7586030fc4d3e0ae4d66b5247371d77b3bd5db7e327a8d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationCloudwatchLoggingOptions",
    jsii_struct_bases=[],
    name_mapping={"log_stream_arn": "logStreamArn", "role_arn": "roleArn"},
)
class KinesisAnalyticsApplicationCloudwatchLoggingOptions:
    def __init__(self, *, log_stream_arn: builtins.str, role_arn: builtins.str) -> None:
        '''
        :param log_stream_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#log_stream_arn KinesisAnalyticsApplication#log_stream_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1540e53f75e14617d6d7828c6593f1e1e3955e4fe4e9a0338657d3421dc25b0a)
            check_type(argname="argument log_stream_arn", value=log_stream_arn, expected_type=type_hints["log_stream_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_stream_arn": log_stream_arn,
            "role_arn": role_arn,
        }

    @builtins.property
    def log_stream_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#log_stream_arn KinesisAnalyticsApplication#log_stream_arn}.'''
        result = self._values.get("log_stream_arn")
        assert result is not None, "Required property 'log_stream_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationCloudwatchLoggingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationCloudwatchLoggingOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationCloudwatchLoggingOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b412611f6d9013805a2e566bdb470a0ea066a8d1ca8dc8d94cc106ec3bb4df3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="logStreamArnInput")
    def log_stream_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamArn")
    def log_stream_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamArn"))

    @log_stream_arn.setter
    def log_stream_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8107c97a70cc0f2f924e183cb42b6f5fd2c999cc6a009c52f425eb7ca8cf9b23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__012a51ffcadb90c90c0226134d0f9b39e6fc2707dc724fe4e294725ce2bdd48c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationCloudwatchLoggingOptions]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationCloudwatchLoggingOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationCloudwatchLoggingOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1b0c53a0fe6ee1d1e58c69da422a688d4c0c0cc76a2fac8e151fd0661a78de1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationConfig",
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
        "cloudwatch_logging_options": "cloudwatchLoggingOptions",
        "code": "code",
        "description": "description",
        "id": "id",
        "inputs": "inputs",
        "outputs": "outputs",
        "reference_data_sources": "referenceDataSources",
        "region": "region",
        "start_application": "startApplication",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class KinesisAnalyticsApplicationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cloudwatch_logging_options: typing.Optional[typing.Union[KinesisAnalyticsApplicationCloudwatchLoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        code: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        inputs: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputs", typing.Dict[builtins.str, typing.Any]]] = None,
        outputs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationOutputs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        reference_data_sources: typing.Optional[typing.Union["KinesisAnalyticsApplicationReferenceDataSources", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        start_application: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#name KinesisAnalyticsApplication#name}.
        :param cloudwatch_logging_options: cloudwatch_logging_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#cloudwatch_logging_options KinesisAnalyticsApplication#cloudwatch_logging_options}
        :param code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#code KinesisAnalyticsApplication#code}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#description KinesisAnalyticsApplication#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#id KinesisAnalyticsApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inputs: inputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#inputs KinesisAnalyticsApplication#inputs}
        :param outputs: outputs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#outputs KinesisAnalyticsApplication#outputs}
        :param reference_data_sources: reference_data_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#reference_data_sources KinesisAnalyticsApplication#reference_data_sources}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#region KinesisAnalyticsApplication#region}
        :param start_application: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#start_application KinesisAnalyticsApplication#start_application}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#tags KinesisAnalyticsApplication#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#tags_all KinesisAnalyticsApplication#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cloudwatch_logging_options, dict):
            cloudwatch_logging_options = KinesisAnalyticsApplicationCloudwatchLoggingOptions(**cloudwatch_logging_options)
        if isinstance(inputs, dict):
            inputs = KinesisAnalyticsApplicationInputs(**inputs)
        if isinstance(reference_data_sources, dict):
            reference_data_sources = KinesisAnalyticsApplicationReferenceDataSources(**reference_data_sources)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__931bda2648b78d9a02bdef76842dab3da4a2417fb1dd145f3eb89994cf51c71f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument cloudwatch_logging_options", value=cloudwatch_logging_options, expected_type=type_hints["cloudwatch_logging_options"])
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument inputs", value=inputs, expected_type=type_hints["inputs"])
            check_type(argname="argument outputs", value=outputs, expected_type=type_hints["outputs"])
            check_type(argname="argument reference_data_sources", value=reference_data_sources, expected_type=type_hints["reference_data_sources"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument start_application", value=start_application, expected_type=type_hints["start_application"])
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
        if cloudwatch_logging_options is not None:
            self._values["cloudwatch_logging_options"] = cloudwatch_logging_options
        if code is not None:
            self._values["code"] = code
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if inputs is not None:
            self._values["inputs"] = inputs
        if outputs is not None:
            self._values["outputs"] = outputs
        if reference_data_sources is not None:
            self._values["reference_data_sources"] = reference_data_sources
        if region is not None:
            self._values["region"] = region
        if start_application is not None:
            self._values["start_application"] = start_application
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#name KinesisAnalyticsApplication#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloudwatch_logging_options(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationCloudwatchLoggingOptions]:
        '''cloudwatch_logging_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#cloudwatch_logging_options KinesisAnalyticsApplication#cloudwatch_logging_options}
        '''
        result = self._values.get("cloudwatch_logging_options")
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationCloudwatchLoggingOptions], result)

    @builtins.property
    def code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#code KinesisAnalyticsApplication#code}.'''
        result = self._values.get("code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#description KinesisAnalyticsApplication#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#id KinesisAnalyticsApplication#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inputs(self) -> typing.Optional["KinesisAnalyticsApplicationInputs"]:
        '''inputs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#inputs KinesisAnalyticsApplication#inputs}
        '''
        result = self._values.get("inputs")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputs"], result)

    @builtins.property
    def outputs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationOutputs"]]]:
        '''outputs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#outputs KinesisAnalyticsApplication#outputs}
        '''
        result = self._values.get("outputs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationOutputs"]]], result)

    @builtins.property
    def reference_data_sources(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationReferenceDataSources"]:
        '''reference_data_sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#reference_data_sources KinesisAnalyticsApplication#reference_data_sources}
        '''
        result = self._values.get("reference_data_sources")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationReferenceDataSources"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#region KinesisAnalyticsApplication#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_application(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#start_application KinesisAnalyticsApplication#start_application}.'''
        result = self._values.get("start_application")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#tags KinesisAnalyticsApplication#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#tags_all KinesisAnalyticsApplication#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputs",
    jsii_struct_bases=[],
    name_mapping={
        "name_prefix": "namePrefix",
        "schema": "schema",
        "kinesis_firehose": "kinesisFirehose",
        "kinesis_stream": "kinesisStream",
        "parallelism": "parallelism",
        "processing_configuration": "processingConfiguration",
        "starting_position_configuration": "startingPositionConfiguration",
    },
)
class KinesisAnalyticsApplicationInputs:
    def __init__(
        self,
        *,
        name_prefix: builtins.str,
        schema: typing.Union["KinesisAnalyticsApplicationInputsSchema", typing.Dict[builtins.str, typing.Any]],
        kinesis_firehose: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsKinesisFirehose", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_stream: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsKinesisStream", typing.Dict[builtins.str, typing.Any]]] = None,
        parallelism: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsParallelism", typing.Dict[builtins.str, typing.Any]]] = None,
        processing_configuration: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsProcessingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        starting_position_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationInputsStartingPositionConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#name_prefix KinesisAnalyticsApplication#name_prefix}.
        :param schema: schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#schema KinesisAnalyticsApplication#schema}
        :param kinesis_firehose: kinesis_firehose block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#kinesis_firehose KinesisAnalyticsApplication#kinesis_firehose}
        :param kinesis_stream: kinesis_stream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#kinesis_stream KinesisAnalyticsApplication#kinesis_stream}
        :param parallelism: parallelism block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#parallelism KinesisAnalyticsApplication#parallelism}
        :param processing_configuration: processing_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#processing_configuration KinesisAnalyticsApplication#processing_configuration}
        :param starting_position_configuration: starting_position_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#starting_position_configuration KinesisAnalyticsApplication#starting_position_configuration}
        '''
        if isinstance(schema, dict):
            schema = KinesisAnalyticsApplicationInputsSchema(**schema)
        if isinstance(kinesis_firehose, dict):
            kinesis_firehose = KinesisAnalyticsApplicationInputsKinesisFirehose(**kinesis_firehose)
        if isinstance(kinesis_stream, dict):
            kinesis_stream = KinesisAnalyticsApplicationInputsKinesisStream(**kinesis_stream)
        if isinstance(parallelism, dict):
            parallelism = KinesisAnalyticsApplicationInputsParallelism(**parallelism)
        if isinstance(processing_configuration, dict):
            processing_configuration = KinesisAnalyticsApplicationInputsProcessingConfiguration(**processing_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dde1abd339ba55bf1233682e2a0283b7eb389e89728cfca9196a3cfafdc0414b)
            check_type(argname="argument name_prefix", value=name_prefix, expected_type=type_hints["name_prefix"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument kinesis_firehose", value=kinesis_firehose, expected_type=type_hints["kinesis_firehose"])
            check_type(argname="argument kinesis_stream", value=kinesis_stream, expected_type=type_hints["kinesis_stream"])
            check_type(argname="argument parallelism", value=parallelism, expected_type=type_hints["parallelism"])
            check_type(argname="argument processing_configuration", value=processing_configuration, expected_type=type_hints["processing_configuration"])
            check_type(argname="argument starting_position_configuration", value=starting_position_configuration, expected_type=type_hints["starting_position_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name_prefix": name_prefix,
            "schema": schema,
        }
        if kinesis_firehose is not None:
            self._values["kinesis_firehose"] = kinesis_firehose
        if kinesis_stream is not None:
            self._values["kinesis_stream"] = kinesis_stream
        if parallelism is not None:
            self._values["parallelism"] = parallelism
        if processing_configuration is not None:
            self._values["processing_configuration"] = processing_configuration
        if starting_position_configuration is not None:
            self._values["starting_position_configuration"] = starting_position_configuration

    @builtins.property
    def name_prefix(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#name_prefix KinesisAnalyticsApplication#name_prefix}.'''
        result = self._values.get("name_prefix")
        assert result is not None, "Required property 'name_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> "KinesisAnalyticsApplicationInputsSchema":
        '''schema block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#schema KinesisAnalyticsApplication#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast("KinesisAnalyticsApplicationInputsSchema", result)

    @builtins.property
    def kinesis_firehose(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsKinesisFirehose"]:
        '''kinesis_firehose block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#kinesis_firehose KinesisAnalyticsApplication#kinesis_firehose}
        '''
        result = self._values.get("kinesis_firehose")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsKinesisFirehose"], result)

    @builtins.property
    def kinesis_stream(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsKinesisStream"]:
        '''kinesis_stream block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#kinesis_stream KinesisAnalyticsApplication#kinesis_stream}
        '''
        result = self._values.get("kinesis_stream")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsKinesisStream"], result)

    @builtins.property
    def parallelism(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsParallelism"]:
        '''parallelism block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#parallelism KinesisAnalyticsApplication#parallelism}
        '''
        result = self._values.get("parallelism")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsParallelism"], result)

    @builtins.property
    def processing_configuration(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsProcessingConfiguration"]:
        '''processing_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#processing_configuration KinesisAnalyticsApplication#processing_configuration}
        '''
        result = self._values.get("processing_configuration")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsProcessingConfiguration"], result)

    @builtins.property
    def starting_position_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationInputsStartingPositionConfiguration"]]]:
        '''starting_position_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#starting_position_configuration KinesisAnalyticsApplication#starting_position_configuration}
        '''
        result = self._values.get("starting_position_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationInputsStartingPositionConfiguration"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsKinesisFirehose",
    jsii_struct_bases=[],
    name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
)
class KinesisAnalyticsApplicationInputsKinesisFirehose:
    def __init__(self, *, resource_arn: builtins.str, role_arn: builtins.str) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7819fb5fd8059ec21ad1ed680b94770ef0f8409d783db57c0fd5413204b7356)
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_arn": resource_arn,
            "role_arn": role_arn,
        }

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.'''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsKinesisFirehose(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationInputsKinesisFirehoseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsKinesisFirehoseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3491500e5a4d609a03d4675b3b49f76be34884bafc5823054b85fdc1221a3379)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceArnInput")
    def resource_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1495896b7d329a06e2421c8f4c801b54293295832f56ad63c7adbd4fe63764e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d40b436c5d393728eeb7b8181e5f0faeec9209adc1ca807ad5aadcf2c906b7e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsKinesisFirehose]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsKinesisFirehose], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputsKinesisFirehose],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0a70ccfa1f986d7cb81cbebb42cdd5ac6fdcb98e175679c3bc0f0dc1ec28b2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsKinesisStream",
    jsii_struct_bases=[],
    name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
)
class KinesisAnalyticsApplicationInputsKinesisStream:
    def __init__(self, *, resource_arn: builtins.str, role_arn: builtins.str) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e8ad6d943ed98b0b8d12c218b17f870f42fd88c4d3d8a086120738cd585f8e)
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_arn": resource_arn,
            "role_arn": role_arn,
        }

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.'''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsKinesisStream(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationInputsKinesisStreamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsKinesisStreamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9d2b31dd1c46b04fe48fd7d595f6639f18e2d03fbfa96118f5eb06ec5fc6c1f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceArnInput")
    def resource_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5b73ccc2e23fdbf39345acf3d1d41edf67e935e7a1cb96dce7132a31cb395d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__090c1ab904e975fe37ad89e976268002913a4bde82bd4a29417fc317ea7d5aff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsKinesisStream]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsKinesisStream], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputsKinesisStream],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3edc2300045359833081f70241b395cd2b0aa861963e03832934a142143fddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationInputsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c734a8bc289e34de41535f73f60d1a91c2254476bea1ac1921f8ec4ca835f14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putKinesisFirehose")
    def put_kinesis_firehose(
        self,
        *,
        resource_arn: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        value = KinesisAnalyticsApplicationInputsKinesisFirehose(
            resource_arn=resource_arn, role_arn=role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putKinesisFirehose", [value]))

    @jsii.member(jsii_name="putKinesisStream")
    def put_kinesis_stream(
        self,
        *,
        resource_arn: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        value = KinesisAnalyticsApplicationInputsKinesisStream(
            resource_arn=resource_arn, role_arn=role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putKinesisStream", [value]))

    @jsii.member(jsii_name="putParallelism")
    def put_parallelism(self, *, count: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#count KinesisAnalyticsApplication#count}.
        '''
        value = KinesisAnalyticsApplicationInputsParallelism(count=count)

        return typing.cast(None, jsii.invoke(self, "putParallelism", [value]))

    @jsii.member(jsii_name="putProcessingConfiguration")
    def put_processing_configuration(
        self,
        *,
        lambda_: typing.Union["KinesisAnalyticsApplicationInputsProcessingConfigurationLambda", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param lambda_: lambda block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#lambda KinesisAnalyticsApplication#lambda}
        '''
        value = KinesisAnalyticsApplicationInputsProcessingConfiguration(
            lambda_=lambda_
        )

        return typing.cast(None, jsii.invoke(self, "putProcessingConfiguration", [value]))

    @jsii.member(jsii_name="putSchema")
    def put_schema(
        self,
        *,
        record_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationInputsSchemaRecordColumns", typing.Dict[builtins.str, typing.Any]]]],
        record_format: typing.Union["KinesisAnalyticsApplicationInputsSchemaRecordFormat", typing.Dict[builtins.str, typing.Any]],
        record_encoding: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param record_columns: record_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_columns KinesisAnalyticsApplication#record_columns}
        :param record_format: record_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_format KinesisAnalyticsApplication#record_format}
        :param record_encoding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_encoding KinesisAnalyticsApplication#record_encoding}.
        '''
        value = KinesisAnalyticsApplicationInputsSchema(
            record_columns=record_columns,
            record_format=record_format,
            record_encoding=record_encoding,
        )

        return typing.cast(None, jsii.invoke(self, "putSchema", [value]))

    @jsii.member(jsii_name="putStartingPositionConfiguration")
    def put_starting_position_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationInputsStartingPositionConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3946a227bc6a62f7635bf0fc85268eb8286021c03d4a5e6af778c815e7b67358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStartingPositionConfiguration", [value]))

    @jsii.member(jsii_name="resetKinesisFirehose")
    def reset_kinesis_firehose(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisFirehose", []))

    @jsii.member(jsii_name="resetKinesisStream")
    def reset_kinesis_stream(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisStream", []))

    @jsii.member(jsii_name="resetParallelism")
    def reset_parallelism(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelism", []))

    @jsii.member(jsii_name="resetProcessingConfiguration")
    def reset_processing_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessingConfiguration", []))

    @jsii.member(jsii_name="resetStartingPositionConfiguration")
    def reset_starting_position_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartingPositionConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehose")
    def kinesis_firehose(
        self,
    ) -> KinesisAnalyticsApplicationInputsKinesisFirehoseOutputReference:
        return typing.cast(KinesisAnalyticsApplicationInputsKinesisFirehoseOutputReference, jsii.get(self, "kinesisFirehose"))

    @builtins.property
    @jsii.member(jsii_name="kinesisStream")
    def kinesis_stream(
        self,
    ) -> KinesisAnalyticsApplicationInputsKinesisStreamOutputReference:
        return typing.cast(KinesisAnalyticsApplicationInputsKinesisStreamOutputReference, jsii.get(self, "kinesisStream"))

    @builtins.property
    @jsii.member(jsii_name="parallelism")
    def parallelism(
        self,
    ) -> "KinesisAnalyticsApplicationInputsParallelismOutputReference":
        return typing.cast("KinesisAnalyticsApplicationInputsParallelismOutputReference", jsii.get(self, "parallelism"))

    @builtins.property
    @jsii.member(jsii_name="processingConfiguration")
    def processing_configuration(
        self,
    ) -> "KinesisAnalyticsApplicationInputsProcessingConfigurationOutputReference":
        return typing.cast("KinesisAnalyticsApplicationInputsProcessingConfigurationOutputReference", jsii.get(self, "processingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> "KinesisAnalyticsApplicationInputsSchemaOutputReference":
        return typing.cast("KinesisAnalyticsApplicationInputsSchemaOutputReference", jsii.get(self, "schema"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionConfiguration")
    def starting_position_configuration(
        self,
    ) -> "KinesisAnalyticsApplicationInputsStartingPositionConfigurationList":
        return typing.cast("KinesisAnalyticsApplicationInputsStartingPositionConfigurationList", jsii.get(self, "startingPositionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="streamNames")
    def stream_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "streamNames"))

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehoseInput")
    def kinesis_firehose_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsKinesisFirehose]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsKinesisFirehose], jsii.get(self, "kinesisFirehoseInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisStreamInput")
    def kinesis_stream_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsKinesisStream]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsKinesisStream], jsii.get(self, "kinesisStreamInput"))

    @builtins.property
    @jsii.member(jsii_name="namePrefixInput")
    def name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelismInput")
    def parallelism_input(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsParallelism"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsParallelism"], jsii.get(self, "parallelismInput"))

    @builtins.property
    @jsii.member(jsii_name="processingConfigurationInput")
    def processing_configuration_input(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsProcessingConfiguration"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsProcessingConfiguration"], jsii.get(self, "processingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsSchema"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsSchema"], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionConfigurationInput")
    def starting_position_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationInputsStartingPositionConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationInputsStartingPositionConfiguration"]]], jsii.get(self, "startingPositionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @name_prefix.setter
    def name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5220559efda3195ac7f0179b6b2ccb65fd09b8a5f75750971ecad592211f78d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KinesisAnalyticsApplicationInputs]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b7396a80b57f0f46ae32dd90c6fe8268123d31e9a3e83b0e05728050c004b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsParallelism",
    jsii_struct_bases=[],
    name_mapping={"count": "count"},
)
class KinesisAnalyticsApplicationInputsParallelism:
    def __init__(self, *, count: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#count KinesisAnalyticsApplication#count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e7b8e9eed392ec1dc04274b7a9a4adc1677e6dd394d159e147e52863922a999)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#count KinesisAnalyticsApplication#count}.'''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsParallelism(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationInputsParallelismOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsParallelismOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a05341a852420a7240b42387a827584c03ebadebde4f2962b447c897d86753f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f0ecb683194f336b31f813ef3dea96f1a7e4807bb8d236f1d6256888343c03d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsParallelism]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsParallelism], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputsParallelism],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b60b3e845a44af2f6d376915a3c84ddf56db0c7c6830091c95527541e24dc78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsProcessingConfiguration",
    jsii_struct_bases=[],
    name_mapping={"lambda_": "lambda"},
)
class KinesisAnalyticsApplicationInputsProcessingConfiguration:
    def __init__(
        self,
        *,
        lambda_: typing.Union["KinesisAnalyticsApplicationInputsProcessingConfigurationLambda", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param lambda_: lambda block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#lambda KinesisAnalyticsApplication#lambda}
        '''
        if isinstance(lambda_, dict):
            lambda_ = KinesisAnalyticsApplicationInputsProcessingConfigurationLambda(**lambda_)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f18c52514cdb475231476cdaaa14324c5e58af60a779e4ee461a62970e6046e8)
            check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lambda_": lambda_,
        }

    @builtins.property
    def lambda_(
        self,
    ) -> "KinesisAnalyticsApplicationInputsProcessingConfigurationLambda":
        '''lambda block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#lambda KinesisAnalyticsApplication#lambda}
        '''
        result = self._values.get("lambda_")
        assert result is not None, "Required property 'lambda_' is missing"
        return typing.cast("KinesisAnalyticsApplicationInputsProcessingConfigurationLambda", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsProcessingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsProcessingConfigurationLambda",
    jsii_struct_bases=[],
    name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
)
class KinesisAnalyticsApplicationInputsProcessingConfigurationLambda:
    def __init__(self, *, resource_arn: builtins.str, role_arn: builtins.str) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7025c59c4202678ddf8dd83e9edc02a161cbbdcbafc554fafc199bb4463636db)
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_arn": resource_arn,
            "role_arn": role_arn,
        }

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.'''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsProcessingConfigurationLambda(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationInputsProcessingConfigurationLambdaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsProcessingConfigurationLambdaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c72774c14797b1d145c76f4006ce20200aaa83ab3e86d38d543b5be580fbac6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceArnInput")
    def resource_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d848075ced3494bd5998512e9006c9509f24032389b5e9c397bb910570dd1c20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b5ca407cd5f1d1b00f615fc51c0086010567a4975844b2a9126cd37ceb9f641)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsProcessingConfigurationLambda]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsProcessingConfigurationLambda], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputsProcessingConfigurationLambda],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae2bb24803d2b7c18a3fccb4e16db97790fdc63686c10a77c9afdd4bc8049e06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationInputsProcessingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsProcessingConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__709af94d710161f14a9cbc43bcde0c650113f6395dcfde0f837ec1fffab5cd0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLambda")
    def put_lambda(self, *, resource_arn: builtins.str, role_arn: builtins.str) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        value = KinesisAnalyticsApplicationInputsProcessingConfigurationLambda(
            resource_arn=resource_arn, role_arn=role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putLambda", [value]))

    @builtins.property
    @jsii.member(jsii_name="lambda")
    def lambda_(
        self,
    ) -> KinesisAnalyticsApplicationInputsProcessingConfigurationLambdaOutputReference:
        return typing.cast(KinesisAnalyticsApplicationInputsProcessingConfigurationLambdaOutputReference, jsii.get(self, "lambda"))

    @builtins.property
    @jsii.member(jsii_name="lambdaInput")
    def lambda_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsProcessingConfigurationLambda]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsProcessingConfigurationLambda], jsii.get(self, "lambdaInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsProcessingConfiguration]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsProcessingConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputsProcessingConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63709ccd4cb0751aa186496fa0e99abd4203e5b23239024c7b499a767fe3319a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchema",
    jsii_struct_bases=[],
    name_mapping={
        "record_columns": "recordColumns",
        "record_format": "recordFormat",
        "record_encoding": "recordEncoding",
    },
)
class KinesisAnalyticsApplicationInputsSchema:
    def __init__(
        self,
        *,
        record_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationInputsSchemaRecordColumns", typing.Dict[builtins.str, typing.Any]]]],
        record_format: typing.Union["KinesisAnalyticsApplicationInputsSchemaRecordFormat", typing.Dict[builtins.str, typing.Any]],
        record_encoding: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param record_columns: record_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_columns KinesisAnalyticsApplication#record_columns}
        :param record_format: record_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_format KinesisAnalyticsApplication#record_format}
        :param record_encoding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_encoding KinesisAnalyticsApplication#record_encoding}.
        '''
        if isinstance(record_format, dict):
            record_format = KinesisAnalyticsApplicationInputsSchemaRecordFormat(**record_format)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a87244b11c978eeb268799a3fd67046ee1187260bb09f1ae945e2f0f8fc63ba7)
            check_type(argname="argument record_columns", value=record_columns, expected_type=type_hints["record_columns"])
            check_type(argname="argument record_format", value=record_format, expected_type=type_hints["record_format"])
            check_type(argname="argument record_encoding", value=record_encoding, expected_type=type_hints["record_encoding"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "record_columns": record_columns,
            "record_format": record_format,
        }
        if record_encoding is not None:
            self._values["record_encoding"] = record_encoding

    @builtins.property
    def record_columns(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationInputsSchemaRecordColumns"]]:
        '''record_columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_columns KinesisAnalyticsApplication#record_columns}
        '''
        result = self._values.get("record_columns")
        assert result is not None, "Required property 'record_columns' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationInputsSchemaRecordColumns"]], result)

    @builtins.property
    def record_format(self) -> "KinesisAnalyticsApplicationInputsSchemaRecordFormat":
        '''record_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_format KinesisAnalyticsApplication#record_format}
        '''
        result = self._values.get("record_format")
        assert result is not None, "Required property 'record_format' is missing"
        return typing.cast("KinesisAnalyticsApplicationInputsSchemaRecordFormat", result)

    @builtins.property
    def record_encoding(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_encoding KinesisAnalyticsApplication#record_encoding}.'''
        result = self._values.get("record_encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsSchema(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationInputsSchemaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd0ee4541409b2cf1f06f965e73fc4703aae15366f13f8508e7692f902720514)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRecordColumns")
    def put_record_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationInputsSchemaRecordColumns", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9499a5486a0c08584971116455d8edc35b4c9e0ee54b01ba12961e40541cce9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRecordColumns", [value]))

    @jsii.member(jsii_name="putRecordFormat")
    def put_record_format(
        self,
        *,
        mapping_parameters: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param mapping_parameters: mapping_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#mapping_parameters KinesisAnalyticsApplication#mapping_parameters}
        '''
        value = KinesisAnalyticsApplicationInputsSchemaRecordFormat(
            mapping_parameters=mapping_parameters
        )

        return typing.cast(None, jsii.invoke(self, "putRecordFormat", [value]))

    @jsii.member(jsii_name="resetRecordEncoding")
    def reset_record_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordEncoding", []))

    @builtins.property
    @jsii.member(jsii_name="recordColumns")
    def record_columns(
        self,
    ) -> "KinesisAnalyticsApplicationInputsSchemaRecordColumnsList":
        return typing.cast("KinesisAnalyticsApplicationInputsSchemaRecordColumnsList", jsii.get(self, "recordColumns"))

    @builtins.property
    @jsii.member(jsii_name="recordFormat")
    def record_format(
        self,
    ) -> "KinesisAnalyticsApplicationInputsSchemaRecordFormatOutputReference":
        return typing.cast("KinesisAnalyticsApplicationInputsSchemaRecordFormatOutputReference", jsii.get(self, "recordFormat"))

    @builtins.property
    @jsii.member(jsii_name="recordColumnsInput")
    def record_columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationInputsSchemaRecordColumns"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationInputsSchemaRecordColumns"]]], jsii.get(self, "recordColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="recordEncodingInput")
    def record_encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordEncodingInput"))

    @builtins.property
    @jsii.member(jsii_name="recordFormatInput")
    def record_format_input(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsSchemaRecordFormat"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsSchemaRecordFormat"], jsii.get(self, "recordFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="recordEncoding")
    def record_encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordEncoding"))

    @record_encoding.setter
    def record_encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c00e7f0ff22f47080de3df6dad26d5f5d6c14a13686d9a01ccc065cc92eab26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordEncoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsSchema]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsSchema], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputsSchema],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc4455e3d8ad4dcc172e31fbeeb51ff0cf97fed2a07b0d83ce75789255ee5e41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordColumns",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "sql_type": "sqlType", "mapping": "mapping"},
)
class KinesisAnalyticsApplicationInputsSchemaRecordColumns:
    def __init__(
        self,
        *,
        name: builtins.str,
        sql_type: builtins.str,
        mapping: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#name KinesisAnalyticsApplication#name}.
        :param sql_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#sql_type KinesisAnalyticsApplication#sql_type}.
        :param mapping: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#mapping KinesisAnalyticsApplication#mapping}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__481bd60e5115ee2d4ca7eb078dc302089cd4f540fbd576a04808b468124f94b9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sql_type", value=sql_type, expected_type=type_hints["sql_type"])
            check_type(argname="argument mapping", value=mapping, expected_type=type_hints["mapping"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "sql_type": sql_type,
        }
        if mapping is not None:
            self._values["mapping"] = mapping

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#name KinesisAnalyticsApplication#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#sql_type KinesisAnalyticsApplication#sql_type}.'''
        result = self._values.get("sql_type")
        assert result is not None, "Required property 'sql_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mapping(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#mapping KinesisAnalyticsApplication#mapping}.'''
        result = self._values.get("mapping")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsSchemaRecordColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationInputsSchemaRecordColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fdac2d92d031b86e1a88f0f7dfd37db3ee74c813f4a5a12e825d2ac3ced56eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KinesisAnalyticsApplicationInputsSchemaRecordColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ee5cba8689aa2a64fd88ae914e80559f9f5cbd162464fc720d83d1777c5165)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KinesisAnalyticsApplicationInputsSchemaRecordColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea507df7de594266163cb2fd65767ac9ee8c387b6b0dd6bb1b59cd6448dccad0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3de93b2494694533ccda520f2609510f8238b0af86afdbadd29b4448b30b9a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5087dee46ebe4079f65c07e191f76996df4a9a814d693058ec447e6eb3fa5f63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationInputsSchemaRecordColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationInputsSchemaRecordColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationInputsSchemaRecordColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d390ece4489dd506f59bb7c24ffabae29d23f2b777022bfe52db6cb3289f2b93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationInputsSchemaRecordColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28d1a14102f2ef6174248051dfaa666e10d02368f4b729d33f7e4c4c1056d1fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMapping")
    def reset_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMapping", []))

    @builtins.property
    @jsii.member(jsii_name="mappingInput")
    def mapping_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mappingInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlTypeInput")
    def sql_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="mapping")
    def mapping(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mapping"))

    @mapping.setter
    def mapping(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43fda08803ce4e18c1fea131a588c075806d23174de41cc7a232b0242cdf010f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ec347aaaaf8718e598cd21d5a6921cc5f9bfa6b9bc7dfbf1a8d3d5056e1a1c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlType")
    def sql_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlType"))

    @sql_type.setter
    def sql_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c92cc0247dfd346183579b3f8e8652328530d6c729ed33dcf8571dd9e583abdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationInputsSchemaRecordColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationInputsSchemaRecordColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationInputsSchemaRecordColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a037241e657827f22605abd54f504401a044cef31eb41b967c1aae6cf7cea4db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordFormat",
    jsii_struct_bases=[],
    name_mapping={"mapping_parameters": "mappingParameters"},
)
class KinesisAnalyticsApplicationInputsSchemaRecordFormat:
    def __init__(
        self,
        *,
        mapping_parameters: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param mapping_parameters: mapping_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#mapping_parameters KinesisAnalyticsApplication#mapping_parameters}
        '''
        if isinstance(mapping_parameters, dict):
            mapping_parameters = KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters(**mapping_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab9feaea829f61d3702588c146def24425db261211a396d39a8541ebc147bb23)
            check_type(argname="argument mapping_parameters", value=mapping_parameters, expected_type=type_hints["mapping_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mapping_parameters is not None:
            self._values["mapping_parameters"] = mapping_parameters

    @builtins.property
    def mapping_parameters(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters"]:
        '''mapping_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#mapping_parameters KinesisAnalyticsApplication#mapping_parameters}
        '''
        result = self._values.get("mapping_parameters")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsSchemaRecordFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters",
    jsii_struct_bases=[],
    name_mapping={"csv": "csv", "json": "json"},
)
class KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters:
    def __init__(
        self,
        *,
        csv: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv", typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union["KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param csv: csv block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#csv KinesisAnalyticsApplication#csv}
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#json KinesisAnalyticsApplication#json}
        '''
        if isinstance(csv, dict):
            csv = KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv(**csv)
        if isinstance(json, dict):
            json = KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson(**json)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b6737a7f654935b1cfac04e66eab1309e3ad4bb3f2a1fc5b4ad6ea2975ff34)
            check_type(argname="argument csv", value=csv, expected_type=type_hints["csv"])
            check_type(argname="argument json", value=json, expected_type=type_hints["json"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if csv is not None:
            self._values["csv"] = csv
        if json is not None:
            self._values["json"] = json

    @builtins.property
    def csv(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv"]:
        '''csv block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#csv KinesisAnalyticsApplication#csv}
        '''
        result = self._values.get("csv")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv"], result)

    @builtins.property
    def json(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson"]:
        '''json block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#json KinesisAnalyticsApplication#json}
        '''
        result = self._values.get("json")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv",
    jsii_struct_bases=[],
    name_mapping={
        "record_column_delimiter": "recordColumnDelimiter",
        "record_row_delimiter": "recordRowDelimiter",
    },
)
class KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv:
    def __init__(
        self,
        *,
        record_column_delimiter: builtins.str,
        record_row_delimiter: builtins.str,
    ) -> None:
        '''
        :param record_column_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_column_delimiter KinesisAnalyticsApplication#record_column_delimiter}.
        :param record_row_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_row_delimiter KinesisAnalyticsApplication#record_row_delimiter}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ea85e4d02873b6a51d3d2a20dcca4401dd6db0115ba795304a338a9cd33bf4e)
            check_type(argname="argument record_column_delimiter", value=record_column_delimiter, expected_type=type_hints["record_column_delimiter"])
            check_type(argname="argument record_row_delimiter", value=record_row_delimiter, expected_type=type_hints["record_row_delimiter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "record_column_delimiter": record_column_delimiter,
            "record_row_delimiter": record_row_delimiter,
        }

    @builtins.property
    def record_column_delimiter(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_column_delimiter KinesisAnalyticsApplication#record_column_delimiter}.'''
        result = self._values.get("record_column_delimiter")
        assert result is not None, "Required property 'record_column_delimiter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def record_row_delimiter(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_row_delimiter KinesisAnalyticsApplication#record_row_delimiter}.'''
        result = self._values.get("record_row_delimiter")
        assert result is not None, "Required property 'record_row_delimiter' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f30a6188df4871030dd0bbcab63414d330ea393a34b7bb735150b0299fff1c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="recordColumnDelimiterInput")
    def record_column_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordColumnDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="recordRowDelimiterInput")
    def record_row_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordRowDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="recordColumnDelimiter")
    def record_column_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordColumnDelimiter"))

    @record_column_delimiter.setter
    def record_column_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__324c80d0414062cebb98fa0f6ff00833401eca781d8b20113287155a19110b99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordColumnDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recordRowDelimiter")
    def record_row_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordRowDelimiter"))

    @record_row_delimiter.setter
    def record_row_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7a65c84d4ac6a4ba9a5348db25b7acb608c954afe6b4190612dacde5ed243aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordRowDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4c9bd9f65d91fdf57b8cce671badaf7b0fba481a7daaae13631542fc0492524)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson",
    jsii_struct_bases=[],
    name_mapping={"record_row_path": "recordRowPath"},
)
class KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson:
    def __init__(self, *, record_row_path: builtins.str) -> None:
        '''
        :param record_row_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_row_path KinesisAnalyticsApplication#record_row_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72d7277237dd8b7d2c79dcb8e8bbafa0d6d7f2b8c19c7675b79f96af08d48aed)
            check_type(argname="argument record_row_path", value=record_row_path, expected_type=type_hints["record_row_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "record_row_path": record_row_path,
        }

    @builtins.property
    def record_row_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_row_path KinesisAnalyticsApplication#record_row_path}.'''
        result = self._values.get("record_row_path")
        assert result is not None, "Required property 'record_row_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJsonOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJsonOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e82eb73527c6a3e0b59c1b2c2987769dc7c9a572e504775286b0e022d14fceb6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="recordRowPathInput")
    def record_row_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordRowPathInput"))

    @builtins.property
    @jsii.member(jsii_name="recordRowPath")
    def record_row_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordRowPath"))

    @record_row_path.setter
    def record_row_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e3d45960b66d4d45b0ed2c140f4d9d31687123a8d25f14dc66bba453d8b3698)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordRowPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab3eb8d8648771fa5b78c1b1db6e8beb684cba214375d3cb70e331efada1213e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83ebbefca202267f60c8e9f17d7021acb75b0f4dc31fe0eaf9c51640cda522ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCsv")
    def put_csv(
        self,
        *,
        record_column_delimiter: builtins.str,
        record_row_delimiter: builtins.str,
    ) -> None:
        '''
        :param record_column_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_column_delimiter KinesisAnalyticsApplication#record_column_delimiter}.
        :param record_row_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_row_delimiter KinesisAnalyticsApplication#record_row_delimiter}.
        '''
        value = KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv(
            record_column_delimiter=record_column_delimiter,
            record_row_delimiter=record_row_delimiter,
        )

        return typing.cast(None, jsii.invoke(self, "putCsv", [value]))

    @jsii.member(jsii_name="putJson")
    def put_json(self, *, record_row_path: builtins.str) -> None:
        '''
        :param record_row_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_row_path KinesisAnalyticsApplication#record_row_path}.
        '''
        value = KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson(
            record_row_path=record_row_path
        )

        return typing.cast(None, jsii.invoke(self, "putJson", [value]))

    @jsii.member(jsii_name="resetCsv")
    def reset_csv(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCsv", []))

    @jsii.member(jsii_name="resetJson")
    def reset_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJson", []))

    @builtins.property
    @jsii.member(jsii_name="csv")
    def csv(
        self,
    ) -> KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsvOutputReference:
        return typing.cast(KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsvOutputReference, jsii.get(self, "csv"))

    @builtins.property
    @jsii.member(jsii_name="json")
    def json(
        self,
    ) -> KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJsonOutputReference:
        return typing.cast(KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJsonOutputReference, jsii.get(self, "json"))

    @builtins.property
    @jsii.member(jsii_name="csvInput")
    def csv_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv], jsii.get(self, "csvInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonInput")
    def json_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson], jsii.get(self, "jsonInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17c1d429b5ca4f6f53a55068fc96b26e58d2fc2e4375d6e98814c326887876bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationInputsSchemaRecordFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsSchemaRecordFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bb2b64abf4dcd8ba72f8b25ea3d69b1b73888e9514bc4b34780f084737ac7ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMappingParameters")
    def put_mapping_parameters(
        self,
        *,
        csv: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv, typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param csv: csv block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#csv KinesisAnalyticsApplication#csv}
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#json KinesisAnalyticsApplication#json}
        '''
        value = KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters(
            csv=csv, json=json
        )

        return typing.cast(None, jsii.invoke(self, "putMappingParameters", [value]))

    @jsii.member(jsii_name="resetMappingParameters")
    def reset_mapping_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMappingParameters", []))

    @builtins.property
    @jsii.member(jsii_name="mappingParameters")
    def mapping_parameters(
        self,
    ) -> KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersOutputReference:
        return typing.cast(KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersOutputReference, jsii.get(self, "mappingParameters"))

    @builtins.property
    @jsii.member(jsii_name="recordFormatType")
    def record_format_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordFormatType"))

    @builtins.property
    @jsii.member(jsii_name="mappingParametersInput")
    def mapping_parameters_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters], jsii.get(self, "mappingParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormat]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd35a394fad958f845ec116f0a3de8f45e562c1456364e69a601e13784b88a69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsStartingPositionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"starting_position": "startingPosition"},
)
class KinesisAnalyticsApplicationInputsStartingPositionConfiguration:
    def __init__(
        self,
        *,
        starting_position: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param starting_position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#starting_position KinesisAnalyticsApplication#starting_position}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd76deb6df29034c4326daa77ee83fbeada2465ec59f6da51674ecdc79f0786)
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if starting_position is not None:
            self._values["starting_position"] = starting_position

    @builtins.property
    def starting_position(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#starting_position KinesisAnalyticsApplication#starting_position}.'''
        result = self._values.get("starting_position")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationInputsStartingPositionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationInputsStartingPositionConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsStartingPositionConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27dfe976398a4f25e8f0bb34e20506d78b102d708774c6904ac03b6ac23ca493)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KinesisAnalyticsApplicationInputsStartingPositionConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__518a7099d9e6369d6b9b1be80e37ed8cee360d485bcd3a211187bcf4c40312ff)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KinesisAnalyticsApplicationInputsStartingPositionConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c8e592acdb3a04705ea33b6c698da4b66078e2313e1b4df54fd72f475c89f3f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68741eef12d3bc04d0c931ee11e2f0225daa54c171b36ac4c633478d4d8377b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a867c6f7ffbbf5e27ee72441847a3240725f4a77218f0aa79c8cf4e0457c714)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationInputsStartingPositionConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationInputsStartingPositionConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationInputsStartingPositionConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c8fa60f2bad434ecbe44c38f62aca68bd041890405542c31df2a0bf275024d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationInputsStartingPositionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationInputsStartingPositionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76d1b0e106eaa9dff432750c8c3e42e2e65968e204edd08454352f3d84d50deb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetStartingPosition")
    def reset_starting_position(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartingPosition", []))

    @builtins.property
    @jsii.member(jsii_name="startingPositionInput")
    def starting_position_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startingPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPosition")
    def starting_position(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startingPosition"))

    @starting_position.setter
    def starting_position(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__243d25b1682f296b4beffc29e38892a84c7f91292a409492037cabb41adbaf7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startingPosition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationInputsStartingPositionConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationInputsStartingPositionConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationInputsStartingPositionConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e9baed07fb4ea6df5abed5bf17ac6753e28fd2007ba333bbe01442d657bb645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputs",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "schema": "schema",
        "kinesis_firehose": "kinesisFirehose",
        "kinesis_stream": "kinesisStream",
        "lambda_": "lambda",
    },
)
class KinesisAnalyticsApplicationOutputs:
    def __init__(
        self,
        *,
        name: builtins.str,
        schema: typing.Union["KinesisAnalyticsApplicationOutputsSchema", typing.Dict[builtins.str, typing.Any]],
        kinesis_firehose: typing.Optional[typing.Union["KinesisAnalyticsApplicationOutputsKinesisFirehose", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_stream: typing.Optional[typing.Union["KinesisAnalyticsApplicationOutputsKinesisStream", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_: typing.Optional[typing.Union["KinesisAnalyticsApplicationOutputsLambda", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#name KinesisAnalyticsApplication#name}.
        :param schema: schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#schema KinesisAnalyticsApplication#schema}
        :param kinesis_firehose: kinesis_firehose block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#kinesis_firehose KinesisAnalyticsApplication#kinesis_firehose}
        :param kinesis_stream: kinesis_stream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#kinesis_stream KinesisAnalyticsApplication#kinesis_stream}
        :param lambda_: lambda block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#lambda KinesisAnalyticsApplication#lambda}
        '''
        if isinstance(schema, dict):
            schema = KinesisAnalyticsApplicationOutputsSchema(**schema)
        if isinstance(kinesis_firehose, dict):
            kinesis_firehose = KinesisAnalyticsApplicationOutputsKinesisFirehose(**kinesis_firehose)
        if isinstance(kinesis_stream, dict):
            kinesis_stream = KinesisAnalyticsApplicationOutputsKinesisStream(**kinesis_stream)
        if isinstance(lambda_, dict):
            lambda_ = KinesisAnalyticsApplicationOutputsLambda(**lambda_)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10ac30e080c76295b6e63d4520353f6c50704d07ec5b18a6c42252c51296a5a6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument kinesis_firehose", value=kinesis_firehose, expected_type=type_hints["kinesis_firehose"])
            check_type(argname="argument kinesis_stream", value=kinesis_stream, expected_type=type_hints["kinesis_stream"])
            check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "schema": schema,
        }
        if kinesis_firehose is not None:
            self._values["kinesis_firehose"] = kinesis_firehose
        if kinesis_stream is not None:
            self._values["kinesis_stream"] = kinesis_stream
        if lambda_ is not None:
            self._values["lambda_"] = lambda_

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#name KinesisAnalyticsApplication#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> "KinesisAnalyticsApplicationOutputsSchema":
        '''schema block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#schema KinesisAnalyticsApplication#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast("KinesisAnalyticsApplicationOutputsSchema", result)

    @builtins.property
    def kinesis_firehose(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationOutputsKinesisFirehose"]:
        '''kinesis_firehose block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#kinesis_firehose KinesisAnalyticsApplication#kinesis_firehose}
        '''
        result = self._values.get("kinesis_firehose")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationOutputsKinesisFirehose"], result)

    @builtins.property
    def kinesis_stream(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationOutputsKinesisStream"]:
        '''kinesis_stream block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#kinesis_stream KinesisAnalyticsApplication#kinesis_stream}
        '''
        result = self._values.get("kinesis_stream")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationOutputsKinesisStream"], result)

    @builtins.property
    def lambda_(self) -> typing.Optional["KinesisAnalyticsApplicationOutputsLambda"]:
        '''lambda block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#lambda KinesisAnalyticsApplication#lambda}
        '''
        result = self._values.get("lambda_")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationOutputsLambda"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationOutputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputsKinesisFirehose",
    jsii_struct_bases=[],
    name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
)
class KinesisAnalyticsApplicationOutputsKinesisFirehose:
    def __init__(self, *, resource_arn: builtins.str, role_arn: builtins.str) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5065a497d1a4e8ff652f5cd591673691d22e8f943724ad2847248b9108207b1d)
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_arn": resource_arn,
            "role_arn": role_arn,
        }

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.'''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationOutputsKinesisFirehose(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationOutputsKinesisFirehoseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputsKinesisFirehoseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34292ea708ce29c0d653c687d64f5a2845b7605cba904c6c8934889d7034245a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceArnInput")
    def resource_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96244c5d6db565d46c0297eb690964cd35a5792abc95ed5a723f3cdeee7eb331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae2643681f064850e86a25dd1b11f6cf2938d2e729c1c96a878f97dc4bc0b10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationOutputsKinesisFirehose]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationOutputsKinesisFirehose], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationOutputsKinesisFirehose],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__794c53496a905ccd1b389222f8e4e276e5db75ec02dfd08b31f63f7ebfefe7a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputsKinesisStream",
    jsii_struct_bases=[],
    name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
)
class KinesisAnalyticsApplicationOutputsKinesisStream:
    def __init__(self, *, resource_arn: builtins.str, role_arn: builtins.str) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccd4f9787ebf44c83a9f0e88bbf6f3de7efb7767e631cf35169a2e4a7bc6d403)
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_arn": resource_arn,
            "role_arn": role_arn,
        }

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.'''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationOutputsKinesisStream(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationOutputsKinesisStreamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputsKinesisStreamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b503b69bec7992c0b04e1d07b1ad0853784c660c71d0b7c6dc0d4f7030b32c3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceArnInput")
    def resource_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cb6e336e4d457b5ad4eadf9e9aec231150da4f54de438bd105b2ad45f85be57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77ae03dfae46c1efa0e7a19ac75d44f7b9c1b73fdd57c5cba17c856d57e5fa7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationOutputsKinesisStream]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationOutputsKinesisStream], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationOutputsKinesisStream],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44f3dc213075e38aabf1e4d82f8dee7416d0490e344d0611c78245c5d59a420c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputsLambda",
    jsii_struct_bases=[],
    name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
)
class KinesisAnalyticsApplicationOutputsLambda:
    def __init__(self, *, resource_arn: builtins.str, role_arn: builtins.str) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a387476bf8040f65fac4ac2aa4fa787cab6b17c52cb9d26944b07c0ed8a34e)
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_arn": resource_arn,
            "role_arn": role_arn,
        }

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.'''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationOutputsLambda(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationOutputsLambdaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputsLambdaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b45f14588999bc3db75e42e37b2fc5f394f73e5b9df72ea52c57fe9d7e4d5e5c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceArnInput")
    def resource_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef4135f3a49bda3e1e498852fb47569d25e93c0d84c1cdd047af84a682b173ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__198f13358937ea5b90e198c7246e2ad3aaac8b68b0ca77b3ec5fc868f836e9e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationOutputsLambda]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationOutputsLambda], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationOutputsLambda],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f101ad4f30e64917ec51dec6d02e1b1da22164f97a1cc7a17b153281582173bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationOutputsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d41f1c396599e4821c3389899bc66728adc99a79b4fd6e4081790d4a2aba1faa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KinesisAnalyticsApplicationOutputsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d59917d24a6233d1b536de82d72489f3fa4c9e8683b5a5f3c682996eea446c40)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KinesisAnalyticsApplicationOutputsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb71f62742ad5e947d8f554534069945b47ddce43d88d5420e60ea05f4d162af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fca8d9e98cde31c134e7bf396b89568cea3554fd47f42fac8aff87999de12f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4b7297a3a236786d3e956d7f0a4a3b8720d00f3b030ea54c412fa4ae171035e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationOutputs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationOutputs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationOutputs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f14da5282867ad807c02431ebfa20f3246c2ef327307665a7787b53e7332b63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationOutputsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e164626bcd11d3ed2af2ce8aada338428240b3e586239ed69d5766b056b7c078)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putKinesisFirehose")
    def put_kinesis_firehose(
        self,
        *,
        resource_arn: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        value = KinesisAnalyticsApplicationOutputsKinesisFirehose(
            resource_arn=resource_arn, role_arn=role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putKinesisFirehose", [value]))

    @jsii.member(jsii_name="putKinesisStream")
    def put_kinesis_stream(
        self,
        *,
        resource_arn: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        value = KinesisAnalyticsApplicationOutputsKinesisStream(
            resource_arn=resource_arn, role_arn=role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putKinesisStream", [value]))

    @jsii.member(jsii_name="putLambda")
    def put_lambda(self, *, resource_arn: builtins.str, role_arn: builtins.str) -> None:
        '''
        :param resource_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#resource_arn KinesisAnalyticsApplication#resource_arn}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        value = KinesisAnalyticsApplicationOutputsLambda(
            resource_arn=resource_arn, role_arn=role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putLambda", [value]))

    @jsii.member(jsii_name="putSchema")
    def put_schema(self, *, record_format_type: builtins.str) -> None:
        '''
        :param record_format_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_format_type KinesisAnalyticsApplication#record_format_type}.
        '''
        value = KinesisAnalyticsApplicationOutputsSchema(
            record_format_type=record_format_type
        )

        return typing.cast(None, jsii.invoke(self, "putSchema", [value]))

    @jsii.member(jsii_name="resetKinesisFirehose")
    def reset_kinesis_firehose(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisFirehose", []))

    @jsii.member(jsii_name="resetKinesisStream")
    def reset_kinesis_stream(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisStream", []))

    @jsii.member(jsii_name="resetLambda")
    def reset_lambda(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambda", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehose")
    def kinesis_firehose(
        self,
    ) -> KinesisAnalyticsApplicationOutputsKinesisFirehoseOutputReference:
        return typing.cast(KinesisAnalyticsApplicationOutputsKinesisFirehoseOutputReference, jsii.get(self, "kinesisFirehose"))

    @builtins.property
    @jsii.member(jsii_name="kinesisStream")
    def kinesis_stream(
        self,
    ) -> KinesisAnalyticsApplicationOutputsKinesisStreamOutputReference:
        return typing.cast(KinesisAnalyticsApplicationOutputsKinesisStreamOutputReference, jsii.get(self, "kinesisStream"))

    @builtins.property
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> KinesisAnalyticsApplicationOutputsLambdaOutputReference:
        return typing.cast(KinesisAnalyticsApplicationOutputsLambdaOutputReference, jsii.get(self, "lambda"))

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> "KinesisAnalyticsApplicationOutputsSchemaOutputReference":
        return typing.cast("KinesisAnalyticsApplicationOutputsSchemaOutputReference", jsii.get(self, "schema"))

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehoseInput")
    def kinesis_firehose_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationOutputsKinesisFirehose]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationOutputsKinesisFirehose], jsii.get(self, "kinesisFirehoseInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisStreamInput")
    def kinesis_stream_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationOutputsKinesisStream]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationOutputsKinesisStream], jsii.get(self, "kinesisStreamInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaInput")
    def lambda_input(self) -> typing.Optional[KinesisAnalyticsApplicationOutputsLambda]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationOutputsLambda], jsii.get(self, "lambdaInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationOutputsSchema"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationOutputsSchema"], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb032311ddb9a50d49b638b565aee80c4585ff0e276c14f2ac8865b117946619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationOutputs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationOutputs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationOutputs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__742ea58156076eb34211e94f4a14b780b27915bb975de298d8e12279333ce3e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputsSchema",
    jsii_struct_bases=[],
    name_mapping={"record_format_type": "recordFormatType"},
)
class KinesisAnalyticsApplicationOutputsSchema:
    def __init__(self, *, record_format_type: builtins.str) -> None:
        '''
        :param record_format_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_format_type KinesisAnalyticsApplication#record_format_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7653f0342a442179cac7a623da67048718bbc86e06ff2059ab43d09d20406f33)
            check_type(argname="argument record_format_type", value=record_format_type, expected_type=type_hints["record_format_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "record_format_type": record_format_type,
        }

    @builtins.property
    def record_format_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_format_type KinesisAnalyticsApplication#record_format_type}.'''
        result = self._values.get("record_format_type")
        assert result is not None, "Required property 'record_format_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationOutputsSchema(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationOutputsSchemaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationOutputsSchemaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd7d85bf1360e64fba2ce5c21138ea593168e29e720406c3a35be1dbe0e3b0bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="recordFormatTypeInput")
    def record_format_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordFormatTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="recordFormatType")
    def record_format_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordFormatType"))

    @record_format_type.setter
    def record_format_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d9f64a01e12291406cd18b4f6226ff7bb67a90dbd250575e94d1e3fc398cd07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordFormatType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationOutputsSchema]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationOutputsSchema], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationOutputsSchema],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e678d315bb1aeda8c3d860ab92eb172ebd3b691b03a7a3abe33a9c7aef24b36b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSources",
    jsii_struct_bases=[],
    name_mapping={"s3": "s3", "schema": "schema", "table_name": "tableName"},
)
class KinesisAnalyticsApplicationReferenceDataSources:
    def __init__(
        self,
        *,
        s3: typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesS3", typing.Dict[builtins.str, typing.Any]],
        schema: typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchema", typing.Dict[builtins.str, typing.Any]],
        table_name: builtins.str,
    ) -> None:
        '''
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#s3 KinesisAnalyticsApplication#s3}
        :param schema: schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#schema KinesisAnalyticsApplication#schema}
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#table_name KinesisAnalyticsApplication#table_name}.
        '''
        if isinstance(s3, dict):
            s3 = KinesisAnalyticsApplicationReferenceDataSourcesS3(**s3)
        if isinstance(schema, dict):
            schema = KinesisAnalyticsApplicationReferenceDataSourcesSchema(**schema)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba22701dfa4a88fc5e332a3d536ac6187e970ab88e1fdcb835ece49983c36b29)
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3": s3,
            "schema": schema,
            "table_name": table_name,
        }

    @builtins.property
    def s3(self) -> "KinesisAnalyticsApplicationReferenceDataSourcesS3":
        '''s3 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#s3 KinesisAnalyticsApplication#s3}
        '''
        result = self._values.get("s3")
        assert result is not None, "Required property 's3' is missing"
        return typing.cast("KinesisAnalyticsApplicationReferenceDataSourcesS3", result)

    @builtins.property
    def schema(self) -> "KinesisAnalyticsApplicationReferenceDataSourcesSchema":
        '''schema block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#schema KinesisAnalyticsApplication#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast("KinesisAnalyticsApplicationReferenceDataSourcesSchema", result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#table_name KinesisAnalyticsApplication#table_name}.'''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationReferenceDataSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationReferenceDataSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bed9a629a44c0b4cfc28381a246bfcbda0608dc1430de7eb0103a66483f593d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putS3")
    def put_s3(
        self,
        *,
        bucket_arn: builtins.str,
        file_key: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''
        :param bucket_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#bucket_arn KinesisAnalyticsApplication#bucket_arn}.
        :param file_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#file_key KinesisAnalyticsApplication#file_key}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        value = KinesisAnalyticsApplicationReferenceDataSourcesS3(
            bucket_arn=bucket_arn, file_key=file_key, role_arn=role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="putSchema")
    def put_schema(
        self,
        *,
        record_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns", typing.Dict[builtins.str, typing.Any]]]],
        record_format: typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat", typing.Dict[builtins.str, typing.Any]],
        record_encoding: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param record_columns: record_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_columns KinesisAnalyticsApplication#record_columns}
        :param record_format: record_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_format KinesisAnalyticsApplication#record_format}
        :param record_encoding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_encoding KinesisAnalyticsApplication#record_encoding}.
        '''
        value = KinesisAnalyticsApplicationReferenceDataSourcesSchema(
            record_columns=record_columns,
            record_format=record_format,
            record_encoding=record_encoding,
        )

        return typing.cast(None, jsii.invoke(self, "putSchema", [value]))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(self) -> "KinesisAnalyticsApplicationReferenceDataSourcesS3OutputReference":
        return typing.cast("KinesisAnalyticsApplicationReferenceDataSourcesS3OutputReference", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(
        self,
    ) -> "KinesisAnalyticsApplicationReferenceDataSourcesSchemaOutputReference":
        return typing.cast("KinesisAnalyticsApplicationReferenceDataSourcesSchemaOutputReference", jsii.get(self, "schema"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesS3"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesS3"], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesSchema"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesSchema"], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b2021bce9bea076d6347c493cbadad285d3efaf5dae6512e579afb7e100563)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationReferenceDataSources]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationReferenceDataSources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d67038e966debe90d6d4ce3527a5da8c9750cb1a31040d9f6b665e1f0c80dfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesS3",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_arn": "bucketArn",
        "file_key": "fileKey",
        "role_arn": "roleArn",
    },
)
class KinesisAnalyticsApplicationReferenceDataSourcesS3:
    def __init__(
        self,
        *,
        bucket_arn: builtins.str,
        file_key: builtins.str,
        role_arn: builtins.str,
    ) -> None:
        '''
        :param bucket_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#bucket_arn KinesisAnalyticsApplication#bucket_arn}.
        :param file_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#file_key KinesisAnalyticsApplication#file_key}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab80fa31f6545ed31a5779bcc8098a8f85d88cb41fa874f7704c638e22317905)
            check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
            check_type(argname="argument file_key", value=file_key, expected_type=type_hints["file_key"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_arn": bucket_arn,
            "file_key": file_key,
            "role_arn": role_arn,
        }

    @builtins.property
    def bucket_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#bucket_arn KinesisAnalyticsApplication#bucket_arn}.'''
        result = self._values.get("bucket_arn")
        assert result is not None, "Required property 'bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def file_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#file_key KinesisAnalyticsApplication#file_key}.'''
        result = self._values.get("file_key")
        assert result is not None, "Required property 'file_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#role_arn KinesisAnalyticsApplication#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationReferenceDataSourcesS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationReferenceDataSourcesS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesS3OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20595936ed52d5ae6a35bcc693732fe6a2c5e653eb0a4af6a4568849ad4cbe6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="bucketArnInput")
    def bucket_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketArnInput"))

    @builtins.property
    @jsii.member(jsii_name="fileKeyInput")
    def file_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketArn"))

    @bucket_arn.setter
    def bucket_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0ea81a855de48957f78ab4978bb1b88cfaa4297405247949098a5e63cd5e983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileKey")
    def file_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileKey"))

    @file_key.setter
    def file_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cce0fec8733c79f418001a809f7c97102d1f3c75add97901c222a94b45b2c141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2ff39baa6aa52744a7e8e003c84e42717b3569a5e6cc842e097f0afb49042b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesS3]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesS3], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesS3],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08067263089544f65c3cc4612dfd78722fb6971c9a0f41714addc4abdbbd6556)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchema",
    jsii_struct_bases=[],
    name_mapping={
        "record_columns": "recordColumns",
        "record_format": "recordFormat",
        "record_encoding": "recordEncoding",
    },
)
class KinesisAnalyticsApplicationReferenceDataSourcesSchema:
    def __init__(
        self,
        *,
        record_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns", typing.Dict[builtins.str, typing.Any]]]],
        record_format: typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat", typing.Dict[builtins.str, typing.Any]],
        record_encoding: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param record_columns: record_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_columns KinesisAnalyticsApplication#record_columns}
        :param record_format: record_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_format KinesisAnalyticsApplication#record_format}
        :param record_encoding: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_encoding KinesisAnalyticsApplication#record_encoding}.
        '''
        if isinstance(record_format, dict):
            record_format = KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat(**record_format)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7905ac13f49b1bc342b2aa6cdfea10e0c9d1680eb1b0f0576713ac17a2a20b37)
            check_type(argname="argument record_columns", value=record_columns, expected_type=type_hints["record_columns"])
            check_type(argname="argument record_format", value=record_format, expected_type=type_hints["record_format"])
            check_type(argname="argument record_encoding", value=record_encoding, expected_type=type_hints["record_encoding"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "record_columns": record_columns,
            "record_format": record_format,
        }
        if record_encoding is not None:
            self._values["record_encoding"] = record_encoding

    @builtins.property
    def record_columns(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns"]]:
        '''record_columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_columns KinesisAnalyticsApplication#record_columns}
        '''
        result = self._values.get("record_columns")
        assert result is not None, "Required property 'record_columns' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns"]], result)

    @builtins.property
    def record_format(
        self,
    ) -> "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat":
        '''record_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_format KinesisAnalyticsApplication#record_format}
        '''
        result = self._values.get("record_format")
        assert result is not None, "Required property 'record_format' is missing"
        return typing.cast("KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat", result)

    @builtins.property
    def record_encoding(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_encoding KinesisAnalyticsApplication#record_encoding}.'''
        result = self._values.get("record_encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationReferenceDataSourcesSchema(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationReferenceDataSourcesSchemaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a84b36110d98e2e3cfd096fff4339d1ed0ffbe21d839b25d25e992ef71c30be1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRecordColumns")
    def put_record_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3211207ffc71487a5e07f5fedafe8fdfefcf22b97045ddc7d0065d2c0c2b8291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRecordColumns", [value]))

    @jsii.member(jsii_name="putRecordFormat")
    def put_record_format(
        self,
        *,
        mapping_parameters: typing.Optional[typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param mapping_parameters: mapping_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#mapping_parameters KinesisAnalyticsApplication#mapping_parameters}
        '''
        value = KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat(
            mapping_parameters=mapping_parameters
        )

        return typing.cast(None, jsii.invoke(self, "putRecordFormat", [value]))

    @jsii.member(jsii_name="resetRecordEncoding")
    def reset_record_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordEncoding", []))

    @builtins.property
    @jsii.member(jsii_name="recordColumns")
    def record_columns(
        self,
    ) -> "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumnsList":
        return typing.cast("KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumnsList", jsii.get(self, "recordColumns"))

    @builtins.property
    @jsii.member(jsii_name="recordFormat")
    def record_format(
        self,
    ) -> "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatOutputReference":
        return typing.cast("KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatOutputReference", jsii.get(self, "recordFormat"))

    @builtins.property
    @jsii.member(jsii_name="recordColumnsInput")
    def record_columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns"]]], jsii.get(self, "recordColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="recordEncodingInput")
    def record_encoding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordEncodingInput"))

    @builtins.property
    @jsii.member(jsii_name="recordFormatInput")
    def record_format_input(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat"]:
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat"], jsii.get(self, "recordFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="recordEncoding")
    def record_encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordEncoding"))

    @record_encoding.setter
    def record_encoding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a98291f86eb7253efa98518f51f2dd664549acd6a2350a34400b7aa5ec62e97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordEncoding", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchema]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchema], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchema],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579e5a498e578b34d3783cf6f3be6f5b64a27b36f27753bfdc21afdf8a47a76e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "sql_type": "sqlType", "mapping": "mapping"},
)
class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns:
    def __init__(
        self,
        *,
        name: builtins.str,
        sql_type: builtins.str,
        mapping: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#name KinesisAnalyticsApplication#name}.
        :param sql_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#sql_type KinesisAnalyticsApplication#sql_type}.
        :param mapping: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#mapping KinesisAnalyticsApplication#mapping}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__121ccd1ec2409992dc944e9e7c88e47d7c4336b7e27e29c5676b4a1093579c41)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sql_type", value=sql_type, expected_type=type_hints["sql_type"])
            check_type(argname="argument mapping", value=mapping, expected_type=type_hints["mapping"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "sql_type": sql_type,
        }
        if mapping is not None:
            self._values["mapping"] = mapping

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#name KinesisAnalyticsApplication#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#sql_type KinesisAnalyticsApplication#sql_type}.'''
        result = self._values.get("sql_type")
        assert result is not None, "Required property 'sql_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mapping(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#mapping KinesisAnalyticsApplication#mapping}.'''
        result = self._values.get("mapping")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9d83c2ee312b072ba0cd1dd87c894e714de810c43af38fe13a4baf9ea6096aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c43c00fba0ae5ec76d63c84a37917c2d487b83b6ddd223f8f0e120c77dd506ce)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dc25df1f752600d1cb89ec033411f43bbc740a7bab5d1a7211a44d775601cb3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64ff2ff64c24e42d80f7dc4f35ac92fc46a429f606c55ba171bc6a3ae08d4e70)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d3d776a44241ee2b3b79cda4cb4bac0233721c1baa0af09f182abc11ae87e3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cb126965b5616847160ed9aee09e328f83b42f726343c204d2890b51de9b137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e48cfb64fd3af5e72e377b4ae334f290402a8002ea2a8a43aa043b3172c4f3a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMapping")
    def reset_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMapping", []))

    @builtins.property
    @jsii.member(jsii_name="mappingInput")
    def mapping_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mappingInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlTypeInput")
    def sql_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="mapping")
    def mapping(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mapping"))

    @mapping.setter
    def mapping(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e509e396e1f4b9bf1103283d636a508f3c06796e3cceeb49cdd84f03f7015474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcf8f76504e7291e08c4b9038266c409f8fdbe49b34d63cef4f6ac9dcae933b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlType")
    def sql_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlType"))

    @sql_type.setter
    def sql_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ba671abc81c25b39fe1ecaa81ad0924cdf5e4276d7e6aaa51a4b7687acf37e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd0473bad0ad6e6ed5de5dcfb9a874a8316999191e9c3efffceb5ca6a512915d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat",
    jsii_struct_bases=[],
    name_mapping={"mapping_parameters": "mappingParameters"},
)
class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat:
    def __init__(
        self,
        *,
        mapping_parameters: typing.Optional[typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param mapping_parameters: mapping_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#mapping_parameters KinesisAnalyticsApplication#mapping_parameters}
        '''
        if isinstance(mapping_parameters, dict):
            mapping_parameters = KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters(**mapping_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5540765f592b2217e18b1707f46fb9c808973c4e8c9d7afd8573b685e31dd537)
            check_type(argname="argument mapping_parameters", value=mapping_parameters, expected_type=type_hints["mapping_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mapping_parameters is not None:
            self._values["mapping_parameters"] = mapping_parameters

    @builtins.property
    def mapping_parameters(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters"]:
        '''mapping_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#mapping_parameters KinesisAnalyticsApplication#mapping_parameters}
        '''
        result = self._values.get("mapping_parameters")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters",
    jsii_struct_bases=[],
    name_mapping={"csv": "csv", "json": "json"},
)
class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters:
    def __init__(
        self,
        *,
        csv: typing.Optional[typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv", typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param csv: csv block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#csv KinesisAnalyticsApplication#csv}
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#json KinesisAnalyticsApplication#json}
        '''
        if isinstance(csv, dict):
            csv = KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv(**csv)
        if isinstance(json, dict):
            json = KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson(**json)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8444a8243e27ede7eef400879e997a36d66049ba5c570d7eefa9dad6f243c072)
            check_type(argname="argument csv", value=csv, expected_type=type_hints["csv"])
            check_type(argname="argument json", value=json, expected_type=type_hints["json"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if csv is not None:
            self._values["csv"] = csv
        if json is not None:
            self._values["json"] = json

    @builtins.property
    def csv(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv"]:
        '''csv block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#csv KinesisAnalyticsApplication#csv}
        '''
        result = self._values.get("csv")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv"], result)

    @builtins.property
    def json(
        self,
    ) -> typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson"]:
        '''json block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#json KinesisAnalyticsApplication#json}
        '''
        result = self._values.get("json")
        return typing.cast(typing.Optional["KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv",
    jsii_struct_bases=[],
    name_mapping={
        "record_column_delimiter": "recordColumnDelimiter",
        "record_row_delimiter": "recordRowDelimiter",
    },
)
class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv:
    def __init__(
        self,
        *,
        record_column_delimiter: builtins.str,
        record_row_delimiter: builtins.str,
    ) -> None:
        '''
        :param record_column_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_column_delimiter KinesisAnalyticsApplication#record_column_delimiter}.
        :param record_row_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_row_delimiter KinesisAnalyticsApplication#record_row_delimiter}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a22872b10675fb7ee4941b0f3ae97838782a8e9c61f785bb8c4810c8be6f358)
            check_type(argname="argument record_column_delimiter", value=record_column_delimiter, expected_type=type_hints["record_column_delimiter"])
            check_type(argname="argument record_row_delimiter", value=record_row_delimiter, expected_type=type_hints["record_row_delimiter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "record_column_delimiter": record_column_delimiter,
            "record_row_delimiter": record_row_delimiter,
        }

    @builtins.property
    def record_column_delimiter(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_column_delimiter KinesisAnalyticsApplication#record_column_delimiter}.'''
        result = self._values.get("record_column_delimiter")
        assert result is not None, "Required property 'record_column_delimiter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def record_row_delimiter(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_row_delimiter KinesisAnalyticsApplication#record_row_delimiter}.'''
        result = self._values.get("record_row_delimiter")
        assert result is not None, "Required property 'record_row_delimiter' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67922398973343711acb4d3e33cad4dd4255f206cad45b51f302718a2b54424b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="recordColumnDelimiterInput")
    def record_column_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordColumnDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="recordRowDelimiterInput")
    def record_row_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordRowDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="recordColumnDelimiter")
    def record_column_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordColumnDelimiter"))

    @record_column_delimiter.setter
    def record_column_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce0ec4ec29b2707f386b4c97fa6b1c790caea275b628aef15093b0b3533bda39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordColumnDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recordRowDelimiter")
    def record_row_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordRowDelimiter"))

    @record_row_delimiter.setter
    def record_row_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bafd84fdbf7231e0b8d31c05b476a7545e830a1f90c8abe732660eee2bb17cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordRowDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c878d5191f9a3f0862649ee8f541bb20d3bcf6366fed61adc496ec59cb5c338)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson",
    jsii_struct_bases=[],
    name_mapping={"record_row_path": "recordRowPath"},
)
class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson:
    def __init__(self, *, record_row_path: builtins.str) -> None:
        '''
        :param record_row_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_row_path KinesisAnalyticsApplication#record_row_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0acc579b60ae28abbc7780f849135bab781b340f9494722055485fe7d987928)
            check_type(argname="argument record_row_path", value=record_row_path, expected_type=type_hints["record_row_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "record_row_path": record_row_path,
        }

    @builtins.property
    def record_row_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_row_path KinesisAnalyticsApplication#record_row_path}.'''
        result = self._values.get("record_row_path")
        assert result is not None, "Required property 'record_row_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJsonOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJsonOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__068fc337a8f9ca95c7ba585ad25df7e60bf41ffbaf80889a3556ea61711a0b85)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="recordRowPathInput")
    def record_row_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordRowPathInput"))

    @builtins.property
    @jsii.member(jsii_name="recordRowPath")
    def record_row_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordRowPath"))

    @record_row_path.setter
    def record_row_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__555d070756b8092794be56d2a3d3e8000b2bed83b4e13c710e56ba36349b1458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordRowPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff1b2734072697d2be5b46407011b5d9b62ef38669b0c5c569eb1f1316221e94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d36ae86db53165003c47f55d54464306839775464d49a00c2109557402cae29f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCsv")
    def put_csv(
        self,
        *,
        record_column_delimiter: builtins.str,
        record_row_delimiter: builtins.str,
    ) -> None:
        '''
        :param record_column_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_column_delimiter KinesisAnalyticsApplication#record_column_delimiter}.
        :param record_row_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_row_delimiter KinesisAnalyticsApplication#record_row_delimiter}.
        '''
        value = KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv(
            record_column_delimiter=record_column_delimiter,
            record_row_delimiter=record_row_delimiter,
        )

        return typing.cast(None, jsii.invoke(self, "putCsv", [value]))

    @jsii.member(jsii_name="putJson")
    def put_json(self, *, record_row_path: builtins.str) -> None:
        '''
        :param record_row_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#record_row_path KinesisAnalyticsApplication#record_row_path}.
        '''
        value = KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson(
            record_row_path=record_row_path
        )

        return typing.cast(None, jsii.invoke(self, "putJson", [value]))

    @jsii.member(jsii_name="resetCsv")
    def reset_csv(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCsv", []))

    @jsii.member(jsii_name="resetJson")
    def reset_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJson", []))

    @builtins.property
    @jsii.member(jsii_name="csv")
    def csv(
        self,
    ) -> KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsvOutputReference:
        return typing.cast(KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsvOutputReference, jsii.get(self, "csv"))

    @builtins.property
    @jsii.member(jsii_name="json")
    def json(
        self,
    ) -> KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJsonOutputReference:
        return typing.cast(KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJsonOutputReference, jsii.get(self, "json"))

    @builtins.property
    @jsii.member(jsii_name="csvInput")
    def csv_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv], jsii.get(self, "csvInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonInput")
    def json_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson], jsii.get(self, "jsonInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cfb542c7ec7e7ef67a4204cf36595eb5e6f1f55cb5cd100d3fbbb56bf37447e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.kinesisAnalyticsApplication.KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9a92b39404a49e6e3ea444a4956039c713628a5adfba70655351fb4ca312d10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMappingParameters")
    def put_mapping_parameters(
        self,
        *,
        csv: typing.Optional[typing.Union[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv, typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param csv: csv block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#csv KinesisAnalyticsApplication#csv}
        :param json: json block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/kinesis_analytics_application#json KinesisAnalyticsApplication#json}
        '''
        value = KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters(
            csv=csv, json=json
        )

        return typing.cast(None, jsii.invoke(self, "putMappingParameters", [value]))

    @jsii.member(jsii_name="resetMappingParameters")
    def reset_mapping_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMappingParameters", []))

    @builtins.property
    @jsii.member(jsii_name="mappingParameters")
    def mapping_parameters(
        self,
    ) -> KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersOutputReference:
        return typing.cast(KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersOutputReference, jsii.get(self, "mappingParameters"))

    @builtins.property
    @jsii.member(jsii_name="recordFormatType")
    def record_format_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordFormatType"))

    @builtins.property
    @jsii.member(jsii_name="mappingParametersInput")
    def mapping_parameters_input(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters], jsii.get(self, "mappingParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat]:
        return typing.cast(typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__006bb9ef276cc71b965f07ca072448dc295ea08a72b79b614afd65212e9661f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "KinesisAnalyticsApplication",
    "KinesisAnalyticsApplicationCloudwatchLoggingOptions",
    "KinesisAnalyticsApplicationCloudwatchLoggingOptionsOutputReference",
    "KinesisAnalyticsApplicationConfig",
    "KinesisAnalyticsApplicationInputs",
    "KinesisAnalyticsApplicationInputsKinesisFirehose",
    "KinesisAnalyticsApplicationInputsKinesisFirehoseOutputReference",
    "KinesisAnalyticsApplicationInputsKinesisStream",
    "KinesisAnalyticsApplicationInputsKinesisStreamOutputReference",
    "KinesisAnalyticsApplicationInputsOutputReference",
    "KinesisAnalyticsApplicationInputsParallelism",
    "KinesisAnalyticsApplicationInputsParallelismOutputReference",
    "KinesisAnalyticsApplicationInputsProcessingConfiguration",
    "KinesisAnalyticsApplicationInputsProcessingConfigurationLambda",
    "KinesisAnalyticsApplicationInputsProcessingConfigurationLambdaOutputReference",
    "KinesisAnalyticsApplicationInputsProcessingConfigurationOutputReference",
    "KinesisAnalyticsApplicationInputsSchema",
    "KinesisAnalyticsApplicationInputsSchemaOutputReference",
    "KinesisAnalyticsApplicationInputsSchemaRecordColumns",
    "KinesisAnalyticsApplicationInputsSchemaRecordColumnsList",
    "KinesisAnalyticsApplicationInputsSchemaRecordColumnsOutputReference",
    "KinesisAnalyticsApplicationInputsSchemaRecordFormat",
    "KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters",
    "KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv",
    "KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsvOutputReference",
    "KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson",
    "KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJsonOutputReference",
    "KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersOutputReference",
    "KinesisAnalyticsApplicationInputsSchemaRecordFormatOutputReference",
    "KinesisAnalyticsApplicationInputsStartingPositionConfiguration",
    "KinesisAnalyticsApplicationInputsStartingPositionConfigurationList",
    "KinesisAnalyticsApplicationInputsStartingPositionConfigurationOutputReference",
    "KinesisAnalyticsApplicationOutputs",
    "KinesisAnalyticsApplicationOutputsKinesisFirehose",
    "KinesisAnalyticsApplicationOutputsKinesisFirehoseOutputReference",
    "KinesisAnalyticsApplicationOutputsKinesisStream",
    "KinesisAnalyticsApplicationOutputsKinesisStreamOutputReference",
    "KinesisAnalyticsApplicationOutputsLambda",
    "KinesisAnalyticsApplicationOutputsLambdaOutputReference",
    "KinesisAnalyticsApplicationOutputsList",
    "KinesisAnalyticsApplicationOutputsOutputReference",
    "KinesisAnalyticsApplicationOutputsSchema",
    "KinesisAnalyticsApplicationOutputsSchemaOutputReference",
    "KinesisAnalyticsApplicationReferenceDataSources",
    "KinesisAnalyticsApplicationReferenceDataSourcesOutputReference",
    "KinesisAnalyticsApplicationReferenceDataSourcesS3",
    "KinesisAnalyticsApplicationReferenceDataSourcesS3OutputReference",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchema",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaOutputReference",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumnsList",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumnsOutputReference",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsvOutputReference",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJsonOutputReference",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersOutputReference",
    "KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatOutputReference",
]

publication.publish()

def _typecheckingstub__dbdb1b7e2478c60d662f69643f3a17c3257094d8bffa0da9bda03347edf70ace(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    cloudwatch_logging_options: typing.Optional[typing.Union[KinesisAnalyticsApplicationCloudwatchLoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    code: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    inputs: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputs, typing.Dict[builtins.str, typing.Any]]] = None,
    outputs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisAnalyticsApplicationOutputs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    reference_data_sources: typing.Optional[typing.Union[KinesisAnalyticsApplicationReferenceDataSources, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    start_application: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__fab4b856a6f82fc332c765a13902780abc0c52c5bb73ca88cec73b3a2b664226(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1be5781422e93b2c175aaeda9f040d4e2acb6dfe0551b567f03162776dffded1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisAnalyticsApplicationOutputs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1e1fa66af70c1f7998b2f4cdb594267718ccb0ad367779af80406d3a12f844(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e7b334a486fd8137c5259d2e22b1da2659d8acbaa4db0177c53e0824a85a7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a30c5cd63f854eec0ed8454a3a0f9b5b184a694b8c07d7c6cf218aa932eb7e93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd8703faa968668acfb77f460fb653bc0d9e4e5224861e53ac84c1034504fd3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10de9e6613cd88d53df5e7badcbb219d7bcfac10d8613f7428a6f56fb67e9820(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063947a72049b6797791e2036c6fdcf2bf108e4a7c77badedb8d9ea21a64b3a2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8739f8f7b66eeb0ba29fa1ea39103ddd293ad86b6d75ed9f22a690a1b4fcd210(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c3363f93296933a7586030fc4d3e0ae4d66b5247371d77b3bd5db7e327a8d0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1540e53f75e14617d6d7828c6593f1e1e3955e4fe4e9a0338657d3421dc25b0a(
    *,
    log_stream_arn: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b412611f6d9013805a2e566bdb470a0ea066a8d1ca8dc8d94cc106ec3bb4df3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8107c97a70cc0f2f924e183cb42b6f5fd2c999cc6a009c52f425eb7ca8cf9b23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__012a51ffcadb90c90c0226134d0f9b39e6fc2707dc724fe4e294725ce2bdd48c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b0c53a0fe6ee1d1e58c69da422a688d4c0c0cc76a2fac8e151fd0661a78de1(
    value: typing.Optional[KinesisAnalyticsApplicationCloudwatchLoggingOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931bda2648b78d9a02bdef76842dab3da4a2417fb1dd145f3eb89994cf51c71f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    cloudwatch_logging_options: typing.Optional[typing.Union[KinesisAnalyticsApplicationCloudwatchLoggingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    code: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    inputs: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputs, typing.Dict[builtins.str, typing.Any]]] = None,
    outputs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisAnalyticsApplicationOutputs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    reference_data_sources: typing.Optional[typing.Union[KinesisAnalyticsApplicationReferenceDataSources, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    start_application: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde1abd339ba55bf1233682e2a0283b7eb389e89728cfca9196a3cfafdc0414b(
    *,
    name_prefix: builtins.str,
    schema: typing.Union[KinesisAnalyticsApplicationInputsSchema, typing.Dict[builtins.str, typing.Any]],
    kinesis_firehose: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputsKinesisFirehose, typing.Dict[builtins.str, typing.Any]]] = None,
    kinesis_stream: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputsKinesisStream, typing.Dict[builtins.str, typing.Any]]] = None,
    parallelism: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputsParallelism, typing.Dict[builtins.str, typing.Any]]] = None,
    processing_configuration: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputsProcessingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    starting_position_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisAnalyticsApplicationInputsStartingPositionConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7819fb5fd8059ec21ad1ed680b94770ef0f8409d783db57c0fd5413204b7356(
    *,
    resource_arn: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3491500e5a4d609a03d4675b3b49f76be34884bafc5823054b85fdc1221a3379(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1495896b7d329a06e2421c8f4c801b54293295832f56ad63c7adbd4fe63764e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d40b436c5d393728eeb7b8181e5f0faeec9209adc1ca807ad5aadcf2c906b7e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0a70ccfa1f986d7cb81cbebb42cdd5ac6fdcb98e175679c3bc0f0dc1ec28b2c(
    value: typing.Optional[KinesisAnalyticsApplicationInputsKinesisFirehose],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e8ad6d943ed98b0b8d12c218b17f870f42fd88c4d3d8a086120738cd585f8e(
    *,
    resource_arn: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d2b31dd1c46b04fe48fd7d595f6639f18e2d03fbfa96118f5eb06ec5fc6c1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b73ccc2e23fdbf39345acf3d1d41edf67e935e7a1cb96dce7132a31cb395d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090c1ab904e975fe37ad89e976268002913a4bde82bd4a29417fc317ea7d5aff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3edc2300045359833081f70241b395cd2b0aa861963e03832934a142143fddf(
    value: typing.Optional[KinesisAnalyticsApplicationInputsKinesisStream],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c734a8bc289e34de41535f73f60d1a91c2254476bea1ac1921f8ec4ca835f14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3946a227bc6a62f7635bf0fc85268eb8286021c03d4a5e6af778c815e7b67358(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisAnalyticsApplicationInputsStartingPositionConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5220559efda3195ac7f0179b6b2ccb65fd09b8a5f75750971ecad592211f78d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b7396a80b57f0f46ae32dd90c6fe8268123d31e9a3e83b0e05728050c004b5(
    value: typing.Optional[KinesisAnalyticsApplicationInputs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7b8e9eed392ec1dc04274b7a9a4adc1677e6dd394d159e147e52863922a999(
    *,
    count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a05341a852420a7240b42387a827584c03ebadebde4f2962b447c897d86753f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0ecb683194f336b31f813ef3dea96f1a7e4807bb8d236f1d6256888343c03d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b60b3e845a44af2f6d376915a3c84ddf56db0c7c6830091c95527541e24dc78(
    value: typing.Optional[KinesisAnalyticsApplicationInputsParallelism],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18c52514cdb475231476cdaaa14324c5e58af60a779e4ee461a62970e6046e8(
    *,
    lambda_: typing.Union[KinesisAnalyticsApplicationInputsProcessingConfigurationLambda, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7025c59c4202678ddf8dd83e9edc02a161cbbdcbafc554fafc199bb4463636db(
    *,
    resource_arn: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72774c14797b1d145c76f4006ce20200aaa83ab3e86d38d543b5be580fbac6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d848075ced3494bd5998512e9006c9509f24032389b5e9c397bb910570dd1c20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b5ca407cd5f1d1b00f615fc51c0086010567a4975844b2a9126cd37ceb9f641(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae2bb24803d2b7c18a3fccb4e16db97790fdc63686c10a77c9afdd4bc8049e06(
    value: typing.Optional[KinesisAnalyticsApplicationInputsProcessingConfigurationLambda],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__709af94d710161f14a9cbc43bcde0c650113f6395dcfde0f837ec1fffab5cd0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63709ccd4cb0751aa186496fa0e99abd4203e5b23239024c7b499a767fe3319a(
    value: typing.Optional[KinesisAnalyticsApplicationInputsProcessingConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87244b11c978eeb268799a3fd67046ee1187260bb09f1ae945e2f0f8fc63ba7(
    *,
    record_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisAnalyticsApplicationInputsSchemaRecordColumns, typing.Dict[builtins.str, typing.Any]]]],
    record_format: typing.Union[KinesisAnalyticsApplicationInputsSchemaRecordFormat, typing.Dict[builtins.str, typing.Any]],
    record_encoding: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd0ee4541409b2cf1f06f965e73fc4703aae15366f13f8508e7692f902720514(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9499a5486a0c08584971116455d8edc35b4c9e0ee54b01ba12961e40541cce9c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisAnalyticsApplicationInputsSchemaRecordColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c00e7f0ff22f47080de3df6dad26d5f5d6c14a13686d9a01ccc065cc92eab26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc4455e3d8ad4dcc172e31fbeeb51ff0cf97fed2a07b0d83ce75789255ee5e41(
    value: typing.Optional[KinesisAnalyticsApplicationInputsSchema],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__481bd60e5115ee2d4ca7eb078dc302089cd4f540fbd576a04808b468124f94b9(
    *,
    name: builtins.str,
    sql_type: builtins.str,
    mapping: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fdac2d92d031b86e1a88f0f7dfd37db3ee74c813f4a5a12e825d2ac3ced56eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ee5cba8689aa2a64fd88ae914e80559f9f5cbd162464fc720d83d1777c5165(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea507df7de594266163cb2fd65767ac9ee8c387b6b0dd6bb1b59cd6448dccad0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3de93b2494694533ccda520f2609510f8238b0af86afdbadd29b4448b30b9a1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5087dee46ebe4079f65c07e191f76996df4a9a814d693058ec447e6eb3fa5f63(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d390ece4489dd506f59bb7c24ffabae29d23f2b777022bfe52db6cb3289f2b93(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationInputsSchemaRecordColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d1a14102f2ef6174248051dfaa666e10d02368f4b729d33f7e4c4c1056d1fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43fda08803ce4e18c1fea131a588c075806d23174de41cc7a232b0242cdf010f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ec347aaaaf8718e598cd21d5a6921cc5f9bfa6b9bc7dfbf1a8d3d5056e1a1c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c92cc0247dfd346183579b3f8e8652328530d6c729ed33dcf8571dd9e583abdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a037241e657827f22605abd54f504401a044cef31eb41b967c1aae6cf7cea4db(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationInputsSchemaRecordColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab9feaea829f61d3702588c146def24425db261211a396d39a8541ebc147bb23(
    *,
    mapping_parameters: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b6737a7f654935b1cfac04e66eab1309e3ad4bb3f2a1fc5b4ad6ea2975ff34(
    *,
    csv: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv, typing.Dict[builtins.str, typing.Any]]] = None,
    json: typing.Optional[typing.Union[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ea85e4d02873b6a51d3d2a20dcca4401dd6db0115ba795304a338a9cd33bf4e(
    *,
    record_column_delimiter: builtins.str,
    record_row_delimiter: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f30a6188df4871030dd0bbcab63414d330ea393a34b7bb735150b0299fff1c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__324c80d0414062cebb98fa0f6ff00833401eca781d8b20113287155a19110b99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7a65c84d4ac6a4ba9a5348db25b7acb608c954afe6b4190612dacde5ed243aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4c9bd9f65d91fdf57b8cce671badaf7b0fba481a7daaae13631542fc0492524(
    value: typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersCsv],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d7277237dd8b7d2c79dcb8e8bbafa0d6d7f2b8c19c7675b79f96af08d48aed(
    *,
    record_row_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82eb73527c6a3e0b59c1b2c2987769dc7c9a572e504775286b0e022d14fceb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e3d45960b66d4d45b0ed2c140f4d9d31687123a8d25f14dc66bba453d8b3698(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab3eb8d8648771fa5b78c1b1db6e8beb684cba214375d3cb70e331efada1213e(
    value: typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParametersJson],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ebbefca202267f60c8e9f17d7021acb75b0f4dc31fe0eaf9c51640cda522ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17c1d429b5ca4f6f53a55068fc96b26e58d2fc2e4375d6e98814c326887876bd(
    value: typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormatMappingParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bb2b64abf4dcd8ba72f8b25ea3d69b1b73888e9514bc4b34780f084737ac7ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd35a394fad958f845ec116f0a3de8f45e562c1456364e69a601e13784b88a69(
    value: typing.Optional[KinesisAnalyticsApplicationInputsSchemaRecordFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd76deb6df29034c4326daa77ee83fbeada2465ec59f6da51674ecdc79f0786(
    *,
    starting_position: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27dfe976398a4f25e8f0bb34e20506d78b102d708774c6904ac03b6ac23ca493(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__518a7099d9e6369d6b9b1be80e37ed8cee360d485bcd3a211187bcf4c40312ff(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8e592acdb3a04705ea33b6c698da4b66078e2313e1b4df54fd72f475c89f3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68741eef12d3bc04d0c931ee11e2f0225daa54c171b36ac4c633478d4d8377b7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a867c6f7ffbbf5e27ee72441847a3240725f4a77218f0aa79c8cf4e0457c714(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c8fa60f2bad434ecbe44c38f62aca68bd041890405542c31df2a0bf275024d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationInputsStartingPositionConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d1b0e106eaa9dff432750c8c3e42e2e65968e204edd08454352f3d84d50deb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__243d25b1682f296b4beffc29e38892a84c7f91292a409492037cabb41adbaf7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e9baed07fb4ea6df5abed5bf17ac6753e28fd2007ba333bbe01442d657bb645(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationInputsStartingPositionConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ac30e080c76295b6e63d4520353f6c50704d07ec5b18a6c42252c51296a5a6(
    *,
    name: builtins.str,
    schema: typing.Union[KinesisAnalyticsApplicationOutputsSchema, typing.Dict[builtins.str, typing.Any]],
    kinesis_firehose: typing.Optional[typing.Union[KinesisAnalyticsApplicationOutputsKinesisFirehose, typing.Dict[builtins.str, typing.Any]]] = None,
    kinesis_stream: typing.Optional[typing.Union[KinesisAnalyticsApplicationOutputsKinesisStream, typing.Dict[builtins.str, typing.Any]]] = None,
    lambda_: typing.Optional[typing.Union[KinesisAnalyticsApplicationOutputsLambda, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5065a497d1a4e8ff652f5cd591673691d22e8f943724ad2847248b9108207b1d(
    *,
    resource_arn: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34292ea708ce29c0d653c687d64f5a2845b7605cba904c6c8934889d7034245a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96244c5d6db565d46c0297eb690964cd35a5792abc95ed5a723f3cdeee7eb331(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae2643681f064850e86a25dd1b11f6cf2938d2e729c1c96a878f97dc4bc0b10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794c53496a905ccd1b389222f8e4e276e5db75ec02dfd08b31f63f7ebfefe7a6(
    value: typing.Optional[KinesisAnalyticsApplicationOutputsKinesisFirehose],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccd4f9787ebf44c83a9f0e88bbf6f3de7efb7767e631cf35169a2e4a7bc6d403(
    *,
    resource_arn: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b503b69bec7992c0b04e1d07b1ad0853784c660c71d0b7c6dc0d4f7030b32c3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb6e336e4d457b5ad4eadf9e9aec231150da4f54de438bd105b2ad45f85be57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77ae03dfae46c1efa0e7a19ac75d44f7b9c1b73fdd57c5cba17c856d57e5fa7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44f3dc213075e38aabf1e4d82f8dee7416d0490e344d0611c78245c5d59a420c(
    value: typing.Optional[KinesisAnalyticsApplicationOutputsKinesisStream],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a387476bf8040f65fac4ac2aa4fa787cab6b17c52cb9d26944b07c0ed8a34e(
    *,
    resource_arn: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b45f14588999bc3db75e42e37b2fc5f394f73e5b9df72ea52c57fe9d7e4d5e5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef4135f3a49bda3e1e498852fb47569d25e93c0d84c1cdd047af84a682b173ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198f13358937ea5b90e198c7246e2ad3aaac8b68b0ca77b3ec5fc868f836e9e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f101ad4f30e64917ec51dec6d02e1b1da22164f97a1cc7a17b153281582173bb(
    value: typing.Optional[KinesisAnalyticsApplicationOutputsLambda],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d41f1c396599e4821c3389899bc66728adc99a79b4fd6e4081790d4a2aba1faa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d59917d24a6233d1b536de82d72489f3fa4c9e8683b5a5f3c682996eea446c40(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb71f62742ad5e947d8f554534069945b47ddce43d88d5420e60ea05f4d162af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fca8d9e98cde31c134e7bf396b89568cea3554fd47f42fac8aff87999de12f9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b7297a3a236786d3e956d7f0a4a3b8720d00f3b030ea54c412fa4ae171035e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f14da5282867ad807c02431ebfa20f3246c2ef327307665a7787b53e7332b63(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationOutputs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e164626bcd11d3ed2af2ce8aada338428240b3e586239ed69d5766b056b7c078(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb032311ddb9a50d49b638b565aee80c4585ff0e276c14f2ac8865b117946619(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742ea58156076eb34211e94f4a14b780b27915bb975de298d8e12279333ce3e5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationOutputs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7653f0342a442179cac7a623da67048718bbc86e06ff2059ab43d09d20406f33(
    *,
    record_format_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7d85bf1360e64fba2ce5c21138ea593168e29e720406c3a35be1dbe0e3b0bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d9f64a01e12291406cd18b4f6226ff7bb67a90dbd250575e94d1e3fc398cd07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e678d315bb1aeda8c3d860ab92eb172ebd3b691b03a7a3abe33a9c7aef24b36b(
    value: typing.Optional[KinesisAnalyticsApplicationOutputsSchema],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba22701dfa4a88fc5e332a3d536ac6187e970ab88e1fdcb835ece49983c36b29(
    *,
    s3: typing.Union[KinesisAnalyticsApplicationReferenceDataSourcesS3, typing.Dict[builtins.str, typing.Any]],
    schema: typing.Union[KinesisAnalyticsApplicationReferenceDataSourcesSchema, typing.Dict[builtins.str, typing.Any]],
    table_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bed9a629a44c0b4cfc28381a246bfcbda0608dc1430de7eb0103a66483f593d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b2021bce9bea076d6347c493cbadad285d3efaf5dae6512e579afb7e100563(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d67038e966debe90d6d4ce3527a5da8c9750cb1a31040d9f6b665e1f0c80dfd(
    value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab80fa31f6545ed31a5779bcc8098a8f85d88cb41fa874f7704c638e22317905(
    *,
    bucket_arn: builtins.str,
    file_key: builtins.str,
    role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20595936ed52d5ae6a35bcc693732fe6a2c5e653eb0a4af6a4568849ad4cbe6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ea81a855de48957f78ab4978bb1b88cfaa4297405247949098a5e63cd5e983(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce0fec8733c79f418001a809f7c97102d1f3c75add97901c222a94b45b2c141(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ff39baa6aa52744a7e8e003c84e42717b3569a5e6cc842e097f0afb49042b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08067263089544f65c3cc4612dfd78722fb6971c9a0f41714addc4abdbbd6556(
    value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesS3],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7905ac13f49b1bc342b2aa6cdfea10e0c9d1680eb1b0f0576713ac17a2a20b37(
    *,
    record_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns, typing.Dict[builtins.str, typing.Any]]]],
    record_format: typing.Union[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat, typing.Dict[builtins.str, typing.Any]],
    record_encoding: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a84b36110d98e2e3cfd096fff4339d1ed0ffbe21d839b25d25e992ef71c30be1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3211207ffc71487a5e07f5fedafe8fdfefcf22b97045ddc7d0065d2c0c2b8291(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a98291f86eb7253efa98518f51f2dd664549acd6a2350a34400b7aa5ec62e97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579e5a498e578b34d3783cf6f3be6f5b64a27b36f27753bfdc21afdf8a47a76e(
    value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchema],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__121ccd1ec2409992dc944e9e7c88e47d7c4336b7e27e29c5676b4a1093579c41(
    *,
    name: builtins.str,
    sql_type: builtins.str,
    mapping: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9d83c2ee312b072ba0cd1dd87c894e714de810c43af38fe13a4baf9ea6096aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c43c00fba0ae5ec76d63c84a37917c2d487b83b6ddd223f8f0e120c77dd506ce(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc25df1f752600d1cb89ec033411f43bbc740a7bab5d1a7211a44d775601cb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ff2ff64c24e42d80f7dc4f35ac92fc46a429f606c55ba171bc6a3ae08d4e70(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3d776a44241ee2b3b79cda4cb4bac0233721c1baa0af09f182abc11ae87e3d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb126965b5616847160ed9aee09e328f83b42f726343c204d2890b51de9b137(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48cfb64fd3af5e72e377b4ae334f290402a8002ea2a8a43aa043b3172c4f3a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e509e396e1f4b9bf1103283d636a508f3c06796e3cceeb49cdd84f03f7015474(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf8f76504e7291e08c4b9038266c409f8fdbe49b34d63cef4f6ac9dcae933b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ba671abc81c25b39fe1ecaa81ad0924cdf5e4276d7e6aaa51a4b7687acf37e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0473bad0ad6e6ed5de5dcfb9a874a8316999191e9c3efffceb5ca6a512915d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5540765f592b2217e18b1707f46fb9c808973c4e8c9d7afd8573b685e31dd537(
    *,
    mapping_parameters: typing.Optional[typing.Union[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8444a8243e27ede7eef400879e997a36d66049ba5c570d7eefa9dad6f243c072(
    *,
    csv: typing.Optional[typing.Union[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv, typing.Dict[builtins.str, typing.Any]]] = None,
    json: typing.Optional[typing.Union[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a22872b10675fb7ee4941b0f3ae97838782a8e9c61f785bb8c4810c8be6f358(
    *,
    record_column_delimiter: builtins.str,
    record_row_delimiter: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67922398973343711acb4d3e33cad4dd4255f206cad45b51f302718a2b54424b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0ec4ec29b2707f386b4c97fa6b1c790caea275b628aef15093b0b3533bda39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bafd84fdbf7231e0b8d31c05b476a7545e830a1f90c8abe732660eee2bb17cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c878d5191f9a3f0862649ee8f541bb20d3bcf6366fed61adc496ec59cb5c338(
    value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersCsv],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0acc579b60ae28abbc7780f849135bab781b340f9494722055485fe7d987928(
    *,
    record_row_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__068fc337a8f9ca95c7ba585ad25df7e60bf41ffbaf80889a3556ea61711a0b85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__555d070756b8092794be56d2a3d3e8000b2bed83b4e13c710e56ba36349b1458(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff1b2734072697d2be5b46407011b5d9b62ef38669b0c5c569eb1f1316221e94(
    value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParametersJson],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36ae86db53165003c47f55d54464306839775464d49a00c2109557402cae29f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cfb542c7ec7e7ef67a4204cf36595eb5e6f1f55cb5cd100d3fbbb56bf37447e(
    value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormatMappingParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a92b39404a49e6e3ea444a4956039c713628a5adfba70655351fb4ca312d10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006bb9ef276cc71b965f07ca072448dc295ea08a72b79b614afd65212e9661f1(
    value: typing.Optional[KinesisAnalyticsApplicationReferenceDataSourcesSchemaRecordFormat],
) -> None:
    """Type checking stubs"""
    pass
