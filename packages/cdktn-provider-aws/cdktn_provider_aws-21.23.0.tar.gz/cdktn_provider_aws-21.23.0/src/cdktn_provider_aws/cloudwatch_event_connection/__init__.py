r'''
# `aws_cloudwatch_event_connection`

Refer to the Terraform Registry for docs: [`aws_cloudwatch_event_connection`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection).
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


class CloudwatchEventConnection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnection",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection aws_cloudwatch_event_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        authorization_type: builtins.str,
        auth_parameters: typing.Union["CloudwatchEventConnectionAuthParameters", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        invocation_connectivity_parameters: typing.Optional[typing.Union["CloudwatchEventConnectionInvocationConnectivityParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        kms_key_identifier: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection aws_cloudwatch_event_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param authorization_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#authorization_type CloudwatchEventConnection#authorization_type}.
        :param auth_parameters: auth_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#auth_parameters CloudwatchEventConnection#auth_parameters}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#name CloudwatchEventConnection#name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#description CloudwatchEventConnection#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#id CloudwatchEventConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param invocation_connectivity_parameters: invocation_connectivity_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#invocation_connectivity_parameters CloudwatchEventConnection#invocation_connectivity_parameters}
        :param kms_key_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#kms_key_identifier CloudwatchEventConnection#kms_key_identifier}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#region CloudwatchEventConnection#region}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__406369d4c4d52e1406d34183b518b86b651c926b8b1905aedabd5401f7b9e834)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudwatchEventConnectionConfig(
            authorization_type=authorization_type,
            auth_parameters=auth_parameters,
            name=name,
            description=description,
            id=id,
            invocation_connectivity_parameters=invocation_connectivity_parameters,
            kms_key_identifier=kms_key_identifier,
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
        '''Generates CDKTF code for importing a CloudwatchEventConnection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudwatchEventConnection to import.
        :param import_from_id: The id of the existing CloudwatchEventConnection that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudwatchEventConnection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed0bbb6b9e5515445a287333739d8b8f5eec16e1604fd6ef2edb58c58f966e02)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuthParameters")
    def put_auth_parameters(
        self,
        *,
        api_key: typing.Optional[typing.Union["CloudwatchEventConnectionAuthParametersApiKey", typing.Dict[builtins.str, typing.Any]]] = None,
        basic: typing.Optional[typing.Union["CloudwatchEventConnectionAuthParametersBasic", typing.Dict[builtins.str, typing.Any]]] = None,
        invocation_http_parameters: typing.Optional[typing.Union["CloudwatchEventConnectionAuthParametersInvocationHttpParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth: typing.Optional[typing.Union["CloudwatchEventConnectionAuthParametersOauth", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param api_key: api_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#api_key CloudwatchEventConnection#api_key}
        :param basic: basic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#basic CloudwatchEventConnection#basic}
        :param invocation_http_parameters: invocation_http_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#invocation_http_parameters CloudwatchEventConnection#invocation_http_parameters}
        :param oauth: oauth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#oauth CloudwatchEventConnection#oauth}
        '''
        value = CloudwatchEventConnectionAuthParameters(
            api_key=api_key,
            basic=basic,
            invocation_http_parameters=invocation_http_parameters,
            oauth=oauth,
        )

        return typing.cast(None, jsii.invoke(self, "putAuthParameters", [value]))

    @jsii.member(jsii_name="putInvocationConnectivityParameters")
    def put_invocation_connectivity_parameters(
        self,
        *,
        resource_parameters: typing.Union["CloudwatchEventConnectionInvocationConnectivityParametersResourceParameters", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param resource_parameters: resource_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#resource_parameters CloudwatchEventConnection#resource_parameters}
        '''
        value = CloudwatchEventConnectionInvocationConnectivityParameters(
            resource_parameters=resource_parameters
        )

        return typing.cast(None, jsii.invoke(self, "putInvocationConnectivityParameters", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInvocationConnectivityParameters")
    def reset_invocation_connectivity_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvocationConnectivityParameters", []))

    @jsii.member(jsii_name="resetKmsKeyIdentifier")
    def reset_kms_key_identifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyIdentifier", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="authParameters")
    def auth_parameters(
        self,
    ) -> "CloudwatchEventConnectionAuthParametersOutputReference":
        return typing.cast("CloudwatchEventConnectionAuthParametersOutputReference", jsii.get(self, "authParameters"))

    @builtins.property
    @jsii.member(jsii_name="invocationConnectivityParameters")
    def invocation_connectivity_parameters(
        self,
    ) -> "CloudwatchEventConnectionInvocationConnectivityParametersOutputReference":
        return typing.cast("CloudwatchEventConnectionInvocationConnectivityParametersOutputReference", jsii.get(self, "invocationConnectivityParameters"))

    @builtins.property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretArn"))

    @builtins.property
    @jsii.member(jsii_name="authorizationTypeInput")
    def authorization_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="authParametersInput")
    def auth_parameters_input(
        self,
    ) -> typing.Optional["CloudwatchEventConnectionAuthParameters"]:
        return typing.cast(typing.Optional["CloudwatchEventConnectionAuthParameters"], jsii.get(self, "authParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="invocationConnectivityParametersInput")
    def invocation_connectivity_parameters_input(
        self,
    ) -> typing.Optional["CloudwatchEventConnectionInvocationConnectivityParameters"]:
        return typing.cast(typing.Optional["CloudwatchEventConnectionInvocationConnectivityParameters"], jsii.get(self, "invocationConnectivityParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdentifierInput")
    def kms_key_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationType")
    def authorization_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationType"))

    @authorization_type.setter
    def authorization_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ea9280162d033e56313cbce9f74bf6a1aaea5b522e7d8950d9cce3e39290c6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1ec0a36fe5d5b3c5804a2f1703b0b47a3b82f6e407dc806253cffc5a3f46f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c34f10b51742705411fa3e34bfbce6833125448c70dcac92e0158c34d900cf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdentifier")
    def kms_key_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyIdentifier"))

    @kms_key_identifier.setter
    def kms_key_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a076695be5ab3942064880e5e84266326f409fcaf3a4aa493378c21df43837e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__103f1bbd7ab12feb7132b6c8b6438091663ef8406b559ece9cc5f1855b7885c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37dec3f7b49cdf0344e1f2058f314ee46222831b1c430edb2774d20a440fc690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParameters",
    jsii_struct_bases=[],
    name_mapping={
        "api_key": "apiKey",
        "basic": "basic",
        "invocation_http_parameters": "invocationHttpParameters",
        "oauth": "oauth",
    },
)
class CloudwatchEventConnectionAuthParameters:
    def __init__(
        self,
        *,
        api_key: typing.Optional[typing.Union["CloudwatchEventConnectionAuthParametersApiKey", typing.Dict[builtins.str, typing.Any]]] = None,
        basic: typing.Optional[typing.Union["CloudwatchEventConnectionAuthParametersBasic", typing.Dict[builtins.str, typing.Any]]] = None,
        invocation_http_parameters: typing.Optional[typing.Union["CloudwatchEventConnectionAuthParametersInvocationHttpParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth: typing.Optional[typing.Union["CloudwatchEventConnectionAuthParametersOauth", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param api_key: api_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#api_key CloudwatchEventConnection#api_key}
        :param basic: basic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#basic CloudwatchEventConnection#basic}
        :param invocation_http_parameters: invocation_http_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#invocation_http_parameters CloudwatchEventConnection#invocation_http_parameters}
        :param oauth: oauth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#oauth CloudwatchEventConnection#oauth}
        '''
        if isinstance(api_key, dict):
            api_key = CloudwatchEventConnectionAuthParametersApiKey(**api_key)
        if isinstance(basic, dict):
            basic = CloudwatchEventConnectionAuthParametersBasic(**basic)
        if isinstance(invocation_http_parameters, dict):
            invocation_http_parameters = CloudwatchEventConnectionAuthParametersInvocationHttpParameters(**invocation_http_parameters)
        if isinstance(oauth, dict):
            oauth = CloudwatchEventConnectionAuthParametersOauth(**oauth)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5948d624e69063e8c7aad03955be35247988584d417e94551be42fa87426b2de)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument basic", value=basic, expected_type=type_hints["basic"])
            check_type(argname="argument invocation_http_parameters", value=invocation_http_parameters, expected_type=type_hints["invocation_http_parameters"])
            check_type(argname="argument oauth", value=oauth, expected_type=type_hints["oauth"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_key is not None:
            self._values["api_key"] = api_key
        if basic is not None:
            self._values["basic"] = basic
        if invocation_http_parameters is not None:
            self._values["invocation_http_parameters"] = invocation_http_parameters
        if oauth is not None:
            self._values["oauth"] = oauth

    @builtins.property
    def api_key(
        self,
    ) -> typing.Optional["CloudwatchEventConnectionAuthParametersApiKey"]:
        '''api_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#api_key CloudwatchEventConnection#api_key}
        '''
        result = self._values.get("api_key")
        return typing.cast(typing.Optional["CloudwatchEventConnectionAuthParametersApiKey"], result)

    @builtins.property
    def basic(self) -> typing.Optional["CloudwatchEventConnectionAuthParametersBasic"]:
        '''basic block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#basic CloudwatchEventConnection#basic}
        '''
        result = self._values.get("basic")
        return typing.cast(typing.Optional["CloudwatchEventConnectionAuthParametersBasic"], result)

    @builtins.property
    def invocation_http_parameters(
        self,
    ) -> typing.Optional["CloudwatchEventConnectionAuthParametersInvocationHttpParameters"]:
        '''invocation_http_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#invocation_http_parameters CloudwatchEventConnection#invocation_http_parameters}
        '''
        result = self._values.get("invocation_http_parameters")
        return typing.cast(typing.Optional["CloudwatchEventConnectionAuthParametersInvocationHttpParameters"], result)

    @builtins.property
    def oauth(self) -> typing.Optional["CloudwatchEventConnectionAuthParametersOauth"]:
        '''oauth block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#oauth CloudwatchEventConnection#oauth}
        '''
        result = self._values.get("oauth")
        return typing.cast(typing.Optional["CloudwatchEventConnectionAuthParametersOauth"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchEventConnectionAuthParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersApiKey",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class CloudwatchEventConnectionAuthParametersApiKey:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#key CloudwatchEventConnection#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#value CloudwatchEventConnection#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70185f0f3148a06870bc7894a2baf7fe0de9ee9fdb197b4e93893a02cf20b4bb)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#key CloudwatchEventConnection#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#value CloudwatchEventConnection#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchEventConnectionAuthParametersApiKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchEventConnectionAuthParametersApiKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersApiKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ddf2d1706396a0eb59f925dcd0916e0abe20f366527c92d9a331c584a5ad154)
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
            type_hints = typing.get_type_hints(_typecheckingstub__025e05c90ab8753c1a2ab10505ec28a616da6858697e837f7c0a4b78a604aa59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88c9243a65b48695e1ce968c345c3e54ab6152247492ad82a7c5aab03c903ab9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudwatchEventConnectionAuthParametersApiKey]:
        return typing.cast(typing.Optional[CloudwatchEventConnectionAuthParametersApiKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudwatchEventConnectionAuthParametersApiKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62a2a286eeddceadf0086d8261b2c044bf67dbc734da94cfc0bc1fed7e3b3712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersBasic",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class CloudwatchEventConnectionAuthParametersBasic:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#password CloudwatchEventConnection#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#username CloudwatchEventConnection#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad4eb9c81711c01d6a7558849f2981722981c3ce8d5a6392c2939a375abc13c7)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#password CloudwatchEventConnection#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#username CloudwatchEventConnection#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchEventConnectionAuthParametersBasic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchEventConnectionAuthParametersBasicOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersBasicOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__382b47a4a8a8de2da1cd5aada1725a83831193bb5f784400ab6a567bd40cfdac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f42c5d8f5c6b7e256ec2d12424487d84f4aece18aff31082cbb219d03c554942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d1fbc335990badb911a50428af1bc7662cc36c35aa155ba8de49b4a4fa2b848)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudwatchEventConnectionAuthParametersBasic]:
        return typing.cast(typing.Optional[CloudwatchEventConnectionAuthParametersBasic], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudwatchEventConnectionAuthParametersBasic],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__209a443deedd09c566619009ece63557acccd3bdf708544f5e0799fc95cfb337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersInvocationHttpParameters",
    jsii_struct_bases=[],
    name_mapping={"body": "body", "header": "header", "query_string": "queryString"},
)
class CloudwatchEventConnectionAuthParametersInvocationHttpParameters:
    def __init__(
        self,
        *,
        body: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody", typing.Dict[builtins.str, typing.Any]]]]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param body: body block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#body CloudwatchEventConnection#body}
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#header CloudwatchEventConnection#header}
        :param query_string: query_string block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#query_string CloudwatchEventConnection#query_string}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6847f7d27e400e5b064738411a8240ae5ad5f6ed2d4783715ee22e8c9cd8416d)
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if body is not None:
            self._values["body"] = body
        if header is not None:
            self._values["header"] = header
        if query_string is not None:
            self._values["query_string"] = query_string

    @builtins.property
    def body(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody"]]]:
        '''body block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#body CloudwatchEventConnection#body}
        '''
        result = self._values.get("body")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody"]]], result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#header CloudwatchEventConnection#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader"]]], result)

    @builtins.property
    def query_string(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString"]]]:
        '''query_string block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#query_string CloudwatchEventConnection#query_string}
        '''
        result = self._values.get("query_string")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchEventConnectionAuthParametersInvocationHttpParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody",
    jsii_struct_bases=[],
    name_mapping={"is_value_secret": "isValueSecret", "key": "key", "value": "value"},
)
class CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody:
    def __init__(
        self,
        *,
        is_value_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param is_value_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#is_value_secret CloudwatchEventConnection#is_value_secret}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#key CloudwatchEventConnection#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#value CloudwatchEventConnection#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3498111605798bbbf92be106f512a5cd1cde9358197e0ea4a2b0a712bd380d3)
            check_type(argname="argument is_value_secret", value=is_value_secret, expected_type=type_hints["is_value_secret"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_value_secret is not None:
            self._values["is_value_secret"] = is_value_secret
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def is_value_secret(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#is_value_secret CloudwatchEventConnection#is_value_secret}.'''
        result = self._values.get("is_value_secret")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#key CloudwatchEventConnection#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#value CloudwatchEventConnection#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchEventConnectionAuthParametersInvocationHttpParametersBodyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersInvocationHttpParametersBodyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__949da568bf6c406fe366dd250296fee821ea50f9597996ac4aa0a29f4417fb08)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchEventConnectionAuthParametersInvocationHttpParametersBodyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__950071c2e375e646b7321b95a3e1e62e969125e2823c12252b2fae54a6ff56fd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchEventConnectionAuthParametersInvocationHttpParametersBodyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff84803a34701ff872504a9cc3d7f999983cd42706dde9205d8b0e86de30e428)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bb704e544056a33b1bfeb7724b27c66c85fc9de9db57dbdac1a40e118032227)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3586f75d6630b48c6efac137318cc8905f2522bc225893d1f73ceb344e588e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__275d2d3124367b241a0858bf2dab7ec11dee9d52995def3ad5ccc29a05427398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchEventConnectionAuthParametersInvocationHttpParametersBodyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersInvocationHttpParametersBodyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdcaed965afa8b6b6ba23cba6723a3b7a7f86116e59e90811d55c4aacd775f00)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIsValueSecret")
    def reset_is_value_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsValueSecret", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="isValueSecretInput")
    def is_value_secret_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isValueSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="isValueSecret")
    def is_value_secret(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isValueSecret"))

    @is_value_secret.setter
    def is_value_secret(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe6e5b6df20b1c3684df1c2157e0b0d4b2e0ff52a09ce0e28664a552b0fc69f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isValueSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb0b79f2f3d36564a56ef845be67f7fbd998226d33cdaff720f8ca344f748474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0a17cf6f9fb1bd37cb5c87ebd40320c779288aff0455950db628bf5b75a66af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d779bc3f54e16271cfcf747d3ad84e2191b1bd79cecb92e36d286eabd2a8b1f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader",
    jsii_struct_bases=[],
    name_mapping={"is_value_secret": "isValueSecret", "key": "key", "value": "value"},
)
class CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader:
    def __init__(
        self,
        *,
        is_value_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param is_value_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#is_value_secret CloudwatchEventConnection#is_value_secret}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#key CloudwatchEventConnection#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#value CloudwatchEventConnection#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b77bc70983244990aa42f5630b8162e15ad6bc37b10fc0b14c586fb3ed49cac)
            check_type(argname="argument is_value_secret", value=is_value_secret, expected_type=type_hints["is_value_secret"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_value_secret is not None:
            self._values["is_value_secret"] = is_value_secret
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def is_value_secret(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#is_value_secret CloudwatchEventConnection#is_value_secret}.'''
        result = self._values.get("is_value_secret")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#key CloudwatchEventConnection#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#value CloudwatchEventConnection#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d0e27f2af9d2d7109fcbd1ea077b84ac7f92aae74e471e2fcba49990b103a1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__683782a2ef9c9771cee9b222d39583c98ac45d4b602e086e2e320f59d9e23338)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7b040838265e36352037be46a0b70b5325296b6109b926fa76a2cfef6d7dc7f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bef1464a256f60d779e46af0c38c87edf09117e8a222791d962520719fc8455)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce8f2ea51a82e0ce65df4d19d66ad64b4d93df5dd7a815119f8a7ac717ca3021)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6301e98e902ff7946e0a2bf07558877a4c8aba2e095493a66ef446b2771db40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__277b0df7bcce9ead0884ad40a5a45e517f43adf0a8b610ad257b6637915852bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIsValueSecret")
    def reset_is_value_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsValueSecret", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="isValueSecretInput")
    def is_value_secret_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isValueSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="isValueSecret")
    def is_value_secret(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isValueSecret"))

    @is_value_secret.setter
    def is_value_secret(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ff5602cb333b137626d033fba511ba4dc13762c1063f282ee69760e2ab853f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isValueSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34fc7a4309283c426c264bece2cff36b5e580f634ef0703837b3dd8ced23a2d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41bf16944b5eb44b82699b2bf583d8a178782afdb3c47c0cc706ef70e990a295)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32ffdb7114a3cbf1a515042d98a2cb10aed62c2fca67fc5948eda12e3cc3767a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchEventConnectionAuthParametersInvocationHttpParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersInvocationHttpParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__967712ba8560126f8f763bdb6be955c7e26ebca086cfdf6b441915aa0d55ce3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBody")
    def put_body(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5350bced58914f3154ad3113637dd86ef0e9f6c17356031ce9088af42acb934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBody", [value]))

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a553e210b07192e7c47af9b9041d7da5fb2ba12ff6c64c1ef48f0493749f34a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="putQueryString")
    def put_query_string(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__487f72f48efe934427e6120e5677783fd5347d44493dd4d0650c33d40dea9b98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putQueryString", [value]))

    @jsii.member(jsii_name="resetBody")
    def reset_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBody", []))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetQueryString")
    def reset_query_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryString", []))

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(
        self,
    ) -> CloudwatchEventConnectionAuthParametersInvocationHttpParametersBodyList:
        return typing.cast(CloudwatchEventConnectionAuthParametersInvocationHttpParametersBodyList, jsii.get(self, "body"))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(
        self,
    ) -> CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeaderList:
        return typing.cast(CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="queryString")
    def query_string(
        self,
    ) -> "CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryStringList":
        return typing.cast("CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryStringList", jsii.get(self, "queryString"))

    @builtins.property
    @jsii.member(jsii_name="bodyInput")
    def body_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody]]], jsii.get(self, "bodyInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringInput")
    def query_string_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString"]]], jsii.get(self, "queryStringInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudwatchEventConnectionAuthParametersInvocationHttpParameters]:
        return typing.cast(typing.Optional[CloudwatchEventConnectionAuthParametersInvocationHttpParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudwatchEventConnectionAuthParametersInvocationHttpParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c308ebce2c9d6b58708b825f6179722f0273a99010430316d133f9d3b82717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString",
    jsii_struct_bases=[],
    name_mapping={"is_value_secret": "isValueSecret", "key": "key", "value": "value"},
)
class CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString:
    def __init__(
        self,
        *,
        is_value_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param is_value_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#is_value_secret CloudwatchEventConnection#is_value_secret}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#key CloudwatchEventConnection#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#value CloudwatchEventConnection#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf3aa0f118229b84aba0056fdca7c68fb2b77846959212349657c8008d30a176)
            check_type(argname="argument is_value_secret", value=is_value_secret, expected_type=type_hints["is_value_secret"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_value_secret is not None:
            self._values["is_value_secret"] = is_value_secret
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def is_value_secret(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#is_value_secret CloudwatchEventConnection#is_value_secret}.'''
        result = self._values.get("is_value_secret")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#key CloudwatchEventConnection#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#value CloudwatchEventConnection#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryStringList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryStringList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec47210df063225f417cdfc45c40285a53149387c0aa952a9fc694a9dedb09f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryStringOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7929d5407d235dd33a50feaff04ecb8cb2e69962f974d227eeac7efe630aded0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryStringOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0843f8c4363b979004abc3e88a695d5e9ebc495a2cbc409dd6207a336b07bcf3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6814c5c760283fb0049a9cf092e7987bb210377c3c367198a24a082a82015332)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75a7ba93e05e4d1b12c55b957c72d91b408dda201453f16799c93045de9c8ae7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__426cb8eb420e2a194090170bb9005a0a57943106ea3b0f4f1db74d4c6793a0ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryStringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryStringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07ef3864fa00f6cb26c90386d662a70e5e26f16d724cddaaa8373e558f452ad0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIsValueSecret")
    def reset_is_value_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsValueSecret", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="isValueSecretInput")
    def is_value_secret_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isValueSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="isValueSecret")
    def is_value_secret(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isValueSecret"))

    @is_value_secret.setter
    def is_value_secret(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39aae0ad56fa1d511344477b957ca67ce2cc0714db2011fc6239501a56a8ff42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isValueSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc8de544f08a2785fe1b153253d62ad01822f85ab5fcc40652f6d33a24e0e40f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__632d36574038e6dc9a50da63413f35a3acb61935a78b98bf1082a59859b02df5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3e9148335f955ec813f3cf9c47396d1976c9ba2fbb605a4d3a6c1719d73200e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersOauth",
    jsii_struct_bases=[],
    name_mapping={
        "authorization_endpoint": "authorizationEndpoint",
        "http_method": "httpMethod",
        "oauth_http_parameters": "oauthHttpParameters",
        "client_parameters": "clientParameters",
    },
)
class CloudwatchEventConnectionAuthParametersOauth:
    def __init__(
        self,
        *,
        authorization_endpoint: builtins.str,
        http_method: builtins.str,
        oauth_http_parameters: typing.Union["CloudwatchEventConnectionAuthParametersOauthOauthHttpParameters", typing.Dict[builtins.str, typing.Any]],
        client_parameters: typing.Optional[typing.Union["CloudwatchEventConnectionAuthParametersOauthClientParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authorization_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#authorization_endpoint CloudwatchEventConnection#authorization_endpoint}.
        :param http_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#http_method CloudwatchEventConnection#http_method}.
        :param oauth_http_parameters: oauth_http_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#oauth_http_parameters CloudwatchEventConnection#oauth_http_parameters}
        :param client_parameters: client_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#client_parameters CloudwatchEventConnection#client_parameters}
        '''
        if isinstance(oauth_http_parameters, dict):
            oauth_http_parameters = CloudwatchEventConnectionAuthParametersOauthOauthHttpParameters(**oauth_http_parameters)
        if isinstance(client_parameters, dict):
            client_parameters = CloudwatchEventConnectionAuthParametersOauthClientParameters(**client_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15db0338d6dcbed706f173ff99420e5f65a84c2c49d011be669283d85de11590)
            check_type(argname="argument authorization_endpoint", value=authorization_endpoint, expected_type=type_hints["authorization_endpoint"])
            check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
            check_type(argname="argument oauth_http_parameters", value=oauth_http_parameters, expected_type=type_hints["oauth_http_parameters"])
            check_type(argname="argument client_parameters", value=client_parameters, expected_type=type_hints["client_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorization_endpoint": authorization_endpoint,
            "http_method": http_method,
            "oauth_http_parameters": oauth_http_parameters,
        }
        if client_parameters is not None:
            self._values["client_parameters"] = client_parameters

    @builtins.property
    def authorization_endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#authorization_endpoint CloudwatchEventConnection#authorization_endpoint}.'''
        result = self._values.get("authorization_endpoint")
        assert result is not None, "Required property 'authorization_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def http_method(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#http_method CloudwatchEventConnection#http_method}.'''
        result = self._values.get("http_method")
        assert result is not None, "Required property 'http_method' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth_http_parameters(
        self,
    ) -> "CloudwatchEventConnectionAuthParametersOauthOauthHttpParameters":
        '''oauth_http_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#oauth_http_parameters CloudwatchEventConnection#oauth_http_parameters}
        '''
        result = self._values.get("oauth_http_parameters")
        assert result is not None, "Required property 'oauth_http_parameters' is missing"
        return typing.cast("CloudwatchEventConnectionAuthParametersOauthOauthHttpParameters", result)

    @builtins.property
    def client_parameters(
        self,
    ) -> typing.Optional["CloudwatchEventConnectionAuthParametersOauthClientParameters"]:
        '''client_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#client_parameters CloudwatchEventConnection#client_parameters}
        '''
        result = self._values.get("client_parameters")
        return typing.cast(typing.Optional["CloudwatchEventConnectionAuthParametersOauthClientParameters"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchEventConnectionAuthParametersOauth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersOauthClientParameters",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId", "client_secret": "clientSecret"},
)
class CloudwatchEventConnectionAuthParametersOauthClientParameters:
    def __init__(self, *, client_id: builtins.str, client_secret: builtins.str) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#client_id CloudwatchEventConnection#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#client_secret CloudwatchEventConnection#client_secret}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad15162c577fbf9fa7f8f76299a574c3598ca480b61fe3867e63733333d84ba9)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
        }

    @builtins.property
    def client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#client_id CloudwatchEventConnection#client_id}.'''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#client_secret CloudwatchEventConnection#client_secret}.'''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchEventConnectionAuthParametersOauthClientParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchEventConnectionAuthParametersOauthClientParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersOauthClientParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__051548505e4c8230fab48876eb33a5b2daf898fd7994db856217d24ac4602f04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5f7ee2c6f5ada95219fecef65ebe359d62a0204917eec370a476b59701a98bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40cbb688fc9566541bb930cbc8a358aa8608a8622a9f6c0f6ce2c7b2ec192836)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudwatchEventConnectionAuthParametersOauthClientParameters]:
        return typing.cast(typing.Optional[CloudwatchEventConnectionAuthParametersOauthClientParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudwatchEventConnectionAuthParametersOauthClientParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b29a5cca20759f79d5381df07ebd5e6e708395ef4eb0e542ac7326ea4ba11d4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersOauthOauthHttpParameters",
    jsii_struct_bases=[],
    name_mapping={"body": "body", "header": "header", "query_string": "queryString"},
)
class CloudwatchEventConnectionAuthParametersOauthOauthHttpParameters:
    def __init__(
        self,
        *,
        body: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody", typing.Dict[builtins.str, typing.Any]]]]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param body: body block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#body CloudwatchEventConnection#body}
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#header CloudwatchEventConnection#header}
        :param query_string: query_string block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#query_string CloudwatchEventConnection#query_string}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bee94363023f70c73ce3b291fd31c7ffcea7d37330ed98d9a11fb935e4041fc)
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if body is not None:
            self._values["body"] = body
        if header is not None:
            self._values["header"] = header
        if query_string is not None:
            self._values["query_string"] = query_string

    @builtins.property
    def body(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody"]]]:
        '''body block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#body CloudwatchEventConnection#body}
        '''
        result = self._values.get("body")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody"]]], result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#header CloudwatchEventConnection#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader"]]], result)

    @builtins.property
    def query_string(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString"]]]:
        '''query_string block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#query_string CloudwatchEventConnection#query_string}
        '''
        result = self._values.get("query_string")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchEventConnectionAuthParametersOauthOauthHttpParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody",
    jsii_struct_bases=[],
    name_mapping={"is_value_secret": "isValueSecret", "key": "key", "value": "value"},
)
class CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody:
    def __init__(
        self,
        *,
        is_value_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param is_value_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#is_value_secret CloudwatchEventConnection#is_value_secret}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#key CloudwatchEventConnection#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#value CloudwatchEventConnection#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a1ab4cea2bbd0bf9628b2717fba4fd0ab465ec05e1c38ba98e3c8d5a9f8f129)
            check_type(argname="argument is_value_secret", value=is_value_secret, expected_type=type_hints["is_value_secret"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_value_secret is not None:
            self._values["is_value_secret"] = is_value_secret
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def is_value_secret(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#is_value_secret CloudwatchEventConnection#is_value_secret}.'''
        result = self._values.get("is_value_secret")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#key CloudwatchEventConnection#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#value CloudwatchEventConnection#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBodyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBodyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff23e026958350578bf41b11efad1a77cc9fc4cf98f143999f6348abe18af2b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBodyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f26e1538aa98df678bdcc5b88db9413b96771cdd663fe25be92fcbdf96758e0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBodyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca77790fcda9a80e8c24b7d871bc9f8b99047ba439b63f25131b6d27503622a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__645b45945077f8887f003294b0a98284d4e226247da40e12663d7e17fb4d0b50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f905c33653d1fb732af5fa92e6cbf6d74aeed335e13f850521d8aa4d78a62c15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__758e6f096089dbace1665b24271cf360f5f3c7c2e00df34c3d91a614ff8ccd5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBodyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBodyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__197f6a9ec4b0776741f47ef0e7c22bb20fe3b612008d7d41ce36b586a7c354bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIsValueSecret")
    def reset_is_value_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsValueSecret", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="isValueSecretInput")
    def is_value_secret_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isValueSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="isValueSecret")
    def is_value_secret(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isValueSecret"))

    @is_value_secret.setter
    def is_value_secret(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d330d72e35e46da0068e95118dfd49e23a224f3adf8cdf832a777e50dd5a8320)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isValueSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92251d06ffa1fb7fecf52b0d747bafb24aed6880530a6c8a431f9dfd15c6bcc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4346d854e39cdf2e21f0d139f8b5bd0c2358e41c53352e3ac38955ff938cb84b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a2c8d746db7dd52249c47456cc362f783661236849874bf9d33ce54488f7631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader",
    jsii_struct_bases=[],
    name_mapping={"is_value_secret": "isValueSecret", "key": "key", "value": "value"},
)
class CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader:
    def __init__(
        self,
        *,
        is_value_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param is_value_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#is_value_secret CloudwatchEventConnection#is_value_secret}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#key CloudwatchEventConnection#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#value CloudwatchEventConnection#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4476ecc84bf8a83b0a9ddae24146f7f7d10b379df81ce7a3fd194f179c68702e)
            check_type(argname="argument is_value_secret", value=is_value_secret, expected_type=type_hints["is_value_secret"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_value_secret is not None:
            self._values["is_value_secret"] = is_value_secret
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def is_value_secret(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#is_value_secret CloudwatchEventConnection#is_value_secret}.'''
        result = self._values.get("is_value_secret")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#key CloudwatchEventConnection#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#value CloudwatchEventConnection#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f277e731f285394ff5514f2fd90d668893d5ca49cfe3223d5d33fab059c8c1b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__530fb5aeb3fad58d4f9b49546abbb566729ae1bc027b3a6d67f05932e2237843)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14261dd9b0b94ac978fbd6946fb1ace1c53371fc96808559ac2471b257024446)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89557e4df47f4effa51206bb3023b9ed2a76a0bc44fdd18c203285cdec0e2041)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ee114cebef8db567dc628cc86ad0dc7cf754979c985456b57a1cd2077346319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__995afebcbd055a5271fdfac9571279a931283cb134fb4df46c8359bb66cc38a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d678dbd7750c621b6e8acf7a0539d9e514863a4a43dd4fa494c7280a36719cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIsValueSecret")
    def reset_is_value_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsValueSecret", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="isValueSecretInput")
    def is_value_secret_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isValueSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="isValueSecret")
    def is_value_secret(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isValueSecret"))

    @is_value_secret.setter
    def is_value_secret(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cc5f4516e81b94856c20f584cb680f443f3de40d698d64ecdf68e3afe1b4011)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isValueSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d97ea26362def766017d520fd42275378829f5650d08ab2bb4ab592f094787a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b507839db61854b881ed72a4758dd6aeafec503d4c849b7476fc91fb181a531a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46feddaef4306d2c79a10dec4cda64bf1c0bb3990757de0d1d4ac1edd15a408e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__800b6a066fc82b9fb87df4d0fb9c9e9b80ccaa3c2d9a41d4844d20e37818c3f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBody")
    def put_body(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df834c87e25b03e52ecc88f2248e20f9c97c2f0de391f48dc02930e6e6894387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBody", [value]))

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ccc8983250dc46990f6e40f2693e95dfc738af57cc9144f4eef47f563cfd129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="putQueryString")
    def put_query_string(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ecfea78fe8ba2fdd926c923cae62f46e5b93a81b388df1856f603f08abad6f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putQueryString", [value]))

    @jsii.member(jsii_name="resetBody")
    def reset_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBody", []))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetQueryString")
    def reset_query_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryString", []))

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(
        self,
    ) -> CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBodyList:
        return typing.cast(CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBodyList, jsii.get(self, "body"))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(
        self,
    ) -> CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeaderList:
        return typing.cast(CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="queryString")
    def query_string(
        self,
    ) -> "CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryStringList":
        return typing.cast("CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryStringList", jsii.get(self, "queryString"))

    @builtins.property
    @jsii.member(jsii_name="bodyInput")
    def body_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody]]], jsii.get(self, "bodyInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringInput")
    def query_string_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString"]]], jsii.get(self, "queryStringInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudwatchEventConnectionAuthParametersOauthOauthHttpParameters]:
        return typing.cast(typing.Optional[CloudwatchEventConnectionAuthParametersOauthOauthHttpParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudwatchEventConnectionAuthParametersOauthOauthHttpParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cf739a1b24f4e748f51554f4b00470816451bbc86a791cfd6c4fe9ea723101e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString",
    jsii_struct_bases=[],
    name_mapping={"is_value_secret": "isValueSecret", "key": "key", "value": "value"},
)
class CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString:
    def __init__(
        self,
        *,
        is_value_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param is_value_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#is_value_secret CloudwatchEventConnection#is_value_secret}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#key CloudwatchEventConnection#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#value CloudwatchEventConnection#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2addeabac918f745c395151ad8e11260c5354a3c18dd06ac8683c196b3919d01)
            check_type(argname="argument is_value_secret", value=is_value_secret, expected_type=type_hints["is_value_secret"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_value_secret is not None:
            self._values["is_value_secret"] = is_value_secret
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def is_value_secret(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#is_value_secret CloudwatchEventConnection#is_value_secret}.'''
        result = self._values.get("is_value_secret")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#key CloudwatchEventConnection#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#value CloudwatchEventConnection#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryStringList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryStringList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb45b4598eb90f4a948f5b63811d21c896fd35ed99ed48fb684a0a40bf031a75)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryStringOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc70db856af1a5df244bee1759d27b0232813f6582350bcc58f8e33080100b7e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryStringOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43d81a434e108127140fcb6f81b6458e2c37a5ffd4a56f6a0470b73dd0719bb0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c589897b6de6c019590bcde06c89e3ad2c19382031132e8b2873188cf7e0806)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9011465a0deeea64d1a7955251d6a8db53b64721ba542e10ebc32acf6b1fdd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91d1851323d3f33d52c6372a14e5cfb850f8fdd50ed21a25eda956356a044942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryStringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryStringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0e19cf798381d96ffc177a67e47d719cdaa5a2a18926ec2773681e581373a46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIsValueSecret")
    def reset_is_value_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsValueSecret", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="isValueSecretInput")
    def is_value_secret_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isValueSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="isValueSecret")
    def is_value_secret(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isValueSecret"))

    @is_value_secret.setter
    def is_value_secret(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0739c244a0a9e9d0bf6593a9294742e8fbbf1d1f10c6eff03706bebf15100500)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isValueSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98d4ef4346a599d66983c2623aa198eeed461f1018ce0e166a11cdfef83aebac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17a0fbb23a8eb29cd65486c26c398a13ff5a02686995fee1d4e3690d00ad6932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab22f6d6cd0a5cf1abe4d60ac46ec39b9bd3f1cd3ed6623a72eb257667b465f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchEventConnectionAuthParametersOauthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersOauthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__293b906b1399f5bcbb9adee3866a6c0e098d82f554da81cdab429beb282b117c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClientParameters")
    def put_client_parameters(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
    ) -> None:
        '''
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#client_id CloudwatchEventConnection#client_id}.
        :param client_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#client_secret CloudwatchEventConnection#client_secret}.
        '''
        value = CloudwatchEventConnectionAuthParametersOauthClientParameters(
            client_id=client_id, client_secret=client_secret
        )

        return typing.cast(None, jsii.invoke(self, "putClientParameters", [value]))

    @jsii.member(jsii_name="putOauthHttpParameters")
    def put_oauth_http_parameters(
        self,
        *,
        body: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody, typing.Dict[builtins.str, typing.Any]]]]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param body: body block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#body CloudwatchEventConnection#body}
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#header CloudwatchEventConnection#header}
        :param query_string: query_string block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#query_string CloudwatchEventConnection#query_string}
        '''
        value = CloudwatchEventConnectionAuthParametersOauthOauthHttpParameters(
            body=body, header=header, query_string=query_string
        )

        return typing.cast(None, jsii.invoke(self, "putOauthHttpParameters", [value]))

    @jsii.member(jsii_name="resetClientParameters")
    def reset_client_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientParameters", []))

    @builtins.property
    @jsii.member(jsii_name="clientParameters")
    def client_parameters(
        self,
    ) -> CloudwatchEventConnectionAuthParametersOauthClientParametersOutputReference:
        return typing.cast(CloudwatchEventConnectionAuthParametersOauthClientParametersOutputReference, jsii.get(self, "clientParameters"))

    @builtins.property
    @jsii.member(jsii_name="oauthHttpParameters")
    def oauth_http_parameters(
        self,
    ) -> CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersOutputReference:
        return typing.cast(CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersOutputReference, jsii.get(self, "oauthHttpParameters"))

    @builtins.property
    @jsii.member(jsii_name="authorizationEndpointInput")
    def authorization_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="clientParametersInput")
    def client_parameters_input(
        self,
    ) -> typing.Optional[CloudwatchEventConnectionAuthParametersOauthClientParameters]:
        return typing.cast(typing.Optional[CloudwatchEventConnectionAuthParametersOauthClientParameters], jsii.get(self, "clientParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="httpMethodInput")
    def http_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthHttpParametersInput")
    def oauth_http_parameters_input(
        self,
    ) -> typing.Optional[CloudwatchEventConnectionAuthParametersOauthOauthHttpParameters]:
        return typing.cast(typing.Optional[CloudwatchEventConnectionAuthParametersOauthOauthHttpParameters], jsii.get(self, "oauthHttpParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationEndpoint")
    def authorization_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationEndpoint"))

    @authorization_endpoint.setter
    def authorization_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fa08a50aec89ff37ceebc8d81a4e633ad2a865712100b892928e202b40b49e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def http_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpMethod"))

    @http_method.setter
    def http_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__712af95004a8ddb4a24c455e568fa9ec73fedb83138473f28fb7b6e145ea9336)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudwatchEventConnectionAuthParametersOauth]:
        return typing.cast(typing.Optional[CloudwatchEventConnectionAuthParametersOauth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudwatchEventConnectionAuthParametersOauth],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d4d4cc6e269f41caa044ad89758084e4dded0a26f74babda814df4f87ed7a8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudwatchEventConnectionAuthParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionAuthParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15e2e241dfd60cc7a7b2400d9a1f6b59f49cf05545ba7469a608adc55e8522ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApiKey")
    def put_api_key(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#key CloudwatchEventConnection#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#value CloudwatchEventConnection#value}.
        '''
        value_ = CloudwatchEventConnectionAuthParametersApiKey(key=key, value=value)

        return typing.cast(None, jsii.invoke(self, "putApiKey", [value_]))

    @jsii.member(jsii_name="putBasic")
    def put_basic(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#password CloudwatchEventConnection#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#username CloudwatchEventConnection#username}.
        '''
        value = CloudwatchEventConnectionAuthParametersBasic(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putBasic", [value]))

    @jsii.member(jsii_name="putInvocationHttpParameters")
    def put_invocation_http_parameters(
        self,
        *,
        body: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody, typing.Dict[builtins.str, typing.Any]]]]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param body: body block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#body CloudwatchEventConnection#body}
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#header CloudwatchEventConnection#header}
        :param query_string: query_string block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#query_string CloudwatchEventConnection#query_string}
        '''
        value = CloudwatchEventConnectionAuthParametersInvocationHttpParameters(
            body=body, header=header, query_string=query_string
        )

        return typing.cast(None, jsii.invoke(self, "putInvocationHttpParameters", [value]))

    @jsii.member(jsii_name="putOauth")
    def put_oauth(
        self,
        *,
        authorization_endpoint: builtins.str,
        http_method: builtins.str,
        oauth_http_parameters: typing.Union[CloudwatchEventConnectionAuthParametersOauthOauthHttpParameters, typing.Dict[builtins.str, typing.Any]],
        client_parameters: typing.Optional[typing.Union[CloudwatchEventConnectionAuthParametersOauthClientParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authorization_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#authorization_endpoint CloudwatchEventConnection#authorization_endpoint}.
        :param http_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#http_method CloudwatchEventConnection#http_method}.
        :param oauth_http_parameters: oauth_http_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#oauth_http_parameters CloudwatchEventConnection#oauth_http_parameters}
        :param client_parameters: client_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#client_parameters CloudwatchEventConnection#client_parameters}
        '''
        value = CloudwatchEventConnectionAuthParametersOauth(
            authorization_endpoint=authorization_endpoint,
            http_method=http_method,
            oauth_http_parameters=oauth_http_parameters,
            client_parameters=client_parameters,
        )

        return typing.cast(None, jsii.invoke(self, "putOauth", [value]))

    @jsii.member(jsii_name="resetApiKey")
    def reset_api_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiKey", []))

    @jsii.member(jsii_name="resetBasic")
    def reset_basic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasic", []))

    @jsii.member(jsii_name="resetInvocationHttpParameters")
    def reset_invocation_http_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvocationHttpParameters", []))

    @jsii.member(jsii_name="resetOauth")
    def reset_oauth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauth", []))

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> CloudwatchEventConnectionAuthParametersApiKeyOutputReference:
        return typing.cast(CloudwatchEventConnectionAuthParametersApiKeyOutputReference, jsii.get(self, "apiKey"))

    @builtins.property
    @jsii.member(jsii_name="basic")
    def basic(self) -> CloudwatchEventConnectionAuthParametersBasicOutputReference:
        return typing.cast(CloudwatchEventConnectionAuthParametersBasicOutputReference, jsii.get(self, "basic"))

    @builtins.property
    @jsii.member(jsii_name="invocationHttpParameters")
    def invocation_http_parameters(
        self,
    ) -> CloudwatchEventConnectionAuthParametersInvocationHttpParametersOutputReference:
        return typing.cast(CloudwatchEventConnectionAuthParametersInvocationHttpParametersOutputReference, jsii.get(self, "invocationHttpParameters"))

    @builtins.property
    @jsii.member(jsii_name="oauth")
    def oauth(self) -> CloudwatchEventConnectionAuthParametersOauthOutputReference:
        return typing.cast(CloudwatchEventConnectionAuthParametersOauthOutputReference, jsii.get(self, "oauth"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(
        self,
    ) -> typing.Optional[CloudwatchEventConnectionAuthParametersApiKey]:
        return typing.cast(typing.Optional[CloudwatchEventConnectionAuthParametersApiKey], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="basicInput")
    def basic_input(
        self,
    ) -> typing.Optional[CloudwatchEventConnectionAuthParametersBasic]:
        return typing.cast(typing.Optional[CloudwatchEventConnectionAuthParametersBasic], jsii.get(self, "basicInput"))

    @builtins.property
    @jsii.member(jsii_name="invocationHttpParametersInput")
    def invocation_http_parameters_input(
        self,
    ) -> typing.Optional[CloudwatchEventConnectionAuthParametersInvocationHttpParameters]:
        return typing.cast(typing.Optional[CloudwatchEventConnectionAuthParametersInvocationHttpParameters], jsii.get(self, "invocationHttpParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthInput")
    def oauth_input(
        self,
    ) -> typing.Optional[CloudwatchEventConnectionAuthParametersOauth]:
        return typing.cast(typing.Optional[CloudwatchEventConnectionAuthParametersOauth], jsii.get(self, "oauthInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudwatchEventConnectionAuthParameters]:
        return typing.cast(typing.Optional[CloudwatchEventConnectionAuthParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudwatchEventConnectionAuthParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18117d155ffac0ec4a935b331f9ce007de44d71591b625b9936b10c40c63e4fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "authorization_type": "authorizationType",
        "auth_parameters": "authParameters",
        "name": "name",
        "description": "description",
        "id": "id",
        "invocation_connectivity_parameters": "invocationConnectivityParameters",
        "kms_key_identifier": "kmsKeyIdentifier",
        "region": "region",
    },
)
class CloudwatchEventConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        authorization_type: builtins.str,
        auth_parameters: typing.Union[CloudwatchEventConnectionAuthParameters, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        invocation_connectivity_parameters: typing.Optional[typing.Union["CloudwatchEventConnectionInvocationConnectivityParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        kms_key_identifier: typing.Optional[builtins.str] = None,
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
        :param authorization_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#authorization_type CloudwatchEventConnection#authorization_type}.
        :param auth_parameters: auth_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#auth_parameters CloudwatchEventConnection#auth_parameters}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#name CloudwatchEventConnection#name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#description CloudwatchEventConnection#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#id CloudwatchEventConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param invocation_connectivity_parameters: invocation_connectivity_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#invocation_connectivity_parameters CloudwatchEventConnection#invocation_connectivity_parameters}
        :param kms_key_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#kms_key_identifier CloudwatchEventConnection#kms_key_identifier}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#region CloudwatchEventConnection#region}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(auth_parameters, dict):
            auth_parameters = CloudwatchEventConnectionAuthParameters(**auth_parameters)
        if isinstance(invocation_connectivity_parameters, dict):
            invocation_connectivity_parameters = CloudwatchEventConnectionInvocationConnectivityParameters(**invocation_connectivity_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dab0d59891f12534a81adf15048a397646e207d6272bba9d943e765896fb3352)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument authorization_type", value=authorization_type, expected_type=type_hints["authorization_type"])
            check_type(argname="argument auth_parameters", value=auth_parameters, expected_type=type_hints["auth_parameters"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument invocation_connectivity_parameters", value=invocation_connectivity_parameters, expected_type=type_hints["invocation_connectivity_parameters"])
            check_type(argname="argument kms_key_identifier", value=kms_key_identifier, expected_type=type_hints["kms_key_identifier"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorization_type": authorization_type,
            "auth_parameters": auth_parameters,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if invocation_connectivity_parameters is not None:
            self._values["invocation_connectivity_parameters"] = invocation_connectivity_parameters
        if kms_key_identifier is not None:
            self._values["kms_key_identifier"] = kms_key_identifier
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
    def authorization_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#authorization_type CloudwatchEventConnection#authorization_type}.'''
        result = self._values.get("authorization_type")
        assert result is not None, "Required property 'authorization_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_parameters(self) -> CloudwatchEventConnectionAuthParameters:
        '''auth_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#auth_parameters CloudwatchEventConnection#auth_parameters}
        '''
        result = self._values.get("auth_parameters")
        assert result is not None, "Required property 'auth_parameters' is missing"
        return typing.cast(CloudwatchEventConnectionAuthParameters, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#name CloudwatchEventConnection#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#description CloudwatchEventConnection#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#id CloudwatchEventConnection#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invocation_connectivity_parameters(
        self,
    ) -> typing.Optional["CloudwatchEventConnectionInvocationConnectivityParameters"]:
        '''invocation_connectivity_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#invocation_connectivity_parameters CloudwatchEventConnection#invocation_connectivity_parameters}
        '''
        result = self._values.get("invocation_connectivity_parameters")
        return typing.cast(typing.Optional["CloudwatchEventConnectionInvocationConnectivityParameters"], result)

    @builtins.property
    def kms_key_identifier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#kms_key_identifier CloudwatchEventConnection#kms_key_identifier}.'''
        result = self._values.get("kms_key_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#region CloudwatchEventConnection#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchEventConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionInvocationConnectivityParameters",
    jsii_struct_bases=[],
    name_mapping={"resource_parameters": "resourceParameters"},
)
class CloudwatchEventConnectionInvocationConnectivityParameters:
    def __init__(
        self,
        *,
        resource_parameters: typing.Union["CloudwatchEventConnectionInvocationConnectivityParametersResourceParameters", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param resource_parameters: resource_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#resource_parameters CloudwatchEventConnection#resource_parameters}
        '''
        if isinstance(resource_parameters, dict):
            resource_parameters = CloudwatchEventConnectionInvocationConnectivityParametersResourceParameters(**resource_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16ba1d5bfa7f128091ac5d70ac6561d21fd4ffa71cf8a5cf3951fccf2c29b740)
            check_type(argname="argument resource_parameters", value=resource_parameters, expected_type=type_hints["resource_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_parameters": resource_parameters,
        }

    @builtins.property
    def resource_parameters(
        self,
    ) -> "CloudwatchEventConnectionInvocationConnectivityParametersResourceParameters":
        '''resource_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#resource_parameters CloudwatchEventConnection#resource_parameters}
        '''
        result = self._values.get("resource_parameters")
        assert result is not None, "Required property 'resource_parameters' is missing"
        return typing.cast("CloudwatchEventConnectionInvocationConnectivityParametersResourceParameters", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchEventConnectionInvocationConnectivityParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchEventConnectionInvocationConnectivityParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionInvocationConnectivityParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc5a9af169335941183093a9cb805e5d0b1b9e187ebe6b6abb848edca89aef39)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putResourceParameters")
    def put_resource_parameters(
        self,
        *,
        resource_configuration_arn: builtins.str,
    ) -> None:
        '''
        :param resource_configuration_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#resource_configuration_arn CloudwatchEventConnection#resource_configuration_arn}.
        '''
        value = CloudwatchEventConnectionInvocationConnectivityParametersResourceParameters(
            resource_configuration_arn=resource_configuration_arn
        )

        return typing.cast(None, jsii.invoke(self, "putResourceParameters", [value]))

    @builtins.property
    @jsii.member(jsii_name="resourceParameters")
    def resource_parameters(
        self,
    ) -> "CloudwatchEventConnectionInvocationConnectivityParametersResourceParametersOutputReference":
        return typing.cast("CloudwatchEventConnectionInvocationConnectivityParametersResourceParametersOutputReference", jsii.get(self, "resourceParameters"))

    @builtins.property
    @jsii.member(jsii_name="resourceParametersInput")
    def resource_parameters_input(
        self,
    ) -> typing.Optional["CloudwatchEventConnectionInvocationConnectivityParametersResourceParameters"]:
        return typing.cast(typing.Optional["CloudwatchEventConnectionInvocationConnectivityParametersResourceParameters"], jsii.get(self, "resourceParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudwatchEventConnectionInvocationConnectivityParameters]:
        return typing.cast(typing.Optional[CloudwatchEventConnectionInvocationConnectivityParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudwatchEventConnectionInvocationConnectivityParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__143306344b33f217cec1d072a1de59bebbdbfa64521e11ad391d8aadfbf73502)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionInvocationConnectivityParametersResourceParameters",
    jsii_struct_bases=[],
    name_mapping={"resource_configuration_arn": "resourceConfigurationArn"},
)
class CloudwatchEventConnectionInvocationConnectivityParametersResourceParameters:
    def __init__(self, *, resource_configuration_arn: builtins.str) -> None:
        '''
        :param resource_configuration_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#resource_configuration_arn CloudwatchEventConnection#resource_configuration_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f11129d787443ecf252b7d9d7d03cbdfb51f38f5759a92b7f65a75d69e4532f5)
            check_type(argname="argument resource_configuration_arn", value=resource_configuration_arn, expected_type=type_hints["resource_configuration_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_configuration_arn": resource_configuration_arn,
        }

    @builtins.property
    def resource_configuration_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudwatch_event_connection#resource_configuration_arn CloudwatchEventConnection#resource_configuration_arn}.'''
        result = self._values.get("resource_configuration_arn")
        assert result is not None, "Required property 'resource_configuration_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchEventConnectionInvocationConnectivityParametersResourceParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchEventConnectionInvocationConnectivityParametersResourceParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudwatchEventConnection.CloudwatchEventConnectionInvocationConnectivityParametersResourceParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7e8991d922dbeb1a0095a8d59bb140a4e3dbf5069f5c7566ec52de4a1a70070)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceAssociationArn")
    def resource_association_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceAssociationArn"))

    @builtins.property
    @jsii.member(jsii_name="resourceConfigurationArnInput")
    def resource_configuration_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceConfigurationArnInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceConfigurationArn")
    def resource_configuration_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceConfigurationArn"))

    @resource_configuration_arn.setter
    def resource_configuration_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d35cb985df5180ae116292a6d46bcc3028c22598f90211727b12538199374a13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceConfigurationArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudwatchEventConnectionInvocationConnectivityParametersResourceParameters]:
        return typing.cast(typing.Optional[CloudwatchEventConnectionInvocationConnectivityParametersResourceParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudwatchEventConnectionInvocationConnectivityParametersResourceParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02840b46ff18f37b4fcf09e0e8236774719dac9ea3123bf5fbd4dcc4ed833283)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudwatchEventConnection",
    "CloudwatchEventConnectionAuthParameters",
    "CloudwatchEventConnectionAuthParametersApiKey",
    "CloudwatchEventConnectionAuthParametersApiKeyOutputReference",
    "CloudwatchEventConnectionAuthParametersBasic",
    "CloudwatchEventConnectionAuthParametersBasicOutputReference",
    "CloudwatchEventConnectionAuthParametersInvocationHttpParameters",
    "CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody",
    "CloudwatchEventConnectionAuthParametersInvocationHttpParametersBodyList",
    "CloudwatchEventConnectionAuthParametersInvocationHttpParametersBodyOutputReference",
    "CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader",
    "CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeaderList",
    "CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeaderOutputReference",
    "CloudwatchEventConnectionAuthParametersInvocationHttpParametersOutputReference",
    "CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString",
    "CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryStringList",
    "CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryStringOutputReference",
    "CloudwatchEventConnectionAuthParametersOauth",
    "CloudwatchEventConnectionAuthParametersOauthClientParameters",
    "CloudwatchEventConnectionAuthParametersOauthClientParametersOutputReference",
    "CloudwatchEventConnectionAuthParametersOauthOauthHttpParameters",
    "CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody",
    "CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBodyList",
    "CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBodyOutputReference",
    "CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader",
    "CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeaderList",
    "CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeaderOutputReference",
    "CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersOutputReference",
    "CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString",
    "CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryStringList",
    "CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryStringOutputReference",
    "CloudwatchEventConnectionAuthParametersOauthOutputReference",
    "CloudwatchEventConnectionAuthParametersOutputReference",
    "CloudwatchEventConnectionConfig",
    "CloudwatchEventConnectionInvocationConnectivityParameters",
    "CloudwatchEventConnectionInvocationConnectivityParametersOutputReference",
    "CloudwatchEventConnectionInvocationConnectivityParametersResourceParameters",
    "CloudwatchEventConnectionInvocationConnectivityParametersResourceParametersOutputReference",
]

publication.publish()

def _typecheckingstub__406369d4c4d52e1406d34183b518b86b651c926b8b1905aedabd5401f7b9e834(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    authorization_type: builtins.str,
    auth_parameters: typing.Union[CloudwatchEventConnectionAuthParameters, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    invocation_connectivity_parameters: typing.Optional[typing.Union[CloudwatchEventConnectionInvocationConnectivityParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    kms_key_identifier: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__ed0bbb6b9e5515445a287333739d8b8f5eec16e1604fd6ef2edb58c58f966e02(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ea9280162d033e56313cbce9f74bf6a1aaea5b522e7d8950d9cce3e39290c6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1ec0a36fe5d5b3c5804a2f1703b0b47a3b82f6e407dc806253cffc5a3f46f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c34f10b51742705411fa3e34bfbce6833125448c70dcac92e0158c34d900cf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a076695be5ab3942064880e5e84266326f409fcaf3a4aa493378c21df43837e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103f1bbd7ab12feb7132b6c8b6438091663ef8406b559ece9cc5f1855b7885c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37dec3f7b49cdf0344e1f2058f314ee46222831b1c430edb2774d20a440fc690(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5948d624e69063e8c7aad03955be35247988584d417e94551be42fa87426b2de(
    *,
    api_key: typing.Optional[typing.Union[CloudwatchEventConnectionAuthParametersApiKey, typing.Dict[builtins.str, typing.Any]]] = None,
    basic: typing.Optional[typing.Union[CloudwatchEventConnectionAuthParametersBasic, typing.Dict[builtins.str, typing.Any]]] = None,
    invocation_http_parameters: typing.Optional[typing.Union[CloudwatchEventConnectionAuthParametersInvocationHttpParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth: typing.Optional[typing.Union[CloudwatchEventConnectionAuthParametersOauth, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70185f0f3148a06870bc7894a2baf7fe0de9ee9fdb197b4e93893a02cf20b4bb(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ddf2d1706396a0eb59f925dcd0916e0abe20f366527c92d9a331c584a5ad154(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025e05c90ab8753c1a2ab10505ec28a616da6858697e837f7c0a4b78a604aa59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c9243a65b48695e1ce968c345c3e54ab6152247492ad82a7c5aab03c903ab9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62a2a286eeddceadf0086d8261b2c044bf67dbc734da94cfc0bc1fed7e3b3712(
    value: typing.Optional[CloudwatchEventConnectionAuthParametersApiKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad4eb9c81711c01d6a7558849f2981722981c3ce8d5a6392c2939a375abc13c7(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382b47a4a8a8de2da1cd5aada1725a83831193bb5f784400ab6a567bd40cfdac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42c5d8f5c6b7e256ec2d12424487d84f4aece18aff31082cbb219d03c554942(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d1fbc335990badb911a50428af1bc7662cc36c35aa155ba8de49b4a4fa2b848(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__209a443deedd09c566619009ece63557acccd3bdf708544f5e0799fc95cfb337(
    value: typing.Optional[CloudwatchEventConnectionAuthParametersBasic],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6847f7d27e400e5b064738411a8240ae5ad5f6ed2d4783715ee22e8c9cd8416d(
    *,
    body: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody, typing.Dict[builtins.str, typing.Any]]]]] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    query_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3498111605798bbbf92be106f512a5cd1cde9358197e0ea4a2b0a712bd380d3(
    *,
    is_value_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__949da568bf6c406fe366dd250296fee821ea50f9597996ac4aa0a29f4417fb08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__950071c2e375e646b7321b95a3e1e62e969125e2823c12252b2fae54a6ff56fd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff84803a34701ff872504a9cc3d7f999983cd42706dde9205d8b0e86de30e428(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb704e544056a33b1bfeb7724b27c66c85fc9de9db57dbdac1a40e118032227(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3586f75d6630b48c6efac137318cc8905f2522bc225893d1f73ceb344e588e7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__275d2d3124367b241a0858bf2dab7ec11dee9d52995def3ad5ccc29a05427398(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdcaed965afa8b6b6ba23cba6723a3b7a7f86116e59e90811d55c4aacd775f00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe6e5b6df20b1c3684df1c2157e0b0d4b2e0ff52a09ce0e28664a552b0fc69f6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0b79f2f3d36564a56ef845be67f7fbd998226d33cdaff720f8ca344f748474(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0a17cf6f9fb1bd37cb5c87ebd40320c779288aff0455950db628bf5b75a66af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d779bc3f54e16271cfcf747d3ad84e2191b1bd79cecb92e36d286eabd2a8b1f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b77bc70983244990aa42f5630b8162e15ad6bc37b10fc0b14c586fb3ed49cac(
    *,
    is_value_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d0e27f2af9d2d7109fcbd1ea077b84ac7f92aae74e471e2fcba49990b103a1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__683782a2ef9c9771cee9b222d39583c98ac45d4b602e086e2e320f59d9e23338(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7b040838265e36352037be46a0b70b5325296b6109b926fa76a2cfef6d7dc7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bef1464a256f60d779e46af0c38c87edf09117e8a222791d962520719fc8455(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce8f2ea51a82e0ce65df4d19d66ad64b4d93df5dd7a815119f8a7ac717ca3021(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6301e98e902ff7946e0a2bf07558877a4c8aba2e095493a66ef446b2771db40(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__277b0df7bcce9ead0884ad40a5a45e517f43adf0a8b610ad257b6637915852bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ff5602cb333b137626d033fba511ba4dc13762c1063f282ee69760e2ab853f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34fc7a4309283c426c264bece2cff36b5e580f634ef0703837b3dd8ced23a2d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41bf16944b5eb44b82699b2bf583d8a178782afdb3c47c0cc706ef70e990a295(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ffdb7114a3cbf1a515042d98a2cb10aed62c2fca67fc5948eda12e3cc3767a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967712ba8560126f8f763bdb6be955c7e26ebca086cfdf6b441915aa0d55ce3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5350bced58914f3154ad3113637dd86ef0e9f6c17356031ce9088af42acb934(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersInvocationHttpParametersBody, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a553e210b07192e7c47af9b9041d7da5fb2ba12ff6c64c1ef48f0493749f34a9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersInvocationHttpParametersHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487f72f48efe934427e6120e5677783fd5347d44493dd4d0650c33d40dea9b98(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c308ebce2c9d6b58708b825f6179722f0273a99010430316d133f9d3b82717(
    value: typing.Optional[CloudwatchEventConnectionAuthParametersInvocationHttpParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3aa0f118229b84aba0056fdca7c68fb2b77846959212349657c8008d30a176(
    *,
    is_value_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec47210df063225f417cdfc45c40285a53149387c0aa952a9fc694a9dedb09f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7929d5407d235dd33a50feaff04ecb8cb2e69962f974d227eeac7efe630aded0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0843f8c4363b979004abc3e88a695d5e9ebc495a2cbc409dd6207a336b07bcf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6814c5c760283fb0049a9cf092e7987bb210377c3c367198a24a082a82015332(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a7ba93e05e4d1b12c55b957c72d91b408dda201453f16799c93045de9c8ae7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__426cb8eb420e2a194090170bb9005a0a57943106ea3b0f4f1db74d4c6793a0ee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ef3864fa00f6cb26c90386d662a70e5e26f16d724cddaaa8373e558f452ad0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39aae0ad56fa1d511344477b957ca67ce2cc0714db2011fc6239501a56a8ff42(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc8de544f08a2785fe1b153253d62ad01822f85ab5fcc40652f6d33a24e0e40f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__632d36574038e6dc9a50da63413f35a3acb61935a78b98bf1082a59859b02df5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e9148335f955ec813f3cf9c47396d1976c9ba2fbb605a4d3a6c1719d73200e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersInvocationHttpParametersQueryString]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15db0338d6dcbed706f173ff99420e5f65a84c2c49d011be669283d85de11590(
    *,
    authorization_endpoint: builtins.str,
    http_method: builtins.str,
    oauth_http_parameters: typing.Union[CloudwatchEventConnectionAuthParametersOauthOauthHttpParameters, typing.Dict[builtins.str, typing.Any]],
    client_parameters: typing.Optional[typing.Union[CloudwatchEventConnectionAuthParametersOauthClientParameters, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad15162c577fbf9fa7f8f76299a574c3598ca480b61fe3867e63733333d84ba9(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051548505e4c8230fab48876eb33a5b2daf898fd7994db856217d24ac4602f04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f7ee2c6f5ada95219fecef65ebe359d62a0204917eec370a476b59701a98bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40cbb688fc9566541bb930cbc8a358aa8608a8622a9f6c0f6ce2c7b2ec192836(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b29a5cca20759f79d5381df07ebd5e6e708395ef4eb0e542ac7326ea4ba11d4b(
    value: typing.Optional[CloudwatchEventConnectionAuthParametersOauthClientParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bee94363023f70c73ce3b291fd31c7ffcea7d37330ed98d9a11fb935e4041fc(
    *,
    body: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody, typing.Dict[builtins.str, typing.Any]]]]] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    query_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a1ab4cea2bbd0bf9628b2717fba4fd0ab465ec05e1c38ba98e3c8d5a9f8f129(
    *,
    is_value_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff23e026958350578bf41b11efad1a77cc9fc4cf98f143999f6348abe18af2b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f26e1538aa98df678bdcc5b88db9413b96771cdd663fe25be92fcbdf96758e0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca77790fcda9a80e8c24b7d871bc9f8b99047ba439b63f25131b6d27503622a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645b45945077f8887f003294b0a98284d4e226247da40e12663d7e17fb4d0b50(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f905c33653d1fb732af5fa92e6cbf6d74aeed335e13f850521d8aa4d78a62c15(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758e6f096089dbace1665b24271cf360f5f3c7c2e00df34c3d91a614ff8ccd5d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__197f6a9ec4b0776741f47ef0e7c22bb20fe3b612008d7d41ce36b586a7c354bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d330d72e35e46da0068e95118dfd49e23a224f3adf8cdf832a777e50dd5a8320(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92251d06ffa1fb7fecf52b0d747bafb24aed6880530a6c8a431f9dfd15c6bcc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4346d854e39cdf2e21f0d139f8b5bd0c2358e41c53352e3ac38955ff938cb84b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2c8d746db7dd52249c47456cc362f783661236849874bf9d33ce54488f7631(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4476ecc84bf8a83b0a9ddae24146f7f7d10b379df81ce7a3fd194f179c68702e(
    *,
    is_value_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f277e731f285394ff5514f2fd90d668893d5ca49cfe3223d5d33fab059c8c1b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530fb5aeb3fad58d4f9b49546abbb566729ae1bc027b3a6d67f05932e2237843(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14261dd9b0b94ac978fbd6946fb1ace1c53371fc96808559ac2471b257024446(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89557e4df47f4effa51206bb3023b9ed2a76a0bc44fdd18c203285cdec0e2041(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee114cebef8db567dc628cc86ad0dc7cf754979c985456b57a1cd2077346319(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__995afebcbd055a5271fdfac9571279a931283cb134fb4df46c8359bb66cc38a1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d678dbd7750c621b6e8acf7a0539d9e514863a4a43dd4fa494c7280a36719cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc5f4516e81b94856c20f584cb680f443f3de40d698d64ecdf68e3afe1b4011(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d97ea26362def766017d520fd42275378829f5650d08ab2bb4ab592f094787a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b507839db61854b881ed72a4758dd6aeafec503d4c849b7476fc91fb181a531a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46feddaef4306d2c79a10dec4cda64bf1c0bb3990757de0d1d4ac1edd15a408e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__800b6a066fc82b9fb87df4d0fb9c9e9b80ccaa3c2d9a41d4844d20e37818c3f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df834c87e25b03e52ecc88f2248e20f9c97c2f0de391f48dc02930e6e6894387(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersBody, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ccc8983250dc46990f6e40f2693e95dfc738af57cc9144f4eef47f563cfd129(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ecfea78fe8ba2fdd926c923cae62f46e5b93a81b388df1856f603f08abad6f6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf739a1b24f4e748f51554f4b00470816451bbc86a791cfd6c4fe9ea723101e(
    value: typing.Optional[CloudwatchEventConnectionAuthParametersOauthOauthHttpParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2addeabac918f745c395151ad8e11260c5354a3c18dd06ac8683c196b3919d01(
    *,
    is_value_secret: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb45b4598eb90f4a948f5b63811d21c896fd35ed99ed48fb684a0a40bf031a75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc70db856af1a5df244bee1759d27b0232813f6582350bcc58f8e33080100b7e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d81a434e108127140fcb6f81b6458e2c37a5ffd4a56f6a0470b73dd0719bb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c589897b6de6c019590bcde06c89e3ad2c19382031132e8b2873188cf7e0806(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9011465a0deeea64d1a7955251d6a8db53b64721ba542e10ebc32acf6b1fdd3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d1851323d3f33d52c6372a14e5cfb850f8fdd50ed21a25eda956356a044942(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e19cf798381d96ffc177a67e47d719cdaa5a2a18926ec2773681e581373a46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0739c244a0a9e9d0bf6593a9294742e8fbbf1d1f10c6eff03706bebf15100500(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d4ef4346a599d66983c2623aa198eeed461f1018ce0e166a11cdfef83aebac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a0fbb23a8eb29cd65486c26c398a13ff5a02686995fee1d4e3690d00ad6932(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab22f6d6cd0a5cf1abe4d60ac46ec39b9bd3f1cd3ed6623a72eb257667b465f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudwatchEventConnectionAuthParametersOauthOauthHttpParametersQueryString]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__293b906b1399f5bcbb9adee3866a6c0e098d82f554da81cdab429beb282b117c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa08a50aec89ff37ceebc8d81a4e633ad2a865712100b892928e202b40b49e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712af95004a8ddb4a24c455e568fa9ec73fedb83138473f28fb7b6e145ea9336(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d4d4cc6e269f41caa044ad89758084e4dded0a26f74babda814df4f87ed7a8a(
    value: typing.Optional[CloudwatchEventConnectionAuthParametersOauth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e2e241dfd60cc7a7b2400d9a1f6b59f49cf05545ba7469a608adc55e8522ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18117d155ffac0ec4a935b331f9ce007de44d71591b625b9936b10c40c63e4fa(
    value: typing.Optional[CloudwatchEventConnectionAuthParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab0d59891f12534a81adf15048a397646e207d6272bba9d943e765896fb3352(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    authorization_type: builtins.str,
    auth_parameters: typing.Union[CloudwatchEventConnectionAuthParameters, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    invocation_connectivity_parameters: typing.Optional[typing.Union[CloudwatchEventConnectionInvocationConnectivityParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    kms_key_identifier: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16ba1d5bfa7f128091ac5d70ac6561d21fd4ffa71cf8a5cf3951fccf2c29b740(
    *,
    resource_parameters: typing.Union[CloudwatchEventConnectionInvocationConnectivityParametersResourceParameters, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc5a9af169335941183093a9cb805e5d0b1b9e187ebe6b6abb848edca89aef39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__143306344b33f217cec1d072a1de59bebbdbfa64521e11ad391d8aadfbf73502(
    value: typing.Optional[CloudwatchEventConnectionInvocationConnectivityParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f11129d787443ecf252b7d9d7d03cbdfb51f38f5759a92b7f65a75d69e4532f5(
    *,
    resource_configuration_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e8991d922dbeb1a0095a8d59bb140a4e3dbf5069f5c7566ec52de4a1a70070(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d35cb985df5180ae116292a6d46bcc3028c22598f90211727b12538199374a13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02840b46ff18f37b4fcf09e0e8236774719dac9ea3123bf5fbd4dcc4ed833283(
    value: typing.Optional[CloudwatchEventConnectionInvocationConnectivityParametersResourceParameters],
) -> None:
    """Type checking stubs"""
    pass
