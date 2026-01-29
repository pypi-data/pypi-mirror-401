r'''
# `aws_wafv2_web_acl_logging_configuration`

Refer to the Terraform Registry for docs: [`aws_wafv2_web_acl_logging_configuration`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration).
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


class Wafv2WebAclLoggingConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration aws_wafv2_web_acl_logging_configuration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        log_destination_configs: typing.Sequence[builtins.str],
        resource_arn: builtins.str,
        id: typing.Optional[builtins.str] = None,
        logging_filter: typing.Optional[typing.Union["Wafv2WebAclLoggingConfigurationLoggingFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        redacted_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclLoggingConfigurationRedactedFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration aws_wafv2_web_acl_logging_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param log_destination_configs: AWS Kinesis Firehose Delivery Stream ARNs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#log_destination_configs Wafv2WebAclLoggingConfiguration#log_destination_configs}
        :param resource_arn: AWS WebACL ARN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#resource_arn Wafv2WebAclLoggingConfiguration#resource_arn}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#id Wafv2WebAclLoggingConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_filter: logging_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#logging_filter Wafv2WebAclLoggingConfiguration#logging_filter}
        :param redacted_fields: redacted_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#redacted_fields Wafv2WebAclLoggingConfiguration#redacted_fields}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#region Wafv2WebAclLoggingConfiguration#region}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d952bf0cea77703cad8a6fe9113f822dfa813f5614502816f1213ef44de5698)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = Wafv2WebAclLoggingConfigurationConfig(
            log_destination_configs=log_destination_configs,
            resource_arn=resource_arn,
            id=id,
            logging_filter=logging_filter,
            redacted_fields=redacted_fields,
            region=region,
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
        '''Generates CDKTF code for importing a Wafv2WebAclLoggingConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Wafv2WebAclLoggingConfiguration to import.
        :param import_from_id: The id of the existing Wafv2WebAclLoggingConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Wafv2WebAclLoggingConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c7c38ef117e003e66d95a670d62c6a8144339732a57205341efca57badfb22f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLoggingFilter")
    def put_logging_filter(
        self,
        *,
        default_behavior: builtins.str,
        filter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclLoggingConfigurationLoggingFilterFilter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param default_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#default_behavior Wafv2WebAclLoggingConfiguration#default_behavior}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#filter Wafv2WebAclLoggingConfiguration#filter}
        '''
        value = Wafv2WebAclLoggingConfigurationLoggingFilter(
            default_behavior=default_behavior, filter=filter
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingFilter", [value]))

    @jsii.member(jsii_name="putRedactedFields")
    def put_redacted_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclLoggingConfigurationRedactedFields", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef92f9d9c8341e10e7e3f9e33b4b498865b45cf33116aeef0900969f59821f6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRedactedFields", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLoggingFilter")
    def reset_logging_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingFilter", []))

    @jsii.member(jsii_name="resetRedactedFields")
    def reset_redacted_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedactedFields", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="loggingFilter")
    def logging_filter(
        self,
    ) -> "Wafv2WebAclLoggingConfigurationLoggingFilterOutputReference":
        return typing.cast("Wafv2WebAclLoggingConfigurationLoggingFilterOutputReference", jsii.get(self, "loggingFilter"))

    @builtins.property
    @jsii.member(jsii_name="redactedFields")
    def redacted_fields(self) -> "Wafv2WebAclLoggingConfigurationRedactedFieldsList":
        return typing.cast("Wafv2WebAclLoggingConfigurationRedactedFieldsList", jsii.get(self, "redactedFields"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logDestinationConfigsInput")
    def log_destination_configs_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "logDestinationConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingFilterInput")
    def logging_filter_input(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationLoggingFilter"]:
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationLoggingFilter"], jsii.get(self, "loggingFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="redactedFieldsInput")
    def redacted_fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclLoggingConfigurationRedactedFields"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclLoggingConfigurationRedactedFields"]]], jsii.get(self, "redactedFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceArnInput")
    def resource_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ac5e9540d869816b980c89f02c5625ebf3d092538220514c7b418787f9604c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logDestinationConfigs")
    def log_destination_configs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "logDestinationConfigs"))

    @log_destination_configs.setter
    def log_destination_configs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3dd17125af18253d3c5e16c7d4e95d4ea182c88dd8c57c54342ba76b0c5cb60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logDestinationConfigs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f083738880cffe394087ad94cb8f0aec9872ab7ccf132fb7068950736e74d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06484f8e15421d241c5fe79841bfec8339edeb61f7cb2c3d44a7138064f545d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "log_destination_configs": "logDestinationConfigs",
        "resource_arn": "resourceArn",
        "id": "id",
        "logging_filter": "loggingFilter",
        "redacted_fields": "redactedFields",
        "region": "region",
    },
)
class Wafv2WebAclLoggingConfigurationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        log_destination_configs: typing.Sequence[builtins.str],
        resource_arn: builtins.str,
        id: typing.Optional[builtins.str] = None,
        logging_filter: typing.Optional[typing.Union["Wafv2WebAclLoggingConfigurationLoggingFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        redacted_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclLoggingConfigurationRedactedFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param log_destination_configs: AWS Kinesis Firehose Delivery Stream ARNs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#log_destination_configs Wafv2WebAclLoggingConfiguration#log_destination_configs}
        :param resource_arn: AWS WebACL ARN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#resource_arn Wafv2WebAclLoggingConfiguration#resource_arn}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#id Wafv2WebAclLoggingConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_filter: logging_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#logging_filter Wafv2WebAclLoggingConfiguration#logging_filter}
        :param redacted_fields: redacted_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#redacted_fields Wafv2WebAclLoggingConfiguration#redacted_fields}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#region Wafv2WebAclLoggingConfiguration#region}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(logging_filter, dict):
            logging_filter = Wafv2WebAclLoggingConfigurationLoggingFilter(**logging_filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbfc8124c19a833f59631b231927d6e24143f31113e5f09cdf4386e601905b30)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument log_destination_configs", value=log_destination_configs, expected_type=type_hints["log_destination_configs"])
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logging_filter", value=logging_filter, expected_type=type_hints["logging_filter"])
            check_type(argname="argument redacted_fields", value=redacted_fields, expected_type=type_hints["redacted_fields"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_destination_configs": log_destination_configs,
            "resource_arn": resource_arn,
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
        if id is not None:
            self._values["id"] = id
        if logging_filter is not None:
            self._values["logging_filter"] = logging_filter
        if redacted_fields is not None:
            self._values["redacted_fields"] = redacted_fields
        if region is not None:
            self._values["region"] = region

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
    def log_destination_configs(self) -> typing.List[builtins.str]:
        '''AWS Kinesis Firehose Delivery Stream ARNs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#log_destination_configs Wafv2WebAclLoggingConfiguration#log_destination_configs}
        '''
        result = self._values.get("log_destination_configs")
        assert result is not None, "Required property 'log_destination_configs' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''AWS WebACL ARN.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#resource_arn Wafv2WebAclLoggingConfiguration#resource_arn}
        '''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#id Wafv2WebAclLoggingConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_filter(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationLoggingFilter"]:
        '''logging_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#logging_filter Wafv2WebAclLoggingConfiguration#logging_filter}
        '''
        result = self._values.get("logging_filter")
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationLoggingFilter"], result)

    @builtins.property
    def redacted_fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclLoggingConfigurationRedactedFields"]]]:
        '''redacted_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#redacted_fields Wafv2WebAclLoggingConfiguration#redacted_fields}
        '''
        result = self._values.get("redacted_fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclLoggingConfigurationRedactedFields"]]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#region Wafv2WebAclLoggingConfiguration#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilter",
    jsii_struct_bases=[],
    name_mapping={"default_behavior": "defaultBehavior", "filter": "filter"},
)
class Wafv2WebAclLoggingConfigurationLoggingFilter:
    def __init__(
        self,
        *,
        default_behavior: builtins.str,
        filter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclLoggingConfigurationLoggingFilterFilter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param default_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#default_behavior Wafv2WebAclLoggingConfiguration#default_behavior}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#filter Wafv2WebAclLoggingConfiguration#filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5725c7a4a75b4b57586f732e2bb6d8d7c5aeafc0d7c2b8d5ce2e3202a59050f)
            check_type(argname="argument default_behavior", value=default_behavior, expected_type=type_hints["default_behavior"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_behavior": default_behavior,
            "filter": filter,
        }

    @builtins.property
    def default_behavior(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#default_behavior Wafv2WebAclLoggingConfiguration#default_behavior}.'''
        result = self._values.get("default_behavior")
        assert result is not None, "Required property 'default_behavior' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclLoggingConfigurationLoggingFilterFilter"]]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#filter Wafv2WebAclLoggingConfiguration#filter}
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclLoggingConfigurationLoggingFilterFilter"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationLoggingFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterFilter",
    jsii_struct_bases=[],
    name_mapping={
        "behavior": "behavior",
        "condition": "condition",
        "requirement": "requirement",
    },
)
class Wafv2WebAclLoggingConfigurationLoggingFilterFilter:
    def __init__(
        self,
        *,
        behavior: builtins.str,
        condition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition", typing.Dict[builtins.str, typing.Any]]]],
        requirement: builtins.str,
    ) -> None:
        '''
        :param behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#behavior Wafv2WebAclLoggingConfiguration#behavior}.
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#condition Wafv2WebAclLoggingConfiguration#condition}
        :param requirement: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#requirement Wafv2WebAclLoggingConfiguration#requirement}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a028dfc88806c7ba8a28ceb7bf89b62c48fff6407192a4cc156aa7ce2daf836a)
            check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument requirement", value=requirement, expected_type=type_hints["requirement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "behavior": behavior,
            "condition": condition,
            "requirement": requirement,
        }

    @builtins.property
    def behavior(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#behavior Wafv2WebAclLoggingConfiguration#behavior}.'''
        result = self._values.get("behavior")
        assert result is not None, "Required property 'behavior' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition"]]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#condition Wafv2WebAclLoggingConfiguration#condition}
        '''
        result = self._values.get("condition")
        assert result is not None, "Required property 'condition' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition"]], result)

    @builtins.property
    def requirement(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#requirement Wafv2WebAclLoggingConfiguration#requirement}.'''
        result = self._values.get("requirement")
        assert result is not None, "Required property 'requirement' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationLoggingFilterFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition",
    jsii_struct_bases=[],
    name_mapping={
        "action_condition": "actionCondition",
        "label_name_condition": "labelNameCondition",
    },
)
class Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition:
    def __init__(
        self,
        *,
        action_condition: typing.Optional[typing.Union["Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        label_name_condition: typing.Optional[typing.Union["Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param action_condition: action_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#action_condition Wafv2WebAclLoggingConfiguration#action_condition}
        :param label_name_condition: label_name_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#label_name_condition Wafv2WebAclLoggingConfiguration#label_name_condition}
        '''
        if isinstance(action_condition, dict):
            action_condition = Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition(**action_condition)
        if isinstance(label_name_condition, dict):
            label_name_condition = Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition(**label_name_condition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7c774f47b9938f923b1da219114e28262efccf39e5b3f4937fbef05415c8763)
            check_type(argname="argument action_condition", value=action_condition, expected_type=type_hints["action_condition"])
            check_type(argname="argument label_name_condition", value=label_name_condition, expected_type=type_hints["label_name_condition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action_condition is not None:
            self._values["action_condition"] = action_condition
        if label_name_condition is not None:
            self._values["label_name_condition"] = label_name_condition

    @builtins.property
    def action_condition(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition"]:
        '''action_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#action_condition Wafv2WebAclLoggingConfiguration#action_condition}
        '''
        result = self._values.get("action_condition")
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition"], result)

    @builtins.property
    def label_name_condition(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition"]:
        '''label_name_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#label_name_condition Wafv2WebAclLoggingConfiguration#label_name_condition}
        '''
        result = self._values.get("label_name_condition")
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition",
    jsii_struct_bases=[],
    name_mapping={"action": "action"},
)
class Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition:
    def __init__(self, *, action: builtins.str) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#action Wafv2WebAclLoggingConfiguration#action}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5e55406547714645b68c243f534da96c2a3629db225d6fad978ffd4a03f4b5b)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
        }

    @builtins.property
    def action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#action Wafv2WebAclLoggingConfiguration#action}.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e8e6994f71d17e9a74e5d693181390dddda11553ec0bcea50cb934bd8187d7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d585fd7fc7ecb1bf796e4dcfa9b06078cab1ed1ccc56e1421534e441824d2068)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition]:
        return typing.cast(typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f4ca34b3f0fe81d5cd3a7db6f9d0d7271a242595169d2acc136d8e2e0be2d0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition",
    jsii_struct_bases=[],
    name_mapping={"label_name": "labelName"},
)
class Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition:
    def __init__(self, *, label_name: builtins.str) -> None:
        '''
        :param label_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#label_name Wafv2WebAclLoggingConfiguration#label_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fe1c98fbca0e3ad493d45563a5527c5d95be70e2539fbf5bf852afebe4cf166)
            check_type(argname="argument label_name", value=label_name, expected_type=type_hints["label_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "label_name": label_name,
        }

    @builtins.property
    def label_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#label_name Wafv2WebAclLoggingConfiguration#label_name}.'''
        result = self._values.get("label_name")
        assert result is not None, "Required property 'label_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35f1e742de0a9377e1c8ba08a6682edb9d933cb4e22798786938865a0a6ffbe1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="labelNameInput")
    def label_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelNameInput"))

    @builtins.property
    @jsii.member(jsii_name="labelName")
    def label_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labelName"))

    @label_name.setter
    def label_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__668342206fe431dfda650ba1ee8e7bf898c8b5ef6ad1ee2a5aa9796237750780)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labelName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition]:
        return typing.cast(typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a825d424142079be2e451c609b66344f6a5926b9ae2281735ec540b1967f232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__789704e731ac1d75f4097b9124005821974a1b4cf5c5b4ddc98405211be85707)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c827fa49ed0216f74b35651ff65a84b3d970e92eedc9cf5a707ceb6c12a7be3c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0277a82bd8a4a2e63437084bc433cb63c31aece0f8ebcab6930300e406048a67)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fc732207ce778c15af2c33bfbcdbda602549fc75bcbc557f8fe5828236bab19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5885f6640043390616c27ca39f0653d6c16c29edc797a89ad4d3247001e47ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6608ed17d6c7b0cc186e156348c0f53117301cb92058c279d2d00d4491ba56d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17636e4adabc6b50da7eac068d93650d312ab30f0741271ed647234af5a8eaf3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putActionCondition")
    def put_action_condition(self, *, action: builtins.str) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#action Wafv2WebAclLoggingConfiguration#action}.
        '''
        value = Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition(
            action=action
        )

        return typing.cast(None, jsii.invoke(self, "putActionCondition", [value]))

    @jsii.member(jsii_name="putLabelNameCondition")
    def put_label_name_condition(self, *, label_name: builtins.str) -> None:
        '''
        :param label_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#label_name Wafv2WebAclLoggingConfiguration#label_name}.
        '''
        value = Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition(
            label_name=label_name
        )

        return typing.cast(None, jsii.invoke(self, "putLabelNameCondition", [value]))

    @jsii.member(jsii_name="resetActionCondition")
    def reset_action_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActionCondition", []))

    @jsii.member(jsii_name="resetLabelNameCondition")
    def reset_label_name_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabelNameCondition", []))

    @builtins.property
    @jsii.member(jsii_name="actionCondition")
    def action_condition(
        self,
    ) -> Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionConditionOutputReference:
        return typing.cast(Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionConditionOutputReference, jsii.get(self, "actionCondition"))

    @builtins.property
    @jsii.member(jsii_name="labelNameCondition")
    def label_name_condition(
        self,
    ) -> Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameConditionOutputReference:
        return typing.cast(Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameConditionOutputReference, jsii.get(self, "labelNameCondition"))

    @builtins.property
    @jsii.member(jsii_name="actionConditionInput")
    def action_condition_input(
        self,
    ) -> typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition]:
        return typing.cast(typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition], jsii.get(self, "actionConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="labelNameConditionInput")
    def label_name_condition_input(
        self,
    ) -> typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition]:
        return typing.cast(typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition], jsii.get(self, "labelNameConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d02f2f81db6fd3cf84e9d084d41b1cece23cdc23e88d245104c08c2ce4e6acf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclLoggingConfigurationLoggingFilterFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6d635cc047bfc7212b3c765d7710227e9326cee130f9586d2165ec3157253be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Wafv2WebAclLoggingConfigurationLoggingFilterFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24ab24b3b6e921d3a7eebf19c4059a0cbe136f4769d3934537af206049aed417)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Wafv2WebAclLoggingConfigurationLoggingFilterFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd0b14cd6b482542e2f2ba44e4b72c71a3708b0d9e678e3fb378f013b456e93a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83c43e7309b1cabfbd852e52263459282d97316471c650a01005945c016035de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6567bcd75d075fbcbe68e22d6447f623211348608f6c6423a9b3cb3eee0f0a0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a373c916c9f4687d142901fc8efb301b08572ac524dc1ef1b78edb773961863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclLoggingConfigurationLoggingFilterFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9de64ff35acb3f0ddadb7f3e0a44b47e8880ca4737cd3e93ea2b81f6f84e3e71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd474c50a97747c52c5a0ffd96ccba5a30b1e6af352d85c8ad71dab3fc96bdb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(
        self,
    ) -> Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionList:
        return typing.cast(Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionList, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="behaviorInput")
    def behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "behaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition]]], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="requirementInput")
    def requirement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requirementInput"))

    @builtins.property
    @jsii.member(jsii_name="behavior")
    def behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "behavior"))

    @behavior.setter
    def behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e87e630e1939a30b93e74fdbe16495fb90b8baf262c3fedada1267cf9fb7c4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "behavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requirement")
    def requirement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requirement"))

    @requirement.setter
    def requirement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a8cc7b7e190af5f87a31e7081a2b8203056fa182be3a995c1b2f1d3f1963a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requirement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationLoggingFilterFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationLoggingFilterFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationLoggingFilterFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd76541f2a723b8fbc1af6a74c6d1d91aa8529ec6fdf5d2455b6547b27464ce5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclLoggingConfigurationLoggingFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationLoggingFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c723f80ee025383962a3175dde337f1ee70dbb1ed39a7a66dcb7ac7a2a798e94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclLoggingConfigurationLoggingFilterFilter, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ed61d31a19b5dab62f89c4384d508a02574af805e017365f51c5def78db7005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> Wafv2WebAclLoggingConfigurationLoggingFilterFilterList:
        return typing.cast(Wafv2WebAclLoggingConfigurationLoggingFilterFilterList, jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="defaultBehaviorInput")
    def default_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilter]]], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultBehavior")
    def default_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultBehavior"))

    @default_behavior.setter
    def default_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7526d0ac68178b0634417402a9779e8a3baf33dfe0665dc167d277da04aad0b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilter]:
        return typing.cast(typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__885f6b48303cd901d34eb86644d71d5fd03dea091c33d01be06ec832a79c105c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFields",
    jsii_struct_bases=[],
    name_mapping={
        "method": "method",
        "query_string": "queryString",
        "single_header": "singleHeader",
        "uri_path": "uriPath",
    },
)
class Wafv2WebAclLoggingConfigurationRedactedFields:
    def __init__(
        self,
        *,
        method: typing.Optional[typing.Union["Wafv2WebAclLoggingConfigurationRedactedFieldsMethod", typing.Dict[builtins.str, typing.Any]]] = None,
        query_string: typing.Optional[typing.Union["Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString", typing.Dict[builtins.str, typing.Any]]] = None,
        single_header: typing.Optional[typing.Union["Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader", typing.Dict[builtins.str, typing.Any]]] = None,
        uri_path: typing.Optional[typing.Union["Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param method: method block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#method Wafv2WebAclLoggingConfiguration#method}
        :param query_string: query_string block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#query_string Wafv2WebAclLoggingConfiguration#query_string}
        :param single_header: single_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#single_header Wafv2WebAclLoggingConfiguration#single_header}
        :param uri_path: uri_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#uri_path Wafv2WebAclLoggingConfiguration#uri_path}
        '''
        if isinstance(method, dict):
            method = Wafv2WebAclLoggingConfigurationRedactedFieldsMethod(**method)
        if isinstance(query_string, dict):
            query_string = Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString(**query_string)
        if isinstance(single_header, dict):
            single_header = Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader(**single_header)
        if isinstance(uri_path, dict):
            uri_path = Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath(**uri_path)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a394e4c31e2183d279ca310ae9e96fd7167ed1cbbed51d8d37fda88b0bc23a)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
            check_type(argname="argument single_header", value=single_header, expected_type=type_hints["single_header"])
            check_type(argname="argument uri_path", value=uri_path, expected_type=type_hints["uri_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if query_string is not None:
            self._values["query_string"] = query_string
        if single_header is not None:
            self._values["single_header"] = single_header
        if uri_path is not None:
            self._values["uri_path"] = uri_path

    @builtins.property
    def method(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsMethod"]:
        '''method block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#method Wafv2WebAclLoggingConfiguration#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsMethod"], result)

    @builtins.property
    def query_string(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString"]:
        '''query_string block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#query_string Wafv2WebAclLoggingConfiguration#query_string}
        '''
        result = self._values.get("query_string")
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString"], result)

    @builtins.property
    def single_header(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader"]:
        '''single_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#single_header Wafv2WebAclLoggingConfiguration#single_header}
        '''
        result = self._values.get("single_header")
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader"], result)

    @builtins.property
    def uri_path(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath"]:
        '''uri_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#uri_path Wafv2WebAclLoggingConfiguration#uri_path}
        '''
        result = self._values.get("uri_path")
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationRedactedFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclLoggingConfigurationRedactedFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae9d9e1654f3446a1d91d9c5de55dca31f8e4e0b7d28ae8f5c09bb5d924a923f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "Wafv2WebAclLoggingConfigurationRedactedFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c3d31e07ef0f166c2b4f7761cea725c515a3075d49ffd803cc67875cffd637c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("Wafv2WebAclLoggingConfigurationRedactedFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e282929e1db27ad5f6b17a05ec4e9c70997afc7f3805539479a40cca47dd3ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__480c1cce53eaf5722093b330b92978abaeb0b684969ae60da35a89339c8ac2ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbe24f429c6b915ba7c78467df0a02620c9ce1c51016985fe6e6b4c9d48e4b5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationRedactedFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationRedactedFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationRedactedFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9559c4d056344311745f8995d7074d4fd032fc329ac5a08ac01f8cb1fa3b5524)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFieldsMethod",
    jsii_struct_bases=[],
    name_mapping={},
)
class Wafv2WebAclLoggingConfigurationRedactedFieldsMethod:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationRedactedFieldsMethod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclLoggingConfigurationRedactedFieldsMethodOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFieldsMethodOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95e2243d2dacef5e96130127241378e7e9ca5190db8ef208445aece419fc31c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsMethod]:
        return typing.cast(typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsMethod], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsMethod],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__875f92a615e8be90b18bc36f20ac1aa5b5d12ddc646e92640959e61542b875d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class Wafv2WebAclLoggingConfigurationRedactedFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c8e82466c60a2b80a4f543e7df9576f53a3e3ba3c6aaf768b6a669aba971a16)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMethod")
    def put_method(self) -> None:
        value = Wafv2WebAclLoggingConfigurationRedactedFieldsMethod()

        return typing.cast(None, jsii.invoke(self, "putMethod", [value]))

    @jsii.member(jsii_name="putQueryString")
    def put_query_string(self) -> None:
        value = Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString()

        return typing.cast(None, jsii.invoke(self, "putQueryString", [value]))

    @jsii.member(jsii_name="putSingleHeader")
    def put_single_header(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#name Wafv2WebAclLoggingConfiguration#name}.
        '''
        value = Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader(name=name)

        return typing.cast(None, jsii.invoke(self, "putSingleHeader", [value]))

    @jsii.member(jsii_name="putUriPath")
    def put_uri_path(self) -> None:
        value = Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath()

        return typing.cast(None, jsii.invoke(self, "putUriPath", [value]))

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @jsii.member(jsii_name="resetQueryString")
    def reset_query_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryString", []))

    @jsii.member(jsii_name="resetSingleHeader")
    def reset_single_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingleHeader", []))

    @jsii.member(jsii_name="resetUriPath")
    def reset_uri_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUriPath", []))

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(
        self,
    ) -> Wafv2WebAclLoggingConfigurationRedactedFieldsMethodOutputReference:
        return typing.cast(Wafv2WebAclLoggingConfigurationRedactedFieldsMethodOutputReference, jsii.get(self, "method"))

    @builtins.property
    @jsii.member(jsii_name="queryString")
    def query_string(
        self,
    ) -> "Wafv2WebAclLoggingConfigurationRedactedFieldsQueryStringOutputReference":
        return typing.cast("Wafv2WebAclLoggingConfigurationRedactedFieldsQueryStringOutputReference", jsii.get(self, "queryString"))

    @builtins.property
    @jsii.member(jsii_name="singleHeader")
    def single_header(
        self,
    ) -> "Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeaderOutputReference":
        return typing.cast("Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeaderOutputReference", jsii.get(self, "singleHeader"))

    @builtins.property
    @jsii.member(jsii_name="uriPath")
    def uri_path(
        self,
    ) -> "Wafv2WebAclLoggingConfigurationRedactedFieldsUriPathOutputReference":
        return typing.cast("Wafv2WebAclLoggingConfigurationRedactedFieldsUriPathOutputReference", jsii.get(self, "uriPath"))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(
        self,
    ) -> typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsMethod]:
        return typing.cast(typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsMethod], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringInput")
    def query_string_input(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString"]:
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString"], jsii.get(self, "queryStringInput"))

    @builtins.property
    @jsii.member(jsii_name="singleHeaderInput")
    def single_header_input(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader"]:
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader"], jsii.get(self, "singleHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="uriPathInput")
    def uri_path_input(
        self,
    ) -> typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath"]:
        return typing.cast(typing.Optional["Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath"], jsii.get(self, "uriPathInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationRedactedFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationRedactedFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationRedactedFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3215507a5951cb3631d550cf18e8d36a7814955f035442d00a4d61ffc3142c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString",
    jsii_struct_bases=[],
    name_mapping={},
)
class Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclLoggingConfigurationRedactedFieldsQueryStringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFieldsQueryStringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a953fcdc6bd513e2b36d5d51018e8486120a92ba4c7b2a8690947393015c279)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString]:
        return typing.cast(typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bea6f98d8afe4bdd390560935c2b14248c79cdf22f9162aa6fe562913b03627)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#name Wafv2WebAclLoggingConfiguration#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__306602029d4b593119fe8fd9a22e0f9cc0922beca7df8ba89c16df0d2782aa2f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/wafv2_web_acl_logging_configuration#name Wafv2WebAclLoggingConfiguration#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__818265465f41b46cbcac2b6f03975158efee92d5cd9ca4a8e0043e12189d7624)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3772dbc79ea160251268cbb7fe407cc4c9c00a8111fc1e206f196bd7d3aaccc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader]:
        return typing.cast(typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e70ec24b35f53105b1228de34b456e988f936998732c03624d42ac9f788f2805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath",
    jsii_struct_bases=[],
    name_mapping={},
)
class Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wafv2WebAclLoggingConfigurationRedactedFieldsUriPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.wafv2WebAclLoggingConfiguration.Wafv2WebAclLoggingConfigurationRedactedFieldsUriPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d88eb6c5b370e485f07a550342c5b5719ffeff7670ce592e3bcb68e828d75eeb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath]:
        return typing.cast(typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b3b0fea06140d41f48062ea032249a6d85d2a8ada2fdbc003d6187741a3e77b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Wafv2WebAclLoggingConfiguration",
    "Wafv2WebAclLoggingConfigurationConfig",
    "Wafv2WebAclLoggingConfigurationLoggingFilter",
    "Wafv2WebAclLoggingConfigurationLoggingFilterFilter",
    "Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition",
    "Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition",
    "Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionConditionOutputReference",
    "Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition",
    "Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameConditionOutputReference",
    "Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionList",
    "Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionOutputReference",
    "Wafv2WebAclLoggingConfigurationLoggingFilterFilterList",
    "Wafv2WebAclLoggingConfigurationLoggingFilterFilterOutputReference",
    "Wafv2WebAclLoggingConfigurationLoggingFilterOutputReference",
    "Wafv2WebAclLoggingConfigurationRedactedFields",
    "Wafv2WebAclLoggingConfigurationRedactedFieldsList",
    "Wafv2WebAclLoggingConfigurationRedactedFieldsMethod",
    "Wafv2WebAclLoggingConfigurationRedactedFieldsMethodOutputReference",
    "Wafv2WebAclLoggingConfigurationRedactedFieldsOutputReference",
    "Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString",
    "Wafv2WebAclLoggingConfigurationRedactedFieldsQueryStringOutputReference",
    "Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader",
    "Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeaderOutputReference",
    "Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath",
    "Wafv2WebAclLoggingConfigurationRedactedFieldsUriPathOutputReference",
]

publication.publish()

def _typecheckingstub__7d952bf0cea77703cad8a6fe9113f822dfa813f5614502816f1213ef44de5698(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    log_destination_configs: typing.Sequence[builtins.str],
    resource_arn: builtins.str,
    id: typing.Optional[builtins.str] = None,
    logging_filter: typing.Optional[typing.Union[Wafv2WebAclLoggingConfigurationLoggingFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    redacted_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclLoggingConfigurationRedactedFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__8c7c38ef117e003e66d95a670d62c6a8144339732a57205341efca57badfb22f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef92f9d9c8341e10e7e3f9e33b4b498865b45cf33116aeef0900969f59821f6d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclLoggingConfigurationRedactedFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ac5e9540d869816b980c89f02c5625ebf3d092538220514c7b418787f9604c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3dd17125af18253d3c5e16c7d4e95d4ea182c88dd8c57c54342ba76b0c5cb60(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f083738880cffe394087ad94cb8f0aec9872ab7ccf132fb7068950736e74d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06484f8e15421d241c5fe79841bfec8339edeb61f7cb2c3d44a7138064f545d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbfc8124c19a833f59631b231927d6e24143f31113e5f09cdf4386e601905b30(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    log_destination_configs: typing.Sequence[builtins.str],
    resource_arn: builtins.str,
    id: typing.Optional[builtins.str] = None,
    logging_filter: typing.Optional[typing.Union[Wafv2WebAclLoggingConfigurationLoggingFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    redacted_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclLoggingConfigurationRedactedFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5725c7a4a75b4b57586f732e2bb6d8d7c5aeafc0d7c2b8d5ce2e3202a59050f(
    *,
    default_behavior: builtins.str,
    filter: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclLoggingConfigurationLoggingFilterFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a028dfc88806c7ba8a28ceb7bf89b62c48fff6407192a4cc156aa7ce2daf836a(
    *,
    behavior: builtins.str,
    condition: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition, typing.Dict[builtins.str, typing.Any]]]],
    requirement: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7c774f47b9938f923b1da219114e28262efccf39e5b3f4937fbef05415c8763(
    *,
    action_condition: typing.Optional[typing.Union[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    label_name_condition: typing.Optional[typing.Union[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e55406547714645b68c243f534da96c2a3629db225d6fad978ffd4a03f4b5b(
    *,
    action: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e8e6994f71d17e9a74e5d693181390dddda11553ec0bcea50cb934bd8187d7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d585fd7fc7ecb1bf796e4dcfa9b06078cab1ed1ccc56e1421534e441824d2068(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f4ca34b3f0fe81d5cd3a7db6f9d0d7271a242595169d2acc136d8e2e0be2d0b(
    value: typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionActionCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe1c98fbca0e3ad493d45563a5527c5d95be70e2539fbf5bf852afebe4cf166(
    *,
    label_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35f1e742de0a9377e1c8ba08a6682edb9d933cb4e22798786938865a0a6ffbe1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668342206fe431dfda650ba1ee8e7bf898c8b5ef6ad1ee2a5aa9796237750780(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a825d424142079be2e451c609b66344f6a5926b9ae2281735ec540b1967f232(
    value: typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilterFilterConditionLabelNameCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__789704e731ac1d75f4097b9124005821974a1b4cf5c5b4ddc98405211be85707(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c827fa49ed0216f74b35651ff65a84b3d970e92eedc9cf5a707ceb6c12a7be3c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0277a82bd8a4a2e63437084bc433cb63c31aece0f8ebcab6930300e406048a67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc732207ce778c15af2c33bfbcdbda602549fc75bcbc557f8fe5828236bab19(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5885f6640043390616c27ca39f0653d6c16c29edc797a89ad4d3247001e47ae0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6608ed17d6c7b0cc186e156348c0f53117301cb92058c279d2d00d4491ba56d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17636e4adabc6b50da7eac068d93650d312ab30f0741271ed647234af5a8eaf3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d02f2f81db6fd3cf84e9d084d41b1cece23cdc23e88d245104c08c2ce4e6acf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d635cc047bfc7212b3c765d7710227e9326cee130f9586d2165ec3157253be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ab24b3b6e921d3a7eebf19c4059a0cbe136f4769d3934537af206049aed417(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd0b14cd6b482542e2f2ba44e4b72c71a3708b0d9e678e3fb378f013b456e93a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c43e7309b1cabfbd852e52263459282d97316471c650a01005945c016035de(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6567bcd75d075fbcbe68e22d6447f623211348608f6c6423a9b3cb3eee0f0a0a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a373c916c9f4687d142901fc8efb301b08572ac524dc1ef1b78edb773961863(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationLoggingFilterFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de64ff35acb3f0ddadb7f3e0a44b47e8880ca4737cd3e93ea2b81f6f84e3e71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd474c50a97747c52c5a0ffd96ccba5a30b1e6af352d85c8ad71dab3fc96bdb6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclLoggingConfigurationLoggingFilterFilterCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e87e630e1939a30b93e74fdbe16495fb90b8baf262c3fedada1267cf9fb7c4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a8cc7b7e190af5f87a31e7081a2b8203056fa182be3a995c1b2f1d3f1963a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd76541f2a723b8fbc1af6a74c6d1d91aa8529ec6fdf5d2455b6547b27464ce5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationLoggingFilterFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c723f80ee025383962a3175dde337f1ee70dbb1ed39a7a66dcb7ac7a2a798e94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ed61d31a19b5dab62f89c4384d508a02574af805e017365f51c5def78db7005(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[Wafv2WebAclLoggingConfigurationLoggingFilterFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7526d0ac68178b0634417402a9779e8a3baf33dfe0665dc167d277da04aad0b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__885f6b48303cd901d34eb86644d71d5fd03dea091c33d01be06ec832a79c105c(
    value: typing.Optional[Wafv2WebAclLoggingConfigurationLoggingFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a394e4c31e2183d279ca310ae9e96fd7167ed1cbbed51d8d37fda88b0bc23a(
    *,
    method: typing.Optional[typing.Union[Wafv2WebAclLoggingConfigurationRedactedFieldsMethod, typing.Dict[builtins.str, typing.Any]]] = None,
    query_string: typing.Optional[typing.Union[Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString, typing.Dict[builtins.str, typing.Any]]] = None,
    single_header: typing.Optional[typing.Union[Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader, typing.Dict[builtins.str, typing.Any]]] = None,
    uri_path: typing.Optional[typing.Union[Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae9d9e1654f3446a1d91d9c5de55dca31f8e4e0b7d28ae8f5c09bb5d924a923f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c3d31e07ef0f166c2b4f7761cea725c515a3075d49ffd803cc67875cffd637c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e282929e1db27ad5f6b17a05ec4e9c70997afc7f3805539479a40cca47dd3ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480c1cce53eaf5722093b330b92978abaeb0b684969ae60da35a89339c8ac2ba(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe24f429c6b915ba7c78467df0a02620c9ce1c51016985fe6e6b4c9d48e4b5f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9559c4d056344311745f8995d7074d4fd032fc329ac5a08ac01f8cb1fa3b5524(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[Wafv2WebAclLoggingConfigurationRedactedFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e2243d2dacef5e96130127241378e7e9ca5190db8ef208445aece419fc31c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__875f92a615e8be90b18bc36f20ac1aa5b5d12ddc646e92640959e61542b875d9(
    value: typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsMethod],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c8e82466c60a2b80a4f543e7df9576f53a3e3ba3c6aaf768b6a669aba971a16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3215507a5951cb3631d550cf18e8d36a7814955f035442d00a4d61ffc3142c3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, Wafv2WebAclLoggingConfigurationRedactedFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a953fcdc6bd513e2b36d5d51018e8486120a92ba4c7b2a8690947393015c279(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bea6f98d8afe4bdd390560935c2b14248c79cdf22f9162aa6fe562913b03627(
    value: typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsQueryString],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306602029d4b593119fe8fd9a22e0f9cc0922beca7df8ba89c16df0d2782aa2f(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__818265465f41b46cbcac2b6f03975158efee92d5cd9ca4a8e0043e12189d7624(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3772dbc79ea160251268cbb7fe407cc4c9c00a8111fc1e206f196bd7d3aaccc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70ec24b35f53105b1228de34b456e988f936998732c03624d42ac9f788f2805(
    value: typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsSingleHeader],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88eb6c5b370e485f07a550342c5b5719ffeff7670ce592e3bcb68e828d75eeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3b0fea06140d41f48062ea032249a6d85d2a8ada2fdbc003d6187741a3e77b(
    value: typing.Optional[Wafv2WebAclLoggingConfigurationRedactedFieldsUriPath],
) -> None:
    """Type checking stubs"""
    pass
