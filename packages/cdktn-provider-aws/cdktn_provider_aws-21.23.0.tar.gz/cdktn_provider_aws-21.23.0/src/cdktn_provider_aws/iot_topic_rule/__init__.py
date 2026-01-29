r'''
# `aws_iot_topic_rule`

Refer to the Terraform Registry for docs: [`aws_iot_topic_rule`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule).
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


class IotTopicRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule aws_iot_topic_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        sql: builtins.str,
        sql_version: builtins.str,
        cloudwatch_alarm: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleCloudwatchAlarm", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cloudwatch_logs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleCloudwatchLogs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cloudwatch_metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleCloudwatchMetric", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        dynamodb: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleDynamodb", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dynamodbv2: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleDynamodbv2", typing.Dict[builtins.str, typing.Any]]]]] = None,
        elasticsearch: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleElasticsearch", typing.Dict[builtins.str, typing.Any]]]]] = None,
        error_action: typing.Optional[typing.Union["IotTopicRuleErrorAction", typing.Dict[builtins.str, typing.Any]]] = None,
        firehose: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleFirehose", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleHttp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        iot_analytics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleIotAnalytics", typing.Dict[builtins.str, typing.Any]]]]] = None,
        iot_events: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleIotEvents", typing.Dict[builtins.str, typing.Any]]]]] = None,
        kafka: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleKafka", typing.Dict[builtins.str, typing.Any]]]]] = None,
        kinesis: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleKinesis", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lambda_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleLambda", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        republish: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleRepublish", typing.Dict[builtins.str, typing.Any]]]]] = None,
        s3: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleS3", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleSns", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sqs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleSqs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        step_functions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleStepFunctions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timestream: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleTimestream", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule aws_iot_topic_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#enabled IotTopicRule#enabled}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#name IotTopicRule#name}.
        :param sql: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#sql IotTopicRule#sql}.
        :param sql_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#sql_version IotTopicRule#sql_version}.
        :param cloudwatch_alarm: cloudwatch_alarm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#cloudwatch_alarm IotTopicRule#cloudwatch_alarm}
        :param cloudwatch_logs: cloudwatch_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#cloudwatch_logs IotTopicRule#cloudwatch_logs}
        :param cloudwatch_metric: cloudwatch_metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#cloudwatch_metric IotTopicRule#cloudwatch_metric}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#description IotTopicRule#description}.
        :param dynamodb: dynamodb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#dynamodb IotTopicRule#dynamodb}
        :param dynamodbv2: dynamodbv2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#dynamodbv2 IotTopicRule#dynamodbv2}
        :param elasticsearch: elasticsearch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#elasticsearch IotTopicRule#elasticsearch}
        :param error_action: error_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#error_action IotTopicRule#error_action}
        :param firehose: firehose block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#firehose IotTopicRule#firehose}
        :param http: http block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#http IotTopicRule#http}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#id IotTopicRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param iot_analytics: iot_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#iot_analytics IotTopicRule#iot_analytics}
        :param iot_events: iot_events block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#iot_events IotTopicRule#iot_events}
        :param kafka: kafka block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#kafka IotTopicRule#kafka}
        :param kinesis: kinesis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#kinesis IotTopicRule#kinesis}
        :param lambda_: lambda block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#lambda IotTopicRule#lambda}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#region IotTopicRule#region}
        :param republish: republish block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#republish IotTopicRule#republish}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#s3 IotTopicRule#s3}
        :param sns: sns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#sns IotTopicRule#sns}
        :param sqs: sqs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#sqs IotTopicRule#sqs}
        :param step_functions: step_functions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#step_functions IotTopicRule#step_functions}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#tags IotTopicRule#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#tags_all IotTopicRule#tags_all}.
        :param timestream: timestream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#timestream IotTopicRule#timestream}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b45e1ae3ba975fb518e21d4913b5680c6553ec7bf5d738ba558a3b215f6b8974)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IotTopicRuleConfig(
            enabled=enabled,
            name=name,
            sql=sql,
            sql_version=sql_version,
            cloudwatch_alarm=cloudwatch_alarm,
            cloudwatch_logs=cloudwatch_logs,
            cloudwatch_metric=cloudwatch_metric,
            description=description,
            dynamodb=dynamodb,
            dynamodbv2=dynamodbv2,
            elasticsearch=elasticsearch,
            error_action=error_action,
            firehose=firehose,
            http=http,
            id=id,
            iot_analytics=iot_analytics,
            iot_events=iot_events,
            kafka=kafka,
            kinesis=kinesis,
            lambda_=lambda_,
            region=region,
            republish=republish,
            s3=s3,
            sns=sns,
            sqs=sqs,
            step_functions=step_functions,
            tags=tags,
            tags_all=tags_all,
            timestream=timestream,
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
        '''Generates CDKTF code for importing a IotTopicRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IotTopicRule to import.
        :param import_from_id: The id of the existing IotTopicRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IotTopicRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a713e3cc295c9802e9b7d0be09158119e2a868a054d750dc29f91666611c0645)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCloudwatchAlarm")
    def put_cloudwatch_alarm(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleCloudwatchAlarm", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d797fa6b787ac7f1745eb7d2dd035735b705bed29447f6480f55b09ebccfce48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCloudwatchAlarm", [value]))

    @jsii.member(jsii_name="putCloudwatchLogs")
    def put_cloudwatch_logs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleCloudwatchLogs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__140bce2e6812ae81d017d2dd79890bb9b9b0367da7d74132203ff38f62b7138d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCloudwatchLogs", [value]))

    @jsii.member(jsii_name="putCloudwatchMetric")
    def put_cloudwatch_metric(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleCloudwatchMetric", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d83bf3e1e4159dd69f952a696a82b3c93a40984aeb980afb889af3abcf471d1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCloudwatchMetric", [value]))

    @jsii.member(jsii_name="putDynamodb")
    def put_dynamodb(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleDynamodb", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bb6dafe34bcbe8b1825e6f0055e100372cd1ddde6e33da26222486eacc0f624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDynamodb", [value]))

    @jsii.member(jsii_name="putDynamodbv2")
    def put_dynamodbv2(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleDynamodbv2", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b40b3eb64ede3602937d725e0859d98d7b75c98b0251f26aedb0ccd19a0d098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDynamodbv2", [value]))

    @jsii.member(jsii_name="putElasticsearch")
    def put_elasticsearch(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleElasticsearch", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87d7b9339cb7dcae977deb36786aabfb2406f9785c586c74ee24988502e75e23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putElasticsearch", [value]))

    @jsii.member(jsii_name="putErrorAction")
    def put_error_action(
        self,
        *,
        cloudwatch_alarm: typing.Optional[typing.Union["IotTopicRuleErrorActionCloudwatchAlarm", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudwatch_logs: typing.Optional[typing.Union["IotTopicRuleErrorActionCloudwatchLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudwatch_metric: typing.Optional[typing.Union["IotTopicRuleErrorActionCloudwatchMetric", typing.Dict[builtins.str, typing.Any]]] = None,
        dynamodb: typing.Optional[typing.Union["IotTopicRuleErrorActionDynamodb", typing.Dict[builtins.str, typing.Any]]] = None,
        dynamodbv2: typing.Optional[typing.Union["IotTopicRuleErrorActionDynamodbv2", typing.Dict[builtins.str, typing.Any]]] = None,
        elasticsearch: typing.Optional[typing.Union["IotTopicRuleErrorActionElasticsearch", typing.Dict[builtins.str, typing.Any]]] = None,
        firehose: typing.Optional[typing.Union["IotTopicRuleErrorActionFirehose", typing.Dict[builtins.str, typing.Any]]] = None,
        http: typing.Optional[typing.Union["IotTopicRuleErrorActionHttp", typing.Dict[builtins.str, typing.Any]]] = None,
        iot_analytics: typing.Optional[typing.Union["IotTopicRuleErrorActionIotAnalytics", typing.Dict[builtins.str, typing.Any]]] = None,
        iot_events: typing.Optional[typing.Union["IotTopicRuleErrorActionIotEvents", typing.Dict[builtins.str, typing.Any]]] = None,
        kafka: typing.Optional[typing.Union["IotTopicRuleErrorActionKafka", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis: typing.Optional[typing.Union["IotTopicRuleErrorActionKinesis", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_: typing.Optional[typing.Union["IotTopicRuleErrorActionLambda", typing.Dict[builtins.str, typing.Any]]] = None,
        republish: typing.Optional[typing.Union["IotTopicRuleErrorActionRepublish", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["IotTopicRuleErrorActionS3", typing.Dict[builtins.str, typing.Any]]] = None,
        sns: typing.Optional[typing.Union["IotTopicRuleErrorActionSns", typing.Dict[builtins.str, typing.Any]]] = None,
        sqs: typing.Optional[typing.Union["IotTopicRuleErrorActionSqs", typing.Dict[builtins.str, typing.Any]]] = None,
        step_functions: typing.Optional[typing.Union["IotTopicRuleErrorActionStepFunctions", typing.Dict[builtins.str, typing.Any]]] = None,
        timestream: typing.Optional[typing.Union["IotTopicRuleErrorActionTimestream", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloudwatch_alarm: cloudwatch_alarm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#cloudwatch_alarm IotTopicRule#cloudwatch_alarm}
        :param cloudwatch_logs: cloudwatch_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#cloudwatch_logs IotTopicRule#cloudwatch_logs}
        :param cloudwatch_metric: cloudwatch_metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#cloudwatch_metric IotTopicRule#cloudwatch_metric}
        :param dynamodb: dynamodb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#dynamodb IotTopicRule#dynamodb}
        :param dynamodbv2: dynamodbv2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#dynamodbv2 IotTopicRule#dynamodbv2}
        :param elasticsearch: elasticsearch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#elasticsearch IotTopicRule#elasticsearch}
        :param firehose: firehose block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#firehose IotTopicRule#firehose}
        :param http: http block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#http IotTopicRule#http}
        :param iot_analytics: iot_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#iot_analytics IotTopicRule#iot_analytics}
        :param iot_events: iot_events block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#iot_events IotTopicRule#iot_events}
        :param kafka: kafka block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#kafka IotTopicRule#kafka}
        :param kinesis: kinesis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#kinesis IotTopicRule#kinesis}
        :param lambda_: lambda block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#lambda IotTopicRule#lambda}
        :param republish: republish block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#republish IotTopicRule#republish}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#s3 IotTopicRule#s3}
        :param sns: sns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#sns IotTopicRule#sns}
        :param sqs: sqs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#sqs IotTopicRule#sqs}
        :param step_functions: step_functions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#step_functions IotTopicRule#step_functions}
        :param timestream: timestream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#timestream IotTopicRule#timestream}
        '''
        value = IotTopicRuleErrorAction(
            cloudwatch_alarm=cloudwatch_alarm,
            cloudwatch_logs=cloudwatch_logs,
            cloudwatch_metric=cloudwatch_metric,
            dynamodb=dynamodb,
            dynamodbv2=dynamodbv2,
            elasticsearch=elasticsearch,
            firehose=firehose,
            http=http,
            iot_analytics=iot_analytics,
            iot_events=iot_events,
            kafka=kafka,
            kinesis=kinesis,
            lambda_=lambda_,
            republish=republish,
            s3=s3,
            sns=sns,
            sqs=sqs,
            step_functions=step_functions,
            timestream=timestream,
        )

        return typing.cast(None, jsii.invoke(self, "putErrorAction", [value]))

    @jsii.member(jsii_name="putFirehose")
    def put_firehose(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleFirehose", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05cdcc38d9687756e2cccd11a4f1ccb0f39a5d40c78062dcc96e507b62c1d6bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFirehose", [value]))

    @jsii.member(jsii_name="putHttp")
    def put_http(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleHttp", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27d58c001f8a9700750e51d8d83a41798e962b6cddecdf3bbdfedcc4c1a789f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttp", [value]))

    @jsii.member(jsii_name="putIotAnalytics")
    def put_iot_analytics(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleIotAnalytics", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61ab0288529bdc66ee7dcec7afe336f5ce91dcfecfbf6070c569cc77fa850ec8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIotAnalytics", [value]))

    @jsii.member(jsii_name="putIotEvents")
    def put_iot_events(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleIotEvents", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1b2bd6af5d4bb2315c4ead64be7600d59b1a720b4b1924fd174bd933b36bb2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIotEvents", [value]))

    @jsii.member(jsii_name="putKafka")
    def put_kafka(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleKafka", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd078726b7bbff972a39a0716216685277f735a324d3f90f155b61854aee9c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putKafka", [value]))

    @jsii.member(jsii_name="putKinesis")
    def put_kinesis(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleKinesis", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d385cbebabbc5480af1b2e429613f512a55f9030407a95bd490eb8788db96778)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putKinesis", [value]))

    @jsii.member(jsii_name="putLambda")
    def put_lambda(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleLambda", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65a2fd2f6542b6ef1cddd15cd3c441e9af4dec3a88e252769125314993af0290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLambda", [value]))

    @jsii.member(jsii_name="putRepublish")
    def put_republish(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleRepublish", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0b54e1b780bf6014f0add89176e5e7f8fb3ec4aea8c2fcb4c3d5329809cc779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRepublish", [value]))

    @jsii.member(jsii_name="putS3")
    def put_s3(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleS3", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d343cbeec79bc43d2e4c9c295bcb1e94d8c4b1f61e5eabfc26372c044866b432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="putSns")
    def put_sns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleSns", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb358933a4524c7137d01d71f735920da557c95c7b4bd570373534694828994)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSns", [value]))

    @jsii.member(jsii_name="putSqs")
    def put_sqs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleSqs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68a04bae15f8544f5de2790917c9a9ac7335a6bc00428ad5dddf84babaa50a29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSqs", [value]))

    @jsii.member(jsii_name="putStepFunctions")
    def put_step_functions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleStepFunctions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f8a6ead495c6065732b3dc9ad82cfa19e6f4d91fcf7d41af8f32f9f32663b00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStepFunctions", [value]))

    @jsii.member(jsii_name="putTimestream")
    def put_timestream(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleTimestream", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__069b369fcc028228a23b2136821e2213dbcb0bf686596b4a4e8067f38d5f73c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTimestream", [value]))

    @jsii.member(jsii_name="resetCloudwatchAlarm")
    def reset_cloudwatch_alarm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchAlarm", []))

    @jsii.member(jsii_name="resetCloudwatchLogs")
    def reset_cloudwatch_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLogs", []))

    @jsii.member(jsii_name="resetCloudwatchMetric")
    def reset_cloudwatch_metric(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchMetric", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDynamodb")
    def reset_dynamodb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamodb", []))

    @jsii.member(jsii_name="resetDynamodbv2")
    def reset_dynamodbv2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamodbv2", []))

    @jsii.member(jsii_name="resetElasticsearch")
    def reset_elasticsearch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearch", []))

    @jsii.member(jsii_name="resetErrorAction")
    def reset_error_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorAction", []))

    @jsii.member(jsii_name="resetFirehose")
    def reset_firehose(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirehose", []))

    @jsii.member(jsii_name="resetHttp")
    def reset_http(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIotAnalytics")
    def reset_iot_analytics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIotAnalytics", []))

    @jsii.member(jsii_name="resetIotEvents")
    def reset_iot_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIotEvents", []))

    @jsii.member(jsii_name="resetKafka")
    def reset_kafka(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKafka", []))

    @jsii.member(jsii_name="resetKinesis")
    def reset_kinesis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesis", []))

    @jsii.member(jsii_name="resetLambda")
    def reset_lambda(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambda", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRepublish")
    def reset_republish(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepublish", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

    @jsii.member(jsii_name="resetSns")
    def reset_sns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSns", []))

    @jsii.member(jsii_name="resetSqs")
    def reset_sqs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqs", []))

    @jsii.member(jsii_name="resetStepFunctions")
    def reset_step_functions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStepFunctions", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTimestream")
    def reset_timestream(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestream", []))

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
    @jsii.member(jsii_name="cloudwatchAlarm")
    def cloudwatch_alarm(self) -> "IotTopicRuleCloudwatchAlarmList":
        return typing.cast("IotTopicRuleCloudwatchAlarmList", jsii.get(self, "cloudwatchAlarm"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogs")
    def cloudwatch_logs(self) -> "IotTopicRuleCloudwatchLogsList":
        return typing.cast("IotTopicRuleCloudwatchLogsList", jsii.get(self, "cloudwatchLogs"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchMetric")
    def cloudwatch_metric(self) -> "IotTopicRuleCloudwatchMetricList":
        return typing.cast("IotTopicRuleCloudwatchMetricList", jsii.get(self, "cloudwatchMetric"))

    @builtins.property
    @jsii.member(jsii_name="dynamodb")
    def dynamodb(self) -> "IotTopicRuleDynamodbList":
        return typing.cast("IotTopicRuleDynamodbList", jsii.get(self, "dynamodb"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbv2")
    def dynamodbv2(self) -> "IotTopicRuleDynamodbv2List":
        return typing.cast("IotTopicRuleDynamodbv2List", jsii.get(self, "dynamodbv2"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearch")
    def elasticsearch(self) -> "IotTopicRuleElasticsearchList":
        return typing.cast("IotTopicRuleElasticsearchList", jsii.get(self, "elasticsearch"))

    @builtins.property
    @jsii.member(jsii_name="errorAction")
    def error_action(self) -> "IotTopicRuleErrorActionOutputReference":
        return typing.cast("IotTopicRuleErrorActionOutputReference", jsii.get(self, "errorAction"))

    @builtins.property
    @jsii.member(jsii_name="firehose")
    def firehose(self) -> "IotTopicRuleFirehoseList":
        return typing.cast("IotTopicRuleFirehoseList", jsii.get(self, "firehose"))

    @builtins.property
    @jsii.member(jsii_name="http")
    def http(self) -> "IotTopicRuleHttpList":
        return typing.cast("IotTopicRuleHttpList", jsii.get(self, "http"))

    @builtins.property
    @jsii.member(jsii_name="iotAnalytics")
    def iot_analytics(self) -> "IotTopicRuleIotAnalyticsList":
        return typing.cast("IotTopicRuleIotAnalyticsList", jsii.get(self, "iotAnalytics"))

    @builtins.property
    @jsii.member(jsii_name="iotEvents")
    def iot_events(self) -> "IotTopicRuleIotEventsList":
        return typing.cast("IotTopicRuleIotEventsList", jsii.get(self, "iotEvents"))

    @builtins.property
    @jsii.member(jsii_name="kafka")
    def kafka(self) -> "IotTopicRuleKafkaList":
        return typing.cast("IotTopicRuleKafkaList", jsii.get(self, "kafka"))

    @builtins.property
    @jsii.member(jsii_name="kinesis")
    def kinesis(self) -> "IotTopicRuleKinesisList":
        return typing.cast("IotTopicRuleKinesisList", jsii.get(self, "kinesis"))

    @builtins.property
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> "IotTopicRuleLambdaList":
        return typing.cast("IotTopicRuleLambdaList", jsii.get(self, "lambda"))

    @builtins.property
    @jsii.member(jsii_name="republish")
    def republish(self) -> "IotTopicRuleRepublishList":
        return typing.cast("IotTopicRuleRepublishList", jsii.get(self, "republish"))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(self) -> "IotTopicRuleS3List":
        return typing.cast("IotTopicRuleS3List", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="sns")
    def sns(self) -> "IotTopicRuleSnsList":
        return typing.cast("IotTopicRuleSnsList", jsii.get(self, "sns"))

    @builtins.property
    @jsii.member(jsii_name="sqs")
    def sqs(self) -> "IotTopicRuleSqsList":
        return typing.cast("IotTopicRuleSqsList", jsii.get(self, "sqs"))

    @builtins.property
    @jsii.member(jsii_name="stepFunctions")
    def step_functions(self) -> "IotTopicRuleStepFunctionsList":
        return typing.cast("IotTopicRuleStepFunctionsList", jsii.get(self, "stepFunctions"))

    @builtins.property
    @jsii.member(jsii_name="timestream")
    def timestream(self) -> "IotTopicRuleTimestreamList":
        return typing.cast("IotTopicRuleTimestreamList", jsii.get(self, "timestream"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchAlarmInput")
    def cloudwatch_alarm_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleCloudwatchAlarm"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleCloudwatchAlarm"]]], jsii.get(self, "cloudwatchAlarmInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogsInput")
    def cloudwatch_logs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleCloudwatchLogs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleCloudwatchLogs"]]], jsii.get(self, "cloudwatchLogsInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchMetricInput")
    def cloudwatch_metric_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleCloudwatchMetric"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleCloudwatchMetric"]]], jsii.get(self, "cloudwatchMetricInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbInput")
    def dynamodb_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleDynamodb"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleDynamodb"]]], jsii.get(self, "dynamodbInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbv2Input")
    def dynamodbv2_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleDynamodbv2"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleDynamodbv2"]]], jsii.get(self, "dynamodbv2Input"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchInput")
    def elasticsearch_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleElasticsearch"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleElasticsearch"]]], jsii.get(self, "elasticsearchInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="errorActionInput")
    def error_action_input(self) -> typing.Optional["IotTopicRuleErrorAction"]:
        return typing.cast(typing.Optional["IotTopicRuleErrorAction"], jsii.get(self, "errorActionInput"))

    @builtins.property
    @jsii.member(jsii_name="firehoseInput")
    def firehose_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleFirehose"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleFirehose"]]], jsii.get(self, "firehoseInput"))

    @builtins.property
    @jsii.member(jsii_name="httpInput")
    def http_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleHttp"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleHttp"]]], jsii.get(self, "httpInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="iotAnalyticsInput")
    def iot_analytics_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleIotAnalytics"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleIotAnalytics"]]], jsii.get(self, "iotAnalyticsInput"))

    @builtins.property
    @jsii.member(jsii_name="iotEventsInput")
    def iot_events_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleIotEvents"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleIotEvents"]]], jsii.get(self, "iotEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="kafkaInput")
    def kafka_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleKafka"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleKafka"]]], jsii.get(self, "kafkaInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisInput")
    def kinesis_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleKinesis"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleKinesis"]]], jsii.get(self, "kinesisInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaInput")
    def lambda_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleLambda"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleLambda"]]], jsii.get(self, "lambdaInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="republishInput")
    def republish_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleRepublish"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleRepublish"]]], jsii.get(self, "republishInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleS3"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleS3"]]], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="snsInput")
    def sns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleSns"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleSns"]]], jsii.get(self, "snsInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlInput")
    def sql_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlVersionInput")
    def sql_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="sqsInput")
    def sqs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleSqs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleSqs"]]], jsii.get(self, "sqsInput"))

    @builtins.property
    @jsii.member(jsii_name="stepFunctionsInput")
    def step_functions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleStepFunctions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleStepFunctions"]]], jsii.get(self, "stepFunctionsInput"))

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
    @jsii.member(jsii_name="timestreamInput")
    def timestream_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleTimestream"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleTimestream"]]], jsii.get(self, "timestreamInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdc08c7c77a900e6a7a014f51abca9108d8051e850ecee3cb64d9890c55a3da5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__26f5e85b3121086e850b8cd84256fffeed1882a1e0754893d0cb59e3e4baa356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d3d9c28b33df5fc10efeadc95080ca4bb97d6bce521edfc4e495eeeede9a39f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00d7abaea17b2bba059f305993879e8679e0624f13a5f48a52dfea890b15e675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf3f33afa6a85a497d7872002f522feb0ea2d4ef8e681fb0ac59cacec39798dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sql")
    def sql(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sql"))

    @sql.setter
    def sql(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb40b58c35acaf50f5c762585273ab06a8875e53840dccccaa4295f1701e6875)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sql", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlVersion")
    def sql_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlVersion"))

    @sql_version.setter
    def sql_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__175235d6524b2dad212ae70a2656655b0f75fab75cba1728a5a5f9bb872b0909)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce7ae3631ebb1b576cea996c6e3d214990f4d89f37779d85bb86155484c4fadb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bede94c35cd68d0020eb5a8dea706f641a7a793d13d7f783ab6e849fa726d1c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleCloudwatchAlarm",
    jsii_struct_bases=[],
    name_mapping={
        "alarm_name": "alarmName",
        "role_arn": "roleArn",
        "state_reason": "stateReason",
        "state_value": "stateValue",
    },
)
class IotTopicRuleCloudwatchAlarm:
    def __init__(
        self,
        *,
        alarm_name: builtins.str,
        role_arn: builtins.str,
        state_reason: builtins.str,
        state_value: builtins.str,
    ) -> None:
        '''
        :param alarm_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#alarm_name IotTopicRule#alarm_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param state_reason: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#state_reason IotTopicRule#state_reason}.
        :param state_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#state_value IotTopicRule#state_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f78171057e8280666918ad6edf9efc89cc4adb00cb36043a02f7934f8fb349)
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument state_reason", value=state_reason, expected_type=type_hints["state_reason"])
            check_type(argname="argument state_value", value=state_value, expected_type=type_hints["state_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alarm_name": alarm_name,
            "role_arn": role_arn,
            "state_reason": state_reason,
            "state_value": state_value,
        }

    @builtins.property
    def alarm_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#alarm_name IotTopicRule#alarm_name}.'''
        result = self._values.get("alarm_name")
        assert result is not None, "Required property 'alarm_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state_reason(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#state_reason IotTopicRule#state_reason}.'''
        result = self._values.get("state_reason")
        assert result is not None, "Required property 'state_reason' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#state_value IotTopicRule#state_value}.'''
        result = self._values.get("state_value")
        assert result is not None, "Required property 'state_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleCloudwatchAlarm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleCloudwatchAlarmList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleCloudwatchAlarmList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__236e0fa0a13083ae880bdf950cc64e589e4d882ce8472884903f88b42811a9a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleCloudwatchAlarmOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__507e6daf464b1f441a516484189a4e3995ac6dd81429b987a1cf4c4b84324c2d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleCloudwatchAlarmOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f313345b104b79935f8db3ddf3948c6f2f0e9c2d0b179c7c0ee852a1fca81ce0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__daeb7b82efb71a66cf18700252551808c37eda28f476a0bee2ae5da4e48d0f67)
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
            type_hints = typing.get_type_hints(_typecheckingstub__424aec70420f70789d658e3eb60690ff91a665cc4b7aece87a063f393237ba9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchAlarm]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchAlarm]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchAlarm]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35e6f1281738fd3f1863d0879f9d3e4121038da3998830b5f843b25425e33e0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleCloudwatchAlarmOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleCloudwatchAlarmOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55aebef1bcf186dddabfef20573910bb8167b2c81e077985984132c6b137b17a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="alarmNameInput")
    def alarm_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alarmNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="stateReasonInput")
    def state_reason_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateReasonInput"))

    @builtins.property
    @jsii.member(jsii_name="stateValueInput")
    def state_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateValueInput"))

    @builtins.property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alarmName"))

    @alarm_name.setter
    def alarm_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96c6fd8e4bbbf2cf81decb1df7a1080d6221ef31aa64bc0b1b782c7846b978ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1702cdd8af7ba07b9e3dc18ac5f92e89788c59105aaf6faa7ebbe2979606370)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stateReason")
    def state_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateReason"))

    @state_reason.setter
    def state_reason(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__305d1f2bd2a246960fdea47662a10c1a5979a832a230c79c6730817d5b9f32fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stateReason", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stateValue")
    def state_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateValue"))

    @state_value.setter
    def state_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e81ad058f9190a3538ee35122c6f7fb11b440e48baac4b17e3431685c9af0f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stateValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchAlarm]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchAlarm]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchAlarm]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ac7fcb487791af6ab8deff6cb35f7478557cfcf1a030116341d1d2a0732394e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleCloudwatchLogs",
    jsii_struct_bases=[],
    name_mapping={
        "log_group_name": "logGroupName",
        "role_arn": "roleArn",
        "batch_mode": "batchMode",
    },
)
class IotTopicRuleCloudwatchLogs:
    def __init__(
        self,
        *,
        log_group_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param log_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#log_group_name IotTopicRule#log_group_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93713ee7d872c594fdfb0e08132caf1cbfaf66341ab164e802f2e5b75cde4057)
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument batch_mode", value=batch_mode, expected_type=type_hints["batch_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group_name": log_group_name,
            "role_arn": role_arn,
        }
        if batch_mode is not None:
            self._values["batch_mode"] = batch_mode

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#log_group_name IotTopicRule#log_group_name}.'''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.'''
        result = self._values.get("batch_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleCloudwatchLogs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleCloudwatchLogsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleCloudwatchLogsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad9b66df9dcf29a49db6e5559f083ada496326fac4870cf8aee3797ba3c08305)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleCloudwatchLogsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61bf7349537d85aff4fa7e44c501f3eef06d63de571a405eba291d6da5f8316e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleCloudwatchLogsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d9a3a7ff03ce3e412989c33553787f288b1fd5ec8900ea5ae32cf50a466a938)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2c9593db9317932ac30364049c69aaed20c8bf603a853bfc4eeb1e2e8f48d80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c7637f4bd129bbfaa83ae2dbaf3eeb20458257fb7e7f61906b44ef92fb3d913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchLogs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchLogs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchLogs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b50124bf02962055fd930534e2facb4e3dca25bbcea4977ac2f221e71748907c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleCloudwatchLogsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleCloudwatchLogsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c7af28cb182003ed5ae4bf594f3532a4f7e4028a53ff5ee66d7d25f1113b5d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBatchMode")
    def reset_batch_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchMode", []))

    @builtins.property
    @jsii.member(jsii_name="batchModeInput")
    def batch_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "batchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupNameInput")
    def log_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="batchMode")
    def batch_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "batchMode"))

    @batch_mode.setter
    def batch_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__164a8ef3d0c2b99e81240afe8a7c86c389c3fcfd4ebf94a04feac8763e627088)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20300e3b9ac827d6852dfaba8e26ec03bf8adca36803e33bc4fa54ac8979cca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8361e1a8e7d4a71b4b168f0df911abc9eb81dc39484bff861523dcd517da39d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchLogs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchLogs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchLogs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff2326e93cfef79d31e6cfcf28b737d2488e86cffa1eb3586adc7b7a38215160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleCloudwatchMetric",
    jsii_struct_bases=[],
    name_mapping={
        "metric_name": "metricName",
        "metric_namespace": "metricNamespace",
        "metric_unit": "metricUnit",
        "metric_value": "metricValue",
        "role_arn": "roleArn",
        "metric_timestamp": "metricTimestamp",
    },
)
class IotTopicRuleCloudwatchMetric:
    def __init__(
        self,
        *,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        metric_unit: builtins.str,
        metric_value: builtins.str,
        role_arn: builtins.str,
        metric_timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metric_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_name IotTopicRule#metric_name}.
        :param metric_namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_namespace IotTopicRule#metric_namespace}.
        :param metric_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_unit IotTopicRule#metric_unit}.
        :param metric_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_value IotTopicRule#metric_value}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param metric_timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_timestamp IotTopicRule#metric_timestamp}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91c1edeb1b50e46f12dcffb2508a171e8df23e7fa3d9027b9cea3e069643dd42)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument metric_unit", value=metric_unit, expected_type=type_hints["metric_unit"])
            check_type(argname="argument metric_value", value=metric_value, expected_type=type_hints["metric_value"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument metric_timestamp", value=metric_timestamp, expected_type=type_hints["metric_timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_name": metric_name,
            "metric_namespace": metric_namespace,
            "metric_unit": metric_unit,
            "metric_value": metric_value,
            "role_arn": role_arn,
        }
        if metric_timestamp is not None:
            self._values["metric_timestamp"] = metric_timestamp

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_name IotTopicRule#metric_name}.'''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_namespace(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_namespace IotTopicRule#metric_namespace}.'''
        result = self._values.get("metric_namespace")
        assert result is not None, "Required property 'metric_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_unit IotTopicRule#metric_unit}.'''
        result = self._values.get("metric_unit")
        assert result is not None, "Required property 'metric_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_value IotTopicRule#metric_value}.'''
        result = self._values.get("metric_value")
        assert result is not None, "Required property 'metric_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_timestamp(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_timestamp IotTopicRule#metric_timestamp}.'''
        result = self._values.get("metric_timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleCloudwatchMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleCloudwatchMetricList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleCloudwatchMetricList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4b54fea1a502f208f7ce70c5fd3f287f71c80942f328f48eaf463b37922a6ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleCloudwatchMetricOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d4b6fe9c43538a123356a92743caf2c6816142088103a587978e257415cd9f7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleCloudwatchMetricOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ba2810e9f780992d0afcf87075e41c3e5ae7476f52c22ce9cde023e963c63e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5d0d3e02546ab7aeccce9229f66480512b206e1aa770c23538996a74db07d05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9ab22bd84e3d899a00ad2d5a0b6daf6ba9e8358bf2a14d6442a8c741d24d920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchMetric]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchMetric]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchMetric]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a755dc3359040762b278d7f08e0d7210e36c8aafa45f5a4df8938daf0fa3f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleCloudwatchMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleCloudwatchMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a1ddc4a783bd0ca8cb8f953bf536c7f821b6975573126e5a2fcec51ddfb8216)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMetricTimestamp")
    def reset_metric_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricTimestamp", []))

    @builtins.property
    @jsii.member(jsii_name="metricNameInput")
    def metric_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricNameInput"))

    @builtins.property
    @jsii.member(jsii_name="metricNamespaceInput")
    def metric_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="metricTimestampInput")
    def metric_timestamp_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricTimestampInput"))

    @builtins.property
    @jsii.member(jsii_name="metricUnitInput")
    def metric_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="metricValueInput")
    def metric_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricValueInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricName"))

    @metric_name.setter
    def metric_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1baeda0bff9cf2aaed12e5d0e2b6f79aec42faefabc4f843c2a36a0f2e4825e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricNamespace")
    def metric_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricNamespace"))

    @metric_namespace.setter
    def metric_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5768537db757b139cd4a168d8c7d984faf440f68c8432b67b6c9ad69a8f50664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricTimestamp")
    def metric_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricTimestamp"))

    @metric_timestamp.setter
    def metric_timestamp(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b04eb177377e8afa17b90a6c7c785529109821f78b50a6be9a7008f9446d584d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricTimestamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricUnit")
    def metric_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricUnit"))

    @metric_unit.setter
    def metric_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c816afa8b83d5384d4ec39c933b8bb320475124b24de424d5a585ae3e588cec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricValue")
    def metric_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricValue"))

    @metric_value.setter
    def metric_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40762939d79f9151cccc5fd28cdd37fc5fcfbefce27cf2add1bebce4123d98c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7d2a76936568fed0c4e10d81cbb7298c9606053926cc496db9ee05c7d86292)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchMetric]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchMetric]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchMetric]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__115305d7ba789f5b5486d6814e99a1a1041c17ba80bcf09e12a6385a72fa50c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "enabled": "enabled",
        "name": "name",
        "sql": "sql",
        "sql_version": "sqlVersion",
        "cloudwatch_alarm": "cloudwatchAlarm",
        "cloudwatch_logs": "cloudwatchLogs",
        "cloudwatch_metric": "cloudwatchMetric",
        "description": "description",
        "dynamodb": "dynamodb",
        "dynamodbv2": "dynamodbv2",
        "elasticsearch": "elasticsearch",
        "error_action": "errorAction",
        "firehose": "firehose",
        "http": "http",
        "id": "id",
        "iot_analytics": "iotAnalytics",
        "iot_events": "iotEvents",
        "kafka": "kafka",
        "kinesis": "kinesis",
        "lambda_": "lambda",
        "region": "region",
        "republish": "republish",
        "s3": "s3",
        "sns": "sns",
        "sqs": "sqs",
        "step_functions": "stepFunctions",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timestream": "timestream",
    },
)
class IotTopicRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        sql: builtins.str,
        sql_version: builtins.str,
        cloudwatch_alarm: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchAlarm, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cloudwatch_logs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchLogs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cloudwatch_metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchMetric, typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        dynamodb: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleDynamodb", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dynamodbv2: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleDynamodbv2", typing.Dict[builtins.str, typing.Any]]]]] = None,
        elasticsearch: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleElasticsearch", typing.Dict[builtins.str, typing.Any]]]]] = None,
        error_action: typing.Optional[typing.Union["IotTopicRuleErrorAction", typing.Dict[builtins.str, typing.Any]]] = None,
        firehose: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleFirehose", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleHttp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        iot_analytics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleIotAnalytics", typing.Dict[builtins.str, typing.Any]]]]] = None,
        iot_events: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleIotEvents", typing.Dict[builtins.str, typing.Any]]]]] = None,
        kafka: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleKafka", typing.Dict[builtins.str, typing.Any]]]]] = None,
        kinesis: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleKinesis", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lambda_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleLambda", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        republish: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleRepublish", typing.Dict[builtins.str, typing.Any]]]]] = None,
        s3: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleS3", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleSns", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sqs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleSqs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        step_functions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleStepFunctions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timestream: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleTimestream", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#enabled IotTopicRule#enabled}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#name IotTopicRule#name}.
        :param sql: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#sql IotTopicRule#sql}.
        :param sql_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#sql_version IotTopicRule#sql_version}.
        :param cloudwatch_alarm: cloudwatch_alarm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#cloudwatch_alarm IotTopicRule#cloudwatch_alarm}
        :param cloudwatch_logs: cloudwatch_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#cloudwatch_logs IotTopicRule#cloudwatch_logs}
        :param cloudwatch_metric: cloudwatch_metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#cloudwatch_metric IotTopicRule#cloudwatch_metric}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#description IotTopicRule#description}.
        :param dynamodb: dynamodb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#dynamodb IotTopicRule#dynamodb}
        :param dynamodbv2: dynamodbv2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#dynamodbv2 IotTopicRule#dynamodbv2}
        :param elasticsearch: elasticsearch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#elasticsearch IotTopicRule#elasticsearch}
        :param error_action: error_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#error_action IotTopicRule#error_action}
        :param firehose: firehose block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#firehose IotTopicRule#firehose}
        :param http: http block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#http IotTopicRule#http}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#id IotTopicRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param iot_analytics: iot_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#iot_analytics IotTopicRule#iot_analytics}
        :param iot_events: iot_events block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#iot_events IotTopicRule#iot_events}
        :param kafka: kafka block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#kafka IotTopicRule#kafka}
        :param kinesis: kinesis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#kinesis IotTopicRule#kinesis}
        :param lambda_: lambda block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#lambda IotTopicRule#lambda}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#region IotTopicRule#region}
        :param republish: republish block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#republish IotTopicRule#republish}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#s3 IotTopicRule#s3}
        :param sns: sns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#sns IotTopicRule#sns}
        :param sqs: sqs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#sqs IotTopicRule#sqs}
        :param step_functions: step_functions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#step_functions IotTopicRule#step_functions}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#tags IotTopicRule#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#tags_all IotTopicRule#tags_all}.
        :param timestream: timestream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#timestream IotTopicRule#timestream}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(error_action, dict):
            error_action = IotTopicRuleErrorAction(**error_action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d5e36ad582bd0bbecb9ef5ebcce1871c33bd0b890877a62f3d2de422abebc9e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sql", value=sql, expected_type=type_hints["sql"])
            check_type(argname="argument sql_version", value=sql_version, expected_type=type_hints["sql_version"])
            check_type(argname="argument cloudwatch_alarm", value=cloudwatch_alarm, expected_type=type_hints["cloudwatch_alarm"])
            check_type(argname="argument cloudwatch_logs", value=cloudwatch_logs, expected_type=type_hints["cloudwatch_logs"])
            check_type(argname="argument cloudwatch_metric", value=cloudwatch_metric, expected_type=type_hints["cloudwatch_metric"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dynamodb", value=dynamodb, expected_type=type_hints["dynamodb"])
            check_type(argname="argument dynamodbv2", value=dynamodbv2, expected_type=type_hints["dynamodbv2"])
            check_type(argname="argument elasticsearch", value=elasticsearch, expected_type=type_hints["elasticsearch"])
            check_type(argname="argument error_action", value=error_action, expected_type=type_hints["error_action"])
            check_type(argname="argument firehose", value=firehose, expected_type=type_hints["firehose"])
            check_type(argname="argument http", value=http, expected_type=type_hints["http"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument iot_analytics", value=iot_analytics, expected_type=type_hints["iot_analytics"])
            check_type(argname="argument iot_events", value=iot_events, expected_type=type_hints["iot_events"])
            check_type(argname="argument kafka", value=kafka, expected_type=type_hints["kafka"])
            check_type(argname="argument kinesis", value=kinesis, expected_type=type_hints["kinesis"])
            check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument republish", value=republish, expected_type=type_hints["republish"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument sns", value=sns, expected_type=type_hints["sns"])
            check_type(argname="argument sqs", value=sqs, expected_type=type_hints["sqs"])
            check_type(argname="argument step_functions", value=step_functions, expected_type=type_hints["step_functions"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timestream", value=timestream, expected_type=type_hints["timestream"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "name": name,
            "sql": sql,
            "sql_version": sql_version,
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
        if cloudwatch_alarm is not None:
            self._values["cloudwatch_alarm"] = cloudwatch_alarm
        if cloudwatch_logs is not None:
            self._values["cloudwatch_logs"] = cloudwatch_logs
        if cloudwatch_metric is not None:
            self._values["cloudwatch_metric"] = cloudwatch_metric
        if description is not None:
            self._values["description"] = description
        if dynamodb is not None:
            self._values["dynamodb"] = dynamodb
        if dynamodbv2 is not None:
            self._values["dynamodbv2"] = dynamodbv2
        if elasticsearch is not None:
            self._values["elasticsearch"] = elasticsearch
        if error_action is not None:
            self._values["error_action"] = error_action
        if firehose is not None:
            self._values["firehose"] = firehose
        if http is not None:
            self._values["http"] = http
        if id is not None:
            self._values["id"] = id
        if iot_analytics is not None:
            self._values["iot_analytics"] = iot_analytics
        if iot_events is not None:
            self._values["iot_events"] = iot_events
        if kafka is not None:
            self._values["kafka"] = kafka
        if kinesis is not None:
            self._values["kinesis"] = kinesis
        if lambda_ is not None:
            self._values["lambda_"] = lambda_
        if region is not None:
            self._values["region"] = region
        if republish is not None:
            self._values["republish"] = republish
        if s3 is not None:
            self._values["s3"] = s3
        if sns is not None:
            self._values["sns"] = sns
        if sqs is not None:
            self._values["sqs"] = sqs
        if step_functions is not None:
            self._values["step_functions"] = step_functions
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timestream is not None:
            self._values["timestream"] = timestream

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
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#enabled IotTopicRule#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#name IotTopicRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#sql IotTopicRule#sql}.'''
        result = self._values.get("sql")
        assert result is not None, "Required property 'sql' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#sql_version IotTopicRule#sql_version}.'''
        result = self._values.get("sql_version")
        assert result is not None, "Required property 'sql_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloudwatch_alarm(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchAlarm]]]:
        '''cloudwatch_alarm block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#cloudwatch_alarm IotTopicRule#cloudwatch_alarm}
        '''
        result = self._values.get("cloudwatch_alarm")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchAlarm]]], result)

    @builtins.property
    def cloudwatch_logs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchLogs]]]:
        '''cloudwatch_logs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#cloudwatch_logs IotTopicRule#cloudwatch_logs}
        '''
        result = self._values.get("cloudwatch_logs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchLogs]]], result)

    @builtins.property
    def cloudwatch_metric(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchMetric]]]:
        '''cloudwatch_metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#cloudwatch_metric IotTopicRule#cloudwatch_metric}
        '''
        result = self._values.get("cloudwatch_metric")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchMetric]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#description IotTopicRule#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dynamodb(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleDynamodb"]]]:
        '''dynamodb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#dynamodb IotTopicRule#dynamodb}
        '''
        result = self._values.get("dynamodb")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleDynamodb"]]], result)

    @builtins.property
    def dynamodbv2(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleDynamodbv2"]]]:
        '''dynamodbv2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#dynamodbv2 IotTopicRule#dynamodbv2}
        '''
        result = self._values.get("dynamodbv2")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleDynamodbv2"]]], result)

    @builtins.property
    def elasticsearch(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleElasticsearch"]]]:
        '''elasticsearch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#elasticsearch IotTopicRule#elasticsearch}
        '''
        result = self._values.get("elasticsearch")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleElasticsearch"]]], result)

    @builtins.property
    def error_action(self) -> typing.Optional["IotTopicRuleErrorAction"]:
        '''error_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#error_action IotTopicRule#error_action}
        '''
        result = self._values.get("error_action")
        return typing.cast(typing.Optional["IotTopicRuleErrorAction"], result)

    @builtins.property
    def firehose(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleFirehose"]]]:
        '''firehose block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#firehose IotTopicRule#firehose}
        '''
        result = self._values.get("firehose")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleFirehose"]]], result)

    @builtins.property
    def http(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleHttp"]]]:
        '''http block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#http IotTopicRule#http}
        '''
        result = self._values.get("http")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleHttp"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#id IotTopicRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iot_analytics(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleIotAnalytics"]]]:
        '''iot_analytics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#iot_analytics IotTopicRule#iot_analytics}
        '''
        result = self._values.get("iot_analytics")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleIotAnalytics"]]], result)

    @builtins.property
    def iot_events(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleIotEvents"]]]:
        '''iot_events block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#iot_events IotTopicRule#iot_events}
        '''
        result = self._values.get("iot_events")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleIotEvents"]]], result)

    @builtins.property
    def kafka(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleKafka"]]]:
        '''kafka block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#kafka IotTopicRule#kafka}
        '''
        result = self._values.get("kafka")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleKafka"]]], result)

    @builtins.property
    def kinesis(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleKinesis"]]]:
        '''kinesis block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#kinesis IotTopicRule#kinesis}
        '''
        result = self._values.get("kinesis")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleKinesis"]]], result)

    @builtins.property
    def lambda_(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleLambda"]]]:
        '''lambda block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#lambda IotTopicRule#lambda}
        '''
        result = self._values.get("lambda_")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleLambda"]]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#region IotTopicRule#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def republish(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleRepublish"]]]:
        '''republish block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#republish IotTopicRule#republish}
        '''
        result = self._values.get("republish")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleRepublish"]]], result)

    @builtins.property
    def s3(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleS3"]]]:
        '''s3 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#s3 IotTopicRule#s3}
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleS3"]]], result)

    @builtins.property
    def sns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleSns"]]]:
        '''sns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#sns IotTopicRule#sns}
        '''
        result = self._values.get("sns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleSns"]]], result)

    @builtins.property
    def sqs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleSqs"]]]:
        '''sqs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#sqs IotTopicRule#sqs}
        '''
        result = self._values.get("sqs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleSqs"]]], result)

    @builtins.property
    def step_functions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleStepFunctions"]]]:
        '''step_functions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#step_functions IotTopicRule#step_functions}
        '''
        result = self._values.get("step_functions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleStepFunctions"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#tags IotTopicRule#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#tags_all IotTopicRule#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timestream(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleTimestream"]]]:
        '''timestream block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#timestream IotTopicRule#timestream}
        '''
        result = self._values.get("timestream")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleTimestream"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleDynamodb",
    jsii_struct_bases=[],
    name_mapping={
        "hash_key_field": "hashKeyField",
        "hash_key_value": "hashKeyValue",
        "role_arn": "roleArn",
        "table_name": "tableName",
        "hash_key_type": "hashKeyType",
        "operation": "operation",
        "payload_field": "payloadField",
        "range_key_field": "rangeKeyField",
        "range_key_type": "rangeKeyType",
        "range_key_value": "rangeKeyValue",
    },
)
class IotTopicRuleDynamodb:
    def __init__(
        self,
        *,
        hash_key_field: builtins.str,
        hash_key_value: builtins.str,
        role_arn: builtins.str,
        table_name: builtins.str,
        hash_key_type: typing.Optional[builtins.str] = None,
        operation: typing.Optional[builtins.str] = None,
        payload_field: typing.Optional[builtins.str] = None,
        range_key_field: typing.Optional[builtins.str] = None,
        range_key_type: typing.Optional[builtins.str] = None,
        range_key_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hash_key_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#hash_key_field IotTopicRule#hash_key_field}.
        :param hash_key_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#hash_key_value IotTopicRule#hash_key_value}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.
        :param hash_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#hash_key_type IotTopicRule#hash_key_type}.
        :param operation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#operation IotTopicRule#operation}.
        :param payload_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#payload_field IotTopicRule#payload_field}.
        :param range_key_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#range_key_field IotTopicRule#range_key_field}.
        :param range_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#range_key_type IotTopicRule#range_key_type}.
        :param range_key_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#range_key_value IotTopicRule#range_key_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8de5bfde10f7023d2e9a39148e23846d5d17348898d1fffe851927cb0431c614)
            check_type(argname="argument hash_key_field", value=hash_key_field, expected_type=type_hints["hash_key_field"])
            check_type(argname="argument hash_key_value", value=hash_key_value, expected_type=type_hints["hash_key_value"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument hash_key_type", value=hash_key_type, expected_type=type_hints["hash_key_type"])
            check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
            check_type(argname="argument payload_field", value=payload_field, expected_type=type_hints["payload_field"])
            check_type(argname="argument range_key_field", value=range_key_field, expected_type=type_hints["range_key_field"])
            check_type(argname="argument range_key_type", value=range_key_type, expected_type=type_hints["range_key_type"])
            check_type(argname="argument range_key_value", value=range_key_value, expected_type=type_hints["range_key_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hash_key_field": hash_key_field,
            "hash_key_value": hash_key_value,
            "role_arn": role_arn,
            "table_name": table_name,
        }
        if hash_key_type is not None:
            self._values["hash_key_type"] = hash_key_type
        if operation is not None:
            self._values["operation"] = operation
        if payload_field is not None:
            self._values["payload_field"] = payload_field
        if range_key_field is not None:
            self._values["range_key_field"] = range_key_field
        if range_key_type is not None:
            self._values["range_key_type"] = range_key_type
        if range_key_value is not None:
            self._values["range_key_value"] = range_key_value

    @builtins.property
    def hash_key_field(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#hash_key_field IotTopicRule#hash_key_field}.'''
        result = self._values.get("hash_key_field")
        assert result is not None, "Required property 'hash_key_field' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hash_key_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#hash_key_value IotTopicRule#hash_key_value}.'''
        result = self._values.get("hash_key_value")
        assert result is not None, "Required property 'hash_key_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.'''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hash_key_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#hash_key_type IotTopicRule#hash_key_type}.'''
        result = self._values.get("hash_key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#operation IotTopicRule#operation}.'''
        result = self._values.get("operation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def payload_field(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#payload_field IotTopicRule#payload_field}.'''
        result = self._values.get("payload_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def range_key_field(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#range_key_field IotTopicRule#range_key_field}.'''
        result = self._values.get("range_key_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def range_key_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#range_key_type IotTopicRule#range_key_type}.'''
        result = self._values.get("range_key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def range_key_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#range_key_value IotTopicRule#range_key_value}.'''
        result = self._values.get("range_key_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleDynamodb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleDynamodbList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleDynamodbList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83784e0ef069f23df98f3060e8b76c8761333965f1470b485d3ac949509361e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleDynamodbOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7a0222a325176c7f5fbc862f2e89fc068ebf7d2edf3c54294dbede9c585006f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleDynamodbOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7c2f6c884e5e6dbecfd6e95609367d6f98b9497907726765266ba0bae81608)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42079d67fe632a37f94f4621969226299596d9d86b19866d5c786d9ece34cc34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac7619fc5f6bff8bb4b1ce09712bd4c459923a6a10b44bf02508d267cc7a829e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleDynamodb]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleDynamodb]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleDynamodb]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6a8ebc2a8e6ca5a7b9477500343d4d064058f1f82ee98eb6ffd862482471847)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleDynamodbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleDynamodbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efba57e5790520fd8ed4b4c7e14297abf9d0b9938361f5f29a9978aa353f52ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetHashKeyType")
    def reset_hash_key_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHashKeyType", []))

    @jsii.member(jsii_name="resetOperation")
    def reset_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperation", []))

    @jsii.member(jsii_name="resetPayloadField")
    def reset_payload_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPayloadField", []))

    @jsii.member(jsii_name="resetRangeKeyField")
    def reset_range_key_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRangeKeyField", []))

    @jsii.member(jsii_name="resetRangeKeyType")
    def reset_range_key_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRangeKeyType", []))

    @jsii.member(jsii_name="resetRangeKeyValue")
    def reset_range_key_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRangeKeyValue", []))

    @builtins.property
    @jsii.member(jsii_name="hashKeyFieldInput")
    def hash_key_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hashKeyFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="hashKeyTypeInput")
    def hash_key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hashKeyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="hashKeyValueInput")
    def hash_key_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hashKeyValueInput"))

    @builtins.property
    @jsii.member(jsii_name="operationInput")
    def operation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadFieldInput")
    def payload_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "payloadFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeKeyFieldInput")
    def range_key_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rangeKeyFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeKeyTypeInput")
    def range_key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rangeKeyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeKeyValueInput")
    def range_key_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rangeKeyValueInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="hashKeyField")
    def hash_key_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hashKeyField"))

    @hash_key_field.setter
    def hash_key_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3941fe9675002efa2d3eaffbee00f741708a0c5ed3e9c37d493f8ab62078dc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hashKeyField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hashKeyType")
    def hash_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hashKeyType"))

    @hash_key_type.setter
    def hash_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__477caa3ae23928c6f784676853e340441f813b0b13e909d687203daa09abd180)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hashKeyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hashKeyValue")
    def hash_key_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hashKeyValue"))

    @hash_key_value.setter
    def hash_key_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c162d106fb95fcdc6f6fcf034ec26cd24ba6474edb5a4352e3d2b07473afc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hashKeyValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operation")
    def operation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operation"))

    @operation.setter
    def operation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3407d54dee4a1de681bc6b36be9b550abe902742fea42781720d72ec2731160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="payloadField")
    def payload_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "payloadField"))

    @payload_field.setter
    def payload_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e75cb4d7a635ddb1bb5ce75bdc116835ecd309d34d094f6c8a52457b979ebb62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payloadField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rangeKeyField")
    def range_key_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rangeKeyField"))

    @range_key_field.setter
    def range_key_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f1d9f3132cc2875d1dcc998caf02d772c2344f18c5761ff3502df0ee421a095)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rangeKeyField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rangeKeyType")
    def range_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rangeKeyType"))

    @range_key_type.setter
    def range_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39fb59bd621764de07c7069a983b25d339d0072908f09153c9fab05d16f70322)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rangeKeyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rangeKeyValue")
    def range_key_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rangeKeyValue"))

    @range_key_value.setter
    def range_key_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91c91fe0aed4299a982072187dd690304a8abd91c528f819a0dd582117c6d697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rangeKeyValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56f2ee818e41a405d8e8241b8cfcf2a4b5076815bfcfefb19620523e0d0a1ed1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2204c501881c002d6353f73bc92159f0c41f9ff4758fa0af51b7f634f361782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleDynamodb]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleDynamodb]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleDynamodb]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7088dd9d0140f5e172f76388b76cb658993b5d4afbcc2223fbbfbce6648dbbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleDynamodbv2",
    jsii_struct_bases=[],
    name_mapping={"role_arn": "roleArn", "put_item": "putItem"},
)
class IotTopicRuleDynamodbv2:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        put_item: typing.Optional[typing.Union["IotTopicRuleDynamodbv2PutItem", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param put_item: put_item block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#put_item IotTopicRule#put_item}
        '''
        if isinstance(put_item, dict):
            put_item = IotTopicRuleDynamodbv2PutItem(**put_item)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a278afcd3e7d39f1647fdfdd200be2659d27b37f113002f1dd82a7507d95d64b)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument put_item", value=put_item, expected_type=type_hints["put_item"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
        }
        if put_item is not None:
            self._values["put_item"] = put_item

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def put_item(self) -> typing.Optional["IotTopicRuleDynamodbv2PutItem"]:
        '''put_item block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#put_item IotTopicRule#put_item}
        '''
        result = self._values.get("put_item")
        return typing.cast(typing.Optional["IotTopicRuleDynamodbv2PutItem"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleDynamodbv2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleDynamodbv2List(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleDynamodbv2List",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7aa8baf1ed4a33f15e1e3b52ba46edfa9f98ef27baf569896a5df025306cb579)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleDynamodbv2OutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__689d7dc073296dd3f0dd072e738a459280debbb4ac7e30b69cf76c656ec2bae9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleDynamodbv2OutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0b48db3c9ce731d4edf90ac140309ea9eca162e3da1395ff8464f540e05942c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a78f1aef77497d17f26e1c68ff78260bfde39d96c1fd674b19869dd2138836b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ac9a0ae096b4095bc67c83bfb373b0deb470adeac553382a88081d31073cb6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleDynamodbv2]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleDynamodbv2]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleDynamodbv2]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1feb555d4c615bbcd71b9b92419402bb381f632cb363f1befee01d65153f6b0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleDynamodbv2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleDynamodbv2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10e60c5a15a461a6ddf8000ee3bef10a41df0e7bb6e3e34b1aa48d5c8156f9f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPutItem")
    def put_put_item(self, *, table_name: builtins.str) -> None:
        '''
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.
        '''
        value = IotTopicRuleDynamodbv2PutItem(table_name=table_name)

        return typing.cast(None, jsii.invoke(self, "putPutItem", [value]))

    @jsii.member(jsii_name="resetPutItem")
    def reset_put_item(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPutItem", []))

    @builtins.property
    @jsii.member(jsii_name="putItem")
    def put_item(self) -> "IotTopicRuleDynamodbv2PutItemOutputReference":
        return typing.cast("IotTopicRuleDynamodbv2PutItemOutputReference", jsii.get(self, "putItem"))

    @builtins.property
    @jsii.member(jsii_name="putItemInput")
    def put_item_input(self) -> typing.Optional["IotTopicRuleDynamodbv2PutItem"]:
        return typing.cast(typing.Optional["IotTopicRuleDynamodbv2PutItem"], jsii.get(self, "putItemInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf4518dbc28105a42b8dc6523a1ac9c63d69953e0b0c8711396aaed58f62b819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleDynamodbv2]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleDynamodbv2]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleDynamodbv2]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf9dc788ed76f6e1f30540cc777b2f62fc56a7676ced00369ee241d68dc4cf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleDynamodbv2PutItem",
    jsii_struct_bases=[],
    name_mapping={"table_name": "tableName"},
)
class IotTopicRuleDynamodbv2PutItem:
    def __init__(self, *, table_name: builtins.str) -> None:
        '''
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b56de5901f8c8320403b4a219629b60211c351f1922ed9f76411ab00a7bd46)
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table_name": table_name,
        }

    @builtins.property
    def table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.'''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleDynamodbv2PutItem(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleDynamodbv2PutItemOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleDynamodbv2PutItemOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c9203f2fa1cede33d55c753b862f655c3c223ed27401e41773f0d6e8e6e85c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__d28cb9909dca30426b046f36f95175eca1cd4b1964a00bbbf040f6b1fbeb3ed5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleDynamodbv2PutItem]:
        return typing.cast(typing.Optional[IotTopicRuleDynamodbv2PutItem], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleDynamodbv2PutItem],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9397ac1bd495777c04184787ea7516defbd378a54dd8e9e88945297538796437)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleElasticsearch",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint": "endpoint",
        "id": "id",
        "index": "index",
        "role_arn": "roleArn",
        "type": "type",
    },
)
class IotTopicRuleElasticsearch:
    def __init__(
        self,
        *,
        endpoint: builtins.str,
        id: builtins.str,
        index: builtins.str,
        role_arn: builtins.str,
        type: builtins.str,
    ) -> None:
        '''
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#endpoint IotTopicRule#endpoint}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#id IotTopicRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#index IotTopicRule#index}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#type IotTopicRule#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c9aa54d683eace9924b11b40c2edf3a5ab14fe3f027cde186b0b010ceb6946c)
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint": endpoint,
            "id": id,
            "index": index,
            "role_arn": role_arn,
            "type": type,
        }

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#endpoint IotTopicRule#endpoint}.'''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#id IotTopicRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def index(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#index IotTopicRule#index}.'''
        result = self._values.get("index")
        assert result is not None, "Required property 'index' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#type IotTopicRule#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleElasticsearch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleElasticsearchList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleElasticsearchList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c259596c94de46e157c74233d68139363a000785f81fdaa2e9ec320abd595184)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleElasticsearchOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5485d611bd71539a3a3a0707237e6ca920d5fab7481dcae26114a5a2885f4df1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleElasticsearchOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07a9a46ffd97eeabf4574bef19761cf9c73727a54128b5c269ee8b415460c1cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__218fa7955b148359eff582591fd60dd8b1211a403702a446568c39ba93354835)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38a33247d18a23ecc7b0bbc0040ec756515597ed89b69d18369cd4c4c15903e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleElasticsearch]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleElasticsearch]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleElasticsearch]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__483176c8c6727b06cd951be31ab64133db8bca47c7c54954e3649a704b70e8ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleElasticsearchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleElasticsearchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbb2df3bd752ab9b5c82f34cfa4330c5c462ec2dfa5d75720a351d3983b9c9ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="indexInput")
    def index_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34447678fcbfb3468f1f8d470206f5330ca1f654df452c0e4cf4e847a37346f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f54f2a1e645426bc56f95d5085e708624637c70f181b5a84131b677696d227b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="index")
    def index(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "index"))

    @index.setter
    def index(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b1de54b34ea946d81a3ad5c1e4af8efd517f72aa125d5e68694ee726598dc97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "index", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03276da3fb065b0a81d74a8247691b05f843da239b6180966aa2394e50aaccc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb64f9bea3aa339026cecdfe0472760769346f86b865c7e7b4cf1236ecceb244)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleElasticsearch]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleElasticsearch]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleElasticsearch]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03e79ff328f52e215c33878800bc29c85f5678ccfb775589cdbad0a4dc3e495e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorAction",
    jsii_struct_bases=[],
    name_mapping={
        "cloudwatch_alarm": "cloudwatchAlarm",
        "cloudwatch_logs": "cloudwatchLogs",
        "cloudwatch_metric": "cloudwatchMetric",
        "dynamodb": "dynamodb",
        "dynamodbv2": "dynamodbv2",
        "elasticsearch": "elasticsearch",
        "firehose": "firehose",
        "http": "http",
        "iot_analytics": "iotAnalytics",
        "iot_events": "iotEvents",
        "kafka": "kafka",
        "kinesis": "kinesis",
        "lambda_": "lambda",
        "republish": "republish",
        "s3": "s3",
        "sns": "sns",
        "sqs": "sqs",
        "step_functions": "stepFunctions",
        "timestream": "timestream",
    },
)
class IotTopicRuleErrorAction:
    def __init__(
        self,
        *,
        cloudwatch_alarm: typing.Optional[typing.Union["IotTopicRuleErrorActionCloudwatchAlarm", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudwatch_logs: typing.Optional[typing.Union["IotTopicRuleErrorActionCloudwatchLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudwatch_metric: typing.Optional[typing.Union["IotTopicRuleErrorActionCloudwatchMetric", typing.Dict[builtins.str, typing.Any]]] = None,
        dynamodb: typing.Optional[typing.Union["IotTopicRuleErrorActionDynamodb", typing.Dict[builtins.str, typing.Any]]] = None,
        dynamodbv2: typing.Optional[typing.Union["IotTopicRuleErrorActionDynamodbv2", typing.Dict[builtins.str, typing.Any]]] = None,
        elasticsearch: typing.Optional[typing.Union["IotTopicRuleErrorActionElasticsearch", typing.Dict[builtins.str, typing.Any]]] = None,
        firehose: typing.Optional[typing.Union["IotTopicRuleErrorActionFirehose", typing.Dict[builtins.str, typing.Any]]] = None,
        http: typing.Optional[typing.Union["IotTopicRuleErrorActionHttp", typing.Dict[builtins.str, typing.Any]]] = None,
        iot_analytics: typing.Optional[typing.Union["IotTopicRuleErrorActionIotAnalytics", typing.Dict[builtins.str, typing.Any]]] = None,
        iot_events: typing.Optional[typing.Union["IotTopicRuleErrorActionIotEvents", typing.Dict[builtins.str, typing.Any]]] = None,
        kafka: typing.Optional[typing.Union["IotTopicRuleErrorActionKafka", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis: typing.Optional[typing.Union["IotTopicRuleErrorActionKinesis", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_: typing.Optional[typing.Union["IotTopicRuleErrorActionLambda", typing.Dict[builtins.str, typing.Any]]] = None,
        republish: typing.Optional[typing.Union["IotTopicRuleErrorActionRepublish", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["IotTopicRuleErrorActionS3", typing.Dict[builtins.str, typing.Any]]] = None,
        sns: typing.Optional[typing.Union["IotTopicRuleErrorActionSns", typing.Dict[builtins.str, typing.Any]]] = None,
        sqs: typing.Optional[typing.Union["IotTopicRuleErrorActionSqs", typing.Dict[builtins.str, typing.Any]]] = None,
        step_functions: typing.Optional[typing.Union["IotTopicRuleErrorActionStepFunctions", typing.Dict[builtins.str, typing.Any]]] = None,
        timestream: typing.Optional[typing.Union["IotTopicRuleErrorActionTimestream", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cloudwatch_alarm: cloudwatch_alarm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#cloudwatch_alarm IotTopicRule#cloudwatch_alarm}
        :param cloudwatch_logs: cloudwatch_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#cloudwatch_logs IotTopicRule#cloudwatch_logs}
        :param cloudwatch_metric: cloudwatch_metric block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#cloudwatch_metric IotTopicRule#cloudwatch_metric}
        :param dynamodb: dynamodb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#dynamodb IotTopicRule#dynamodb}
        :param dynamodbv2: dynamodbv2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#dynamodbv2 IotTopicRule#dynamodbv2}
        :param elasticsearch: elasticsearch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#elasticsearch IotTopicRule#elasticsearch}
        :param firehose: firehose block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#firehose IotTopicRule#firehose}
        :param http: http block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#http IotTopicRule#http}
        :param iot_analytics: iot_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#iot_analytics IotTopicRule#iot_analytics}
        :param iot_events: iot_events block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#iot_events IotTopicRule#iot_events}
        :param kafka: kafka block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#kafka IotTopicRule#kafka}
        :param kinesis: kinesis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#kinesis IotTopicRule#kinesis}
        :param lambda_: lambda block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#lambda IotTopicRule#lambda}
        :param republish: republish block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#republish IotTopicRule#republish}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#s3 IotTopicRule#s3}
        :param sns: sns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#sns IotTopicRule#sns}
        :param sqs: sqs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#sqs IotTopicRule#sqs}
        :param step_functions: step_functions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#step_functions IotTopicRule#step_functions}
        :param timestream: timestream block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#timestream IotTopicRule#timestream}
        '''
        if isinstance(cloudwatch_alarm, dict):
            cloudwatch_alarm = IotTopicRuleErrorActionCloudwatchAlarm(**cloudwatch_alarm)
        if isinstance(cloudwatch_logs, dict):
            cloudwatch_logs = IotTopicRuleErrorActionCloudwatchLogs(**cloudwatch_logs)
        if isinstance(cloudwatch_metric, dict):
            cloudwatch_metric = IotTopicRuleErrorActionCloudwatchMetric(**cloudwatch_metric)
        if isinstance(dynamodb, dict):
            dynamodb = IotTopicRuleErrorActionDynamodb(**dynamodb)
        if isinstance(dynamodbv2, dict):
            dynamodbv2 = IotTopicRuleErrorActionDynamodbv2(**dynamodbv2)
        if isinstance(elasticsearch, dict):
            elasticsearch = IotTopicRuleErrorActionElasticsearch(**elasticsearch)
        if isinstance(firehose, dict):
            firehose = IotTopicRuleErrorActionFirehose(**firehose)
        if isinstance(http, dict):
            http = IotTopicRuleErrorActionHttp(**http)
        if isinstance(iot_analytics, dict):
            iot_analytics = IotTopicRuleErrorActionIotAnalytics(**iot_analytics)
        if isinstance(iot_events, dict):
            iot_events = IotTopicRuleErrorActionIotEvents(**iot_events)
        if isinstance(kafka, dict):
            kafka = IotTopicRuleErrorActionKafka(**kafka)
        if isinstance(kinesis, dict):
            kinesis = IotTopicRuleErrorActionKinesis(**kinesis)
        if isinstance(lambda_, dict):
            lambda_ = IotTopicRuleErrorActionLambda(**lambda_)
        if isinstance(republish, dict):
            republish = IotTopicRuleErrorActionRepublish(**republish)
        if isinstance(s3, dict):
            s3 = IotTopicRuleErrorActionS3(**s3)
        if isinstance(sns, dict):
            sns = IotTopicRuleErrorActionSns(**sns)
        if isinstance(sqs, dict):
            sqs = IotTopicRuleErrorActionSqs(**sqs)
        if isinstance(step_functions, dict):
            step_functions = IotTopicRuleErrorActionStepFunctions(**step_functions)
        if isinstance(timestream, dict):
            timestream = IotTopicRuleErrorActionTimestream(**timestream)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d5218b66bab7b0668e523e8d495820176210dab6e47099ae5ed9bde2e84e1d1)
            check_type(argname="argument cloudwatch_alarm", value=cloudwatch_alarm, expected_type=type_hints["cloudwatch_alarm"])
            check_type(argname="argument cloudwatch_logs", value=cloudwatch_logs, expected_type=type_hints["cloudwatch_logs"])
            check_type(argname="argument cloudwatch_metric", value=cloudwatch_metric, expected_type=type_hints["cloudwatch_metric"])
            check_type(argname="argument dynamodb", value=dynamodb, expected_type=type_hints["dynamodb"])
            check_type(argname="argument dynamodbv2", value=dynamodbv2, expected_type=type_hints["dynamodbv2"])
            check_type(argname="argument elasticsearch", value=elasticsearch, expected_type=type_hints["elasticsearch"])
            check_type(argname="argument firehose", value=firehose, expected_type=type_hints["firehose"])
            check_type(argname="argument http", value=http, expected_type=type_hints["http"])
            check_type(argname="argument iot_analytics", value=iot_analytics, expected_type=type_hints["iot_analytics"])
            check_type(argname="argument iot_events", value=iot_events, expected_type=type_hints["iot_events"])
            check_type(argname="argument kafka", value=kafka, expected_type=type_hints["kafka"])
            check_type(argname="argument kinesis", value=kinesis, expected_type=type_hints["kinesis"])
            check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
            check_type(argname="argument republish", value=republish, expected_type=type_hints["republish"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument sns", value=sns, expected_type=type_hints["sns"])
            check_type(argname="argument sqs", value=sqs, expected_type=type_hints["sqs"])
            check_type(argname="argument step_functions", value=step_functions, expected_type=type_hints["step_functions"])
            check_type(argname="argument timestream", value=timestream, expected_type=type_hints["timestream"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloudwatch_alarm is not None:
            self._values["cloudwatch_alarm"] = cloudwatch_alarm
        if cloudwatch_logs is not None:
            self._values["cloudwatch_logs"] = cloudwatch_logs
        if cloudwatch_metric is not None:
            self._values["cloudwatch_metric"] = cloudwatch_metric
        if dynamodb is not None:
            self._values["dynamodb"] = dynamodb
        if dynamodbv2 is not None:
            self._values["dynamodbv2"] = dynamodbv2
        if elasticsearch is not None:
            self._values["elasticsearch"] = elasticsearch
        if firehose is not None:
            self._values["firehose"] = firehose
        if http is not None:
            self._values["http"] = http
        if iot_analytics is not None:
            self._values["iot_analytics"] = iot_analytics
        if iot_events is not None:
            self._values["iot_events"] = iot_events
        if kafka is not None:
            self._values["kafka"] = kafka
        if kinesis is not None:
            self._values["kinesis"] = kinesis
        if lambda_ is not None:
            self._values["lambda_"] = lambda_
        if republish is not None:
            self._values["republish"] = republish
        if s3 is not None:
            self._values["s3"] = s3
        if sns is not None:
            self._values["sns"] = sns
        if sqs is not None:
            self._values["sqs"] = sqs
        if step_functions is not None:
            self._values["step_functions"] = step_functions
        if timestream is not None:
            self._values["timestream"] = timestream

    @builtins.property
    def cloudwatch_alarm(
        self,
    ) -> typing.Optional["IotTopicRuleErrorActionCloudwatchAlarm"]:
        '''cloudwatch_alarm block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#cloudwatch_alarm IotTopicRule#cloudwatch_alarm}
        '''
        result = self._values.get("cloudwatch_alarm")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionCloudwatchAlarm"], result)

    @builtins.property
    def cloudwatch_logs(
        self,
    ) -> typing.Optional["IotTopicRuleErrorActionCloudwatchLogs"]:
        '''cloudwatch_logs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#cloudwatch_logs IotTopicRule#cloudwatch_logs}
        '''
        result = self._values.get("cloudwatch_logs")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionCloudwatchLogs"], result)

    @builtins.property
    def cloudwatch_metric(
        self,
    ) -> typing.Optional["IotTopicRuleErrorActionCloudwatchMetric"]:
        '''cloudwatch_metric block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#cloudwatch_metric IotTopicRule#cloudwatch_metric}
        '''
        result = self._values.get("cloudwatch_metric")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionCloudwatchMetric"], result)

    @builtins.property
    def dynamodb(self) -> typing.Optional["IotTopicRuleErrorActionDynamodb"]:
        '''dynamodb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#dynamodb IotTopicRule#dynamodb}
        '''
        result = self._values.get("dynamodb")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionDynamodb"], result)

    @builtins.property
    def dynamodbv2(self) -> typing.Optional["IotTopicRuleErrorActionDynamodbv2"]:
        '''dynamodbv2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#dynamodbv2 IotTopicRule#dynamodbv2}
        '''
        result = self._values.get("dynamodbv2")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionDynamodbv2"], result)

    @builtins.property
    def elasticsearch(self) -> typing.Optional["IotTopicRuleErrorActionElasticsearch"]:
        '''elasticsearch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#elasticsearch IotTopicRule#elasticsearch}
        '''
        result = self._values.get("elasticsearch")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionElasticsearch"], result)

    @builtins.property
    def firehose(self) -> typing.Optional["IotTopicRuleErrorActionFirehose"]:
        '''firehose block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#firehose IotTopicRule#firehose}
        '''
        result = self._values.get("firehose")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionFirehose"], result)

    @builtins.property
    def http(self) -> typing.Optional["IotTopicRuleErrorActionHttp"]:
        '''http block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#http IotTopicRule#http}
        '''
        result = self._values.get("http")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionHttp"], result)

    @builtins.property
    def iot_analytics(self) -> typing.Optional["IotTopicRuleErrorActionIotAnalytics"]:
        '''iot_analytics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#iot_analytics IotTopicRule#iot_analytics}
        '''
        result = self._values.get("iot_analytics")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionIotAnalytics"], result)

    @builtins.property
    def iot_events(self) -> typing.Optional["IotTopicRuleErrorActionIotEvents"]:
        '''iot_events block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#iot_events IotTopicRule#iot_events}
        '''
        result = self._values.get("iot_events")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionIotEvents"], result)

    @builtins.property
    def kafka(self) -> typing.Optional["IotTopicRuleErrorActionKafka"]:
        '''kafka block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#kafka IotTopicRule#kafka}
        '''
        result = self._values.get("kafka")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionKafka"], result)

    @builtins.property
    def kinesis(self) -> typing.Optional["IotTopicRuleErrorActionKinesis"]:
        '''kinesis block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#kinesis IotTopicRule#kinesis}
        '''
        result = self._values.get("kinesis")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionKinesis"], result)

    @builtins.property
    def lambda_(self) -> typing.Optional["IotTopicRuleErrorActionLambda"]:
        '''lambda block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#lambda IotTopicRule#lambda}
        '''
        result = self._values.get("lambda_")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionLambda"], result)

    @builtins.property
    def republish(self) -> typing.Optional["IotTopicRuleErrorActionRepublish"]:
        '''republish block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#republish IotTopicRule#republish}
        '''
        result = self._values.get("republish")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionRepublish"], result)

    @builtins.property
    def s3(self) -> typing.Optional["IotTopicRuleErrorActionS3"]:
        '''s3 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#s3 IotTopicRule#s3}
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionS3"], result)

    @builtins.property
    def sns(self) -> typing.Optional["IotTopicRuleErrorActionSns"]:
        '''sns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#sns IotTopicRule#sns}
        '''
        result = self._values.get("sns")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionSns"], result)

    @builtins.property
    def sqs(self) -> typing.Optional["IotTopicRuleErrorActionSqs"]:
        '''sqs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#sqs IotTopicRule#sqs}
        '''
        result = self._values.get("sqs")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionSqs"], result)

    @builtins.property
    def step_functions(self) -> typing.Optional["IotTopicRuleErrorActionStepFunctions"]:
        '''step_functions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#step_functions IotTopicRule#step_functions}
        '''
        result = self._values.get("step_functions")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionStepFunctions"], result)

    @builtins.property
    def timestream(self) -> typing.Optional["IotTopicRuleErrorActionTimestream"]:
        '''timestream block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#timestream IotTopicRule#timestream}
        '''
        result = self._values.get("timestream")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionTimestream"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionCloudwatchAlarm",
    jsii_struct_bases=[],
    name_mapping={
        "alarm_name": "alarmName",
        "role_arn": "roleArn",
        "state_reason": "stateReason",
        "state_value": "stateValue",
    },
)
class IotTopicRuleErrorActionCloudwatchAlarm:
    def __init__(
        self,
        *,
        alarm_name: builtins.str,
        role_arn: builtins.str,
        state_reason: builtins.str,
        state_value: builtins.str,
    ) -> None:
        '''
        :param alarm_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#alarm_name IotTopicRule#alarm_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param state_reason: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#state_reason IotTopicRule#state_reason}.
        :param state_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#state_value IotTopicRule#state_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31ec52e73f453a37aaa910eee67b494d2e65ebcf71eef4a8315fd9325844b0ff)
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument state_reason", value=state_reason, expected_type=type_hints["state_reason"])
            check_type(argname="argument state_value", value=state_value, expected_type=type_hints["state_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alarm_name": alarm_name,
            "role_arn": role_arn,
            "state_reason": state_reason,
            "state_value": state_value,
        }

    @builtins.property
    def alarm_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#alarm_name IotTopicRule#alarm_name}.'''
        result = self._values.get("alarm_name")
        assert result is not None, "Required property 'alarm_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state_reason(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#state_reason IotTopicRule#state_reason}.'''
        result = self._values.get("state_reason")
        assert result is not None, "Required property 'state_reason' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#state_value IotTopicRule#state_value}.'''
        result = self._values.get("state_value")
        assert result is not None, "Required property 'state_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionCloudwatchAlarm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionCloudwatchAlarmOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionCloudwatchAlarmOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d961dc75e0afa1e0f4d62d603b4d8cb2c80c59c2ae704d94409d1e79668c41b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="alarmNameInput")
    def alarm_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alarmNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="stateReasonInput")
    def state_reason_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateReasonInput"))

    @builtins.property
    @jsii.member(jsii_name="stateValueInput")
    def state_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateValueInput"))

    @builtins.property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alarmName"))

    @alarm_name.setter
    def alarm_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9658585f4fbf4fe47e2f077f5335680d54403fc3a6c389474f58b64ca2eb9414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3145eb0c30048a377434f8be190e2de41b50afdabac121aafd52f165eebd9ca3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stateReason")
    def state_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateReason"))

    @state_reason.setter
    def state_reason(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11b7044d43ca3975a9503a1f310fb0280c75f0d9e8ebfc644522dfd66dffcd09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stateReason", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stateValue")
    def state_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateValue"))

    @state_value.setter
    def state_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f660d6461d801dd04eaab028b485404880a3c05f0d39316fbe825e9c98bd300)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stateValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionCloudwatchAlarm]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionCloudwatchAlarm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionCloudwatchAlarm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21a37e009bb2f53cadb702f1ecbf64345d3e966dfa5925b7173343911ddd7696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionCloudwatchLogs",
    jsii_struct_bases=[],
    name_mapping={
        "log_group_name": "logGroupName",
        "role_arn": "roleArn",
        "batch_mode": "batchMode",
    },
)
class IotTopicRuleErrorActionCloudwatchLogs:
    def __init__(
        self,
        *,
        log_group_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param log_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#log_group_name IotTopicRule#log_group_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__257012640b51813558139969c202d4368478abe1067fd1dbb5134e7f686c513e)
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument batch_mode", value=batch_mode, expected_type=type_hints["batch_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group_name": log_group_name,
            "role_arn": role_arn,
        }
        if batch_mode is not None:
            self._values["batch_mode"] = batch_mode

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#log_group_name IotTopicRule#log_group_name}.'''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.'''
        result = self._values.get("batch_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionCloudwatchLogs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionCloudwatchLogsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionCloudwatchLogsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdc62889bca2f770ace431f39e532fc8c3b4aff3f6aaa1b59eff6dd3ea80153c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBatchMode")
    def reset_batch_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchMode", []))

    @builtins.property
    @jsii.member(jsii_name="batchModeInput")
    def batch_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "batchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupNameInput")
    def log_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="batchMode")
    def batch_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "batchMode"))

    @batch_mode.setter
    def batch_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ea89f5b0962c5352943948dc3f34bb23c983d5b0b544c545c2c3456376348f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__002b6f278e4b4dd2a58d6319e976e8acdeda7a8a4f8f0ccd6e39684f56643895)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deb9981a05e3b200d4412029275e30757cdfcfb3ac1763ae3c17cd2d9ce04f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionCloudwatchLogs]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionCloudwatchLogs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionCloudwatchLogs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f20711efa311b3af460609d9e2b9908d815d213b2bd238c0c228b232f654355)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionCloudwatchMetric",
    jsii_struct_bases=[],
    name_mapping={
        "metric_name": "metricName",
        "metric_namespace": "metricNamespace",
        "metric_unit": "metricUnit",
        "metric_value": "metricValue",
        "role_arn": "roleArn",
        "metric_timestamp": "metricTimestamp",
    },
)
class IotTopicRuleErrorActionCloudwatchMetric:
    def __init__(
        self,
        *,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        metric_unit: builtins.str,
        metric_value: builtins.str,
        role_arn: builtins.str,
        metric_timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metric_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_name IotTopicRule#metric_name}.
        :param metric_namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_namespace IotTopicRule#metric_namespace}.
        :param metric_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_unit IotTopicRule#metric_unit}.
        :param metric_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_value IotTopicRule#metric_value}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param metric_timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_timestamp IotTopicRule#metric_timestamp}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be5658fae73dcd7ae5a7f368c98c3a48d56f2ae6484971644df06ed4474ae994)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument metric_unit", value=metric_unit, expected_type=type_hints["metric_unit"])
            check_type(argname="argument metric_value", value=metric_value, expected_type=type_hints["metric_value"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument metric_timestamp", value=metric_timestamp, expected_type=type_hints["metric_timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_name": metric_name,
            "metric_namespace": metric_namespace,
            "metric_unit": metric_unit,
            "metric_value": metric_value,
            "role_arn": role_arn,
        }
        if metric_timestamp is not None:
            self._values["metric_timestamp"] = metric_timestamp

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_name IotTopicRule#metric_name}.'''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_namespace(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_namespace IotTopicRule#metric_namespace}.'''
        result = self._values.get("metric_namespace")
        assert result is not None, "Required property 'metric_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_unit IotTopicRule#metric_unit}.'''
        result = self._values.get("metric_unit")
        assert result is not None, "Required property 'metric_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_value IotTopicRule#metric_value}.'''
        result = self._values.get("metric_value")
        assert result is not None, "Required property 'metric_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_timestamp(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_timestamp IotTopicRule#metric_timestamp}.'''
        result = self._values.get("metric_timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionCloudwatchMetric(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionCloudwatchMetricOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionCloudwatchMetricOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20fd375ef64c508e107e31dd21af226070098af2fa28fb737a9f5627cba4fc25)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricTimestamp")
    def reset_metric_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricTimestamp", []))

    @builtins.property
    @jsii.member(jsii_name="metricNameInput")
    def metric_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricNameInput"))

    @builtins.property
    @jsii.member(jsii_name="metricNamespaceInput")
    def metric_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="metricTimestampInput")
    def metric_timestamp_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricTimestampInput"))

    @builtins.property
    @jsii.member(jsii_name="metricUnitInput")
    def metric_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="metricValueInput")
    def metric_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricValueInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricName"))

    @metric_name.setter
    def metric_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be4882ce8e99b16a5d5126d72564557bdb6d5292c4506369b0e41ca779672d52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricNamespace")
    def metric_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricNamespace"))

    @metric_namespace.setter
    def metric_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f105f887cd86d213d0fceb98fca178c5e6cdb8909c8c26f5c5dae704137eb740)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricTimestamp")
    def metric_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricTimestamp"))

    @metric_timestamp.setter
    def metric_timestamp(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a2173244eeeeec39653b1ae7838722815c97a7466b225d235ab9d1bba5287ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricTimestamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricUnit")
    def metric_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricUnit"))

    @metric_unit.setter
    def metric_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbae9c6d8a0adc188fc06e127d5bfcf177ecdd71ab34503217f71396d32e01c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricValue")
    def metric_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricValue"))

    @metric_value.setter
    def metric_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e16b5eb63a6a1fe86677fe9e892f786cf72dacdb04a5f0a75188005873489f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42a9d4939f24132dd55bdabfd70c9abd441ebfebd2fc9071d542e52142edd57c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IotTopicRuleErrorActionCloudwatchMetric]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionCloudwatchMetric], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionCloudwatchMetric],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e12a0a24f3078a904169462dd3de5e1096f5e9fb17f3641f448854addf476285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionDynamodb",
    jsii_struct_bases=[],
    name_mapping={
        "hash_key_field": "hashKeyField",
        "hash_key_value": "hashKeyValue",
        "role_arn": "roleArn",
        "table_name": "tableName",
        "hash_key_type": "hashKeyType",
        "operation": "operation",
        "payload_field": "payloadField",
        "range_key_field": "rangeKeyField",
        "range_key_type": "rangeKeyType",
        "range_key_value": "rangeKeyValue",
    },
)
class IotTopicRuleErrorActionDynamodb:
    def __init__(
        self,
        *,
        hash_key_field: builtins.str,
        hash_key_value: builtins.str,
        role_arn: builtins.str,
        table_name: builtins.str,
        hash_key_type: typing.Optional[builtins.str] = None,
        operation: typing.Optional[builtins.str] = None,
        payload_field: typing.Optional[builtins.str] = None,
        range_key_field: typing.Optional[builtins.str] = None,
        range_key_type: typing.Optional[builtins.str] = None,
        range_key_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hash_key_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#hash_key_field IotTopicRule#hash_key_field}.
        :param hash_key_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#hash_key_value IotTopicRule#hash_key_value}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.
        :param hash_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#hash_key_type IotTopicRule#hash_key_type}.
        :param operation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#operation IotTopicRule#operation}.
        :param payload_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#payload_field IotTopicRule#payload_field}.
        :param range_key_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#range_key_field IotTopicRule#range_key_field}.
        :param range_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#range_key_type IotTopicRule#range_key_type}.
        :param range_key_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#range_key_value IotTopicRule#range_key_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f625d24ea319b6ca47f9b9a94ff9769b5b324f7779d6808f8527f0780c5a6151)
            check_type(argname="argument hash_key_field", value=hash_key_field, expected_type=type_hints["hash_key_field"])
            check_type(argname="argument hash_key_value", value=hash_key_value, expected_type=type_hints["hash_key_value"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument hash_key_type", value=hash_key_type, expected_type=type_hints["hash_key_type"])
            check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
            check_type(argname="argument payload_field", value=payload_field, expected_type=type_hints["payload_field"])
            check_type(argname="argument range_key_field", value=range_key_field, expected_type=type_hints["range_key_field"])
            check_type(argname="argument range_key_type", value=range_key_type, expected_type=type_hints["range_key_type"])
            check_type(argname="argument range_key_value", value=range_key_value, expected_type=type_hints["range_key_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hash_key_field": hash_key_field,
            "hash_key_value": hash_key_value,
            "role_arn": role_arn,
            "table_name": table_name,
        }
        if hash_key_type is not None:
            self._values["hash_key_type"] = hash_key_type
        if operation is not None:
            self._values["operation"] = operation
        if payload_field is not None:
            self._values["payload_field"] = payload_field
        if range_key_field is not None:
            self._values["range_key_field"] = range_key_field
        if range_key_type is not None:
            self._values["range_key_type"] = range_key_type
        if range_key_value is not None:
            self._values["range_key_value"] = range_key_value

    @builtins.property
    def hash_key_field(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#hash_key_field IotTopicRule#hash_key_field}.'''
        result = self._values.get("hash_key_field")
        assert result is not None, "Required property 'hash_key_field' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hash_key_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#hash_key_value IotTopicRule#hash_key_value}.'''
        result = self._values.get("hash_key_value")
        assert result is not None, "Required property 'hash_key_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.'''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hash_key_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#hash_key_type IotTopicRule#hash_key_type}.'''
        result = self._values.get("hash_key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#operation IotTopicRule#operation}.'''
        result = self._values.get("operation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def payload_field(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#payload_field IotTopicRule#payload_field}.'''
        result = self._values.get("payload_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def range_key_field(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#range_key_field IotTopicRule#range_key_field}.'''
        result = self._values.get("range_key_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def range_key_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#range_key_type IotTopicRule#range_key_type}.'''
        result = self._values.get("range_key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def range_key_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#range_key_value IotTopicRule#range_key_value}.'''
        result = self._values.get("range_key_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionDynamodb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionDynamodbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionDynamodbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39d386780a825da6a356fdd684436be2a39c6528e0f47031be59291180d0dbf8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHashKeyType")
    def reset_hash_key_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHashKeyType", []))

    @jsii.member(jsii_name="resetOperation")
    def reset_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperation", []))

    @jsii.member(jsii_name="resetPayloadField")
    def reset_payload_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPayloadField", []))

    @jsii.member(jsii_name="resetRangeKeyField")
    def reset_range_key_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRangeKeyField", []))

    @jsii.member(jsii_name="resetRangeKeyType")
    def reset_range_key_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRangeKeyType", []))

    @jsii.member(jsii_name="resetRangeKeyValue")
    def reset_range_key_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRangeKeyValue", []))

    @builtins.property
    @jsii.member(jsii_name="hashKeyFieldInput")
    def hash_key_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hashKeyFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="hashKeyTypeInput")
    def hash_key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hashKeyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="hashKeyValueInput")
    def hash_key_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hashKeyValueInput"))

    @builtins.property
    @jsii.member(jsii_name="operationInput")
    def operation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadFieldInput")
    def payload_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "payloadFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeKeyFieldInput")
    def range_key_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rangeKeyFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeKeyTypeInput")
    def range_key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rangeKeyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeKeyValueInput")
    def range_key_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rangeKeyValueInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="hashKeyField")
    def hash_key_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hashKeyField"))

    @hash_key_field.setter
    def hash_key_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab2b629fd278d624dfb809faf2cfa0d46ae405924b3953f2c9adc397cf5ea973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hashKeyField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hashKeyType")
    def hash_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hashKeyType"))

    @hash_key_type.setter
    def hash_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a6a38c3ddc07d2d7950d80624b65b10392a53706c081f7eb8a61ed8d606085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hashKeyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hashKeyValue")
    def hash_key_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hashKeyValue"))

    @hash_key_value.setter
    def hash_key_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1665f1a41b11535621723e6d4b93702159a17e78fb6bc0a2e914055ceec85eae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hashKeyValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operation")
    def operation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operation"))

    @operation.setter
    def operation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eacc234eff1ec97e00f1443ef32be666023dd66e4718fe6cb35a597645a9c973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="payloadField")
    def payload_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "payloadField"))

    @payload_field.setter
    def payload_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a10cd62f267fe404a711726c1f636fb79dfedbe2c4947d160bce06f3d15604ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payloadField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rangeKeyField")
    def range_key_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rangeKeyField"))

    @range_key_field.setter
    def range_key_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31bd8d22fa206e441e9c7e3868784fd0974fdda4937d7842aeb775bc94fc5994)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rangeKeyField", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rangeKeyType")
    def range_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rangeKeyType"))

    @range_key_type.setter
    def range_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e9406736a39c56084d3d5c7eeec3587d68a4ab058ede4445bdd0e31ee4a637f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rangeKeyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rangeKeyValue")
    def range_key_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rangeKeyValue"))

    @range_key_value.setter
    def range_key_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d8a442c8a31051f88cb150c69ea7eced1a29a7723de635d887af8338962e9cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rangeKeyValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c6cddeb5340592761116767fb98ea939c7c93799e04ff418d5aaa3d8e74c613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f9e51da26e1b0775a35ec706f9d33f86efd3e8a68c73898693fca819c9f7fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionDynamodb]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionDynamodb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionDynamodb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c2d37b766eea6eb078a892c62db3878e058547ed940d6971c5a08f928c61c1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionDynamodbv2",
    jsii_struct_bases=[],
    name_mapping={"role_arn": "roleArn", "put_item": "putItem"},
)
class IotTopicRuleErrorActionDynamodbv2:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        put_item: typing.Optional[typing.Union["IotTopicRuleErrorActionDynamodbv2PutItem", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param put_item: put_item block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#put_item IotTopicRule#put_item}
        '''
        if isinstance(put_item, dict):
            put_item = IotTopicRuleErrorActionDynamodbv2PutItem(**put_item)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48ef4a5b7dc9fb57b6ee79fbfd677e4bc81a97636d13180db9e739be8ceabfb5)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument put_item", value=put_item, expected_type=type_hints["put_item"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
        }
        if put_item is not None:
            self._values["put_item"] = put_item

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def put_item(self) -> typing.Optional["IotTopicRuleErrorActionDynamodbv2PutItem"]:
        '''put_item block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#put_item IotTopicRule#put_item}
        '''
        result = self._values.get("put_item")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionDynamodbv2PutItem"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionDynamodbv2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionDynamodbv2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionDynamodbv2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a567a67e0ec2a934e719d009b2d715e8d0d29e78ad950eae92b618f00fedeaf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPutItem")
    def put_put_item(self, *, table_name: builtins.str) -> None:
        '''
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.
        '''
        value = IotTopicRuleErrorActionDynamodbv2PutItem(table_name=table_name)

        return typing.cast(None, jsii.invoke(self, "putPutItem", [value]))

    @jsii.member(jsii_name="resetPutItem")
    def reset_put_item(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPutItem", []))

    @builtins.property
    @jsii.member(jsii_name="putItem")
    def put_item(self) -> "IotTopicRuleErrorActionDynamodbv2PutItemOutputReference":
        return typing.cast("IotTopicRuleErrorActionDynamodbv2PutItemOutputReference", jsii.get(self, "putItem"))

    @builtins.property
    @jsii.member(jsii_name="putItemInput")
    def put_item_input(
        self,
    ) -> typing.Optional["IotTopicRuleErrorActionDynamodbv2PutItem"]:
        return typing.cast(typing.Optional["IotTopicRuleErrorActionDynamodbv2PutItem"], jsii.get(self, "putItemInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf91bcf1f323b8b4afe632d6098c9906c18afe2965c013785e9beb680c66e7b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionDynamodbv2]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionDynamodbv2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionDynamodbv2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46bb8221b2f5cba8d8f5c1d7128f7c36abc5002235c215404be811f89a32c06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionDynamodbv2PutItem",
    jsii_struct_bases=[],
    name_mapping={"table_name": "tableName"},
)
class IotTopicRuleErrorActionDynamodbv2PutItem:
    def __init__(self, *, table_name: builtins.str) -> None:
        '''
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2163d3f19b374dcef0582cdba51feba84618ce5d727f2393021db5898a827479)
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table_name": table_name,
        }

    @builtins.property
    def table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.'''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionDynamodbv2PutItem(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionDynamodbv2PutItemOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionDynamodbv2PutItemOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31a3ef2646b9efdc001e9201919dc3f7aec6851f1361cf8a58497c0e9e259f9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__ade47b2cb411151808e3ec61701e4c38a31c51974ccb2b8e1332675789743564)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IotTopicRuleErrorActionDynamodbv2PutItem]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionDynamodbv2PutItem], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionDynamodbv2PutItem],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1eea2814da2ada7025dbd8ef87f1846f135aba54031f03dd1d82426ac8300b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionElasticsearch",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint": "endpoint",
        "id": "id",
        "index": "index",
        "role_arn": "roleArn",
        "type": "type",
    },
)
class IotTopicRuleErrorActionElasticsearch:
    def __init__(
        self,
        *,
        endpoint: builtins.str,
        id: builtins.str,
        index: builtins.str,
        role_arn: builtins.str,
        type: builtins.str,
    ) -> None:
        '''
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#endpoint IotTopicRule#endpoint}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#id IotTopicRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#index IotTopicRule#index}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#type IotTopicRule#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32b0d55420f69ec18f229d27a3d5007ba854a951103638a1aa72efd9671c10a8)
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint": endpoint,
            "id": id,
            "index": index,
            "role_arn": role_arn,
            "type": type,
        }

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#endpoint IotTopicRule#endpoint}.'''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#id IotTopicRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def index(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#index IotTopicRule#index}.'''
        result = self._values.get("index")
        assert result is not None, "Required property 'index' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#type IotTopicRule#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionElasticsearch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionElasticsearchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionElasticsearchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5b64e14fd8ed646ec052285cac354e2f10e01287fc229897fb28029cf0d3df4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="indexInput")
    def index_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d295eacfb1e93c4a52245a5f04554b420ddfeca15ffb1bea69c69ada4dc1edb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7dde59ff47162f880f81fc93f15e8068c0ea75b5605488a0723fccca0411e4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="index")
    def index(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "index"))

    @index.setter
    def index(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2addc828b97d2230129127650f74e934e3983eeae49c6d1396f0910170586a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "index", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9d2f0f40e4618507adc07532c6c0d523a86caabdd25d2094c6923d61ad3cb8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f84237e9d1403dfc70d731a674a5d7e304cefa1e9fab1b06514f583a21ada52c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionElasticsearch]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionElasticsearch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionElasticsearch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bd8bc81237e95a5b93efd2ada59a7bc4e2077da3bf31367122a49e5ba6483b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionFirehose",
    jsii_struct_bases=[],
    name_mapping={
        "delivery_stream_name": "deliveryStreamName",
        "role_arn": "roleArn",
        "batch_mode": "batchMode",
        "separator": "separator",
    },
)
class IotTopicRuleErrorActionFirehose:
    def __init__(
        self,
        *,
        delivery_stream_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        separator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delivery_stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#delivery_stream_name IotTopicRule#delivery_stream_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        :param separator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#separator IotTopicRule#separator}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd6474100e82d11b9b62a8d8948b95e543e71711cb623d56657077bacd4e00c1)
            check_type(argname="argument delivery_stream_name", value=delivery_stream_name, expected_type=type_hints["delivery_stream_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument batch_mode", value=batch_mode, expected_type=type_hints["batch_mode"])
            check_type(argname="argument separator", value=separator, expected_type=type_hints["separator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delivery_stream_name": delivery_stream_name,
            "role_arn": role_arn,
        }
        if batch_mode is not None:
            self._values["batch_mode"] = batch_mode
        if separator is not None:
            self._values["separator"] = separator

    @builtins.property
    def delivery_stream_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#delivery_stream_name IotTopicRule#delivery_stream_name}.'''
        result = self._values.get("delivery_stream_name")
        assert result is not None, "Required property 'delivery_stream_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.'''
        result = self._values.get("batch_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def separator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#separator IotTopicRule#separator}.'''
        result = self._values.get("separator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionFirehose(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionFirehoseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionFirehoseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__917b697065eeb5ae19110f55a10af04f98051f27f81b0252891b709f4576c1c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBatchMode")
    def reset_batch_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchMode", []))

    @jsii.member(jsii_name="resetSeparator")
    def reset_separator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeparator", []))

    @builtins.property
    @jsii.member(jsii_name="batchModeInput")
    def batch_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "batchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamNameInput")
    def delivery_stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deliveryStreamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="separatorInput")
    def separator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "separatorInput"))

    @builtins.property
    @jsii.member(jsii_name="batchMode")
    def batch_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "batchMode"))

    @batch_mode.setter
    def batch_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85625a6e613a797f86631a28e41b3a5f5cd358323bcd0c98a54016e4613d6950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamName")
    def delivery_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deliveryStreamName"))

    @delivery_stream_name.setter
    def delivery_stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b09a5e74be52f6719efc668eb0ce240d286eb74f47f886634f67264175ce7531)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deliveryStreamName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bef889c77fa63834ef28596c8bece994dc9f0c65a99f5e15d46f8d63c99fa243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="separator")
    def separator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "separator"))

    @separator.setter
    def separator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbf53ec60048478af350b7a5121141ba648e8d7ac20f044ddbb58d4db454bc18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "separator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionFirehose]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionFirehose], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionFirehose],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1effc66ab2ef16fe7b5e0b0e32fd1e3a58cee84b6557cec3b7e55e83a8c7e873)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionHttp",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "confirmation_url": "confirmationUrl",
        "http_header": "httpHeader",
    },
)
class IotTopicRuleErrorActionHttp:
    def __init__(
        self,
        *,
        url: builtins.str,
        confirmation_url: typing.Optional[builtins.str] = None,
        http_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleErrorActionHttpHttpHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#url IotTopicRule#url}.
        :param confirmation_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#confirmation_url IotTopicRule#confirmation_url}.
        :param http_header: http_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#http_header IotTopicRule#http_header}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61ff4e2b0982a09252aa6fecc02cf8d2294de1d4e3a5005937f3ace8bae1ea7d)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument confirmation_url", value=confirmation_url, expected_type=type_hints["confirmation_url"])
            check_type(argname="argument http_header", value=http_header, expected_type=type_hints["http_header"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if confirmation_url is not None:
            self._values["confirmation_url"] = confirmation_url
        if http_header is not None:
            self._values["http_header"] = http_header

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#url IotTopicRule#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def confirmation_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#confirmation_url IotTopicRule#confirmation_url}.'''
        result = self._values.get("confirmation_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleErrorActionHttpHttpHeader"]]]:
        '''http_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#http_header IotTopicRule#http_header}
        '''
        result = self._values.get("http_header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleErrorActionHttpHttpHeader"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionHttp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionHttpHttpHeader",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class IotTopicRuleErrorActionHttpHttpHeader:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3161a5617435a1a7e3e81bfcd2d0b691859e6c4be738d326e93874d49a7d1977)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionHttpHttpHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionHttpHttpHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionHttpHttpHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28fcb8fff41725f63d255289236e0e439671a95542bf9c05c14e54e1cb57fd53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IotTopicRuleErrorActionHttpHttpHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d75905c228715d12b25853189bb6327391b17e48f99eea410263d2b26ef0b1b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleErrorActionHttpHttpHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7e445cbea33f38a7f583c111d1ac753f03de5e43b1addcd2c16ed6bba65c73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9880e1e6ef2e268078ea583fb9e1c0c553c7dbda1fa2c02ad3c23db8af70bfee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68c135c06a8b14e6fa6feb700d4e107bbc98d1cb734c26c96f317faf93742449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionHttpHttpHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionHttpHttpHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionHttpHttpHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01ec591d82b0c7c9f20c99e2d9130eb1af9f8a94dd38d4aa35fd0ae1055708d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleErrorActionHttpHttpHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionHttpHttpHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32472a8ae63cc40eaf0c5d0412e7d626f60fabbf06e1e95a1d7bcb7538aa5582)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db853ac4ef6ec9cb9a6d0cf18c5333dc6e4f13a08cf0945f4f75953e791c6dad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__032409b3ac5a2c81592e4246eed04cdd2f5b87b718d765c94fc62864a2d3f8d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionHttpHttpHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionHttpHttpHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionHttpHttpHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7107347bdd62c313e7e1620ff29a9f9854c9faf48cc7739b9498f9ed8ddbb089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleErrorActionHttpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionHttpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fe695b9718105bfd6a212a76af9f3931c338f9b3f9c9c06ce04e76afaaa7fc6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpHeader")
    def put_http_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionHttpHttpHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4af0c69107be95058a146e295e5d86c650703e4967e5f00cae7d6d7b0cdf8b21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttpHeader", [value]))

    @jsii.member(jsii_name="resetConfirmationUrl")
    def reset_confirmation_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfirmationUrl", []))

    @jsii.member(jsii_name="resetHttpHeader")
    def reset_http_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpHeader", []))

    @builtins.property
    @jsii.member(jsii_name="httpHeader")
    def http_header(self) -> IotTopicRuleErrorActionHttpHttpHeaderList:
        return typing.cast(IotTopicRuleErrorActionHttpHttpHeaderList, jsii.get(self, "httpHeader"))

    @builtins.property
    @jsii.member(jsii_name="confirmationUrlInput")
    def confirmation_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "confirmationUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHeaderInput")
    def http_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionHttpHttpHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionHttpHttpHeader]]], jsii.get(self, "httpHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="confirmationUrl")
    def confirmation_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "confirmationUrl"))

    @confirmation_url.setter
    def confirmation_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b936d5b14781da253869e2f6aec723de3bae78edc7b1bc573a54edb5078e0aae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confirmationUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd1f584ed27d642c538aaaf3e1ef2faa83df8b12148f10742c2364a158e416a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionHttp]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionHttp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionHttp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce5addf0629625645ee977f096d38e8e4b270079d5e581b1f358974650486e01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionIotAnalytics",
    jsii_struct_bases=[],
    name_mapping={
        "channel_name": "channelName",
        "role_arn": "roleArn",
        "batch_mode": "batchMode",
    },
)
class IotTopicRuleErrorActionIotAnalytics:
    def __init__(
        self,
        *,
        channel_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param channel_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#channel_name IotTopicRule#channel_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e6d2b6c494a29402c882da3e80e101f54e00f16743f80775552d04e82b867c6)
            check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument batch_mode", value=batch_mode, expected_type=type_hints["batch_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "channel_name": channel_name,
            "role_arn": role_arn,
        }
        if batch_mode is not None:
            self._values["batch_mode"] = batch_mode

    @builtins.property
    def channel_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#channel_name IotTopicRule#channel_name}.'''
        result = self._values.get("channel_name")
        assert result is not None, "Required property 'channel_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.'''
        result = self._values.get("batch_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionIotAnalytics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionIotAnalyticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionIotAnalyticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__328350afc87c374b8cdaa61fe68c2c0172084e9c4c4752383edbce58b3169912)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBatchMode")
    def reset_batch_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchMode", []))

    @builtins.property
    @jsii.member(jsii_name="batchModeInput")
    def batch_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "batchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="channelNameInput")
    def channel_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "channelNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="batchMode")
    def batch_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "batchMode"))

    @batch_mode.setter
    def batch_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2238ab70dd4b62847e99fad2190d3d1816cdd7de31f8c28aea90bbe03fa8fb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="channelName")
    def channel_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channelName"))

    @channel_name.setter
    def channel_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b093b93c1775f342cd2f75a25373a86e972f0627f44ef4be1abff1b246e00d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9986631e35a6c61b0271fff8229b0b36be23a6bca96aff450da00e9c69d44fba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionIotAnalytics]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionIotAnalytics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionIotAnalytics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3e0039e960bc861f800af710dd30cd002e7799963656d1b43ba5d2ecafc8109)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionIotEvents",
    jsii_struct_bases=[],
    name_mapping={
        "input_name": "inputName",
        "role_arn": "roleArn",
        "batch_mode": "batchMode",
        "message_id": "messageId",
    },
)
class IotTopicRuleErrorActionIotEvents:
    def __init__(
        self,
        *,
        input_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        message_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param input_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#input_name IotTopicRule#input_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        :param message_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#message_id IotTopicRule#message_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4eb7ed2a537711e6afbdce3ba52c1c62ccdcb4b1abe503bc0ecaf71b64d9257)
            check_type(argname="argument input_name", value=input_name, expected_type=type_hints["input_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument batch_mode", value=batch_mode, expected_type=type_hints["batch_mode"])
            check_type(argname="argument message_id", value=message_id, expected_type=type_hints["message_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "input_name": input_name,
            "role_arn": role_arn,
        }
        if batch_mode is not None:
            self._values["batch_mode"] = batch_mode
        if message_id is not None:
            self._values["message_id"] = message_id

    @builtins.property
    def input_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#input_name IotTopicRule#input_name}.'''
        result = self._values.get("input_name")
        assert result is not None, "Required property 'input_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.'''
        result = self._values.get("batch_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def message_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#message_id IotTopicRule#message_id}.'''
        result = self._values.get("message_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionIotEvents(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionIotEventsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionIotEventsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c14c802539ee07fdb780e2bdb83fa593db32db5dcae1d79a21f563daea33569f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBatchMode")
    def reset_batch_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchMode", []))

    @jsii.member(jsii_name="resetMessageId")
    def reset_message_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageId", []))

    @builtins.property
    @jsii.member(jsii_name="batchModeInput")
    def batch_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "batchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="inputNameInput")
    def input_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputNameInput"))

    @builtins.property
    @jsii.member(jsii_name="messageIdInput")
    def message_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageIdInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="batchMode")
    def batch_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "batchMode"))

    @batch_mode.setter
    def batch_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73243d0b4f372aaeea96d46bb50cf82341423d6803663610828e284e7729e1fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputName")
    def input_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inputName"))

    @input_name.setter
    def input_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db92210a8e2c44ea227baca481d2f5d78ac73f2a1565cc387c708092c7b27d5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="messageId")
    def message_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageId"))

    @message_id.setter
    def message_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2da3aa713de1e14d4b960fa02b47ee4d691c143d6981a596ea9c47b5a628761a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c61fe6fd37eb777fb63f6c4fae2b2e47c1017521a05194c88836880cfbe1e52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionIotEvents]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionIotEvents], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionIotEvents],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__292e6f309cec8d33807b833b7c02749753713e2d1147e696d51388e2bdeadb88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionKafka",
    jsii_struct_bases=[],
    name_mapping={
        "client_properties": "clientProperties",
        "destination_arn": "destinationArn",
        "topic": "topic",
        "header": "header",
        "key": "key",
        "partition": "partition",
    },
)
class IotTopicRuleErrorActionKafka:
    def __init__(
        self,
        *,
        client_properties: typing.Mapping[builtins.str, builtins.str],
        destination_arn: builtins.str,
        topic: builtins.str,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleErrorActionKafkaHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        key: typing.Optional[builtins.str] = None,
        partition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#client_properties IotTopicRule#client_properties}.
        :param destination_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#destination_arn IotTopicRule#destination_arn}.
        :param topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#topic IotTopicRule#topic}.
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#header IotTopicRule#header}
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.
        :param partition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#partition IotTopicRule#partition}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__382b961f835e2c7ece842a763415d0225e58f1e92e8285686687b2d3d88b77ef)
            check_type(argname="argument client_properties", value=client_properties, expected_type=type_hints["client_properties"])
            check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument partition", value=partition, expected_type=type_hints["partition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_properties": client_properties,
            "destination_arn": destination_arn,
            "topic": topic,
        }
        if header is not None:
            self._values["header"] = header
        if key is not None:
            self._values["key"] = key
        if partition is not None:
            self._values["partition"] = partition

    @builtins.property
    def client_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#client_properties IotTopicRule#client_properties}.'''
        result = self._values.get("client_properties")
        assert result is not None, "Required property 'client_properties' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def destination_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#destination_arn IotTopicRule#destination_arn}.'''
        result = self._values.get("destination_arn")
        assert result is not None, "Required property 'destination_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#topic IotTopicRule#topic}.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleErrorActionKafkaHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#header IotTopicRule#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleErrorActionKafkaHeader"]]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#partition IotTopicRule#partition}.'''
        result = self._values.get("partition")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionKafka(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionKafkaHeader",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class IotTopicRuleErrorActionKafkaHeader:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c4abaeaac9481c7fb4925abbbec5d4948b6aa9efc57ed066960a50226405cb)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionKafkaHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionKafkaHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionKafkaHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28e4a3b77775cd7a040f93df2276a35ca2900e3c4d6daa958436932c1a6ef7d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IotTopicRuleErrorActionKafkaHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d028e0265ea74a85a1e605371fccc7882cc6e5a41a8efd2d7c03f73f18538da)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleErrorActionKafkaHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6284954fdbbb781566d3f87895453da8ae515485ef46521049ff5a37820e0ac3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d1ad8512e11f6d34b03845a28b01d3501831ab6d7904dd3287ec0a9744bf780)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f63013e0d9e363b33b6955c097eddc3592cc833bd2a6edca8449922f550f5fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionKafkaHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionKafkaHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionKafkaHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0924af469ae3e7a41eb865c3a8f7efd3ee2ca7a6768135e748cedd79e985dba1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleErrorActionKafkaHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionKafkaHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b58578e42b5f0b0b06998ad01ea52f45f74d12065a4fe93d90c69b4af63cb5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__528cf2cd6eeafd58a6b7b0a267688bd2dcfc98f517b37c0c6c39d31bc29ebc22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e22f0089c02bb44e078194b5776d0f749d7b9841f958a516cf33e26173ac6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionKafkaHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionKafkaHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionKafkaHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0632603bd9c3fd34f5de2b1a67f3ec174278259aaefd02dafa5cde94621b0e9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleErrorActionKafkaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionKafkaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f70ea2e0c13dee64e48269950ccdbe5d7be67c4c3c8df5fcaa0b4d601aa37306)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionKafkaHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__866c22b5ef96c4cb2aad870b325f1e87da72bcca21b8eb677603f7b2bb4ff5f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetPartition")
    def reset_partition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartition", []))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> IotTopicRuleErrorActionKafkaHeaderList:
        return typing.cast(IotTopicRuleErrorActionKafkaHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="clientPropertiesInput")
    def client_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "clientPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationArnInput")
    def destination_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationArnInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionKafkaHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionKafkaHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionInput")
    def partition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partitionInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="clientProperties")
    def client_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "clientProperties"))

    @client_properties.setter
    def client_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71aebbba0e71fd920f1bbdb50c4cd8a198fdf02218b1b047688b50b859d4465e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationArn"))

    @destination_arn.setter
    def destination_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02a632416f85aeb33fc87fc796b93d38b2e8ba7598748876f80064d3a8ccae5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1442c4d7a743f87701884e13deb64bc7f216de2d672575bd3b6ca9af5a906f9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partition")
    def partition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partition"))

    @partition.setter
    def partition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95aad458437235b8a292394f2c66cf3e32883df4b2051421fa4763da380c4b71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93ffb3a949b71a71ea4f6b0285e392b365b8ee6badddba5f9f7a93feaef65b2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionKafka]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionKafka], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionKafka],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1b895d5ce4db645a7916b7b14667c556d779c4d1e0f51fc56c5f9db33572a2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionKinesis",
    jsii_struct_bases=[],
    name_mapping={
        "role_arn": "roleArn",
        "stream_name": "streamName",
        "partition_key": "partitionKey",
    },
)
class IotTopicRuleErrorActionKinesis:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        stream_name: builtins.str,
        partition_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#stream_name IotTopicRule#stream_name}.
        :param partition_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#partition_key IotTopicRule#partition_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b64cda47a53f3f062ab92a434c13c4bacc6e5ef9c20d08996a2df2a572415e5)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
            check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
            "stream_name": stream_name,
        }
        if partition_key is not None:
            self._values["partition_key"] = partition_key

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stream_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#stream_name IotTopicRule#stream_name}.'''
        result = self._values.get("stream_name")
        assert result is not None, "Required property 'stream_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def partition_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#partition_key IotTopicRule#partition_key}.'''
        result = self._values.get("partition_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionKinesis(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionKinesisOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionKinesisOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2868e7b3ee2270d29edfa315f96606f2e8f44532dcb36ac86b657a06abbfd3a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPartitionKey")
    def reset_partition_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartitionKey", []))

    @builtins.property
    @jsii.member(jsii_name="partitionKeyInput")
    def partition_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partitionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="streamNameInput")
    def stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionKey")
    def partition_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partitionKey"))

    @partition_key.setter
    def partition_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5e41e18a1ca33d6a5a31df49933d84353da016b867422d8372ab9799559e928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74116133c2ea69a0d7cc891b36c2449a8df4e0886589d8b27f957b94378ffbf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamName"))

    @stream_name.setter
    def stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dae4ee9d56355afcef84055c10d320bcabf973d6a57a08fdf56347d5c6843099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionKinesis]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionKinesis], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionKinesis],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45498924e68fa8d235991e8d446e517fe78feb47529c0f108e9d899d3b6a0acb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionLambda",
    jsii_struct_bases=[],
    name_mapping={"function_arn": "functionArn"},
)
class IotTopicRuleErrorActionLambda:
    def __init__(self, *, function_arn: builtins.str) -> None:
        '''
        :param function_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#function_arn IotTopicRule#function_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1f41f7c5f9b20ec224dc9634f33ca7c14a1e1a3bf704b62531c0f41a89540d5)
            check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_arn": function_arn,
        }

    @builtins.property
    def function_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#function_arn IotTopicRule#function_arn}.'''
        result = self._values.get("function_arn")
        assert result is not None, "Required property 'function_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionLambda(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionLambdaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionLambdaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d713cb8b50b046611a2871bc578014753359698331ef00641f8f784f1ed311b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="functionArnInput")
    def function_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionArn"))

    @function_arn.setter
    def function_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__255985a8f75ccda3fca47510357177fb16134d03477bd027b4e39c6d41be229b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionLambda]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionLambda], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionLambda],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__598becffe55607c2d38d0d53dbb6c2017e6a8bf711a3cdace5dda79c45c1deae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleErrorActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9242400c9b46cb367af24dc2cfdd1a89168b09db81ea4f2060c193f037878076)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCloudwatchAlarm")
    def put_cloudwatch_alarm(
        self,
        *,
        alarm_name: builtins.str,
        role_arn: builtins.str,
        state_reason: builtins.str,
        state_value: builtins.str,
    ) -> None:
        '''
        :param alarm_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#alarm_name IotTopicRule#alarm_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param state_reason: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#state_reason IotTopicRule#state_reason}.
        :param state_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#state_value IotTopicRule#state_value}.
        '''
        value = IotTopicRuleErrorActionCloudwatchAlarm(
            alarm_name=alarm_name,
            role_arn=role_arn,
            state_reason=state_reason,
            state_value=state_value,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchAlarm", [value]))

    @jsii.member(jsii_name="putCloudwatchLogs")
    def put_cloudwatch_logs(
        self,
        *,
        log_group_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param log_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#log_group_name IotTopicRule#log_group_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        '''
        value = IotTopicRuleErrorActionCloudwatchLogs(
            log_group_name=log_group_name, role_arn=role_arn, batch_mode=batch_mode
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchLogs", [value]))

    @jsii.member(jsii_name="putCloudwatchMetric")
    def put_cloudwatch_metric(
        self,
        *,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        metric_unit: builtins.str,
        metric_value: builtins.str,
        role_arn: builtins.str,
        metric_timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metric_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_name IotTopicRule#metric_name}.
        :param metric_namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_namespace IotTopicRule#metric_namespace}.
        :param metric_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_unit IotTopicRule#metric_unit}.
        :param metric_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_value IotTopicRule#metric_value}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param metric_timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#metric_timestamp IotTopicRule#metric_timestamp}.
        '''
        value = IotTopicRuleErrorActionCloudwatchMetric(
            metric_name=metric_name,
            metric_namespace=metric_namespace,
            metric_unit=metric_unit,
            metric_value=metric_value,
            role_arn=role_arn,
            metric_timestamp=metric_timestamp,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudwatchMetric", [value]))

    @jsii.member(jsii_name="putDynamodb")
    def put_dynamodb(
        self,
        *,
        hash_key_field: builtins.str,
        hash_key_value: builtins.str,
        role_arn: builtins.str,
        table_name: builtins.str,
        hash_key_type: typing.Optional[builtins.str] = None,
        operation: typing.Optional[builtins.str] = None,
        payload_field: typing.Optional[builtins.str] = None,
        range_key_field: typing.Optional[builtins.str] = None,
        range_key_type: typing.Optional[builtins.str] = None,
        range_key_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hash_key_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#hash_key_field IotTopicRule#hash_key_field}.
        :param hash_key_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#hash_key_value IotTopicRule#hash_key_value}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.
        :param hash_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#hash_key_type IotTopicRule#hash_key_type}.
        :param operation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#operation IotTopicRule#operation}.
        :param payload_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#payload_field IotTopicRule#payload_field}.
        :param range_key_field: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#range_key_field IotTopicRule#range_key_field}.
        :param range_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#range_key_type IotTopicRule#range_key_type}.
        :param range_key_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#range_key_value IotTopicRule#range_key_value}.
        '''
        value = IotTopicRuleErrorActionDynamodb(
            hash_key_field=hash_key_field,
            hash_key_value=hash_key_value,
            role_arn=role_arn,
            table_name=table_name,
            hash_key_type=hash_key_type,
            operation=operation,
            payload_field=payload_field,
            range_key_field=range_key_field,
            range_key_type=range_key_type,
            range_key_value=range_key_value,
        )

        return typing.cast(None, jsii.invoke(self, "putDynamodb", [value]))

    @jsii.member(jsii_name="putDynamodbv2")
    def put_dynamodbv2(
        self,
        *,
        role_arn: builtins.str,
        put_item: typing.Optional[typing.Union[IotTopicRuleErrorActionDynamodbv2PutItem, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param put_item: put_item block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#put_item IotTopicRule#put_item}
        '''
        value = IotTopicRuleErrorActionDynamodbv2(role_arn=role_arn, put_item=put_item)

        return typing.cast(None, jsii.invoke(self, "putDynamodbv2", [value]))

    @jsii.member(jsii_name="putElasticsearch")
    def put_elasticsearch(
        self,
        *,
        endpoint: builtins.str,
        id: builtins.str,
        index: builtins.str,
        role_arn: builtins.str,
        type: builtins.str,
    ) -> None:
        '''
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#endpoint IotTopicRule#endpoint}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#id IotTopicRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#index IotTopicRule#index}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#type IotTopicRule#type}.
        '''
        value = IotTopicRuleErrorActionElasticsearch(
            endpoint=endpoint, id=id, index=index, role_arn=role_arn, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putElasticsearch", [value]))

    @jsii.member(jsii_name="putFirehose")
    def put_firehose(
        self,
        *,
        delivery_stream_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        separator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delivery_stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#delivery_stream_name IotTopicRule#delivery_stream_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        :param separator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#separator IotTopicRule#separator}.
        '''
        value = IotTopicRuleErrorActionFirehose(
            delivery_stream_name=delivery_stream_name,
            role_arn=role_arn,
            batch_mode=batch_mode,
            separator=separator,
        )

        return typing.cast(None, jsii.invoke(self, "putFirehose", [value]))

    @jsii.member(jsii_name="putHttp")
    def put_http(
        self,
        *,
        url: builtins.str,
        confirmation_url: typing.Optional[builtins.str] = None,
        http_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionHttpHttpHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#url IotTopicRule#url}.
        :param confirmation_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#confirmation_url IotTopicRule#confirmation_url}.
        :param http_header: http_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#http_header IotTopicRule#http_header}
        '''
        value = IotTopicRuleErrorActionHttp(
            url=url, confirmation_url=confirmation_url, http_header=http_header
        )

        return typing.cast(None, jsii.invoke(self, "putHttp", [value]))

    @jsii.member(jsii_name="putIotAnalytics")
    def put_iot_analytics(
        self,
        *,
        channel_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param channel_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#channel_name IotTopicRule#channel_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        '''
        value = IotTopicRuleErrorActionIotAnalytics(
            channel_name=channel_name, role_arn=role_arn, batch_mode=batch_mode
        )

        return typing.cast(None, jsii.invoke(self, "putIotAnalytics", [value]))

    @jsii.member(jsii_name="putIotEvents")
    def put_iot_events(
        self,
        *,
        input_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        message_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param input_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#input_name IotTopicRule#input_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        :param message_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#message_id IotTopicRule#message_id}.
        '''
        value = IotTopicRuleErrorActionIotEvents(
            input_name=input_name,
            role_arn=role_arn,
            batch_mode=batch_mode,
            message_id=message_id,
        )

        return typing.cast(None, jsii.invoke(self, "putIotEvents", [value]))

    @jsii.member(jsii_name="putKafka")
    def put_kafka(
        self,
        *,
        client_properties: typing.Mapping[builtins.str, builtins.str],
        destination_arn: builtins.str,
        topic: builtins.str,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionKafkaHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
        key: typing.Optional[builtins.str] = None,
        partition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#client_properties IotTopicRule#client_properties}.
        :param destination_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#destination_arn IotTopicRule#destination_arn}.
        :param topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#topic IotTopicRule#topic}.
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#header IotTopicRule#header}
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.
        :param partition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#partition IotTopicRule#partition}.
        '''
        value = IotTopicRuleErrorActionKafka(
            client_properties=client_properties,
            destination_arn=destination_arn,
            topic=topic,
            header=header,
            key=key,
            partition=partition,
        )

        return typing.cast(None, jsii.invoke(self, "putKafka", [value]))

    @jsii.member(jsii_name="putKinesis")
    def put_kinesis(
        self,
        *,
        role_arn: builtins.str,
        stream_name: builtins.str,
        partition_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#stream_name IotTopicRule#stream_name}.
        :param partition_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#partition_key IotTopicRule#partition_key}.
        '''
        value = IotTopicRuleErrorActionKinesis(
            role_arn=role_arn, stream_name=stream_name, partition_key=partition_key
        )

        return typing.cast(None, jsii.invoke(self, "putKinesis", [value]))

    @jsii.member(jsii_name="putLambda")
    def put_lambda(self, *, function_arn: builtins.str) -> None:
        '''
        :param function_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#function_arn IotTopicRule#function_arn}.
        '''
        value = IotTopicRuleErrorActionLambda(function_arn=function_arn)

        return typing.cast(None, jsii.invoke(self, "putLambda", [value]))

    @jsii.member(jsii_name="putRepublish")
    def put_republish(
        self,
        *,
        role_arn: builtins.str,
        topic: builtins.str,
        qos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#topic IotTopicRule#topic}.
        :param qos: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#qos IotTopicRule#qos}.
        '''
        value = IotTopicRuleErrorActionRepublish(
            role_arn=role_arn, topic=topic, qos=qos
        )

        return typing.cast(None, jsii.invoke(self, "putRepublish", [value]))

    @jsii.member(jsii_name="putS3")
    def put_s3(
        self,
        *,
        bucket_name: builtins.str,
        key: builtins.str,
        role_arn: builtins.str,
        canned_acl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#bucket_name IotTopicRule#bucket_name}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param canned_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#canned_acl IotTopicRule#canned_acl}.
        '''
        value = IotTopicRuleErrorActionS3(
            bucket_name=bucket_name, key=key, role_arn=role_arn, canned_acl=canned_acl
        )

        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="putSns")
    def put_sns(
        self,
        *,
        role_arn: builtins.str,
        target_arn: builtins.str,
        message_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param target_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#target_arn IotTopicRule#target_arn}.
        :param message_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#message_format IotTopicRule#message_format}.
        '''
        value = IotTopicRuleErrorActionSns(
            role_arn=role_arn, target_arn=target_arn, message_format=message_format
        )

        return typing.cast(None, jsii.invoke(self, "putSns", [value]))

    @jsii.member(jsii_name="putSqs")
    def put_sqs(
        self,
        *,
        queue_url: builtins.str,
        role_arn: builtins.str,
        use_base64: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param queue_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#queue_url IotTopicRule#queue_url}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param use_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#use_base64 IotTopicRule#use_base64}.
        '''
        value = IotTopicRuleErrorActionSqs(
            queue_url=queue_url, role_arn=role_arn, use_base64=use_base64
        )

        return typing.cast(None, jsii.invoke(self, "putSqs", [value]))

    @jsii.member(jsii_name="putStepFunctions")
    def put_step_functions(
        self,
        *,
        role_arn: builtins.str,
        state_machine_name: builtins.str,
        execution_name_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param state_machine_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#state_machine_name IotTopicRule#state_machine_name}.
        :param execution_name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#execution_name_prefix IotTopicRule#execution_name_prefix}.
        '''
        value = IotTopicRuleErrorActionStepFunctions(
            role_arn=role_arn,
            state_machine_name=state_machine_name,
            execution_name_prefix=execution_name_prefix,
        )

        return typing.cast(None, jsii.invoke(self, "putStepFunctions", [value]))

    @jsii.member(jsii_name="putTimestream")
    def put_timestream(
        self,
        *,
        database_name: builtins.str,
        dimension: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleErrorActionTimestreamDimension", typing.Dict[builtins.str, typing.Any]]]],
        role_arn: builtins.str,
        table_name: builtins.str,
        timestamp: typing.Optional[typing.Union["IotTopicRuleErrorActionTimestreamTimestamp", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#database_name IotTopicRule#database_name}.
        :param dimension: dimension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#dimension IotTopicRule#dimension}
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.
        :param timestamp: timestamp block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#timestamp IotTopicRule#timestamp}
        '''
        value = IotTopicRuleErrorActionTimestream(
            database_name=database_name,
            dimension=dimension,
            role_arn=role_arn,
            table_name=table_name,
            timestamp=timestamp,
        )

        return typing.cast(None, jsii.invoke(self, "putTimestream", [value]))

    @jsii.member(jsii_name="resetCloudwatchAlarm")
    def reset_cloudwatch_alarm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchAlarm", []))

    @jsii.member(jsii_name="resetCloudwatchLogs")
    def reset_cloudwatch_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchLogs", []))

    @jsii.member(jsii_name="resetCloudwatchMetric")
    def reset_cloudwatch_metric(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudwatchMetric", []))

    @jsii.member(jsii_name="resetDynamodb")
    def reset_dynamodb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamodb", []))

    @jsii.member(jsii_name="resetDynamodbv2")
    def reset_dynamodbv2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamodbv2", []))

    @jsii.member(jsii_name="resetElasticsearch")
    def reset_elasticsearch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearch", []))

    @jsii.member(jsii_name="resetFirehose")
    def reset_firehose(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirehose", []))

    @jsii.member(jsii_name="resetHttp")
    def reset_http(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp", []))

    @jsii.member(jsii_name="resetIotAnalytics")
    def reset_iot_analytics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIotAnalytics", []))

    @jsii.member(jsii_name="resetIotEvents")
    def reset_iot_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIotEvents", []))

    @jsii.member(jsii_name="resetKafka")
    def reset_kafka(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKafka", []))

    @jsii.member(jsii_name="resetKinesis")
    def reset_kinesis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesis", []))

    @jsii.member(jsii_name="resetLambda")
    def reset_lambda(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambda", []))

    @jsii.member(jsii_name="resetRepublish")
    def reset_republish(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepublish", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

    @jsii.member(jsii_name="resetSns")
    def reset_sns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSns", []))

    @jsii.member(jsii_name="resetSqs")
    def reset_sqs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqs", []))

    @jsii.member(jsii_name="resetStepFunctions")
    def reset_step_functions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStepFunctions", []))

    @jsii.member(jsii_name="resetTimestream")
    def reset_timestream(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestream", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchAlarm")
    def cloudwatch_alarm(self) -> IotTopicRuleErrorActionCloudwatchAlarmOutputReference:
        return typing.cast(IotTopicRuleErrorActionCloudwatchAlarmOutputReference, jsii.get(self, "cloudwatchAlarm"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogs")
    def cloudwatch_logs(self) -> IotTopicRuleErrorActionCloudwatchLogsOutputReference:
        return typing.cast(IotTopicRuleErrorActionCloudwatchLogsOutputReference, jsii.get(self, "cloudwatchLogs"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchMetric")
    def cloudwatch_metric(
        self,
    ) -> IotTopicRuleErrorActionCloudwatchMetricOutputReference:
        return typing.cast(IotTopicRuleErrorActionCloudwatchMetricOutputReference, jsii.get(self, "cloudwatchMetric"))

    @builtins.property
    @jsii.member(jsii_name="dynamodb")
    def dynamodb(self) -> IotTopicRuleErrorActionDynamodbOutputReference:
        return typing.cast(IotTopicRuleErrorActionDynamodbOutputReference, jsii.get(self, "dynamodb"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbv2")
    def dynamodbv2(self) -> IotTopicRuleErrorActionDynamodbv2OutputReference:
        return typing.cast(IotTopicRuleErrorActionDynamodbv2OutputReference, jsii.get(self, "dynamodbv2"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearch")
    def elasticsearch(self) -> IotTopicRuleErrorActionElasticsearchOutputReference:
        return typing.cast(IotTopicRuleErrorActionElasticsearchOutputReference, jsii.get(self, "elasticsearch"))

    @builtins.property
    @jsii.member(jsii_name="firehose")
    def firehose(self) -> IotTopicRuleErrorActionFirehoseOutputReference:
        return typing.cast(IotTopicRuleErrorActionFirehoseOutputReference, jsii.get(self, "firehose"))

    @builtins.property
    @jsii.member(jsii_name="http")
    def http(self) -> IotTopicRuleErrorActionHttpOutputReference:
        return typing.cast(IotTopicRuleErrorActionHttpOutputReference, jsii.get(self, "http"))

    @builtins.property
    @jsii.member(jsii_name="iotAnalytics")
    def iot_analytics(self) -> IotTopicRuleErrorActionIotAnalyticsOutputReference:
        return typing.cast(IotTopicRuleErrorActionIotAnalyticsOutputReference, jsii.get(self, "iotAnalytics"))

    @builtins.property
    @jsii.member(jsii_name="iotEvents")
    def iot_events(self) -> IotTopicRuleErrorActionIotEventsOutputReference:
        return typing.cast(IotTopicRuleErrorActionIotEventsOutputReference, jsii.get(self, "iotEvents"))

    @builtins.property
    @jsii.member(jsii_name="kafka")
    def kafka(self) -> IotTopicRuleErrorActionKafkaOutputReference:
        return typing.cast(IotTopicRuleErrorActionKafkaOutputReference, jsii.get(self, "kafka"))

    @builtins.property
    @jsii.member(jsii_name="kinesis")
    def kinesis(self) -> IotTopicRuleErrorActionKinesisOutputReference:
        return typing.cast(IotTopicRuleErrorActionKinesisOutputReference, jsii.get(self, "kinesis"))

    @builtins.property
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> IotTopicRuleErrorActionLambdaOutputReference:
        return typing.cast(IotTopicRuleErrorActionLambdaOutputReference, jsii.get(self, "lambda"))

    @builtins.property
    @jsii.member(jsii_name="republish")
    def republish(self) -> "IotTopicRuleErrorActionRepublishOutputReference":
        return typing.cast("IotTopicRuleErrorActionRepublishOutputReference", jsii.get(self, "republish"))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(self) -> "IotTopicRuleErrorActionS3OutputReference":
        return typing.cast("IotTopicRuleErrorActionS3OutputReference", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="sns")
    def sns(self) -> "IotTopicRuleErrorActionSnsOutputReference":
        return typing.cast("IotTopicRuleErrorActionSnsOutputReference", jsii.get(self, "sns"))

    @builtins.property
    @jsii.member(jsii_name="sqs")
    def sqs(self) -> "IotTopicRuleErrorActionSqsOutputReference":
        return typing.cast("IotTopicRuleErrorActionSqsOutputReference", jsii.get(self, "sqs"))

    @builtins.property
    @jsii.member(jsii_name="stepFunctions")
    def step_functions(self) -> "IotTopicRuleErrorActionStepFunctionsOutputReference":
        return typing.cast("IotTopicRuleErrorActionStepFunctionsOutputReference", jsii.get(self, "stepFunctions"))

    @builtins.property
    @jsii.member(jsii_name="timestream")
    def timestream(self) -> "IotTopicRuleErrorActionTimestreamOutputReference":
        return typing.cast("IotTopicRuleErrorActionTimestreamOutputReference", jsii.get(self, "timestream"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchAlarmInput")
    def cloudwatch_alarm_input(
        self,
    ) -> typing.Optional[IotTopicRuleErrorActionCloudwatchAlarm]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionCloudwatchAlarm], jsii.get(self, "cloudwatchAlarmInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogsInput")
    def cloudwatch_logs_input(
        self,
    ) -> typing.Optional[IotTopicRuleErrorActionCloudwatchLogs]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionCloudwatchLogs], jsii.get(self, "cloudwatchLogsInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchMetricInput")
    def cloudwatch_metric_input(
        self,
    ) -> typing.Optional[IotTopicRuleErrorActionCloudwatchMetric]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionCloudwatchMetric], jsii.get(self, "cloudwatchMetricInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbInput")
    def dynamodb_input(self) -> typing.Optional[IotTopicRuleErrorActionDynamodb]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionDynamodb], jsii.get(self, "dynamodbInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbv2Input")
    def dynamodbv2_input(self) -> typing.Optional[IotTopicRuleErrorActionDynamodbv2]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionDynamodbv2], jsii.get(self, "dynamodbv2Input"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchInput")
    def elasticsearch_input(
        self,
    ) -> typing.Optional[IotTopicRuleErrorActionElasticsearch]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionElasticsearch], jsii.get(self, "elasticsearchInput"))

    @builtins.property
    @jsii.member(jsii_name="firehoseInput")
    def firehose_input(self) -> typing.Optional[IotTopicRuleErrorActionFirehose]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionFirehose], jsii.get(self, "firehoseInput"))

    @builtins.property
    @jsii.member(jsii_name="httpInput")
    def http_input(self) -> typing.Optional[IotTopicRuleErrorActionHttp]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionHttp], jsii.get(self, "httpInput"))

    @builtins.property
    @jsii.member(jsii_name="iotAnalyticsInput")
    def iot_analytics_input(
        self,
    ) -> typing.Optional[IotTopicRuleErrorActionIotAnalytics]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionIotAnalytics], jsii.get(self, "iotAnalyticsInput"))

    @builtins.property
    @jsii.member(jsii_name="iotEventsInput")
    def iot_events_input(self) -> typing.Optional[IotTopicRuleErrorActionIotEvents]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionIotEvents], jsii.get(self, "iotEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="kafkaInput")
    def kafka_input(self) -> typing.Optional[IotTopicRuleErrorActionKafka]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionKafka], jsii.get(self, "kafkaInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisInput")
    def kinesis_input(self) -> typing.Optional[IotTopicRuleErrorActionKinesis]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionKinesis], jsii.get(self, "kinesisInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaInput")
    def lambda_input(self) -> typing.Optional[IotTopicRuleErrorActionLambda]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionLambda], jsii.get(self, "lambdaInput"))

    @builtins.property
    @jsii.member(jsii_name="republishInput")
    def republish_input(self) -> typing.Optional["IotTopicRuleErrorActionRepublish"]:
        return typing.cast(typing.Optional["IotTopicRuleErrorActionRepublish"], jsii.get(self, "republishInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(self) -> typing.Optional["IotTopicRuleErrorActionS3"]:
        return typing.cast(typing.Optional["IotTopicRuleErrorActionS3"], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="snsInput")
    def sns_input(self) -> typing.Optional["IotTopicRuleErrorActionSns"]:
        return typing.cast(typing.Optional["IotTopicRuleErrorActionSns"], jsii.get(self, "snsInput"))

    @builtins.property
    @jsii.member(jsii_name="sqsInput")
    def sqs_input(self) -> typing.Optional["IotTopicRuleErrorActionSqs"]:
        return typing.cast(typing.Optional["IotTopicRuleErrorActionSqs"], jsii.get(self, "sqsInput"))

    @builtins.property
    @jsii.member(jsii_name="stepFunctionsInput")
    def step_functions_input(
        self,
    ) -> typing.Optional["IotTopicRuleErrorActionStepFunctions"]:
        return typing.cast(typing.Optional["IotTopicRuleErrorActionStepFunctions"], jsii.get(self, "stepFunctionsInput"))

    @builtins.property
    @jsii.member(jsii_name="timestreamInput")
    def timestream_input(self) -> typing.Optional["IotTopicRuleErrorActionTimestream"]:
        return typing.cast(typing.Optional["IotTopicRuleErrorActionTimestream"], jsii.get(self, "timestreamInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorAction]:
        return typing.cast(typing.Optional[IotTopicRuleErrorAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[IotTopicRuleErrorAction]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab87b64125f281b0657ed115642982b348500c91170adcd7f1c7e4146b7a00ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionRepublish",
    jsii_struct_bases=[],
    name_mapping={"role_arn": "roleArn", "topic": "topic", "qos": "qos"},
)
class IotTopicRuleErrorActionRepublish:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        topic: builtins.str,
        qos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#topic IotTopicRule#topic}.
        :param qos: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#qos IotTopicRule#qos}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e4f8d0a9060cfee44884056a9257abee2b3c9f57d5c720940d28925112748af)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument qos", value=qos, expected_type=type_hints["qos"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
            "topic": topic,
        }
        if qos is not None:
            self._values["qos"] = qos

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#topic IotTopicRule#topic}.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def qos(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#qos IotTopicRule#qos}.'''
        result = self._values.get("qos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionRepublish(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionRepublishOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionRepublishOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20770824548ec4238e02d74793731d61f58a360e67ae145a083aee2c3e480acb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetQos")
    def reset_qos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQos", []))

    @builtins.property
    @jsii.member(jsii_name="qosInput")
    def qos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "qosInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="qos")
    def qos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "qos"))

    @qos.setter
    def qos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe3c1ca3a50654cf5eaf942083523a4d98fcd78c675dae86d26f961fc4baaa70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26c69d5e0d92c950938217beb21a9882e9f01cb7b47d9cdfbcaa67ec6daeebfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__342fccfb3112afb9dcd6d3781ef9d4065c5ee803eb59652b42c37a8741072ec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionRepublish]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionRepublish], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionRepublish],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d197c41cbcf6c9089e5b597f8638dc6c1874f3168a713a046531ac05e3a3bf44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionS3",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "key": "key",
        "role_arn": "roleArn",
        "canned_acl": "cannedAcl",
    },
)
class IotTopicRuleErrorActionS3:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        key: builtins.str,
        role_arn: builtins.str,
        canned_acl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#bucket_name IotTopicRule#bucket_name}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param canned_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#canned_acl IotTopicRule#canned_acl}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b57561a8f2fcfd4ecda5fc69466d933c45ce0de553d2a3a61aa5bcf576e9d7f)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument canned_acl", value=canned_acl, expected_type=type_hints["canned_acl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "key": key,
            "role_arn": role_arn,
        }
        if canned_acl is not None:
            self._values["canned_acl"] = canned_acl

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#bucket_name IotTopicRule#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def canned_acl(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#canned_acl IotTopicRule#canned_acl}.'''
        result = self._values.get("canned_acl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionS3OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ebaf886267e36169d392ae8c7d44f7a11a8ddfbe916910f8e53bddf6e422da1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCannedAcl")
    def reset_canned_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCannedAcl", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="cannedAclInput")
    def canned_acl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cannedAclInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__040ec99ec84a499584d883e419b18f41b34f09f290b6786eb8d680bc0e4522eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cannedAcl")
    def canned_acl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cannedAcl"))

    @canned_acl.setter
    def canned_acl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7aa13d68ac0b770daed598178ae4ac9a875cd1167da6a431ec0fcac471d9d07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cannedAcl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a82b3a0d857b42f50bde9ce99a5254bd63732a03281b3c4cf63e61bc83ef1143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd26a923d3ac4db41dbf9aea151cfe58cda013abd07179cf916875e81308739)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionS3]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionS3], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[IotTopicRuleErrorActionS3]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__221820370306b6362aacc0506f901155b3948e5b2038103505f0d1539e4bc716)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionSns",
    jsii_struct_bases=[],
    name_mapping={
        "role_arn": "roleArn",
        "target_arn": "targetArn",
        "message_format": "messageFormat",
    },
)
class IotTopicRuleErrorActionSns:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        target_arn: builtins.str,
        message_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param target_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#target_arn IotTopicRule#target_arn}.
        :param message_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#message_format IotTopicRule#message_format}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2701eab489642b57e35f0ad6d2b0fa1d75927c9d9044911861a055baa3c7f3a)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
            check_type(argname="argument message_format", value=message_format, expected_type=type_hints["message_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
            "target_arn": target_arn,
        }
        if message_format is not None:
            self._values["message_format"] = message_format

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#target_arn IotTopicRule#target_arn}.'''
        result = self._values.get("target_arn")
        assert result is not None, "Required property 'target_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def message_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#message_format IotTopicRule#message_format}.'''
        result = self._values.get("message_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionSns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionSnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionSnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e6ce5ae02f824bc0cffee5a84aa69a02d01f09c3e1959685fc1ecac3159aaec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMessageFormat")
    def reset_message_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageFormat", []))

    @builtins.property
    @jsii.member(jsii_name="messageFormatInput")
    def message_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="targetArnInput")
    def target_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetArnInput"))

    @builtins.property
    @jsii.member(jsii_name="messageFormat")
    def message_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageFormat"))

    @message_format.setter
    def message_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bd6469360fceba7d68e081ef66185c38e655c0006e9435ab8c6a7e06f1a11d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dff3982c5084e6d535f3a38cb05d38ab6e7fcaaba1ec06b9a1513b1cdb4428c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))

    @target_arn.setter
    def target_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c815fe69ee53143cc5574890f8bfdcfa3405900c1d552f07030d138627c7f07b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionSns]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionSns], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionSns],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fda3beb285b9f0a36b6083793393c367311e61d17a94c34f2d92d69c0f10c15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionSqs",
    jsii_struct_bases=[],
    name_mapping={
        "queue_url": "queueUrl",
        "role_arn": "roleArn",
        "use_base64": "useBase64",
    },
)
class IotTopicRuleErrorActionSqs:
    def __init__(
        self,
        *,
        queue_url: builtins.str,
        role_arn: builtins.str,
        use_base64: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param queue_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#queue_url IotTopicRule#queue_url}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param use_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#use_base64 IotTopicRule#use_base64}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6602c92ba4cb1477093579c81a2038f3aa774279ebba38bfae0c76e50d11b7d)
            check_type(argname="argument queue_url", value=queue_url, expected_type=type_hints["queue_url"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument use_base64", value=use_base64, expected_type=type_hints["use_base64"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "queue_url": queue_url,
            "role_arn": role_arn,
            "use_base64": use_base64,
        }

    @builtins.property
    def queue_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#queue_url IotTopicRule#queue_url}.'''
        result = self._values.get("queue_url")
        assert result is not None, "Required property 'queue_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def use_base64(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#use_base64 IotTopicRule#use_base64}.'''
        result = self._values.get("use_base64")
        assert result is not None, "Required property 'use_base64' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionSqs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionSqsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionSqsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__236d254fce613fc43c69743292de9074a8ec0ff84ba85e1a3fd1333bb9c34538)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="queueUrlInput")
    def queue_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queueUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="useBase64Input")
    def use_base64_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useBase64Input"))

    @builtins.property
    @jsii.member(jsii_name="queueUrl")
    def queue_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queueUrl"))

    @queue_url.setter
    def queue_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce40d036d2beade6d55c794867a6d418f9805ceb1c459e00bfebdd74d574d986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f916173fe8dd931b05d643c165e811de88512fcb47d71709c495f5837cd684c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useBase64")
    def use_base64(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useBase64"))

    @use_base64.setter
    def use_base64(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4c58e1ecb18874fa687d7c7f700e319f73041350012b2242a26036f22b980fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionSqs]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionSqs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionSqs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d274d675f409779aeb252e9744787ecfde6a38639e3d4ec8cf1861f616ea4e65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionStepFunctions",
    jsii_struct_bases=[],
    name_mapping={
        "role_arn": "roleArn",
        "state_machine_name": "stateMachineName",
        "execution_name_prefix": "executionNamePrefix",
    },
)
class IotTopicRuleErrorActionStepFunctions:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        state_machine_name: builtins.str,
        execution_name_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param state_machine_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#state_machine_name IotTopicRule#state_machine_name}.
        :param execution_name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#execution_name_prefix IotTopicRule#execution_name_prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2625f1d5ea87076e18f700284d694cbd8b32c3b9a2ec2a72194cb92642a6247d)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument state_machine_name", value=state_machine_name, expected_type=type_hints["state_machine_name"])
            check_type(argname="argument execution_name_prefix", value=execution_name_prefix, expected_type=type_hints["execution_name_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
            "state_machine_name": state_machine_name,
        }
        if execution_name_prefix is not None:
            self._values["execution_name_prefix"] = execution_name_prefix

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state_machine_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#state_machine_name IotTopicRule#state_machine_name}.'''
        result = self._values.get("state_machine_name")
        assert result is not None, "Required property 'state_machine_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def execution_name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#execution_name_prefix IotTopicRule#execution_name_prefix}.'''
        result = self._values.get("execution_name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionStepFunctions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionStepFunctionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionStepFunctionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efb6ca62d4f392cea3b5b3efe0951657324057a5f4979fc615ce27181cc3edde)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExecutionNamePrefix")
    def reset_execution_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionNamePrefix", []))

    @builtins.property
    @jsii.member(jsii_name="executionNamePrefixInput")
    def execution_name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionNamePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="stateMachineNameInput")
    def state_machine_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateMachineNameInput"))

    @builtins.property
    @jsii.member(jsii_name="executionNamePrefix")
    def execution_name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionNamePrefix"))

    @execution_name_prefix.setter
    def execution_name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__357a760aedee56cf421f3bbfd1a9b3f452a4124ab36ab26e3b4ff0ee077ded71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionNamePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcbb2fd9007d19907bb461cac46de102cac577609ca3dd9994cae2f52dbb2f9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stateMachineName")
    def state_machine_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateMachineName"))

    @state_machine_name.setter
    def state_machine_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a5684d1423b6b1772eeadd185bf023c3255d64a062e116f73399f99d952ee0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stateMachineName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionStepFunctions]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionStepFunctions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionStepFunctions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eae046bff12a29a2dd4ec97eedf5cdd619d660ea6bdd0663698236ae46061854)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionTimestream",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "dimension": "dimension",
        "role_arn": "roleArn",
        "table_name": "tableName",
        "timestamp": "timestamp",
    },
)
class IotTopicRuleErrorActionTimestream:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        dimension: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleErrorActionTimestreamDimension", typing.Dict[builtins.str, typing.Any]]]],
        role_arn: builtins.str,
        table_name: builtins.str,
        timestamp: typing.Optional[typing.Union["IotTopicRuleErrorActionTimestreamTimestamp", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#database_name IotTopicRule#database_name}.
        :param dimension: dimension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#dimension IotTopicRule#dimension}
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.
        :param timestamp: timestamp block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#timestamp IotTopicRule#timestamp}
        '''
        if isinstance(timestamp, dict):
            timestamp = IotTopicRuleErrorActionTimestreamTimestamp(**timestamp)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1db45c956761bb6888f5fb0a4bdda2b6b68bb6148187a60fa058ecca9ac4ba2)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
            "dimension": dimension,
            "role_arn": role_arn,
            "table_name": table_name,
        }
        if timestamp is not None:
            self._values["timestamp"] = timestamp

    @builtins.property
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#database_name IotTopicRule#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dimension(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleErrorActionTimestreamDimension"]]:
        '''dimension block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#dimension IotTopicRule#dimension}
        '''
        result = self._values.get("dimension")
        assert result is not None, "Required property 'dimension' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleErrorActionTimestreamDimension"]], result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.'''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timestamp(
        self,
    ) -> typing.Optional["IotTopicRuleErrorActionTimestreamTimestamp"]:
        '''timestamp block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#timestamp IotTopicRule#timestamp}
        '''
        result = self._values.get("timestamp")
        return typing.cast(typing.Optional["IotTopicRuleErrorActionTimestreamTimestamp"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionTimestream(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionTimestreamDimension",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class IotTopicRuleErrorActionTimestreamDimension:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#name IotTopicRule#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9176aee76c15ebec47aee9555a394ba1a3c018eab7cf5f6bf4d4e3b2c4b4cb3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#name IotTopicRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionTimestreamDimension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionTimestreamDimensionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionTimestreamDimensionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__961d0e606b5b07e49dc7de3a7c3b74c09e82d19728244c4952188df77eb1b10a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IotTopicRuleErrorActionTimestreamDimensionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6e9902afff5be697e188799804350be62b594a4d18c9d55939680c73ac2da95)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleErrorActionTimestreamDimensionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b10797ed6a91c94971ca07bf5204d22da567649bd4d696d25cebdaae4523247c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f83e0edc7647fa6f6b309379405165e09ad0b62544153b0ab0415db1707e2f17)
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
            type_hints = typing.get_type_hints(_typecheckingstub__88c3ab6681ae285eb65f20b234cb7ced9e62b2e9e0feac67db548920c9696f2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionTimestreamDimension]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionTimestreamDimension]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionTimestreamDimension]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d35a0997495fb10cfc769c9d5930ef4efca9552c9ab7df1dc61384f7ba74527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleErrorActionTimestreamDimensionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionTimestreamDimensionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00ca9876ab579f377345bd2db57af588f41aaf385bdb31fab25a98ff35c98d91)
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
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d9066798162b8d169559bb5802a18c4472ff0ee07b28d84a16f46684690419e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b6ea9fda1e93b02a6da969ca4993f358dd226dc0ec546ed107717a877d76528)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionTimestreamDimension]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionTimestreamDimension]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionTimestreamDimension]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf52cffecc1af0ba896406b67479a144bbdccbd324df3db3b5aa52b12ac10326)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleErrorActionTimestreamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionTimestreamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__823f4c7bef9d0eeebcdb5ab6d6d875ddac781bace169c1a9bdda4306f1b6d045)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDimension")
    def put_dimension(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionTimestreamDimension, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad740cdd6934997d72cb58eea5a5d56d5c4133435424c6940907bfdd0346e02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDimension", [value]))

    @jsii.member(jsii_name="putTimestamp")
    def put_timestamp(self, *, unit: builtins.str, value: builtins.str) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#unit IotTopicRule#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.
        '''
        value_ = IotTopicRuleErrorActionTimestreamTimestamp(unit=unit, value=value)

        return typing.cast(None, jsii.invoke(self, "putTimestamp", [value_]))

    @jsii.member(jsii_name="resetTimestamp")
    def reset_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestamp", []))

    @builtins.property
    @jsii.member(jsii_name="dimension")
    def dimension(self) -> IotTopicRuleErrorActionTimestreamDimensionList:
        return typing.cast(IotTopicRuleErrorActionTimestreamDimensionList, jsii.get(self, "dimension"))

    @builtins.property
    @jsii.member(jsii_name="timestamp")
    def timestamp(self) -> "IotTopicRuleErrorActionTimestreamTimestampOutputReference":
        return typing.cast("IotTopicRuleErrorActionTimestreamTimestampOutputReference", jsii.get(self, "timestamp"))

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionInput")
    def dimension_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionTimestreamDimension]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionTimestreamDimension]]], jsii.get(self, "dimensionInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampInput")
    def timestamp_input(
        self,
    ) -> typing.Optional["IotTopicRuleErrorActionTimestreamTimestamp"]:
        return typing.cast(typing.Optional["IotTopicRuleErrorActionTimestreamTimestamp"], jsii.get(self, "timestampInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9338c409db957ed3785141160f71df26e9e3af43ce8498032f49e7520f3d561b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66d45f7d8eb82f01d5e6d972fb14f24bd681fa19b8ac20993bfba0de0d05d06f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24c845ff1f047f222d0398396b4743478bbf94e5c7ba745a6db7305045b32b2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleErrorActionTimestream]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionTimestream], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionTimestream],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0aeb5dd00d7d445ef455a7192f4f80708b4c25a2931892430f850957659027c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionTimestreamTimestamp",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class IotTopicRuleErrorActionTimestreamTimestamp:
    def __init__(self, *, unit: builtins.str, value: builtins.str) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#unit IotTopicRule#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be850aba3c7d7b20fe514ccfb0a595d7015f096a89813f6e74f06c887e85e840)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#unit IotTopicRule#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleErrorActionTimestreamTimestamp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleErrorActionTimestreamTimestampOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleErrorActionTimestreamTimestampOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0fb649f97fad7c89677c10d1e28e75ae5124e5d0ff815d1979b0434afa4f39d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="unitInput")
    def unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unit"))

    @unit.setter
    def unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55c8c9fbea482842e877244fc6b00bf0ed80b720b5ae6f0c121639d28f07b596)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc797b69527afdc565312ca3a3143a987cb45067b9da323c10add113904892a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IotTopicRuleErrorActionTimestreamTimestamp]:
        return typing.cast(typing.Optional[IotTopicRuleErrorActionTimestreamTimestamp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleErrorActionTimestreamTimestamp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cc76846bcd099f4a92b1674151a73b5075d169e59766835effdfdbdb7f847a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleFirehose",
    jsii_struct_bases=[],
    name_mapping={
        "delivery_stream_name": "deliveryStreamName",
        "role_arn": "roleArn",
        "batch_mode": "batchMode",
        "separator": "separator",
    },
)
class IotTopicRuleFirehose:
    def __init__(
        self,
        *,
        delivery_stream_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        separator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delivery_stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#delivery_stream_name IotTopicRule#delivery_stream_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        :param separator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#separator IotTopicRule#separator}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38b1e23f70f8134be5882afefe6f1bd45c48da7d9328086855f95f4318bbe203)
            check_type(argname="argument delivery_stream_name", value=delivery_stream_name, expected_type=type_hints["delivery_stream_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument batch_mode", value=batch_mode, expected_type=type_hints["batch_mode"])
            check_type(argname="argument separator", value=separator, expected_type=type_hints["separator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delivery_stream_name": delivery_stream_name,
            "role_arn": role_arn,
        }
        if batch_mode is not None:
            self._values["batch_mode"] = batch_mode
        if separator is not None:
            self._values["separator"] = separator

    @builtins.property
    def delivery_stream_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#delivery_stream_name IotTopicRule#delivery_stream_name}.'''
        result = self._values.get("delivery_stream_name")
        assert result is not None, "Required property 'delivery_stream_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.'''
        result = self._values.get("batch_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def separator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#separator IotTopicRule#separator}.'''
        result = self._values.get("separator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleFirehose(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleFirehoseList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleFirehoseList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b549533f6420a43d2bb26f6c772816f5e99136bafeac4a0bf8bd749b288a0250)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleFirehoseOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67646a54f0319ecce37836ada18d6a4453eef45072f3fea5071019e6c7a7095e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleFirehoseOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c718bae2707d6c54d32e4f00bb20a8ffe0e898bed9dab747584b88090446c9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5919badc04d3cf987d76829289da36458a750af92df3f494ce203cc0cb54dac5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89ddfca73656774ed3dd18c87b40940502b6855ca77cd8cfb695ab75155f8df3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleFirehose]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleFirehose]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleFirehose]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f649b193f57906792f7911f042f6739e100ab71ee60f4b74d2d3ff72b04842d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleFirehoseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleFirehoseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3decb07acadbcaf4bb772d98ddaa73f64e537bd40265085661e3c3fccd139964)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBatchMode")
    def reset_batch_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchMode", []))

    @jsii.member(jsii_name="resetSeparator")
    def reset_separator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeparator", []))

    @builtins.property
    @jsii.member(jsii_name="batchModeInput")
    def batch_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "batchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamNameInput")
    def delivery_stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deliveryStreamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="separatorInput")
    def separator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "separatorInput"))

    @builtins.property
    @jsii.member(jsii_name="batchMode")
    def batch_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "batchMode"))

    @batch_mode.setter
    def batch_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dddd048662c3fa6a7d1efb6d8d2f1172884cd46fb19828ec6517ef1b84ae166)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamName")
    def delivery_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deliveryStreamName"))

    @delivery_stream_name.setter
    def delivery_stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9991294f223dfb97757ec6a70341023c67f5998b4e7ef5c5d20e5169a60898b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deliveryStreamName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34fc1d1ee66a19fef053067b49af3e9d6c96f04bb04ae55e87ac46bc9e2ec335)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="separator")
    def separator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "separator"))

    @separator.setter
    def separator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ab35feb550504b89fb0d4e153d7b7e26ab4f4b2142658b15533c3b3f84a84d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "separator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleFirehose]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleFirehose]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleFirehose]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fd8f4be29e1b224410a6a7d4481f2b09c5c0d8b548b3ddd124862e0aa627e80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleHttp",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "confirmation_url": "confirmationUrl",
        "http_header": "httpHeader",
    },
)
class IotTopicRuleHttp:
    def __init__(
        self,
        *,
        url: builtins.str,
        confirmation_url: typing.Optional[builtins.str] = None,
        http_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleHttpHttpHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#url IotTopicRule#url}.
        :param confirmation_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#confirmation_url IotTopicRule#confirmation_url}.
        :param http_header: http_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#http_header IotTopicRule#http_header}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6eb74cd181847fb91fb990ef198322085f88706bf8cafbd57167bd535cfef77)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument confirmation_url", value=confirmation_url, expected_type=type_hints["confirmation_url"])
            check_type(argname="argument http_header", value=http_header, expected_type=type_hints["http_header"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if confirmation_url is not None:
            self._values["confirmation_url"] = confirmation_url
        if http_header is not None:
            self._values["http_header"] = http_header

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#url IotTopicRule#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def confirmation_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#confirmation_url IotTopicRule#confirmation_url}.'''
        result = self._values.get("confirmation_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleHttpHttpHeader"]]]:
        '''http_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#http_header IotTopicRule#http_header}
        '''
        result = self._values.get("http_header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleHttpHttpHeader"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleHttp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleHttpHttpHeader",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class IotTopicRuleHttpHttpHeader:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e06dc4c41d8d5eef4d1458eb16bf7787b072489cb23983e40671697386f905a4)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleHttpHttpHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleHttpHttpHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleHttpHttpHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__615e15038ba5362a288f0c954f89a9b3362b0a478d2da212e15e247610f35d21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleHttpHttpHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__507c4b3a271fccf71231d461c3327939928ab9c75c123136255a17eaa78c5b26)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleHttpHttpHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__567caa4b2314df2b41ec7fde86a2ebbe37b9ec80e8f521816f2fda63095d63a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc5c74e160f09d027b632d32d1609bad51fc4e3a92d91ed1e4177fd7d7577b03)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e09a1382cec026a1f51e7a66c455703a6d072c8f1e6594aa3a6100e5a6fef632)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleHttpHttpHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleHttpHttpHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleHttpHttpHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9863308448197136fe5bd4e4382ffe75cb17c537f8818b6c24a12fcdb9d746e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleHttpHttpHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleHttpHttpHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2453fc916a1227cd9bbe8348883e9f73d0a8a59c83c9b415e561eba75e407969)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19a6ba5b5a6160e42fc7fe366050e34f0abd7b883f5c4fe5d02555b46652b44d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5697c52ebee0a695f9e4c472fe8836c7b04d25dafcdbf5fea0b8a4b92a36274)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleHttpHttpHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleHttpHttpHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleHttpHttpHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12338b2a8748dbf9879f197df31607ec0eea98f2c203186e0be90e93b9a6df5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleHttpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleHttpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef78a5586f8868fba72f2daeea5084c9f3d44bb73581fbcc9cf04a91dea13a9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleHttpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__337bc022fa44282880b42fc3b7b551e168345f53209764a8cadd7b2aab37b800)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleHttpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd071eda3cc88b33a20ae61341de176fb0d38f81c6910939d6bfd948abee9f81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21a1b10a469502cfea00b546b17c364ec425ba49b4b3c8e708645bdaafe2bd8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7ec20d9612e6148735021c258bc21e01f8428f7db50f27e0e65b1472001bc25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleHttp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleHttp]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleHttp]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22fa0a9f970469f0c4c207ce32e71c33954c8353802b808529dcea0f1f7f901b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleHttpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleHttpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__286dfddc821da074d57377c5dc0378932dc2f95f4350545c6a5bb131c46be70b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHttpHeader")
    def put_http_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleHttpHttpHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3d63a269286ceec18636a69d6e51d216583e7d4eb0322513f977fe55b8c5a94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttpHeader", [value]))

    @jsii.member(jsii_name="resetConfirmationUrl")
    def reset_confirmation_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfirmationUrl", []))

    @jsii.member(jsii_name="resetHttpHeader")
    def reset_http_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpHeader", []))

    @builtins.property
    @jsii.member(jsii_name="httpHeader")
    def http_header(self) -> IotTopicRuleHttpHttpHeaderList:
        return typing.cast(IotTopicRuleHttpHttpHeaderList, jsii.get(self, "httpHeader"))

    @builtins.property
    @jsii.member(jsii_name="confirmationUrlInput")
    def confirmation_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "confirmationUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHeaderInput")
    def http_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleHttpHttpHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleHttpHttpHeader]]], jsii.get(self, "httpHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="confirmationUrl")
    def confirmation_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "confirmationUrl"))

    @confirmation_url.setter
    def confirmation_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ebae0929dfdd0ff79d25af27211bd38c3e8cd2f50ab90701812162eafe89a63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confirmationUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dc0486e4f36cf751f9a66c44f44b6191acd7c55d1b2e78351d43170c3e408bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleHttp]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleHttp]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleHttp]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc6b9839729b4a9e633b916e194b05dcf12ddabba610b52628aae25d20545c29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleIotAnalytics",
    jsii_struct_bases=[],
    name_mapping={
        "channel_name": "channelName",
        "role_arn": "roleArn",
        "batch_mode": "batchMode",
    },
)
class IotTopicRuleIotAnalytics:
    def __init__(
        self,
        *,
        channel_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param channel_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#channel_name IotTopicRule#channel_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bcdda0b5718945cb7f0a115727f56e0c95bf9a014f4cb1f4349f9ffb4a04c24)
            check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument batch_mode", value=batch_mode, expected_type=type_hints["batch_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "channel_name": channel_name,
            "role_arn": role_arn,
        }
        if batch_mode is not None:
            self._values["batch_mode"] = batch_mode

    @builtins.property
    def channel_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#channel_name IotTopicRule#channel_name}.'''
        result = self._values.get("channel_name")
        assert result is not None, "Required property 'channel_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.'''
        result = self._values.get("batch_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleIotAnalytics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleIotAnalyticsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleIotAnalyticsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86467426c259393e5075c3fd9b2219657cc901e046d687e5659f0db91cd9bd06)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleIotAnalyticsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eeceede42b62727bd208af4664e3723d83bf304ff0662d2c31ebd7593535462)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleIotAnalyticsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb4d624c5ea6cf3ee04dc379fa355f4b23e3ee7cdbbcc2984a3088aa9b5b9ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e4e7420c45920ec51a46c3a5fe5b3a56064779e23add0502f2d87d4ecfe5e04)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1e7158b3dec87d4d4a8a5fdce17a27f242fb8a4d0d5020012ebedd319ae13b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleIotAnalytics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleIotAnalytics]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleIotAnalytics]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f45a8c578d83b02c7d728123406ce491e717007521b3ef42d8646bbe228ca73d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleIotAnalyticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleIotAnalyticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcb80ca4d72f48b23f79ab870c89570bcd98762ed6796edbfa7deee6e7bc0752)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBatchMode")
    def reset_batch_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchMode", []))

    @builtins.property
    @jsii.member(jsii_name="batchModeInput")
    def batch_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "batchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="channelNameInput")
    def channel_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "channelNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="batchMode")
    def batch_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "batchMode"))

    @batch_mode.setter
    def batch_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__271b41396c8da5965109849e90f501cab5f430aa9d34e7631416ce5bda4e194f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="channelName")
    def channel_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channelName"))

    @channel_name.setter
    def channel_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d046c46022d44c7cb658f391ce5cbfb6d3852388e6b3cffc87fc4335e5d4ca6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bd94996e669c00c05e9ba268ac0a57c30a9c854f6be62caf780167a5413f140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleIotAnalytics]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleIotAnalytics]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleIotAnalytics]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cab460061e0f9c0a68721315d4de5a5d2cb92c41697cac8a8f0ea94aa7870e1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleIotEvents",
    jsii_struct_bases=[],
    name_mapping={
        "input_name": "inputName",
        "role_arn": "roleArn",
        "batch_mode": "batchMode",
        "message_id": "messageId",
    },
)
class IotTopicRuleIotEvents:
    def __init__(
        self,
        *,
        input_name: builtins.str,
        role_arn: builtins.str,
        batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        message_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param input_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#input_name IotTopicRule#input_name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param batch_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.
        :param message_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#message_id IotTopicRule#message_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36d2d7a8a576c5a924c3a05d335afefad8493e30a04c9233f5a827251247481d)
            check_type(argname="argument input_name", value=input_name, expected_type=type_hints["input_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument batch_mode", value=batch_mode, expected_type=type_hints["batch_mode"])
            check_type(argname="argument message_id", value=message_id, expected_type=type_hints["message_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "input_name": input_name,
            "role_arn": role_arn,
        }
        if batch_mode is not None:
            self._values["batch_mode"] = batch_mode
        if message_id is not None:
            self._values["message_id"] = message_id

    @builtins.property
    def input_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#input_name IotTopicRule#input_name}.'''
        result = self._values.get("input_name")
        assert result is not None, "Required property 'input_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def batch_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#batch_mode IotTopicRule#batch_mode}.'''
        result = self._values.get("batch_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def message_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#message_id IotTopicRule#message_id}.'''
        result = self._values.get("message_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleIotEvents(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleIotEventsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleIotEventsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63ec6b773ea881755349e71b650d3aeb8651d6bbd8bdd46bf44924d085ae7573)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleIotEventsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cdcb351f270afc210fad3b01bb2310f3519eedf4b18b89268b627fca0a31f8a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleIotEventsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__718e3bbcc21fb12f455413235d0ba8ba3d796c4e6731289c9236b1421c563ec7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df46d688e8ed1eb7b2ea4b6e74558ad71847394a0ee6f454e3e9f056e9f09d5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d648f507dde752209b03bd5914c52ff4b05bb6710a1a5c2b023a3f1899e97da4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleIotEvents]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleIotEvents]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleIotEvents]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5ca65b3e560592561e8fd14dd0e912dfbe98b0d7a6b69711ce9cd8bb6bc99dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleIotEventsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleIotEventsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__005342832d0de621083574e277a87539a340e7cd16810136afd9661648bd532d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBatchMode")
    def reset_batch_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchMode", []))

    @jsii.member(jsii_name="resetMessageId")
    def reset_message_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageId", []))

    @builtins.property
    @jsii.member(jsii_name="batchModeInput")
    def batch_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "batchModeInput"))

    @builtins.property
    @jsii.member(jsii_name="inputNameInput")
    def input_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inputNameInput"))

    @builtins.property
    @jsii.member(jsii_name="messageIdInput")
    def message_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageIdInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="batchMode")
    def batch_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "batchMode"))

    @batch_mode.setter
    def batch_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77043f374c293123e2dad9f4a3469bcc8c4e5b20c80ce37d36b7facfa408a583)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputName")
    def input_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inputName"))

    @input_name.setter
    def input_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a66ff0966094faadad0fb1200e0a92c708adf57a96d52fbacd9ac337b831993d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="messageId")
    def message_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageId"))

    @message_id.setter
    def message_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c673f625b9fd8c9708bf3e373ff18b47b83c7957175f1a66f4d7e5a1bab853cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3475336cf8cd824e2b761ab5ae501a1d9f450fa3852a11a3b597e1ce4142dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleIotEvents]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleIotEvents]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleIotEvents]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49989f0b6b11af5df05ee251a5c8f93fc86ee2e284bc4563c33122b000f82a35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleKafka",
    jsii_struct_bases=[],
    name_mapping={
        "client_properties": "clientProperties",
        "destination_arn": "destinationArn",
        "topic": "topic",
        "header": "header",
        "key": "key",
        "partition": "partition",
    },
)
class IotTopicRuleKafka:
    def __init__(
        self,
        *,
        client_properties: typing.Mapping[builtins.str, builtins.str],
        destination_arn: builtins.str,
        topic: builtins.str,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleKafkaHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        key: typing.Optional[builtins.str] = None,
        partition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#client_properties IotTopicRule#client_properties}.
        :param destination_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#destination_arn IotTopicRule#destination_arn}.
        :param topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#topic IotTopicRule#topic}.
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#header IotTopicRule#header}
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.
        :param partition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#partition IotTopicRule#partition}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__959e64e52b405e9d2a26e9b10c594d3fe47d232d07d415e6861f1693a189d6c4)
            check_type(argname="argument client_properties", value=client_properties, expected_type=type_hints["client_properties"])
            check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument partition", value=partition, expected_type=type_hints["partition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_properties": client_properties,
            "destination_arn": destination_arn,
            "topic": topic,
        }
        if header is not None:
            self._values["header"] = header
        if key is not None:
            self._values["key"] = key
        if partition is not None:
            self._values["partition"] = partition

    @builtins.property
    def client_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#client_properties IotTopicRule#client_properties}.'''
        result = self._values.get("client_properties")
        assert result is not None, "Required property 'client_properties' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def destination_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#destination_arn IotTopicRule#destination_arn}.'''
        result = self._values.get("destination_arn")
        assert result is not None, "Required property 'destination_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#topic IotTopicRule#topic}.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleKafkaHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#header IotTopicRule#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleKafkaHeader"]]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#partition IotTopicRule#partition}.'''
        result = self._values.get("partition")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleKafka(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleKafkaHeader",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class IotTopicRuleKafkaHeader:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2906504c75e928160861a70de9f3e60e058fc9e0f3dbd6c4e46435117bdd3a44)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleKafkaHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleKafkaHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleKafkaHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__468a79200fc06a1755ca03221d5ba8d539b2d4abac2c0f42060391162e626cb2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleKafkaHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a362161fa5eda4c0986b66984b8762f7990f499508cce093a7914f51f0db94)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleKafkaHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c5846b21beb2bb6f44eec2ab72348c9990c4aee398b24210325e81a529855a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cdf6c5af31e571e71f765ea7880664005425134ccef2ab8c83cf0e156299429)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0bb4516c0f5908693571143de4c549179ed52c6f2b88363492a1f07451c18fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKafkaHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKafkaHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKafkaHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93af7e201aec005cd848a891d6a320b6e0926c73dc8731f3d747e12fae4edbfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleKafkaHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleKafkaHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6574eaa2b6857393eda2c5f4a08e47b445ac361ba3955da17f30209905b75975)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11982b1c59c51cab7ce5a24385b949c077f0a3bfa14373f02e49176d1a46b99a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32cbd7cf757393f0f9d082d045534db02dcd8975b5ebedc1639ca080e9b1eff9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKafkaHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKafkaHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKafkaHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1191980a46fe9375e4003c8ad6c314bdda8cbefe6a1c0d472024f8dd9cb7a3bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleKafkaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleKafkaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e2b3db84db6375b1cc138874c6b14694bfc0504a4fb7326eec29ffb29059fb8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleKafkaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e6a3d2a2387271489af2c26d0f7e78cd2be5ce02a7beb83b138528c37482004)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleKafkaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c11953a6cda0c3d9977cb2aaaea48f7269cb8eb3b74b15381f758082c61d8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de0ffc4b50d2f6c5dcda4b28bad36c6d73c37b156cef01ac214654e247884e4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__299a8ba93a245292300db5aebe32d908ecd11ab2d87afeb2cc17e8d2f6dfff7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKafka]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKafka]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKafka]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0d8379dc362165c2088175855184727447f0039d4cf69aa276d3612933250ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleKafkaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleKafkaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3a4c0deed6b0b116b0458be5b07c4302fdb424b795a94eb83ea8627db876bd1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleKafkaHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6128d9a973f4c265a9de9e4e6fce6d2904fcce5e36560a82dcd556b78c0956e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetPartition")
    def reset_partition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartition", []))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> IotTopicRuleKafkaHeaderList:
        return typing.cast(IotTopicRuleKafkaHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="clientPropertiesInput")
    def client_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "clientPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationArnInput")
    def destination_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationArnInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKafkaHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKafkaHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionInput")
    def partition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partitionInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="clientProperties")
    def client_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "clientProperties"))

    @client_properties.setter
    def client_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1306ffcbd1805e208244b9587523fdb3b5db1d2f3050da566d1cb8a73a52e404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationArn"))

    @destination_arn.setter
    def destination_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e62a7920bc3b25d20b22230713a3be087589b0b7e4caa7f423eb81de23d509e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__730647fe944e5bac2cbaee9fd929af777c628017bc3a56fcaa951b90ad5856b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partition")
    def partition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partition"))

    @partition.setter
    def partition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__540d09d20f4dd16a4757c1c9e691be9f6111537148a5a4b0c0870ef4ce40dce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1048feaa60950ed972af6348da8cb6e2fd4e9549c9c62701318144a7b955cc94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKafka]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKafka]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKafka]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03a80a27e04d9cba2d5879e22c9423edcaf5764920f7a59f281ba4f365e60554)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleKinesis",
    jsii_struct_bases=[],
    name_mapping={
        "role_arn": "roleArn",
        "stream_name": "streamName",
        "partition_key": "partitionKey",
    },
)
class IotTopicRuleKinesis:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        stream_name: builtins.str,
        partition_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param stream_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#stream_name IotTopicRule#stream_name}.
        :param partition_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#partition_key IotTopicRule#partition_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70e255f6336ea11f9d907461398d15620c6e1035d50393876ee63a753ffe8191)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
            check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
            "stream_name": stream_name,
        }
        if partition_key is not None:
            self._values["partition_key"] = partition_key

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stream_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#stream_name IotTopicRule#stream_name}.'''
        result = self._values.get("stream_name")
        assert result is not None, "Required property 'stream_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def partition_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#partition_key IotTopicRule#partition_key}.'''
        result = self._values.get("partition_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleKinesis(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleKinesisList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleKinesisList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00f7dc0eb273fdb14460d6394185cbedab2d54cce17dd3990ae6bee38ab90a44)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleKinesisOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba4dfba30bd2e419e42dad6eabeac3a67368c8285454e22f2b0c5b47aff5e43c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleKinesisOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d73157c9c87474f5f279393477fb82e4b466fb8744f6c9fcdcb002565c7e24f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e879e452c608b09e00c918fc3207c150dac6575bc14f950a8c7a4af5e1ed0d31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__980389de7735d0ac0c0410714e983c1075a34b941151fb1ec042bcc3c2fdf113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKinesis]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKinesis]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKinesis]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__980f4bd44a7b7e08529feebdef9c7fa821d205ea904809f3ab52d21296ae4323)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleKinesisOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleKinesisOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cb82441decd11ed55094babba497242e7b2514cdb0803c06ad14119ee628101)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPartitionKey")
    def reset_partition_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartitionKey", []))

    @builtins.property
    @jsii.member(jsii_name="partitionKeyInput")
    def partition_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partitionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="streamNameInput")
    def stream_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamNameInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionKey")
    def partition_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partitionKey"))

    @partition_key.setter
    def partition_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af1801296e23a620becd171764eb6f8021b740e232909a6cc3ba5858f1e25768)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0412e7467c1d21fc52a2e3e50dffa394c73655fc79ed612721fd7b6c7807448f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streamName")
    def stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamName"))

    @stream_name.setter
    def stream_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef4943663c06b3563d1191464fe4fe330463727271d60750d9ea0d57cd1142f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKinesis]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKinesis]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKinesis]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ef997c475b9dc5932c30fc7c1c89af2a5cefa43c6c1e6d10c97319447858a95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleLambda",
    jsii_struct_bases=[],
    name_mapping={"function_arn": "functionArn"},
)
class IotTopicRuleLambda:
    def __init__(self, *, function_arn: builtins.str) -> None:
        '''
        :param function_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#function_arn IotTopicRule#function_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d84bce0dcf01a8529f03e4b7100790d12286bf0bacb2dcab521c15b55493d957)
            check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_arn": function_arn,
        }

    @builtins.property
    def function_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#function_arn IotTopicRule#function_arn}.'''
        result = self._values.get("function_arn")
        assert result is not None, "Required property 'function_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleLambda(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleLambdaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleLambdaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca42ef6b7f6e7058a0933adca0c1ea98b92b08abc3a0bcb2d262d1e764185080)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleLambdaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__309e19ab268b92372fe07eed4874f0ea0511c19c28f5ab29e193cd5edfc166de)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleLambdaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43a3cf1728a772c49788ab20c747d71fc4accfddc3e529b363398f19c6f183fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd544143b416d7b7cf2a1d4864df2d991fe975822e23caec3096727ce6d018ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ae39743538db69d1007f0cee7a407b04030f45ab29208068d62954e62c258c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleLambda]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleLambda]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleLambda]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddaa06c059dec143027d02b8d45ee8898cd270b6f232dd54e60879f57408317c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleLambdaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleLambdaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__258b711a09995a0a90dc84186623b51714178c8062ab585c5e14b69f8b4ffb14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="functionArnInput")
    def function_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionArn"))

    @function_arn.setter
    def function_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68722d5d18c23f9d3c6c38052110c213bbcd368a187e1787310908b57e3c659f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleLambda]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleLambda]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleLambda]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b81c3b7ccd7fda1f493bab7e500d26724854f71ae14bc796d864635f933b2563)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleRepublish",
    jsii_struct_bases=[],
    name_mapping={"role_arn": "roleArn", "topic": "topic", "qos": "qos"},
)
class IotTopicRuleRepublish:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        topic: builtins.str,
        qos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param topic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#topic IotTopicRule#topic}.
        :param qos: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#qos IotTopicRule#qos}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e08fe52f07447f0833199f8645456f5d63448030b5f091dcb3bb24d374afba)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument qos", value=qos, expected_type=type_hints["qos"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
            "topic": topic,
        }
        if qos is not None:
            self._values["qos"] = qos

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#topic IotTopicRule#topic}.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def qos(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#qos IotTopicRule#qos}.'''
        result = self._values.get("qos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleRepublish(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleRepublishList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleRepublishList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16bc7b2159e28465e7c6ebff022ce81530a53d434fa71c19ff37b1d9847f340c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleRepublishOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba9607e15699ec886bb59f6f7448ed9fbaf2b1a0aff6a83d3ddf6a907d99410b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleRepublishOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9db952130002920e821d2a0aa297f91f6e450cc00cf88f88993468369551fe6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f594bb233e8b023e58774a3080be9e733c19b9fbd94ccc83dc87dd86916726df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e05e6a2a838561a29a30c822c344e60b1e8887730af12b71e43802dbda13bac8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleRepublish]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleRepublish]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleRepublish]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6be1726f0ff4b5ab75d33ab54e76a676174fcbab902fd033ee24f65f7fca085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleRepublishOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleRepublishOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c4eb61661335403985e4b1cb9fee0f29229c684fe491933fcf6ce82ff98ae22)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetQos")
    def reset_qos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQos", []))

    @builtins.property
    @jsii.member(jsii_name="qosInput")
    def qos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "qosInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="topicInput")
    def topic_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicInput"))

    @builtins.property
    @jsii.member(jsii_name="qos")
    def qos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "qos"))

    @qos.setter
    def qos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c440c368276eddea29a8ebf2a0182f37e5e312e5461dea8b02fe06c0c0c178fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35e62f94f8d18f4799724da10aaf0006a8599098439cdec9a91375aeb3f8ea92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75c27987ea95923fcd310d31afe8d4934d46c4c7ca73de01a3ca4de057679110)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleRepublish]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleRepublish]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleRepublish]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__168f231918661426f6238d6ce9bf245830d08607ddae19556b4853a35b84de56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleS3",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "key": "key",
        "role_arn": "roleArn",
        "canned_acl": "cannedAcl",
    },
)
class IotTopicRuleS3:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        key: builtins.str,
        role_arn: builtins.str,
        canned_acl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#bucket_name IotTopicRule#bucket_name}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param canned_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#canned_acl IotTopicRule#canned_acl}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab44c78bec3b7f943fa7509dd1c08ee033f107c0708733e1b918e5ffa2649de)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument canned_acl", value=canned_acl, expected_type=type_hints["canned_acl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "key": key,
            "role_arn": role_arn,
        }
        if canned_acl is not None:
            self._values["canned_acl"] = canned_acl

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#bucket_name IotTopicRule#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#key IotTopicRule#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def canned_acl(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#canned_acl IotTopicRule#canned_acl}.'''
        result = self._values.get("canned_acl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleS3List(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleS3List",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3e456a74d8bc835bce617cfa089f6a121e107bfb85639884f59401d02c0140a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleS3OutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c349726045ae5cdc4907db391f072e25f546156446efdacae2a4e9252e996a8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleS3OutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e2fc8f40f19623cc129eb53a91e540470fed39c24260402abc3a7f75933fc9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63f6ad50e1891c0515323cc2586ec8f4591f2e87eaa88d92af2d4e9d31b24ca4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9159db11961547e93b790d4c4af8371d95e0f1cba495090b1580e711e0399d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleS3]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleS3]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleS3]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12f66ded1825ec245d3875c985aff99f09ca6a07602ffb97d0dc918cb7c8ba83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleS3OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9023ccbb4cfce3f647caa16c0ab57a0f463b33de9c57c4d71335189eef34efc9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCannedAcl")
    def reset_canned_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCannedAcl", []))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="cannedAclInput")
    def canned_acl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cannedAclInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72a42b4d674a71f429a4e79716db0fcef5fbd3d14ee585a754b0b778d5fe4d55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cannedAcl")
    def canned_acl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cannedAcl"))

    @canned_acl.setter
    def canned_acl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6806767cc9112bfc8b41bac409c6de4d38803cb55b7ec7b5e268f5eca82f5af6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cannedAcl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf8fbb6e012520d2183c3b300a7b57624f29530fa98f7b858bc639052396c137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398e5259d5ee547e7a27edc24535eea168d305420f32c08806bf10dc45852e26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleS3]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleS3]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleS3]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__695cd3bb81cf232c302222bcd01a16ccaa6385bc6d18e8d860296cb761441732)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleSns",
    jsii_struct_bases=[],
    name_mapping={
        "role_arn": "roleArn",
        "target_arn": "targetArn",
        "message_format": "messageFormat",
    },
)
class IotTopicRuleSns:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        target_arn: builtins.str,
        message_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param target_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#target_arn IotTopicRule#target_arn}.
        :param message_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#message_format IotTopicRule#message_format}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b70853d0a444764b2cab4d9c44a1ded4fee1a94f5df5d74d7291ba2502e2df7)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
            check_type(argname="argument message_format", value=message_format, expected_type=type_hints["message_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
            "target_arn": target_arn,
        }
        if message_format is not None:
            self._values["message_format"] = message_format

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#target_arn IotTopicRule#target_arn}.'''
        result = self._values.get("target_arn")
        assert result is not None, "Required property 'target_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def message_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#message_format IotTopicRule#message_format}.'''
        result = self._values.get("message_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleSns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleSnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleSnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bbf0d65f3a33395b6c8e3689f216c95ee952de668519922604ca1eb691d3a1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleSnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__290bf9985523cdb33ef73d8dbf9292ea480149e5727955ef59a9b72092d4111a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleSnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fba95e7ba76e1363bf5a36bf63d3b1c1e5c3d16c27f1245ac719074495f2bced)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17f82669e97ae730cc1dc3c14348ea5a60b92c38becf487c57db9c31821db5d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e581b3b2a1c66be72274ba87d4c3e39cd4ac97b4fc57ea83ae33bfeebfec32a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleSns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleSns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleSns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a27ab745379625527a3c725bff6ec509ab43d77ef9892e38fef1507485a69792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleSnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleSnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f13802204d5d75a186afe0230deb5ff16275fb917349df64a19f396709f162c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMessageFormat")
    def reset_message_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessageFormat", []))

    @builtins.property
    @jsii.member(jsii_name="messageFormatInput")
    def message_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="targetArnInput")
    def target_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetArnInput"))

    @builtins.property
    @jsii.member(jsii_name="messageFormat")
    def message_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "messageFormat"))

    @message_format.setter
    def message_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5183bad06fa7cd1f44953dd29e73e7ce2c9a6976600251adbe5125303257907b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22ab4c529ce65a598d5b6e8c13547aa29435f59fcde4e52a3e2a45c19080177)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))

    @target_arn.setter
    def target_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbc0accd7e8f163b69d0fb4343e08905e1c7f4fad8a9f3f0d1e03b8bec8d646d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleSns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleSns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleSns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac245301cef0f06fe49bf43b0e6c083745aa97e98ec2cffbe3efc3c84102c801)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleSqs",
    jsii_struct_bases=[],
    name_mapping={
        "queue_url": "queueUrl",
        "role_arn": "roleArn",
        "use_base64": "useBase64",
    },
)
class IotTopicRuleSqs:
    def __init__(
        self,
        *,
        queue_url: builtins.str,
        role_arn: builtins.str,
        use_base64: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param queue_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#queue_url IotTopicRule#queue_url}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param use_base64: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#use_base64 IotTopicRule#use_base64}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89995371b9db7b828002c8aaf6c40fedbf03ccd48c7a53127185d2e1be8bf3e6)
            check_type(argname="argument queue_url", value=queue_url, expected_type=type_hints["queue_url"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument use_base64", value=use_base64, expected_type=type_hints["use_base64"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "queue_url": queue_url,
            "role_arn": role_arn,
            "use_base64": use_base64,
        }

    @builtins.property
    def queue_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#queue_url IotTopicRule#queue_url}.'''
        result = self._values.get("queue_url")
        assert result is not None, "Required property 'queue_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def use_base64(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#use_base64 IotTopicRule#use_base64}.'''
        result = self._values.get("use_base64")
        assert result is not None, "Required property 'use_base64' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleSqs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleSqsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleSqsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ac4b74d3c2c91df367554c5a83de20776e3d02ded07b82955b2c6c9d96797ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleSqsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f40f9e510df0205a826e1eb7de3899ac5044c4bb4bbbe900bb43391c9ee9529)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleSqsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a97fb3e3a58e85431f18dd54b7f11925dada8d7ccded0b98cf76ae589b9a09b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56753b9334e27f847125683e812e28fe1057c569d321a476349d2ce0fee92aa7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22697d7024a0ada259d446f7f2e2c4115e45ed1b105fd731c4c9c84d56d941c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleSqs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleSqs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleSqs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5339be1e0553e8cafd209c1d39cab65d75f353311a6e67cc135f727e8bdf40c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleSqsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleSqsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cf967a78c9af1a19c9a68d7e4d68a6747eb703fa6223f9db60cf7cf7bbb9000)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="queueUrlInput")
    def queue_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queueUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="useBase64Input")
    def use_base64_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useBase64Input"))

    @builtins.property
    @jsii.member(jsii_name="queueUrl")
    def queue_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queueUrl"))

    @queue_url.setter
    def queue_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a5cbae448fa5ad407014fa690b89eb7aaf2eed18e236a002e15f682ec68160a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6439786f88506da0be7245e296afe68ad83d8ea40758c1ad296b796547c937fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useBase64")
    def use_base64(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useBase64"))

    @use_base64.setter
    def use_base64(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9c091bec874f968ebccaa964bb5d5388cf38b51ba5f2c18d5f1d36189ea66be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleSqs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleSqs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleSqs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0de4d8f6d4a225541a4446eb017e74da6c1d3360b3e97aae694c1681f4c1dea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleStepFunctions",
    jsii_struct_bases=[],
    name_mapping={
        "role_arn": "roleArn",
        "state_machine_name": "stateMachineName",
        "execution_name_prefix": "executionNamePrefix",
    },
)
class IotTopicRuleStepFunctions:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        state_machine_name: builtins.str,
        execution_name_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param state_machine_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#state_machine_name IotTopicRule#state_machine_name}.
        :param execution_name_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#execution_name_prefix IotTopicRule#execution_name_prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b87ef73b4e0e92d254df820fba902e183d8af2cff2dfa3faae99e1bdd94f7333)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument state_machine_name", value=state_machine_name, expected_type=type_hints["state_machine_name"])
            check_type(argname="argument execution_name_prefix", value=execution_name_prefix, expected_type=type_hints["execution_name_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
            "state_machine_name": state_machine_name,
        }
        if execution_name_prefix is not None:
            self._values["execution_name_prefix"] = execution_name_prefix

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state_machine_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#state_machine_name IotTopicRule#state_machine_name}.'''
        result = self._values.get("state_machine_name")
        assert result is not None, "Required property 'state_machine_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def execution_name_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#execution_name_prefix IotTopicRule#execution_name_prefix}.'''
        result = self._values.get("execution_name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleStepFunctions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleStepFunctionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleStepFunctionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac5aec2f79c17d53033365d2443bfa650c02d72aaf7f2a13c5a150ce5b2e3394)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleStepFunctionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71d43b6e8fe0aabda909f6ca73ef664b3967fcc4e55452f8353794290ba55bdd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleStepFunctionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d576933533699e27b6c939cf5f5e69f04f9b6c621ceadb71d209fc01a81cdd7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__860704e8dd9a96c322ce472666607b380361bc08ce2f09a88289cd67d1e60c60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffa227954250e0ab42439047866b389b6c0253a8cc3155c81a690ed41c894086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleStepFunctions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleStepFunctions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleStepFunctions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__514785969113b41dd1907176a605966215bb0a89fdac38800f43da61b9f92671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleStepFunctionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleStepFunctionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e74f3721188300018d7e56a7ad0b238b793183c234e999385e3ac12dce98d49)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExecutionNamePrefix")
    def reset_execution_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionNamePrefix", []))

    @builtins.property
    @jsii.member(jsii_name="executionNamePrefixInput")
    def execution_name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionNamePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="stateMachineNameInput")
    def state_machine_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateMachineNameInput"))

    @builtins.property
    @jsii.member(jsii_name="executionNamePrefix")
    def execution_name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionNamePrefix"))

    @execution_name_prefix.setter
    def execution_name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf98ff68d7afcaff136d9dbbd9c6d58ef8af3ae0d56739bebcf1b07cb95bc6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionNamePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0f3c523e77e19b90e028ce8753fb6766411d9f296b619f95e1a33ac7fc37576)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stateMachineName")
    def state_machine_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateMachineName"))

    @state_machine_name.setter
    def state_machine_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00a694b3febf4573bad6b5bd07fab2bd873fe91b6ffe2fb0801a12a78958cd23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stateMachineName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleStepFunctions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleStepFunctions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleStepFunctions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2bdd6b188a9ce41627898907f45316034dd5a8411a8e7d789eaf6b86e56c2c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleTimestream",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "dimension": "dimension",
        "role_arn": "roleArn",
        "table_name": "tableName",
        "timestamp": "timestamp",
    },
)
class IotTopicRuleTimestream:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        dimension: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTopicRuleTimestreamDimension", typing.Dict[builtins.str, typing.Any]]]],
        role_arn: builtins.str,
        table_name: builtins.str,
        timestamp: typing.Optional[typing.Union["IotTopicRuleTimestreamTimestamp", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#database_name IotTopicRule#database_name}.
        :param dimension: dimension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#dimension IotTopicRule#dimension}
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.
        :param timestamp: timestamp block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#timestamp IotTopicRule#timestamp}
        '''
        if isinstance(timestamp, dict):
            timestamp = IotTopicRuleTimestreamTimestamp(**timestamp)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__108d7531d3d89160ba18ec723ad8459643a39501baf5c63ee0d41ee9e5a97831)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
            "dimension": dimension,
            "role_arn": role_arn,
            "table_name": table_name,
        }
        if timestamp is not None:
            self._values["timestamp"] = timestamp

    @builtins.property
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#database_name IotTopicRule#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dimension(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleTimestreamDimension"]]:
        '''dimension block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#dimension IotTopicRule#dimension}
        '''
        result = self._values.get("dimension")
        assert result is not None, "Required property 'dimension' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTopicRuleTimestreamDimension"]], result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#role_arn IotTopicRule#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#table_name IotTopicRule#table_name}.'''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timestamp(self) -> typing.Optional["IotTopicRuleTimestreamTimestamp"]:
        '''timestamp block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#timestamp IotTopicRule#timestamp}
        '''
        result = self._values.get("timestamp")
        return typing.cast(typing.Optional["IotTopicRuleTimestreamTimestamp"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleTimestream(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleTimestreamDimension",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class IotTopicRuleTimestreamDimension:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#name IotTopicRule#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f6f7febbf204f417d22179d294bb0c608c904029cbc03a0305db0de6bb5846e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#name IotTopicRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleTimestreamDimension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleTimestreamDimensionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleTimestreamDimensionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f0ecc1898b50cb180327035e1508c4b44df359c10a6a13eef5c330a928d5d9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IotTopicRuleTimestreamDimensionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abebfa251347308d58babe946d9305b2c4c88a553434113cebf08060a71cf58a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleTimestreamDimensionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c267095bfcf5b5bfbebedf02ecf52bd2ff494c20c85032b0994c948e95b83c75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f8343fb9b149b4eb94184f2159774ee4dd2fcdc0364848663e0e01e73c3401b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__061b08ec7afdb8eb7505de88452832387920e401009734a0f9767f26c8cfb569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleTimestreamDimension]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleTimestreamDimension]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleTimestreamDimension]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__147927de7d760226d57540946cb36afe3bfe51f77d940ee81cfeb0fe4283330e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleTimestreamDimensionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleTimestreamDimensionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__661e33e03a5c2d8bab4444c8ef78dd787251972c0ba17dca3a9ba86061a93e3f)
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
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2796d5f57a9e10e8c875829b89305bb920b03b405c1aca4cceb15cbadf19392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__136ffb0ffaa6329c840908998e265c5670f53597ba7f9eff3dd840d7fb975ec3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleTimestreamDimension]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleTimestreamDimension]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleTimestreamDimension]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db6bd033952bf015705952deeabe3562e61d65a6c426ed6ff5c82bffc6544590)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleTimestreamList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleTimestreamList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5a8ba3df92963c166bc605387ec70c92956bf106180c457f62193e2b43e4103)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "IotTopicRuleTimestreamOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7f91bc139968cea21026931cf7dae49810724bd4187bb365249dee8c2d13c0d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTopicRuleTimestreamOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1312bed4498686e7e676e659405e0f07190542d159c7563895331fe5760fbf8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a0fbb77c7748b272bdf3625d9b428a91080cb1830473983825b6b67d282ae4a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5379e7be50401859a75045a252881378f66f82fa142b61da06ef36a3b72ba3eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleTimestream]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleTimestream]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleTimestream]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24c359ab52d6021a0cc10f539469ffa8af20fa09c6801cb214fa0955d74ef347)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotTopicRuleTimestreamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleTimestreamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f720048d97753a644d25ae435d008ba4cf6eb0704c1e30fee550353f823b688f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDimension")
    def put_dimension(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleTimestreamDimension, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2af6fcafde1725aaf32d2c172c5d8976574493ca43af63cdae109c3de7d4fe35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDimension", [value]))

    @jsii.member(jsii_name="putTimestamp")
    def put_timestamp(self, *, unit: builtins.str, value: builtins.str) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#unit IotTopicRule#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.
        '''
        value_ = IotTopicRuleTimestreamTimestamp(unit=unit, value=value)

        return typing.cast(None, jsii.invoke(self, "putTimestamp", [value_]))

    @jsii.member(jsii_name="resetTimestamp")
    def reset_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestamp", []))

    @builtins.property
    @jsii.member(jsii_name="dimension")
    def dimension(self) -> IotTopicRuleTimestreamDimensionList:
        return typing.cast(IotTopicRuleTimestreamDimensionList, jsii.get(self, "dimension"))

    @builtins.property
    @jsii.member(jsii_name="timestamp")
    def timestamp(self) -> "IotTopicRuleTimestreamTimestampOutputReference":
        return typing.cast("IotTopicRuleTimestreamTimestampOutputReference", jsii.get(self, "timestamp"))

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionInput")
    def dimension_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleTimestreamDimension]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleTimestreamDimension]]], jsii.get(self, "dimensionInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampInput")
    def timestamp_input(self) -> typing.Optional["IotTopicRuleTimestreamTimestamp"]:
        return typing.cast(typing.Optional["IotTopicRuleTimestreamTimestamp"], jsii.get(self, "timestampInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b5d13d24846ba8377443a2050fe5505774f8b00c3a5aaba69bf2154306e3c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b66ba66d94de46eab4b7b7e4f5e76896e8f5bb4e60081701379be88edf476e37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2f983158fd61ddc2fe83f06e27bfdfc66824f7b9a4a906826ed1a29fd9365bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleTimestream]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleTimestream]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleTimestream]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99cc2e0f456d1921cf1e636a5d0b996e5ee44645dcd7bcc5e718c5e70264a8f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleTimestreamTimestamp",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class IotTopicRuleTimestreamTimestamp:
    def __init__(self, *, unit: builtins.str, value: builtins.str) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#unit IotTopicRule#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d734b0fb8a7187601faaff56b8fa9a170ea33e164fabac79963b881fd1453d30)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#unit IotTopicRule#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/iot_topic_rule#value IotTopicRule#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTopicRuleTimestreamTimestamp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTopicRuleTimestreamTimestampOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.iotTopicRule.IotTopicRuleTimestreamTimestampOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__085af48fd5833630a07412203da0d2a0fd9f464c2babc79f8e7e19f0e500ac4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="unitInput")
    def unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unit"))

    @unit.setter
    def unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3d285c0260f99924c3d89e58d8b3bd6ade80a21c04b3147d1b13e4b0dd7dc4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ce9b6376bad56878a5294a50028af705ba5efbdbf46e28cbee6cd6908f1a9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[IotTopicRuleTimestreamTimestamp]:
        return typing.cast(typing.Optional[IotTopicRuleTimestreamTimestamp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotTopicRuleTimestreamTimestamp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1291238d4f2ad30cfbff56bc82c58df648512adc52e9fcca3038f2106d11449a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IotTopicRule",
    "IotTopicRuleCloudwatchAlarm",
    "IotTopicRuleCloudwatchAlarmList",
    "IotTopicRuleCloudwatchAlarmOutputReference",
    "IotTopicRuleCloudwatchLogs",
    "IotTopicRuleCloudwatchLogsList",
    "IotTopicRuleCloudwatchLogsOutputReference",
    "IotTopicRuleCloudwatchMetric",
    "IotTopicRuleCloudwatchMetricList",
    "IotTopicRuleCloudwatchMetricOutputReference",
    "IotTopicRuleConfig",
    "IotTopicRuleDynamodb",
    "IotTopicRuleDynamodbList",
    "IotTopicRuleDynamodbOutputReference",
    "IotTopicRuleDynamodbv2",
    "IotTopicRuleDynamodbv2List",
    "IotTopicRuleDynamodbv2OutputReference",
    "IotTopicRuleDynamodbv2PutItem",
    "IotTopicRuleDynamodbv2PutItemOutputReference",
    "IotTopicRuleElasticsearch",
    "IotTopicRuleElasticsearchList",
    "IotTopicRuleElasticsearchOutputReference",
    "IotTopicRuleErrorAction",
    "IotTopicRuleErrorActionCloudwatchAlarm",
    "IotTopicRuleErrorActionCloudwatchAlarmOutputReference",
    "IotTopicRuleErrorActionCloudwatchLogs",
    "IotTopicRuleErrorActionCloudwatchLogsOutputReference",
    "IotTopicRuleErrorActionCloudwatchMetric",
    "IotTopicRuleErrorActionCloudwatchMetricOutputReference",
    "IotTopicRuleErrorActionDynamodb",
    "IotTopicRuleErrorActionDynamodbOutputReference",
    "IotTopicRuleErrorActionDynamodbv2",
    "IotTopicRuleErrorActionDynamodbv2OutputReference",
    "IotTopicRuleErrorActionDynamodbv2PutItem",
    "IotTopicRuleErrorActionDynamodbv2PutItemOutputReference",
    "IotTopicRuleErrorActionElasticsearch",
    "IotTopicRuleErrorActionElasticsearchOutputReference",
    "IotTopicRuleErrorActionFirehose",
    "IotTopicRuleErrorActionFirehoseOutputReference",
    "IotTopicRuleErrorActionHttp",
    "IotTopicRuleErrorActionHttpHttpHeader",
    "IotTopicRuleErrorActionHttpHttpHeaderList",
    "IotTopicRuleErrorActionHttpHttpHeaderOutputReference",
    "IotTopicRuleErrorActionHttpOutputReference",
    "IotTopicRuleErrorActionIotAnalytics",
    "IotTopicRuleErrorActionIotAnalyticsOutputReference",
    "IotTopicRuleErrorActionIotEvents",
    "IotTopicRuleErrorActionIotEventsOutputReference",
    "IotTopicRuleErrorActionKafka",
    "IotTopicRuleErrorActionKafkaHeader",
    "IotTopicRuleErrorActionKafkaHeaderList",
    "IotTopicRuleErrorActionKafkaHeaderOutputReference",
    "IotTopicRuleErrorActionKafkaOutputReference",
    "IotTopicRuleErrorActionKinesis",
    "IotTopicRuleErrorActionKinesisOutputReference",
    "IotTopicRuleErrorActionLambda",
    "IotTopicRuleErrorActionLambdaOutputReference",
    "IotTopicRuleErrorActionOutputReference",
    "IotTopicRuleErrorActionRepublish",
    "IotTopicRuleErrorActionRepublishOutputReference",
    "IotTopicRuleErrorActionS3",
    "IotTopicRuleErrorActionS3OutputReference",
    "IotTopicRuleErrorActionSns",
    "IotTopicRuleErrorActionSnsOutputReference",
    "IotTopicRuleErrorActionSqs",
    "IotTopicRuleErrorActionSqsOutputReference",
    "IotTopicRuleErrorActionStepFunctions",
    "IotTopicRuleErrorActionStepFunctionsOutputReference",
    "IotTopicRuleErrorActionTimestream",
    "IotTopicRuleErrorActionTimestreamDimension",
    "IotTopicRuleErrorActionTimestreamDimensionList",
    "IotTopicRuleErrorActionTimestreamDimensionOutputReference",
    "IotTopicRuleErrorActionTimestreamOutputReference",
    "IotTopicRuleErrorActionTimestreamTimestamp",
    "IotTopicRuleErrorActionTimestreamTimestampOutputReference",
    "IotTopicRuleFirehose",
    "IotTopicRuleFirehoseList",
    "IotTopicRuleFirehoseOutputReference",
    "IotTopicRuleHttp",
    "IotTopicRuleHttpHttpHeader",
    "IotTopicRuleHttpHttpHeaderList",
    "IotTopicRuleHttpHttpHeaderOutputReference",
    "IotTopicRuleHttpList",
    "IotTopicRuleHttpOutputReference",
    "IotTopicRuleIotAnalytics",
    "IotTopicRuleIotAnalyticsList",
    "IotTopicRuleIotAnalyticsOutputReference",
    "IotTopicRuleIotEvents",
    "IotTopicRuleIotEventsList",
    "IotTopicRuleIotEventsOutputReference",
    "IotTopicRuleKafka",
    "IotTopicRuleKafkaHeader",
    "IotTopicRuleKafkaHeaderList",
    "IotTopicRuleKafkaHeaderOutputReference",
    "IotTopicRuleKafkaList",
    "IotTopicRuleKafkaOutputReference",
    "IotTopicRuleKinesis",
    "IotTopicRuleKinesisList",
    "IotTopicRuleKinesisOutputReference",
    "IotTopicRuleLambda",
    "IotTopicRuleLambdaList",
    "IotTopicRuleLambdaOutputReference",
    "IotTopicRuleRepublish",
    "IotTopicRuleRepublishList",
    "IotTopicRuleRepublishOutputReference",
    "IotTopicRuleS3",
    "IotTopicRuleS3List",
    "IotTopicRuleS3OutputReference",
    "IotTopicRuleSns",
    "IotTopicRuleSnsList",
    "IotTopicRuleSnsOutputReference",
    "IotTopicRuleSqs",
    "IotTopicRuleSqsList",
    "IotTopicRuleSqsOutputReference",
    "IotTopicRuleStepFunctions",
    "IotTopicRuleStepFunctionsList",
    "IotTopicRuleStepFunctionsOutputReference",
    "IotTopicRuleTimestream",
    "IotTopicRuleTimestreamDimension",
    "IotTopicRuleTimestreamDimensionList",
    "IotTopicRuleTimestreamDimensionOutputReference",
    "IotTopicRuleTimestreamList",
    "IotTopicRuleTimestreamOutputReference",
    "IotTopicRuleTimestreamTimestamp",
    "IotTopicRuleTimestreamTimestampOutputReference",
]

publication.publish()

def _typecheckingstub__b45e1ae3ba975fb518e21d4913b5680c6553ec7bf5d738ba558a3b215f6b8974(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    sql: builtins.str,
    sql_version: builtins.str,
    cloudwatch_alarm: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchAlarm, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cloudwatch_logs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchLogs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cloudwatch_metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchMetric, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    dynamodb: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleDynamodb, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dynamodbv2: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleDynamodbv2, typing.Dict[builtins.str, typing.Any]]]]] = None,
    elasticsearch: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleElasticsearch, typing.Dict[builtins.str, typing.Any]]]]] = None,
    error_action: typing.Optional[typing.Union[IotTopicRuleErrorAction, typing.Dict[builtins.str, typing.Any]]] = None,
    firehose: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleFirehose, typing.Dict[builtins.str, typing.Any]]]]] = None,
    http: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleHttp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    iot_analytics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleIotAnalytics, typing.Dict[builtins.str, typing.Any]]]]] = None,
    iot_events: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleIotEvents, typing.Dict[builtins.str, typing.Any]]]]] = None,
    kafka: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleKafka, typing.Dict[builtins.str, typing.Any]]]]] = None,
    kinesis: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleKinesis, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lambda_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleLambda, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    republish: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleRepublish, typing.Dict[builtins.str, typing.Any]]]]] = None,
    s3: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleS3, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleSns, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sqs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleSqs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    step_functions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleStepFunctions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timestream: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleTimestream, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__a713e3cc295c9802e9b7d0be09158119e2a868a054d750dc29f91666611c0645(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d797fa6b787ac7f1745eb7d2dd035735b705bed29447f6480f55b09ebccfce48(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchAlarm, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140bce2e6812ae81d017d2dd79890bb9b9b0367da7d74132203ff38f62b7138d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchLogs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83bf3e1e4159dd69f952a696a82b3c93a40984aeb980afb889af3abcf471d1e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchMetric, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bb6dafe34bcbe8b1825e6f0055e100372cd1ddde6e33da26222486eacc0f624(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleDynamodb, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b40b3eb64ede3602937d725e0859d98d7b75c98b0251f26aedb0ccd19a0d098(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleDynamodbv2, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d7b9339cb7dcae977deb36786aabfb2406f9785c586c74ee24988502e75e23(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleElasticsearch, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05cdcc38d9687756e2cccd11a4f1ccb0f39a5d40c78062dcc96e507b62c1d6bb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleFirehose, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d58c001f8a9700750e51d8d83a41798e962b6cddecdf3bbdfedcc4c1a789f0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleHttp, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61ab0288529bdc66ee7dcec7afe336f5ce91dcfecfbf6070c569cc77fa850ec8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleIotAnalytics, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b2bd6af5d4bb2315c4ead64be7600d59b1a720b4b1924fd174bd933b36bb2e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleIotEvents, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd078726b7bbff972a39a0716216685277f735a324d3f90f155b61854aee9c1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleKafka, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d385cbebabbc5480af1b2e429613f512a55f9030407a95bd490eb8788db96778(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleKinesis, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a2fd2f6542b6ef1cddd15cd3c441e9af4dec3a88e252769125314993af0290(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleLambda, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b54e1b780bf6014f0add89176e5e7f8fb3ec4aea8c2fcb4c3d5329809cc779(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleRepublish, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d343cbeec79bc43d2e4c9c295bcb1e94d8c4b1f61e5eabfc26372c044866b432(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleS3, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb358933a4524c7137d01d71f735920da557c95c7b4bd570373534694828994(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleSns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68a04bae15f8544f5de2790917c9a9ac7335a6bc00428ad5dddf84babaa50a29(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleSqs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8a6ead495c6065732b3dc9ad82cfa19e6f4d91fcf7d41af8f32f9f32663b00(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleStepFunctions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__069b369fcc028228a23b2136821e2213dbcb0bf686596b4a4e8067f38d5f73c0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleTimestream, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc08c7c77a900e6a7a014f51abca9108d8051e850ecee3cb64d9890c55a3da5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26f5e85b3121086e850b8cd84256fffeed1882a1e0754893d0cb59e3e4baa356(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3d9c28b33df5fc10efeadc95080ca4bb97d6bce521edfc4e495eeeede9a39f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00d7abaea17b2bba059f305993879e8679e0624f13a5f48a52dfea890b15e675(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3f33afa6a85a497d7872002f522feb0ea2d4ef8e681fb0ac59cacec39798dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb40b58c35acaf50f5c762585273ab06a8875e53840dccccaa4295f1701e6875(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175235d6524b2dad212ae70a2656655b0f75fab75cba1728a5a5f9bb872b0909(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7ae3631ebb1b576cea996c6e3d214990f4d89f37779d85bb86155484c4fadb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bede94c35cd68d0020eb5a8dea706f641a7a793d13d7f783ab6e849fa726d1c3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f78171057e8280666918ad6edf9efc89cc4adb00cb36043a02f7934f8fb349(
    *,
    alarm_name: builtins.str,
    role_arn: builtins.str,
    state_reason: builtins.str,
    state_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__236e0fa0a13083ae880bdf950cc64e589e4d882ce8472884903f88b42811a9a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__507e6daf464b1f441a516484189a4e3995ac6dd81429b987a1cf4c4b84324c2d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f313345b104b79935f8db3ddf3948c6f2f0e9c2d0b179c7c0ee852a1fca81ce0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daeb7b82efb71a66cf18700252551808c37eda28f476a0bee2ae5da4e48d0f67(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424aec70420f70789d658e3eb60690ff91a665cc4b7aece87a063f393237ba9e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35e6f1281738fd3f1863d0879f9d3e4121038da3998830b5f843b25425e33e0b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchAlarm]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55aebef1bcf186dddabfef20573910bb8167b2c81e077985984132c6b137b17a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c6fd8e4bbbf2cf81decb1df7a1080d6221ef31aa64bc0b1b782c7846b978ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1702cdd8af7ba07b9e3dc18ac5f92e89788c59105aaf6faa7ebbe2979606370(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__305d1f2bd2a246960fdea47662a10c1a5979a832a230c79c6730817d5b9f32fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e81ad058f9190a3538ee35122c6f7fb11b440e48baac4b17e3431685c9af0f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac7fcb487791af6ab8deff6cb35f7478557cfcf1a030116341d1d2a0732394e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchAlarm]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93713ee7d872c594fdfb0e08132caf1cbfaf66341ab164e802f2e5b75cde4057(
    *,
    log_group_name: builtins.str,
    role_arn: builtins.str,
    batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9b66df9dcf29a49db6e5559f083ada496326fac4870cf8aee3797ba3c08305(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61bf7349537d85aff4fa7e44c501f3eef06d63de571a405eba291d6da5f8316e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d9a3a7ff03ce3e412989c33553787f288b1fd5ec8900ea5ae32cf50a466a938(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2c9593db9317932ac30364049c69aaed20c8bf603a853bfc4eeb1e2e8f48d80(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7637f4bd129bbfaa83ae2dbaf3eeb20458257fb7e7f61906b44ef92fb3d913(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50124bf02962055fd930534e2facb4e3dca25bbcea4977ac2f221e71748907c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchLogs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7af28cb182003ed5ae4bf594f3532a4f7e4028a53ff5ee66d7d25f1113b5d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__164a8ef3d0c2b99e81240afe8a7c86c389c3fcfd4ebf94a04feac8763e627088(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20300e3b9ac827d6852dfaba8e26ec03bf8adca36803e33bc4fa54ac8979cca8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8361e1a8e7d4a71b4b168f0df911abc9eb81dc39484bff861523dcd517da39d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff2326e93cfef79d31e6cfcf28b737d2488e86cffa1eb3586adc7b7a38215160(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchLogs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91c1edeb1b50e46f12dcffb2508a171e8df23e7fa3d9027b9cea3e069643dd42(
    *,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    metric_unit: builtins.str,
    metric_value: builtins.str,
    role_arn: builtins.str,
    metric_timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b54fea1a502f208f7ce70c5fd3f287f71c80942f328f48eaf463b37922a6ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d4b6fe9c43538a123356a92743caf2c6816142088103a587978e257415cd9f7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba2810e9f780992d0afcf87075e41c3e5ae7476f52c22ce9cde023e963c63e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5d0d3e02546ab7aeccce9229f66480512b206e1aa770c23538996a74db07d05(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ab22bd84e3d899a00ad2d5a0b6daf6ba9e8358bf2a14d6442a8c741d24d920(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a755dc3359040762b278d7f08e0d7210e36c8aafa45f5a4df8938daf0fa3f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleCloudwatchMetric]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1ddc4a783bd0ca8cb8f953bf536c7f821b6975573126e5a2fcec51ddfb8216(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1baeda0bff9cf2aaed12e5d0e2b6f79aec42faefabc4f843c2a36a0f2e4825e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5768537db757b139cd4a168d8c7d984faf440f68c8432b67b6c9ad69a8f50664(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b04eb177377e8afa17b90a6c7c785529109821f78b50a6be9a7008f9446d584d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c816afa8b83d5384d4ec39c933b8bb320475124b24de424d5a585ae3e588cec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40762939d79f9151cccc5fd28cdd37fc5fcfbefce27cf2add1bebce4123d98c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7d2a76936568fed0c4e10d81cbb7298c9606053926cc496db9ee05c7d86292(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__115305d7ba789f5b5486d6814e99a1a1041c17ba80bcf09e12a6385a72fa50c6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleCloudwatchMetric]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d5e36ad582bd0bbecb9ef5ebcce1871c33bd0b890877a62f3d2de422abebc9e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    sql: builtins.str,
    sql_version: builtins.str,
    cloudwatch_alarm: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchAlarm, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cloudwatch_logs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchLogs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cloudwatch_metric: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleCloudwatchMetric, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    dynamodb: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleDynamodb, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dynamodbv2: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleDynamodbv2, typing.Dict[builtins.str, typing.Any]]]]] = None,
    elasticsearch: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleElasticsearch, typing.Dict[builtins.str, typing.Any]]]]] = None,
    error_action: typing.Optional[typing.Union[IotTopicRuleErrorAction, typing.Dict[builtins.str, typing.Any]]] = None,
    firehose: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleFirehose, typing.Dict[builtins.str, typing.Any]]]]] = None,
    http: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleHttp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    iot_analytics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleIotAnalytics, typing.Dict[builtins.str, typing.Any]]]]] = None,
    iot_events: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleIotEvents, typing.Dict[builtins.str, typing.Any]]]]] = None,
    kafka: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleKafka, typing.Dict[builtins.str, typing.Any]]]]] = None,
    kinesis: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleKinesis, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lambda_: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleLambda, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    republish: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleRepublish, typing.Dict[builtins.str, typing.Any]]]]] = None,
    s3: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleS3, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleSns, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sqs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleSqs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    step_functions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleStepFunctions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timestream: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleTimestream, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de5bfde10f7023d2e9a39148e23846d5d17348898d1fffe851927cb0431c614(
    *,
    hash_key_field: builtins.str,
    hash_key_value: builtins.str,
    role_arn: builtins.str,
    table_name: builtins.str,
    hash_key_type: typing.Optional[builtins.str] = None,
    operation: typing.Optional[builtins.str] = None,
    payload_field: typing.Optional[builtins.str] = None,
    range_key_field: typing.Optional[builtins.str] = None,
    range_key_type: typing.Optional[builtins.str] = None,
    range_key_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83784e0ef069f23df98f3060e8b76c8761333965f1470b485d3ac949509361e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7a0222a325176c7f5fbc862f2e89fc068ebf7d2edf3c54294dbede9c585006f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7c2f6c884e5e6dbecfd6e95609367d6f98b9497907726765266ba0bae81608(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42079d67fe632a37f94f4621969226299596d9d86b19866d5c786d9ece34cc34(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac7619fc5f6bff8bb4b1ce09712bd4c459923a6a10b44bf02508d267cc7a829e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a8ebc2a8e6ca5a7b9477500343d4d064058f1f82ee98eb6ffd862482471847(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleDynamodb]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efba57e5790520fd8ed4b4c7e14297abf9d0b9938361f5f29a9978aa353f52ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3941fe9675002efa2d3eaffbee00f741708a0c5ed3e9c37d493f8ab62078dc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__477caa3ae23928c6f784676853e340441f813b0b13e909d687203daa09abd180(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c162d106fb95fcdc6f6fcf034ec26cd24ba6474edb5a4352e3d2b07473afc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3407d54dee4a1de681bc6b36be9b550abe902742fea42781720d72ec2731160(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75cb4d7a635ddb1bb5ce75bdc116835ecd309d34d094f6c8a52457b979ebb62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f1d9f3132cc2875d1dcc998caf02d772c2344f18c5761ff3502df0ee421a095(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39fb59bd621764de07c7069a983b25d339d0072908f09153c9fab05d16f70322(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91c91fe0aed4299a982072187dd690304a8abd91c528f819a0dd582117c6d697(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56f2ee818e41a405d8e8241b8cfcf2a4b5076815bfcfefb19620523e0d0a1ed1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2204c501881c002d6353f73bc92159f0c41f9ff4758fa0af51b7f634f361782(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7088dd9d0140f5e172f76388b76cb658993b5d4afbcc2223fbbfbce6648dbbf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleDynamodb]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a278afcd3e7d39f1647fdfdd200be2659d27b37f113002f1dd82a7507d95d64b(
    *,
    role_arn: builtins.str,
    put_item: typing.Optional[typing.Union[IotTopicRuleDynamodbv2PutItem, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa8baf1ed4a33f15e1e3b52ba46edfa9f98ef27baf569896a5df025306cb579(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__689d7dc073296dd3f0dd072e738a459280debbb4ac7e30b69cf76c656ec2bae9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b48db3c9ce731d4edf90ac140309ea9eca162e3da1395ff8464f540e05942c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a78f1aef77497d17f26e1c68ff78260bfde39d96c1fd674b19869dd2138836b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac9a0ae096b4095bc67c83bfb373b0deb470adeac553382a88081d31073cb6d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1feb555d4c615bbcd71b9b92419402bb381f632cb363f1befee01d65153f6b0f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleDynamodbv2]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e60c5a15a461a6ddf8000ee3bef10a41df0e7bb6e3e34b1aa48d5c8156f9f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4518dbc28105a42b8dc6523a1ac9c63d69953e0b0c8711396aaed58f62b819(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf9dc788ed76f6e1f30540cc777b2f62fc56a7676ced00369ee241d68dc4cf7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleDynamodbv2]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b56de5901f8c8320403b4a219629b60211c351f1922ed9f76411ab00a7bd46(
    *,
    table_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c9203f2fa1cede33d55c753b862f655c3c223ed27401e41773f0d6e8e6e85c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d28cb9909dca30426b046f36f95175eca1cd4b1964a00bbbf040f6b1fbeb3ed5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9397ac1bd495777c04184787ea7516defbd378a54dd8e9e88945297538796437(
    value: typing.Optional[IotTopicRuleDynamodbv2PutItem],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c9aa54d683eace9924b11b40c2edf3a5ab14fe3f027cde186b0b010ceb6946c(
    *,
    endpoint: builtins.str,
    id: builtins.str,
    index: builtins.str,
    role_arn: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c259596c94de46e157c74233d68139363a000785f81fdaa2e9ec320abd595184(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5485d611bd71539a3a3a0707237e6ca920d5fab7481dcae26114a5a2885f4df1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a9a46ffd97eeabf4574bef19761cf9c73727a54128b5c269ee8b415460c1cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__218fa7955b148359eff582591fd60dd8b1211a403702a446568c39ba93354835(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a33247d18a23ecc7b0bbc0040ec756515597ed89b69d18369cd4c4c15903e4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__483176c8c6727b06cd951be31ab64133db8bca47c7c54954e3649a704b70e8ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleElasticsearch]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb2df3bd752ab9b5c82f34cfa4330c5c462ec2dfa5d75720a351d3983b9c9ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34447678fcbfb3468f1f8d470206f5330ca1f654df452c0e4cf4e847a37346f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54f2a1e645426bc56f95d5085e708624637c70f181b5a84131b677696d227b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b1de54b34ea946d81a3ad5c1e4af8efd517f72aa125d5e68694ee726598dc97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03276da3fb065b0a81d74a8247691b05f843da239b6180966aa2394e50aaccc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb64f9bea3aa339026cecdfe0472760769346f86b865c7e7b4cf1236ecceb244(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e79ff328f52e215c33878800bc29c85f5678ccfb775589cdbad0a4dc3e495e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleElasticsearch]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d5218b66bab7b0668e523e8d495820176210dab6e47099ae5ed9bde2e84e1d1(
    *,
    cloudwatch_alarm: typing.Optional[typing.Union[IotTopicRuleErrorActionCloudwatchAlarm, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudwatch_logs: typing.Optional[typing.Union[IotTopicRuleErrorActionCloudwatchLogs, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudwatch_metric: typing.Optional[typing.Union[IotTopicRuleErrorActionCloudwatchMetric, typing.Dict[builtins.str, typing.Any]]] = None,
    dynamodb: typing.Optional[typing.Union[IotTopicRuleErrorActionDynamodb, typing.Dict[builtins.str, typing.Any]]] = None,
    dynamodbv2: typing.Optional[typing.Union[IotTopicRuleErrorActionDynamodbv2, typing.Dict[builtins.str, typing.Any]]] = None,
    elasticsearch: typing.Optional[typing.Union[IotTopicRuleErrorActionElasticsearch, typing.Dict[builtins.str, typing.Any]]] = None,
    firehose: typing.Optional[typing.Union[IotTopicRuleErrorActionFirehose, typing.Dict[builtins.str, typing.Any]]] = None,
    http: typing.Optional[typing.Union[IotTopicRuleErrorActionHttp, typing.Dict[builtins.str, typing.Any]]] = None,
    iot_analytics: typing.Optional[typing.Union[IotTopicRuleErrorActionIotAnalytics, typing.Dict[builtins.str, typing.Any]]] = None,
    iot_events: typing.Optional[typing.Union[IotTopicRuleErrorActionIotEvents, typing.Dict[builtins.str, typing.Any]]] = None,
    kafka: typing.Optional[typing.Union[IotTopicRuleErrorActionKafka, typing.Dict[builtins.str, typing.Any]]] = None,
    kinesis: typing.Optional[typing.Union[IotTopicRuleErrorActionKinesis, typing.Dict[builtins.str, typing.Any]]] = None,
    lambda_: typing.Optional[typing.Union[IotTopicRuleErrorActionLambda, typing.Dict[builtins.str, typing.Any]]] = None,
    republish: typing.Optional[typing.Union[IotTopicRuleErrorActionRepublish, typing.Dict[builtins.str, typing.Any]]] = None,
    s3: typing.Optional[typing.Union[IotTopicRuleErrorActionS3, typing.Dict[builtins.str, typing.Any]]] = None,
    sns: typing.Optional[typing.Union[IotTopicRuleErrorActionSns, typing.Dict[builtins.str, typing.Any]]] = None,
    sqs: typing.Optional[typing.Union[IotTopicRuleErrorActionSqs, typing.Dict[builtins.str, typing.Any]]] = None,
    step_functions: typing.Optional[typing.Union[IotTopicRuleErrorActionStepFunctions, typing.Dict[builtins.str, typing.Any]]] = None,
    timestream: typing.Optional[typing.Union[IotTopicRuleErrorActionTimestream, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ec52e73f453a37aaa910eee67b494d2e65ebcf71eef4a8315fd9325844b0ff(
    *,
    alarm_name: builtins.str,
    role_arn: builtins.str,
    state_reason: builtins.str,
    state_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d961dc75e0afa1e0f4d62d603b4d8cb2c80c59c2ae704d94409d1e79668c41b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9658585f4fbf4fe47e2f077f5335680d54403fc3a6c389474f58b64ca2eb9414(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3145eb0c30048a377434f8be190e2de41b50afdabac121aafd52f165eebd9ca3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11b7044d43ca3975a9503a1f310fb0280c75f0d9e8ebfc644522dfd66dffcd09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f660d6461d801dd04eaab028b485404880a3c05f0d39316fbe825e9c98bd300(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21a37e009bb2f53cadb702f1ecbf64345d3e966dfa5925b7173343911ddd7696(
    value: typing.Optional[IotTopicRuleErrorActionCloudwatchAlarm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257012640b51813558139969c202d4368478abe1067fd1dbb5134e7f686c513e(
    *,
    log_group_name: builtins.str,
    role_arn: builtins.str,
    batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc62889bca2f770ace431f39e532fc8c3b4aff3f6aaa1b59eff6dd3ea80153c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea89f5b0962c5352943948dc3f34bb23c983d5b0b544c545c2c3456376348f2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002b6f278e4b4dd2a58d6319e976e8acdeda7a8a4f8f0ccd6e39684f56643895(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb9981a05e3b200d4412029275e30757cdfcfb3ac1763ae3c17cd2d9ce04f44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f20711efa311b3af460609d9e2b9908d815d213b2bd238c0c228b232f654355(
    value: typing.Optional[IotTopicRuleErrorActionCloudwatchLogs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be5658fae73dcd7ae5a7f368c98c3a48d56f2ae6484971644df06ed4474ae994(
    *,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    metric_unit: builtins.str,
    metric_value: builtins.str,
    role_arn: builtins.str,
    metric_timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fd375ef64c508e107e31dd21af226070098af2fa28fb737a9f5627cba4fc25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be4882ce8e99b16a5d5126d72564557bdb6d5292c4506369b0e41ca779672d52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f105f887cd86d213d0fceb98fca178c5e6cdb8909c8c26f5c5dae704137eb740(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a2173244eeeeec39653b1ae7838722815c97a7466b225d235ab9d1bba5287ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbae9c6d8a0adc188fc06e127d5bfcf177ecdd71ab34503217f71396d32e01c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e16b5eb63a6a1fe86677fe9e892f786cf72dacdb04a5f0a75188005873489f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a9d4939f24132dd55bdabfd70c9abd441ebfebd2fc9071d542e52142edd57c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12a0a24f3078a904169462dd3de5e1096f5e9fb17f3641f448854addf476285(
    value: typing.Optional[IotTopicRuleErrorActionCloudwatchMetric],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f625d24ea319b6ca47f9b9a94ff9769b5b324f7779d6808f8527f0780c5a6151(
    *,
    hash_key_field: builtins.str,
    hash_key_value: builtins.str,
    role_arn: builtins.str,
    table_name: builtins.str,
    hash_key_type: typing.Optional[builtins.str] = None,
    operation: typing.Optional[builtins.str] = None,
    payload_field: typing.Optional[builtins.str] = None,
    range_key_field: typing.Optional[builtins.str] = None,
    range_key_type: typing.Optional[builtins.str] = None,
    range_key_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d386780a825da6a356fdd684436be2a39c6528e0f47031be59291180d0dbf8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2b629fd278d624dfb809faf2cfa0d46ae405924b3953f2c9adc397cf5ea973(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a6a38c3ddc07d2d7950d80624b65b10392a53706c081f7eb8a61ed8d606085(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1665f1a41b11535621723e6d4b93702159a17e78fb6bc0a2e914055ceec85eae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eacc234eff1ec97e00f1443ef32be666023dd66e4718fe6cb35a597645a9c973(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a10cd62f267fe404a711726c1f636fb79dfedbe2c4947d160bce06f3d15604ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31bd8d22fa206e441e9c7e3868784fd0974fdda4937d7842aeb775bc94fc5994(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e9406736a39c56084d3d5c7eeec3587d68a4ab058ede4445bdd0e31ee4a637f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d8a442c8a31051f88cb150c69ea7eced1a29a7723de635d887af8338962e9cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c6cddeb5340592761116767fb98ea939c7c93799e04ff418d5aaa3d8e74c613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f9e51da26e1b0775a35ec706f9d33f86efd3e8a68c73898693fca819c9f7fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2d37b766eea6eb078a892c62db3878e058547ed940d6971c5a08f928c61c1d(
    value: typing.Optional[IotTopicRuleErrorActionDynamodb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48ef4a5b7dc9fb57b6ee79fbfd677e4bc81a97636d13180db9e739be8ceabfb5(
    *,
    role_arn: builtins.str,
    put_item: typing.Optional[typing.Union[IotTopicRuleErrorActionDynamodbv2PutItem, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a567a67e0ec2a934e719d009b2d715e8d0d29e78ad950eae92b618f00fedeaf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf91bcf1f323b8b4afe632d6098c9906c18afe2965c013785e9beb680c66e7b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46bb8221b2f5cba8d8f5c1d7128f7c36abc5002235c215404be811f89a32c06(
    value: typing.Optional[IotTopicRuleErrorActionDynamodbv2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2163d3f19b374dcef0582cdba51feba84618ce5d727f2393021db5898a827479(
    *,
    table_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31a3ef2646b9efdc001e9201919dc3f7aec6851f1361cf8a58497c0e9e259f9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade47b2cb411151808e3ec61701e4c38a31c51974ccb2b8e1332675789743564(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1eea2814da2ada7025dbd8ef87f1846f135aba54031f03dd1d82426ac8300b4(
    value: typing.Optional[IotTopicRuleErrorActionDynamodbv2PutItem],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b0d55420f69ec18f229d27a3d5007ba854a951103638a1aa72efd9671c10a8(
    *,
    endpoint: builtins.str,
    id: builtins.str,
    index: builtins.str,
    role_arn: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b64e14fd8ed646ec052285cac354e2f10e01287fc229897fb28029cf0d3df4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d295eacfb1e93c4a52245a5f04554b420ddfeca15ffb1bea69c69ada4dc1edb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7dde59ff47162f880f81fc93f15e8068c0ea75b5605488a0723fccca0411e4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2addc828b97d2230129127650f74e934e3983eeae49c6d1396f0910170586a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d2f0f40e4618507adc07532c6c0d523a86caabdd25d2094c6923d61ad3cb8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f84237e9d1403dfc70d731a674a5d7e304cefa1e9fab1b06514f583a21ada52c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd8bc81237e95a5b93efd2ada59a7bc4e2077da3bf31367122a49e5ba6483b2(
    value: typing.Optional[IotTopicRuleErrorActionElasticsearch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd6474100e82d11b9b62a8d8948b95e543e71711cb623d56657077bacd4e00c1(
    *,
    delivery_stream_name: builtins.str,
    role_arn: builtins.str,
    batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    separator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917b697065eeb5ae19110f55a10af04f98051f27f81b0252891b709f4576c1c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85625a6e613a797f86631a28e41b3a5f5cd358323bcd0c98a54016e4613d6950(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b09a5e74be52f6719efc668eb0ce240d286eb74f47f886634f67264175ce7531(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef889c77fa63834ef28596c8bece994dc9f0c65a99f5e15d46f8d63c99fa243(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf53ec60048478af350b7a5121141ba648e8d7ac20f044ddbb58d4db454bc18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1effc66ab2ef16fe7b5e0b0e32fd1e3a58cee84b6557cec3b7e55e83a8c7e873(
    value: typing.Optional[IotTopicRuleErrorActionFirehose],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61ff4e2b0982a09252aa6fecc02cf8d2294de1d4e3a5005937f3ace8bae1ea7d(
    *,
    url: builtins.str,
    confirmation_url: typing.Optional[builtins.str] = None,
    http_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionHttpHttpHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3161a5617435a1a7e3e81bfcd2d0b691859e6c4be738d326e93874d49a7d1977(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28fcb8fff41725f63d255289236e0e439671a95542bf9c05c14e54e1cb57fd53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d75905c228715d12b25853189bb6327391b17e48f99eea410263d2b26ef0b1b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7e445cbea33f38a7f583c111d1ac753f03de5e43b1addcd2c16ed6bba65c73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9880e1e6ef2e268078ea583fb9e1c0c553c7dbda1fa2c02ad3c23db8af70bfee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c135c06a8b14e6fa6feb700d4e107bbc98d1cb734c26c96f317faf93742449(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01ec591d82b0c7c9f20c99e2d9130eb1af9f8a94dd38d4aa35fd0ae1055708d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionHttpHttpHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32472a8ae63cc40eaf0c5d0412e7d626f60fabbf06e1e95a1d7bcb7538aa5582(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db853ac4ef6ec9cb9a6d0cf18c5333dc6e4f13a08cf0945f4f75953e791c6dad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032409b3ac5a2c81592e4246eed04cdd2f5b87b718d765c94fc62864a2d3f8d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7107347bdd62c313e7e1620ff29a9f9854c9faf48cc7739b9498f9ed8ddbb089(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionHttpHttpHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fe695b9718105bfd6a212a76af9f3931c338f9b3f9c9c06ce04e76afaaa7fc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af0c69107be95058a146e295e5d86c650703e4967e5f00cae7d6d7b0cdf8b21(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionHttpHttpHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b936d5b14781da253869e2f6aec723de3bae78edc7b1bc573a54edb5078e0aae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd1f584ed27d642c538aaaf3e1ef2faa83df8b12148f10742c2364a158e416a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce5addf0629625645ee977f096d38e8e4b270079d5e581b1f358974650486e01(
    value: typing.Optional[IotTopicRuleErrorActionHttp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e6d2b6c494a29402c882da3e80e101f54e00f16743f80775552d04e82b867c6(
    *,
    channel_name: builtins.str,
    role_arn: builtins.str,
    batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328350afc87c374b8cdaa61fe68c2c0172084e9c4c4752383edbce58b3169912(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2238ab70dd4b62847e99fad2190d3d1816cdd7de31f8c28aea90bbe03fa8fb8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b093b93c1775f342cd2f75a25373a86e972f0627f44ef4be1abff1b246e00d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9986631e35a6c61b0271fff8229b0b36be23a6bca96aff450da00e9c69d44fba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e0039e960bc861f800af710dd30cd002e7799963656d1b43ba5d2ecafc8109(
    value: typing.Optional[IotTopicRuleErrorActionIotAnalytics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4eb7ed2a537711e6afbdce3ba52c1c62ccdcb4b1abe503bc0ecaf71b64d9257(
    *,
    input_name: builtins.str,
    role_arn: builtins.str,
    batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    message_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c14c802539ee07fdb780e2bdb83fa593db32db5dcae1d79a21f563daea33569f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73243d0b4f372aaeea96d46bb50cf82341423d6803663610828e284e7729e1fc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db92210a8e2c44ea227baca481d2f5d78ac73f2a1565cc387c708092c7b27d5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2da3aa713de1e14d4b960fa02b47ee4d691c143d6981a596ea9c47b5a628761a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c61fe6fd37eb777fb63f6c4fae2b2e47c1017521a05194c88836880cfbe1e52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292e6f309cec8d33807b833b7c02749753713e2d1147e696d51388e2bdeadb88(
    value: typing.Optional[IotTopicRuleErrorActionIotEvents],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382b961f835e2c7ece842a763415d0225e58f1e92e8285686687b2d3d88b77ef(
    *,
    client_properties: typing.Mapping[builtins.str, builtins.str],
    destination_arn: builtins.str,
    topic: builtins.str,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionKafkaHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key: typing.Optional[builtins.str] = None,
    partition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c4abaeaac9481c7fb4925abbbec5d4948b6aa9efc57ed066960a50226405cb(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e4a3b77775cd7a040f93df2276a35ca2900e3c4d6daa958436932c1a6ef7d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d028e0265ea74a85a1e605371fccc7882cc6e5a41a8efd2d7c03f73f18538da(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6284954fdbbb781566d3f87895453da8ae515485ef46521049ff5a37820e0ac3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d1ad8512e11f6d34b03845a28b01d3501831ab6d7904dd3287ec0a9744bf780(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f63013e0d9e363b33b6955c097eddc3592cc833bd2a6edca8449922f550f5fd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0924af469ae3e7a41eb865c3a8f7efd3ee2ca7a6768135e748cedd79e985dba1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionKafkaHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b58578e42b5f0b0b06998ad01ea52f45f74d12065a4fe93d90c69b4af63cb5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528cf2cd6eeafd58a6b7b0a267688bd2dcfc98f517b37c0c6c39d31bc29ebc22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e22f0089c02bb44e078194b5776d0f749d7b9841f958a516cf33e26173ac6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0632603bd9c3fd34f5de2b1a67f3ec174278259aaefd02dafa5cde94621b0e9f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionKafkaHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f70ea2e0c13dee64e48269950ccdbe5d7be67c4c3c8df5fcaa0b4d601aa37306(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__866c22b5ef96c4cb2aad870b325f1e87da72bcca21b8eb677603f7b2bb4ff5f5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionKafkaHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71aebbba0e71fd920f1bbdb50c4cd8a198fdf02218b1b047688b50b859d4465e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a632416f85aeb33fc87fc796b93d38b2e8ba7598748876f80064d3a8ccae5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1442c4d7a743f87701884e13deb64bc7f216de2d672575bd3b6ca9af5a906f9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95aad458437235b8a292394f2c66cf3e32883df4b2051421fa4763da380c4b71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ffb3a949b71a71ea4f6b0285e392b365b8ee6badddba5f9f7a93feaef65b2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b895d5ce4db645a7916b7b14667c556d779c4d1e0f51fc56c5f9db33572a2e(
    value: typing.Optional[IotTopicRuleErrorActionKafka],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b64cda47a53f3f062ab92a434c13c4bacc6e5ef9c20d08996a2df2a572415e5(
    *,
    role_arn: builtins.str,
    stream_name: builtins.str,
    partition_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2868e7b3ee2270d29edfa315f96606f2e8f44532dcb36ac86b657a06abbfd3a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e41e18a1ca33d6a5a31df49933d84353da016b867422d8372ab9799559e928(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74116133c2ea69a0d7cc891b36c2449a8df4e0886589d8b27f957b94378ffbf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dae4ee9d56355afcef84055c10d320bcabf973d6a57a08fdf56347d5c6843099(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45498924e68fa8d235991e8d446e517fe78feb47529c0f108e9d899d3b6a0acb(
    value: typing.Optional[IotTopicRuleErrorActionKinesis],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f41f7c5f9b20ec224dc9634f33ca7c14a1e1a3bf704b62531c0f41a89540d5(
    *,
    function_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d713cb8b50b046611a2871bc578014753359698331ef00641f8f784f1ed311b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__255985a8f75ccda3fca47510357177fb16134d03477bd027b4e39c6d41be229b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__598becffe55607c2d38d0d53dbb6c2017e6a8bf711a3cdace5dda79c45c1deae(
    value: typing.Optional[IotTopicRuleErrorActionLambda],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9242400c9b46cb367af24dc2cfdd1a89168b09db81ea4f2060c193f037878076(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab87b64125f281b0657ed115642982b348500c91170adcd7f1c7e4146b7a00ae(
    value: typing.Optional[IotTopicRuleErrorAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4f8d0a9060cfee44884056a9257abee2b3c9f57d5c720940d28925112748af(
    *,
    role_arn: builtins.str,
    topic: builtins.str,
    qos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20770824548ec4238e02d74793731d61f58a360e67ae145a083aee2c3e480acb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3c1ca3a50654cf5eaf942083523a4d98fcd78c675dae86d26f961fc4baaa70(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c69d5e0d92c950938217beb21a9882e9f01cb7b47d9cdfbcaa67ec6daeebfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342fccfb3112afb9dcd6d3781ef9d4065c5ee803eb59652b42c37a8741072ec9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d197c41cbcf6c9089e5b597f8638dc6c1874f3168a713a046531ac05e3a3bf44(
    value: typing.Optional[IotTopicRuleErrorActionRepublish],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b57561a8f2fcfd4ecda5fc69466d933c45ce0de553d2a3a61aa5bcf576e9d7f(
    *,
    bucket_name: builtins.str,
    key: builtins.str,
    role_arn: builtins.str,
    canned_acl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ebaf886267e36169d392ae8c7d44f7a11a8ddfbe916910f8e53bddf6e422da1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__040ec99ec84a499584d883e419b18f41b34f09f290b6786eb8d680bc0e4522eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7aa13d68ac0b770daed598178ae4ac9a875cd1167da6a431ec0fcac471d9d07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a82b3a0d857b42f50bde9ce99a5254bd63732a03281b3c4cf63e61bc83ef1143(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd26a923d3ac4db41dbf9aea151cfe58cda013abd07179cf916875e81308739(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__221820370306b6362aacc0506f901155b3948e5b2038103505f0d1539e4bc716(
    value: typing.Optional[IotTopicRuleErrorActionS3],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2701eab489642b57e35f0ad6d2b0fa1d75927c9d9044911861a055baa3c7f3a(
    *,
    role_arn: builtins.str,
    target_arn: builtins.str,
    message_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6ce5ae02f824bc0cffee5a84aa69a02d01f09c3e1959685fc1ecac3159aaec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bd6469360fceba7d68e081ef66185c38e655c0006e9435ab8c6a7e06f1a11d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff3982c5084e6d535f3a38cb05d38ab6e7fcaaba1ec06b9a1513b1cdb4428c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c815fe69ee53143cc5574890f8bfdcfa3405900c1d552f07030d138627c7f07b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fda3beb285b9f0a36b6083793393c367311e61d17a94c34f2d92d69c0f10c15(
    value: typing.Optional[IotTopicRuleErrorActionSns],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6602c92ba4cb1477093579c81a2038f3aa774279ebba38bfae0c76e50d11b7d(
    *,
    queue_url: builtins.str,
    role_arn: builtins.str,
    use_base64: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__236d254fce613fc43c69743292de9074a8ec0ff84ba85e1a3fd1333bb9c34538(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce40d036d2beade6d55c794867a6d418f9805ceb1c459e00bfebdd74d574d986(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f916173fe8dd931b05d643c165e811de88512fcb47d71709c495f5837cd684c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c58e1ecb18874fa687d7c7f700e319f73041350012b2242a26036f22b980fb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d274d675f409779aeb252e9744787ecfde6a38639e3d4ec8cf1861f616ea4e65(
    value: typing.Optional[IotTopicRuleErrorActionSqs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2625f1d5ea87076e18f700284d694cbd8b32c3b9a2ec2a72194cb92642a6247d(
    *,
    role_arn: builtins.str,
    state_machine_name: builtins.str,
    execution_name_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efb6ca62d4f392cea3b5b3efe0951657324057a5f4979fc615ce27181cc3edde(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__357a760aedee56cf421f3bbfd1a9b3f452a4124ab36ab26e3b4ff0ee077ded71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcbb2fd9007d19907bb461cac46de102cac577609ca3dd9994cae2f52dbb2f9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a5684d1423b6b1772eeadd185bf023c3255d64a062e116f73399f99d952ee0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae046bff12a29a2dd4ec97eedf5cdd619d660ea6bdd0663698236ae46061854(
    value: typing.Optional[IotTopicRuleErrorActionStepFunctions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1db45c956761bb6888f5fb0a4bdda2b6b68bb6148187a60fa058ecca9ac4ba2(
    *,
    database_name: builtins.str,
    dimension: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionTimestreamDimension, typing.Dict[builtins.str, typing.Any]]]],
    role_arn: builtins.str,
    table_name: builtins.str,
    timestamp: typing.Optional[typing.Union[IotTopicRuleErrorActionTimestreamTimestamp, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9176aee76c15ebec47aee9555a394ba1a3c018eab7cf5f6bf4d4e3b2c4b4cb3(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961d0e606b5b07e49dc7de3a7c3b74c09e82d19728244c4952188df77eb1b10a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e9902afff5be697e188799804350be62b594a4d18c9d55939680c73ac2da95(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10797ed6a91c94971ca07bf5204d22da567649bd4d696d25cebdaae4523247c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83e0edc7647fa6f6b309379405165e09ad0b62544153b0ab0415db1707e2f17(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c3ab6681ae285eb65f20b234cb7ced9e62b2e9e0feac67db548920c9696f2a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d35a0997495fb10cfc769c9d5930ef4efca9552c9ab7df1dc61384f7ba74527(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleErrorActionTimestreamDimension]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ca9876ab579f377345bd2db57af588f41aaf385bdb31fab25a98ff35c98d91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9066798162b8d169559bb5802a18c4472ff0ee07b28d84a16f46684690419e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b6ea9fda1e93b02a6da969ca4993f358dd226dc0ec546ed107717a877d76528(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf52cffecc1af0ba896406b67479a144bbdccbd324df3db3b5aa52b12ac10326(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleErrorActionTimestreamDimension]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__823f4c7bef9d0eeebcdb5ab6d6d875ddac781bace169c1a9bdda4306f1b6d045(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad740cdd6934997d72cb58eea5a5d56d5c4133435424c6940907bfdd0346e02(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleErrorActionTimestreamDimension, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9338c409db957ed3785141160f71df26e9e3af43ce8498032f49e7520f3d561b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d45f7d8eb82f01d5e6d972fb14f24bd681fa19b8ac20993bfba0de0d05d06f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c845ff1f047f222d0398396b4743478bbf94e5c7ba745a6db7305045b32b2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0aeb5dd00d7d445ef455a7192f4f80708b4c25a2931892430f850957659027c(
    value: typing.Optional[IotTopicRuleErrorActionTimestream],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be850aba3c7d7b20fe514ccfb0a595d7015f096a89813f6e74f06c887e85e840(
    *,
    unit: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0fb649f97fad7c89677c10d1e28e75ae5124e5d0ff815d1979b0434afa4f39d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55c8c9fbea482842e877244fc6b00bf0ed80b720b5ae6f0c121639d28f07b596(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc797b69527afdc565312ca3a3143a987cb45067b9da323c10add113904892a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cc76846bcd099f4a92b1674151a73b5075d169e59766835effdfdbdb7f847a8(
    value: typing.Optional[IotTopicRuleErrorActionTimestreamTimestamp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38b1e23f70f8134be5882afefe6f1bd45c48da7d9328086855f95f4318bbe203(
    *,
    delivery_stream_name: builtins.str,
    role_arn: builtins.str,
    batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    separator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b549533f6420a43d2bb26f6c772816f5e99136bafeac4a0bf8bd749b288a0250(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67646a54f0319ecce37836ada18d6a4453eef45072f3fea5071019e6c7a7095e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c718bae2707d6c54d32e4f00bb20a8ffe0e898bed9dab747584b88090446c9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5919badc04d3cf987d76829289da36458a750af92df3f494ce203cc0cb54dac5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ddfca73656774ed3dd18c87b40940502b6855ca77cd8cfb695ab75155f8df3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f649b193f57906792f7911f042f6739e100ab71ee60f4b74d2d3ff72b04842d9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleFirehose]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3decb07acadbcaf4bb772d98ddaa73f64e537bd40265085661e3c3fccd139964(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dddd048662c3fa6a7d1efb6d8d2f1172884cd46fb19828ec6517ef1b84ae166(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9991294f223dfb97757ec6a70341023c67f5998b4e7ef5c5d20e5169a60898b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34fc1d1ee66a19fef053067b49af3e9d6c96f04bb04ae55e87ac46bc9e2ec335(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ab35feb550504b89fb0d4e153d7b7e26ab4f4b2142658b15533c3b3f84a84d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd8f4be29e1b224410a6a7d4481f2b09c5c0d8b548b3ddd124862e0aa627e80(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleFirehose]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6eb74cd181847fb91fb990ef198322085f88706bf8cafbd57167bd535cfef77(
    *,
    url: builtins.str,
    confirmation_url: typing.Optional[builtins.str] = None,
    http_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleHttpHttpHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e06dc4c41d8d5eef4d1458eb16bf7787b072489cb23983e40671697386f905a4(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__615e15038ba5362a288f0c954f89a9b3362b0a478d2da212e15e247610f35d21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__507c4b3a271fccf71231d461c3327939928ab9c75c123136255a17eaa78c5b26(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567caa4b2314df2b41ec7fde86a2ebbe37b9ec80e8f521816f2fda63095d63a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5c74e160f09d027b632d32d1609bad51fc4e3a92d91ed1e4177fd7d7577b03(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e09a1382cec026a1f51e7a66c455703a6d072c8f1e6594aa3a6100e5a6fef632(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9863308448197136fe5bd4e4382ffe75cb17c537f8818b6c24a12fcdb9d746e6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleHttpHttpHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2453fc916a1227cd9bbe8348883e9f73d0a8a59c83c9b415e561eba75e407969(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a6ba5b5a6160e42fc7fe366050e34f0abd7b883f5c4fe5d02555b46652b44d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5697c52ebee0a695f9e4c472fe8836c7b04d25dafcdbf5fea0b8a4b92a36274(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12338b2a8748dbf9879f197df31607ec0eea98f2c203186e0be90e93b9a6df5d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleHttpHttpHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef78a5586f8868fba72f2daeea5084c9f3d44bb73581fbcc9cf04a91dea13a9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__337bc022fa44282880b42fc3b7b551e168345f53209764a8cadd7b2aab37b800(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd071eda3cc88b33a20ae61341de176fb0d38f81c6910939d6bfd948abee9f81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21a1b10a469502cfea00b546b17c364ec425ba49b4b3c8e708645bdaafe2bd8f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ec20d9612e6148735021c258bc21e01f8428f7db50f27e0e65b1472001bc25(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22fa0a9f970469f0c4c207ce32e71c33954c8353802b808529dcea0f1f7f901b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleHttp]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286dfddc821da074d57377c5dc0378932dc2f95f4350545c6a5bb131c46be70b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d63a269286ceec18636a69d6e51d216583e7d4eb0322513f977fe55b8c5a94(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleHttpHttpHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ebae0929dfdd0ff79d25af27211bd38c3e8cd2f50ab90701812162eafe89a63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc0486e4f36cf751f9a66c44f44b6191acd7c55d1b2e78351d43170c3e408bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6b9839729b4a9e633b916e194b05dcf12ddabba610b52628aae25d20545c29(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleHttp]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bcdda0b5718945cb7f0a115727f56e0c95bf9a014f4cb1f4349f9ffb4a04c24(
    *,
    channel_name: builtins.str,
    role_arn: builtins.str,
    batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86467426c259393e5075c3fd9b2219657cc901e046d687e5659f0db91cd9bd06(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eeceede42b62727bd208af4664e3723d83bf304ff0662d2c31ebd7593535462(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb4d624c5ea6cf3ee04dc379fa355f4b23e3ee7cdbbcc2984a3088aa9b5b9ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e4e7420c45920ec51a46c3a5fe5b3a56064779e23add0502f2d87d4ecfe5e04(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e7158b3dec87d4d4a8a5fdce17a27f242fb8a4d0d5020012ebedd319ae13b6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f45a8c578d83b02c7d728123406ce491e717007521b3ef42d8646bbe228ca73d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleIotAnalytics]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb80ca4d72f48b23f79ab870c89570bcd98762ed6796edbfa7deee6e7bc0752(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271b41396c8da5965109849e90f501cab5f430aa9d34e7631416ce5bda4e194f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d046c46022d44c7cb658f391ce5cbfb6d3852388e6b3cffc87fc4335e5d4ca6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd94996e669c00c05e9ba268ac0a57c30a9c854f6be62caf780167a5413f140(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab460061e0f9c0a68721315d4de5a5d2cb92c41697cac8a8f0ea94aa7870e1e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleIotAnalytics]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d2d7a8a576c5a924c3a05d335afefad8493e30a04c9233f5a827251247481d(
    *,
    input_name: builtins.str,
    role_arn: builtins.str,
    batch_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    message_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ec6b773ea881755349e71b650d3aeb8651d6bbd8bdd46bf44924d085ae7573(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cdcb351f270afc210fad3b01bb2310f3519eedf4b18b89268b627fca0a31f8a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718e3bbcc21fb12f455413235d0ba8ba3d796c4e6731289c9236b1421c563ec7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df46d688e8ed1eb7b2ea4b6e74558ad71847394a0ee6f454e3e9f056e9f09d5c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d648f507dde752209b03bd5914c52ff4b05bb6710a1a5c2b023a3f1899e97da4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ca65b3e560592561e8fd14dd0e912dfbe98b0d7a6b69711ce9cd8bb6bc99dd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleIotEvents]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005342832d0de621083574e277a87539a340e7cd16810136afd9661648bd532d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77043f374c293123e2dad9f4a3469bcc8c4e5b20c80ce37d36b7facfa408a583(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66ff0966094faadad0fb1200e0a92c708adf57a96d52fbacd9ac337b831993d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c673f625b9fd8c9708bf3e373ff18b47b83c7957175f1a66f4d7e5a1bab853cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3475336cf8cd824e2b761ab5ae501a1d9f450fa3852a11a3b597e1ce4142dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49989f0b6b11af5df05ee251a5c8f93fc86ee2e284bc4563c33122b000f82a35(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleIotEvents]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__959e64e52b405e9d2a26e9b10c594d3fe47d232d07d415e6861f1693a189d6c4(
    *,
    client_properties: typing.Mapping[builtins.str, builtins.str],
    destination_arn: builtins.str,
    topic: builtins.str,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleKafkaHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key: typing.Optional[builtins.str] = None,
    partition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2906504c75e928160861a70de9f3e60e058fc9e0f3dbd6c4e46435117bdd3a44(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468a79200fc06a1755ca03221d5ba8d539b2d4abac2c0f42060391162e626cb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a362161fa5eda4c0986b66984b8762f7990f499508cce093a7914f51f0db94(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5846b21beb2bb6f44eec2ab72348c9990c4aee398b24210325e81a529855a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cdf6c5af31e571e71f765ea7880664005425134ccef2ab8c83cf0e156299429(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0bb4516c0f5908693571143de4c549179ed52c6f2b88363492a1f07451c18fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93af7e201aec005cd848a891d6a320b6e0926c73dc8731f3d747e12fae4edbfb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKafkaHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6574eaa2b6857393eda2c5f4a08e47b445ac361ba3955da17f30209905b75975(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11982b1c59c51cab7ce5a24385b949c077f0a3bfa14373f02e49176d1a46b99a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32cbd7cf757393f0f9d082d045534db02dcd8975b5ebedc1639ca080e9b1eff9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1191980a46fe9375e4003c8ad6c314bdda8cbefe6a1c0d472024f8dd9cb7a3bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKafkaHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e2b3db84db6375b1cc138874c6b14694bfc0504a4fb7326eec29ffb29059fb8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6a3d2a2387271489af2c26d0f7e78cd2be5ce02a7beb83b138528c37482004(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c11953a6cda0c3d9977cb2aaaea48f7269cb8eb3b74b15381f758082c61d8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de0ffc4b50d2f6c5dcda4b28bad36c6d73c37b156cef01ac214654e247884e4c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299a8ba93a245292300db5aebe32d908ecd11ab2d87afeb2cc17e8d2f6dfff7b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d8379dc362165c2088175855184727447f0039d4cf69aa276d3612933250ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKafka]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a4c0deed6b0b116b0458be5b07c4302fdb424b795a94eb83ea8627db876bd1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6128d9a973f4c265a9de9e4e6fce6d2904fcce5e36560a82dcd556b78c0956e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleKafkaHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1306ffcbd1805e208244b9587523fdb3b5db1d2f3050da566d1cb8a73a52e404(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e62a7920bc3b25d20b22230713a3be087589b0b7e4caa7f423eb81de23d509e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__730647fe944e5bac2cbaee9fd929af777c628017bc3a56fcaa951b90ad5856b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__540d09d20f4dd16a4757c1c9e691be9f6111537148a5a4b0c0870ef4ce40dce3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1048feaa60950ed972af6348da8cb6e2fd4e9549c9c62701318144a7b955cc94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a80a27e04d9cba2d5879e22c9423edcaf5764920f7a59f281ba4f365e60554(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKafka]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e255f6336ea11f9d907461398d15620c6e1035d50393876ee63a753ffe8191(
    *,
    role_arn: builtins.str,
    stream_name: builtins.str,
    partition_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00f7dc0eb273fdb14460d6394185cbedab2d54cce17dd3990ae6bee38ab90a44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba4dfba30bd2e419e42dad6eabeac3a67368c8285454e22f2b0c5b47aff5e43c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73157c9c87474f5f279393477fb82e4b466fb8744f6c9fcdcb002565c7e24f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e879e452c608b09e00c918fc3207c150dac6575bc14f950a8c7a4af5e1ed0d31(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980389de7735d0ac0c0410714e983c1075a34b941151fb1ec042bcc3c2fdf113(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980f4bd44a7b7e08529feebdef9c7fa821d205ea904809f3ab52d21296ae4323(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleKinesis]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb82441decd11ed55094babba497242e7b2514cdb0803c06ad14119ee628101(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af1801296e23a620becd171764eb6f8021b740e232909a6cc3ba5858f1e25768(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0412e7467c1d21fc52a2e3e50dffa394c73655fc79ed612721fd7b6c7807448f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef4943663c06b3563d1191464fe4fe330463727271d60750d9ea0d57cd1142f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ef997c475b9dc5932c30fc7c1c89af2a5cefa43c6c1e6d10c97319447858a95(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleKinesis]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d84bce0dcf01a8529f03e4b7100790d12286bf0bacb2dcab521c15b55493d957(
    *,
    function_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca42ef6b7f6e7058a0933adca0c1ea98b92b08abc3a0bcb2d262d1e764185080(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__309e19ab268b92372fe07eed4874f0ea0511c19c28f5ab29e193cd5edfc166de(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a3cf1728a772c49788ab20c747d71fc4accfddc3e529b363398f19c6f183fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd544143b416d7b7cf2a1d4864df2d991fe975822e23caec3096727ce6d018ef(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae39743538db69d1007f0cee7a407b04030f45ab29208068d62954e62c258c1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddaa06c059dec143027d02b8d45ee8898cd270b6f232dd54e60879f57408317c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleLambda]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__258b711a09995a0a90dc84186623b51714178c8062ab585c5e14b69f8b4ffb14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68722d5d18c23f9d3c6c38052110c213bbcd368a187e1787310908b57e3c659f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b81c3b7ccd7fda1f493bab7e500d26724854f71ae14bc796d864635f933b2563(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleLambda]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e08fe52f07447f0833199f8645456f5d63448030b5f091dcb3bb24d374afba(
    *,
    role_arn: builtins.str,
    topic: builtins.str,
    qos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16bc7b2159e28465e7c6ebff022ce81530a53d434fa71c19ff37b1d9847f340c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9607e15699ec886bb59f6f7448ed9fbaf2b1a0aff6a83d3ddf6a907d99410b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db952130002920e821d2a0aa297f91f6e450cc00cf88f88993468369551fe6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f594bb233e8b023e58774a3080be9e733c19b9fbd94ccc83dc87dd86916726df(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e05e6a2a838561a29a30c822c344e60b1e8887730af12b71e43802dbda13bac8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6be1726f0ff4b5ab75d33ab54e76a676174fcbab902fd033ee24f65f7fca085(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleRepublish]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c4eb61661335403985e4b1cb9fee0f29229c684fe491933fcf6ce82ff98ae22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c440c368276eddea29a8ebf2a0182f37e5e312e5461dea8b02fe06c0c0c178fe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35e62f94f8d18f4799724da10aaf0006a8599098439cdec9a91375aeb3f8ea92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c27987ea95923fcd310d31afe8d4934d46c4c7ca73de01a3ca4de057679110(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__168f231918661426f6238d6ce9bf245830d08607ddae19556b4853a35b84de56(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleRepublish]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab44c78bec3b7f943fa7509dd1c08ee033f107c0708733e1b918e5ffa2649de(
    *,
    bucket_name: builtins.str,
    key: builtins.str,
    role_arn: builtins.str,
    canned_acl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e456a74d8bc835bce617cfa089f6a121e107bfb85639884f59401d02c0140a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c349726045ae5cdc4907db391f072e25f546156446efdacae2a4e9252e996a8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e2fc8f40f19623cc129eb53a91e540470fed39c24260402abc3a7f75933fc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63f6ad50e1891c0515323cc2586ec8f4591f2e87eaa88d92af2d4e9d31b24ca4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9159db11961547e93b790d4c4af8371d95e0f1cba495090b1580e711e0399d4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12f66ded1825ec245d3875c985aff99f09ca6a07602ffb97d0dc918cb7c8ba83(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleS3]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9023ccbb4cfce3f647caa16c0ab57a0f463b33de9c57c4d71335189eef34efc9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a42b4d674a71f429a4e79716db0fcef5fbd3d14ee585a754b0b778d5fe4d55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6806767cc9112bfc8b41bac409c6de4d38803cb55b7ec7b5e268f5eca82f5af6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf8fbb6e012520d2183c3b300a7b57624f29530fa98f7b858bc639052396c137(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398e5259d5ee547e7a27edc24535eea168d305420f32c08806bf10dc45852e26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__695cd3bb81cf232c302222bcd01a16ccaa6385bc6d18e8d860296cb761441732(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleS3]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b70853d0a444764b2cab4d9c44a1ded4fee1a94f5df5d74d7291ba2502e2df7(
    *,
    role_arn: builtins.str,
    target_arn: builtins.str,
    message_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bbf0d65f3a33395b6c8e3689f216c95ee952de668519922604ca1eb691d3a1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__290bf9985523cdb33ef73d8dbf9292ea480149e5727955ef59a9b72092d4111a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba95e7ba76e1363bf5a36bf63d3b1c1e5c3d16c27f1245ac719074495f2bced(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f82669e97ae730cc1dc3c14348ea5a60b92c38becf487c57db9c31821db5d7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e581b3b2a1c66be72274ba87d4c3e39cd4ac97b4fc57ea83ae33bfeebfec32a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a27ab745379625527a3c725bff6ec509ab43d77ef9892e38fef1507485a69792(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleSns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f13802204d5d75a186afe0230deb5ff16275fb917349df64a19f396709f162c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5183bad06fa7cd1f44953dd29e73e7ce2c9a6976600251adbe5125303257907b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22ab4c529ce65a598d5b6e8c13547aa29435f59fcde4e52a3e2a45c19080177(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbc0accd7e8f163b69d0fb4343e08905e1c7f4fad8a9f3f0d1e03b8bec8d646d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac245301cef0f06fe49bf43b0e6c083745aa97e98ec2cffbe3efc3c84102c801(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleSns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89995371b9db7b828002c8aaf6c40fedbf03ccd48c7a53127185d2e1be8bf3e6(
    *,
    queue_url: builtins.str,
    role_arn: builtins.str,
    use_base64: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ac4b74d3c2c91df367554c5a83de20776e3d02ded07b82955b2c6c9d96797ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f40f9e510df0205a826e1eb7de3899ac5044c4bb4bbbe900bb43391c9ee9529(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a97fb3e3a58e85431f18dd54b7f11925dada8d7ccded0b98cf76ae589b9a09b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56753b9334e27f847125683e812e28fe1057c569d321a476349d2ce0fee92aa7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22697d7024a0ada259d446f7f2e2c4115e45ed1b105fd731c4c9c84d56d941c6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5339be1e0553e8cafd209c1d39cab65d75f353311a6e67cc135f727e8bdf40c6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleSqs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf967a78c9af1a19c9a68d7e4d68a6747eb703fa6223f9db60cf7cf7bbb9000(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5cbae448fa5ad407014fa690b89eb7aaf2eed18e236a002e15f682ec68160a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6439786f88506da0be7245e296afe68ad83d8ea40758c1ad296b796547c937fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c091bec874f968ebccaa964bb5d5388cf38b51ba5f2c18d5f1d36189ea66be(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0de4d8f6d4a225541a4446eb017e74da6c1d3360b3e97aae694c1681f4c1dea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleSqs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87ef73b4e0e92d254df820fba902e183d8af2cff2dfa3faae99e1bdd94f7333(
    *,
    role_arn: builtins.str,
    state_machine_name: builtins.str,
    execution_name_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5aec2f79c17d53033365d2443bfa650c02d72aaf7f2a13c5a150ce5b2e3394(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d43b6e8fe0aabda909f6ca73ef664b3967fcc4e55452f8353794290ba55bdd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d576933533699e27b6c939cf5f5e69f04f9b6c621ceadb71d209fc01a81cdd7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860704e8dd9a96c322ce472666607b380361bc08ce2f09a88289cd67d1e60c60(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa227954250e0ab42439047866b389b6c0253a8cc3155c81a690ed41c894086(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514785969113b41dd1907176a605966215bb0a89fdac38800f43da61b9f92671(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleStepFunctions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e74f3721188300018d7e56a7ad0b238b793183c234e999385e3ac12dce98d49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf98ff68d7afcaff136d9dbbd9c6d58ef8af3ae0d56739bebcf1b07cb95bc6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0f3c523e77e19b90e028ce8753fb6766411d9f296b619f95e1a33ac7fc37576(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00a694b3febf4573bad6b5bd07fab2bd873fe91b6ffe2fb0801a12a78958cd23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2bdd6b188a9ce41627898907f45316034dd5a8411a8e7d789eaf6b86e56c2c1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleStepFunctions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__108d7531d3d89160ba18ec723ad8459643a39501baf5c63ee0d41ee9e5a97831(
    *,
    database_name: builtins.str,
    dimension: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleTimestreamDimension, typing.Dict[builtins.str, typing.Any]]]],
    role_arn: builtins.str,
    table_name: builtins.str,
    timestamp: typing.Optional[typing.Union[IotTopicRuleTimestreamTimestamp, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f6f7febbf204f417d22179d294bb0c608c904029cbc03a0305db0de6bb5846e(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0ecc1898b50cb180327035e1508c4b44df359c10a6a13eef5c330a928d5d9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abebfa251347308d58babe946d9305b2c4c88a553434113cebf08060a71cf58a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c267095bfcf5b5bfbebedf02ecf52bd2ff494c20c85032b0994c948e95b83c75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f8343fb9b149b4eb94184f2159774ee4dd2fcdc0364848663e0e01e73c3401b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061b08ec7afdb8eb7505de88452832387920e401009734a0f9767f26c8cfb569(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__147927de7d760226d57540946cb36afe3bfe51f77d940ee81cfeb0fe4283330e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleTimestreamDimension]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661e33e03a5c2d8bab4444c8ef78dd787251972c0ba17dca3a9ba86061a93e3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2796d5f57a9e10e8c875829b89305bb920b03b405c1aca4cceb15cbadf19392(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__136ffb0ffaa6329c840908998e265c5670f53597ba7f9eff3dd840d7fb975ec3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db6bd033952bf015705952deeabe3562e61d65a6c426ed6ff5c82bffc6544590(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleTimestreamDimension]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5a8ba3df92963c166bc605387ec70c92956bf106180c457f62193e2b43e4103(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f91bc139968cea21026931cf7dae49810724bd4187bb365249dee8c2d13c0d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1312bed4498686e7e676e659405e0f07190542d159c7563895331fe5760fbf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a0fbb77c7748b272bdf3625d9b428a91080cb1830473983825b6b67d282ae4a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5379e7be50401859a75045a252881378f66f82fa142b61da06ef36a3b72ba3eb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c359ab52d6021a0cc10f539469ffa8af20fa09c6801cb214fa0955d74ef347(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTopicRuleTimestream]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f720048d97753a644d25ae435d008ba4cf6eb0704c1e30fee550353f823b688f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2af6fcafde1725aaf32d2c172c5d8976574493ca43af63cdae109c3de7d4fe35(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTopicRuleTimestreamDimension, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b5d13d24846ba8377443a2050fe5505774f8b00c3a5aaba69bf2154306e3c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66ba66d94de46eab4b7b7e4f5e76896e8f5bb4e60081701379be88edf476e37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f983158fd61ddc2fe83f06e27bfdfc66824f7b9a4a906826ed1a29fd9365bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99cc2e0f456d1921cf1e636a5d0b996e5ee44645dcd7bcc5e718c5e70264a8f2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotTopicRuleTimestream]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d734b0fb8a7187601faaff56b8fa9a170ea33e164fabac79963b881fd1453d30(
    *,
    unit: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085af48fd5833630a07412203da0d2a0fd9f464c2babc79f8e7e19f0e500ac4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d285c0260f99924c3d89e58d8b3bd6ade80a21c04b3147d1b13e4b0dd7dc4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ce9b6376bad56878a5294a50028af705ba5efbdbf46e28cbee6cd6908f1a9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1291238d4f2ad30cfbff56bc82c58df648512adc52e9fcca3038f2106d11449a(
    value: typing.Optional[IotTopicRuleTimestreamTimestamp],
) -> None:
    """Type checking stubs"""
    pass
