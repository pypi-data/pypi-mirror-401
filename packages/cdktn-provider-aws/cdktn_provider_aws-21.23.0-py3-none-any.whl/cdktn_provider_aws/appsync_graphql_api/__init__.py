r'''
# `aws_appsync_graphql_api`

Refer to the Terraform Registry for docs: [`aws_appsync_graphql_api`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api).
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


class AppsyncGraphqlApi(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApi",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api aws_appsync_graphql_api}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        authentication_type: builtins.str,
        name: builtins.str,
        additional_authentication_provider: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncGraphqlApiAdditionalAuthenticationProvider", typing.Dict[builtins.str, typing.Any]]]]] = None,
        api_type: typing.Optional[builtins.str] = None,
        enhanced_metrics_config: typing.Optional[typing.Union["AppsyncGraphqlApiEnhancedMetricsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        introspection_config: typing.Optional[builtins.str] = None,
        lambda_authorizer_config: typing.Optional[typing.Union["AppsyncGraphqlApiLambdaAuthorizerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        log_config: typing.Optional[typing.Union["AppsyncGraphqlApiLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        merged_api_execution_role_arn: typing.Optional[builtins.str] = None,
        openid_connect_config: typing.Optional[typing.Union["AppsyncGraphqlApiOpenidConnectConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        query_depth_limit: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        resolver_count_limit: typing.Optional[jsii.Number] = None,
        schema: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        user_pool_config: typing.Optional[typing.Union["AppsyncGraphqlApiUserPoolConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        visibility: typing.Optional[builtins.str] = None,
        xray_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api aws_appsync_graphql_api} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#authentication_type AppsyncGraphqlApi#authentication_type}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#name AppsyncGraphqlApi#name}.
        :param additional_authentication_provider: additional_authentication_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#additional_authentication_provider AppsyncGraphqlApi#additional_authentication_provider}
        :param api_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#api_type AppsyncGraphqlApi#api_type}.
        :param enhanced_metrics_config: enhanced_metrics_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#enhanced_metrics_config AppsyncGraphqlApi#enhanced_metrics_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#id AppsyncGraphqlApi#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param introspection_config: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#introspection_config AppsyncGraphqlApi#introspection_config}.
        :param lambda_authorizer_config: lambda_authorizer_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#lambda_authorizer_config AppsyncGraphqlApi#lambda_authorizer_config}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#log_config AppsyncGraphqlApi#log_config}
        :param merged_api_execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#merged_api_execution_role_arn AppsyncGraphqlApi#merged_api_execution_role_arn}.
        :param openid_connect_config: openid_connect_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#openid_connect_config AppsyncGraphqlApi#openid_connect_config}
        :param query_depth_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#query_depth_limit AppsyncGraphqlApi#query_depth_limit}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#region AppsyncGraphqlApi#region}
        :param resolver_count_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#resolver_count_limit AppsyncGraphqlApi#resolver_count_limit}.
        :param schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#schema AppsyncGraphqlApi#schema}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#tags AppsyncGraphqlApi#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#tags_all AppsyncGraphqlApi#tags_all}.
        :param user_pool_config: user_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#user_pool_config AppsyncGraphqlApi#user_pool_config}
        :param visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#visibility AppsyncGraphqlApi#visibility}.
        :param xray_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#xray_enabled AppsyncGraphqlApi#xray_enabled}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc9175da39096934ba7623d1c246b4ec73608c6b36c3249181dda3e2f2b0ff09)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppsyncGraphqlApiConfig(
            authentication_type=authentication_type,
            name=name,
            additional_authentication_provider=additional_authentication_provider,
            api_type=api_type,
            enhanced_metrics_config=enhanced_metrics_config,
            id=id,
            introspection_config=introspection_config,
            lambda_authorizer_config=lambda_authorizer_config,
            log_config=log_config,
            merged_api_execution_role_arn=merged_api_execution_role_arn,
            openid_connect_config=openid_connect_config,
            query_depth_limit=query_depth_limit,
            region=region,
            resolver_count_limit=resolver_count_limit,
            schema=schema,
            tags=tags,
            tags_all=tags_all,
            user_pool_config=user_pool_config,
            visibility=visibility,
            xray_enabled=xray_enabled,
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
        '''Generates CDKTF code for importing a AppsyncGraphqlApi resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AppsyncGraphqlApi to import.
        :param import_from_id: The id of the existing AppsyncGraphqlApi that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AppsyncGraphqlApi to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0639819eb56169019ce7509b0c9082ba7ef3209285ff0b2f8e4b115684808fa1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdditionalAuthenticationProvider")
    def put_additional_authentication_provider(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsyncGraphqlApiAdditionalAuthenticationProvider", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__601d2d542c2b0292524707b9183d28c2f07980200568a769c0db6fc77232356f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalAuthenticationProvider", [value]))

    @jsii.member(jsii_name="putEnhancedMetricsConfig")
    def put_enhanced_metrics_config(
        self,
        *,
        data_source_level_metrics_behavior: builtins.str,
        operation_level_metrics_config: builtins.str,
        resolver_level_metrics_behavior: builtins.str,
    ) -> None:
        '''
        :param data_source_level_metrics_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#data_source_level_metrics_behavior AppsyncGraphqlApi#data_source_level_metrics_behavior}.
        :param operation_level_metrics_config: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#operation_level_metrics_config AppsyncGraphqlApi#operation_level_metrics_config}.
        :param resolver_level_metrics_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#resolver_level_metrics_behavior AppsyncGraphqlApi#resolver_level_metrics_behavior}.
        '''
        value = AppsyncGraphqlApiEnhancedMetricsConfig(
            data_source_level_metrics_behavior=data_source_level_metrics_behavior,
            operation_level_metrics_config=operation_level_metrics_config,
            resolver_level_metrics_behavior=resolver_level_metrics_behavior,
        )

        return typing.cast(None, jsii.invoke(self, "putEnhancedMetricsConfig", [value]))

    @jsii.member(jsii_name="putLambdaAuthorizerConfig")
    def put_lambda_authorizer_config(
        self,
        *,
        authorizer_uri: builtins.str,
        authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number] = None,
        identity_validation_expression: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#authorizer_uri AppsyncGraphqlApi#authorizer_uri}.
        :param authorizer_result_ttl_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#authorizer_result_ttl_in_seconds AppsyncGraphqlApi#authorizer_result_ttl_in_seconds}.
        :param identity_validation_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#identity_validation_expression AppsyncGraphqlApi#identity_validation_expression}.
        '''
        value = AppsyncGraphqlApiLambdaAuthorizerConfig(
            authorizer_uri=authorizer_uri,
            authorizer_result_ttl_in_seconds=authorizer_result_ttl_in_seconds,
            identity_validation_expression=identity_validation_expression,
        )

        return typing.cast(None, jsii.invoke(self, "putLambdaAuthorizerConfig", [value]))

    @jsii.member(jsii_name="putLogConfig")
    def put_log_config(
        self,
        *,
        cloudwatch_logs_role_arn: builtins.str,
        field_log_level: builtins.str,
        exclude_verbose_content: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cloudwatch_logs_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#cloudwatch_logs_role_arn AppsyncGraphqlApi#cloudwatch_logs_role_arn}.
        :param field_log_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#field_log_level AppsyncGraphqlApi#field_log_level}.
        :param exclude_verbose_content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#exclude_verbose_content AppsyncGraphqlApi#exclude_verbose_content}.
        '''
        value = AppsyncGraphqlApiLogConfig(
            cloudwatch_logs_role_arn=cloudwatch_logs_role_arn,
            field_log_level=field_log_level,
            exclude_verbose_content=exclude_verbose_content,
        )

        return typing.cast(None, jsii.invoke(self, "putLogConfig", [value]))

    @jsii.member(jsii_name="putOpenidConnectConfig")
    def put_openid_connect_config(
        self,
        *,
        issuer: builtins.str,
        auth_ttl: typing.Optional[jsii.Number] = None,
        client_id: typing.Optional[builtins.str] = None,
        iat_ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param issuer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#issuer AppsyncGraphqlApi#issuer}.
        :param auth_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#auth_ttl AppsyncGraphqlApi#auth_ttl}.
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#client_id AppsyncGraphqlApi#client_id}.
        :param iat_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#iat_ttl AppsyncGraphqlApi#iat_ttl}.
        '''
        value = AppsyncGraphqlApiOpenidConnectConfig(
            issuer=issuer, auth_ttl=auth_ttl, client_id=client_id, iat_ttl=iat_ttl
        )

        return typing.cast(None, jsii.invoke(self, "putOpenidConnectConfig", [value]))

    @jsii.member(jsii_name="putUserPoolConfig")
    def put_user_pool_config(
        self,
        *,
        default_action: builtins.str,
        user_pool_id: builtins.str,
        app_id_client_regex: typing.Optional[builtins.str] = None,
        aws_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#default_action AppsyncGraphqlApi#default_action}.
        :param user_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#user_pool_id AppsyncGraphqlApi#user_pool_id}.
        :param app_id_client_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#app_id_client_regex AppsyncGraphqlApi#app_id_client_regex}.
        :param aws_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#aws_region AppsyncGraphqlApi#aws_region}.
        '''
        value = AppsyncGraphqlApiUserPoolConfig(
            default_action=default_action,
            user_pool_id=user_pool_id,
            app_id_client_regex=app_id_client_regex,
            aws_region=aws_region,
        )

        return typing.cast(None, jsii.invoke(self, "putUserPoolConfig", [value]))

    @jsii.member(jsii_name="resetAdditionalAuthenticationProvider")
    def reset_additional_authentication_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalAuthenticationProvider", []))

    @jsii.member(jsii_name="resetApiType")
    def reset_api_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiType", []))

    @jsii.member(jsii_name="resetEnhancedMetricsConfig")
    def reset_enhanced_metrics_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnhancedMetricsConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIntrospectionConfig")
    def reset_introspection_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntrospectionConfig", []))

    @jsii.member(jsii_name="resetLambdaAuthorizerConfig")
    def reset_lambda_authorizer_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaAuthorizerConfig", []))

    @jsii.member(jsii_name="resetLogConfig")
    def reset_log_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogConfig", []))

    @jsii.member(jsii_name="resetMergedApiExecutionRoleArn")
    def reset_merged_api_execution_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergedApiExecutionRoleArn", []))

    @jsii.member(jsii_name="resetOpenidConnectConfig")
    def reset_openid_connect_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOpenidConnectConfig", []))

    @jsii.member(jsii_name="resetQueryDepthLimit")
    def reset_query_depth_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryDepthLimit", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetResolverCountLimit")
    def reset_resolver_count_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResolverCountLimit", []))

    @jsii.member(jsii_name="resetSchema")
    def reset_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchema", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetUserPoolConfig")
    def reset_user_pool_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserPoolConfig", []))

    @jsii.member(jsii_name="resetVisibility")
    def reset_visibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisibility", []))

    @jsii.member(jsii_name="resetXrayEnabled")
    def reset_xray_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXrayEnabled", []))

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
    @jsii.member(jsii_name="additionalAuthenticationProvider")
    def additional_authentication_provider(
        self,
    ) -> "AppsyncGraphqlApiAdditionalAuthenticationProviderList":
        return typing.cast("AppsyncGraphqlApiAdditionalAuthenticationProviderList", jsii.get(self, "additionalAuthenticationProvider"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="enhancedMetricsConfig")
    def enhanced_metrics_config(
        self,
    ) -> "AppsyncGraphqlApiEnhancedMetricsConfigOutputReference":
        return typing.cast("AppsyncGraphqlApiEnhancedMetricsConfigOutputReference", jsii.get(self, "enhancedMetricsConfig"))

    @builtins.property
    @jsii.member(jsii_name="lambdaAuthorizerConfig")
    def lambda_authorizer_config(
        self,
    ) -> "AppsyncGraphqlApiLambdaAuthorizerConfigOutputReference":
        return typing.cast("AppsyncGraphqlApiLambdaAuthorizerConfigOutputReference", jsii.get(self, "lambdaAuthorizerConfig"))

    @builtins.property
    @jsii.member(jsii_name="logConfig")
    def log_config(self) -> "AppsyncGraphqlApiLogConfigOutputReference":
        return typing.cast("AppsyncGraphqlApiLogConfigOutputReference", jsii.get(self, "logConfig"))

    @builtins.property
    @jsii.member(jsii_name="openidConnectConfig")
    def openid_connect_config(
        self,
    ) -> "AppsyncGraphqlApiOpenidConnectConfigOutputReference":
        return typing.cast("AppsyncGraphqlApiOpenidConnectConfigOutputReference", jsii.get(self, "openidConnectConfig"))

    @builtins.property
    @jsii.member(jsii_name="uris")
    def uris(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "uris"))

    @builtins.property
    @jsii.member(jsii_name="userPoolConfig")
    def user_pool_config(self) -> "AppsyncGraphqlApiUserPoolConfigOutputReference":
        return typing.cast("AppsyncGraphqlApiUserPoolConfigOutputReference", jsii.get(self, "userPoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="additionalAuthenticationProviderInput")
    def additional_authentication_provider_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncGraphqlApiAdditionalAuthenticationProvider"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsyncGraphqlApiAdditionalAuthenticationProvider"]]], jsii.get(self, "additionalAuthenticationProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="apiTypeInput")
    def api_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationTypeInput")
    def authentication_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="enhancedMetricsConfigInput")
    def enhanced_metrics_config_input(
        self,
    ) -> typing.Optional["AppsyncGraphqlApiEnhancedMetricsConfig"]:
        return typing.cast(typing.Optional["AppsyncGraphqlApiEnhancedMetricsConfig"], jsii.get(self, "enhancedMetricsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="introspectionConfigInput")
    def introspection_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "introspectionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaAuthorizerConfigInput")
    def lambda_authorizer_config_input(
        self,
    ) -> typing.Optional["AppsyncGraphqlApiLambdaAuthorizerConfig"]:
        return typing.cast(typing.Optional["AppsyncGraphqlApiLambdaAuthorizerConfig"], jsii.get(self, "lambdaAuthorizerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="logConfigInput")
    def log_config_input(self) -> typing.Optional["AppsyncGraphqlApiLogConfig"]:
        return typing.cast(typing.Optional["AppsyncGraphqlApiLogConfig"], jsii.get(self, "logConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="mergedApiExecutionRoleArnInput")
    def merged_api_execution_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mergedApiExecutionRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="openidConnectConfigInput")
    def openid_connect_config_input(
        self,
    ) -> typing.Optional["AppsyncGraphqlApiOpenidConnectConfig"]:
        return typing.cast(typing.Optional["AppsyncGraphqlApiOpenidConnectConfig"], jsii.get(self, "openidConnectConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="queryDepthLimitInput")
    def query_depth_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "queryDepthLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="resolverCountLimitInput")
    def resolver_count_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "resolverCountLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

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
    @jsii.member(jsii_name="userPoolConfigInput")
    def user_pool_config_input(
        self,
    ) -> typing.Optional["AppsyncGraphqlApiUserPoolConfig"]:
        return typing.cast(typing.Optional["AppsyncGraphqlApiUserPoolConfig"], jsii.get(self, "userPoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="visibilityInput")
    def visibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="xrayEnabledInput")
    def xray_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "xrayEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="apiType")
    def api_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiType"))

    @api_type.setter
    def api_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d400a06d8bb56cbdf7987121c3daa9130e81545889a129b4152b7b99cbe2375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authenticationType")
    def authentication_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationType"))

    @authentication_type.setter
    def authentication_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7753ca040691a60a2a102926160b546d17062b5cf4624ec4b6cd3ff360e4fdca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ffec4f2205b37bf274138a2271c58239ae2377ed3f40a1a5dc44d3f7a793f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="introspectionConfig")
    def introspection_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "introspectionConfig"))

    @introspection_config.setter
    def introspection_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3799196a3b35809f1b50f77da73fe59fd48770f0d3c0e1ca6569f4fa0c6ac11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "introspectionConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mergedApiExecutionRoleArn")
    def merged_api_execution_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mergedApiExecutionRoleArn"))

    @merged_api_execution_role_arn.setter
    def merged_api_execution_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc7900583a37d016079026ef79e4232efdef6ef4d3c0708ad8bcf8454f8a910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mergedApiExecutionRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c5d4acb3fa816800e413e87e45d56df530468caa04a4e187a8a1b2a26c60298)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryDepthLimit")
    def query_depth_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queryDepthLimit"))

    @query_depth_limit.setter
    def query_depth_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea15b73e22539a888b03da8b7daa027987dd0289ca48f8c34c2c56f1c1923d61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryDepthLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4bc9942e1f9ce19411d61df895b262fd10c0a5f7de004e1443c72f9c1999d0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resolverCountLimit")
    def resolver_count_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "resolverCountLimit"))

    @resolver_count_limit.setter
    def resolver_count_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3412c48ec591fcff6c2e395211694fce13d15a85e9018d6eaf86ad7c8b103f46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resolverCountLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0bf62a5f6411ae3d80f5d1ff0e89743e3e46ec802c96b90aecde144aec8bdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__533d8a36a26d2c6454dc5ccd09caf02419993df232bee2986f8aed0f26e6f1d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c951b0ecc58a915b8084f36db34619232bf3d342ab831f74f959c5808d91fb54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibility")
    def visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibility"))

    @visibility.setter
    def visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7fe64ccfd886823556bbf86ecc904b25b48a4c058e41cb592cc08175609f851)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibility", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="xrayEnabled")
    def xray_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "xrayEnabled"))

    @xray_enabled.setter
    def xray_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__271bb52fb0734623121f640f8b30f134a8a46e9a5a718e6b24849672f495b40c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xrayEnabled", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApiAdditionalAuthenticationProvider",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_type": "authenticationType",
        "lambda_authorizer_config": "lambdaAuthorizerConfig",
        "openid_connect_config": "openidConnectConfig",
        "user_pool_config": "userPoolConfig",
    },
)
class AppsyncGraphqlApiAdditionalAuthenticationProvider:
    def __init__(
        self,
        *,
        authentication_type: builtins.str,
        lambda_authorizer_config: typing.Optional[typing.Union["AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        openid_connect_config: typing.Optional[typing.Union["AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        user_pool_config: typing.Optional[typing.Union["AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#authentication_type AppsyncGraphqlApi#authentication_type}.
        :param lambda_authorizer_config: lambda_authorizer_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#lambda_authorizer_config AppsyncGraphqlApi#lambda_authorizer_config}
        :param openid_connect_config: openid_connect_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#openid_connect_config AppsyncGraphqlApi#openid_connect_config}
        :param user_pool_config: user_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#user_pool_config AppsyncGraphqlApi#user_pool_config}
        '''
        if isinstance(lambda_authorizer_config, dict):
            lambda_authorizer_config = AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfig(**lambda_authorizer_config)
        if isinstance(openid_connect_config, dict):
            openid_connect_config = AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfig(**openid_connect_config)
        if isinstance(user_pool_config, dict):
            user_pool_config = AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfig(**user_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fb3399357ffec344794abda81c2e3ff520af237da5fe50bb0ac06ceb7357049)
            check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            check_type(argname="argument lambda_authorizer_config", value=lambda_authorizer_config, expected_type=type_hints["lambda_authorizer_config"])
            check_type(argname="argument openid_connect_config", value=openid_connect_config, expected_type=type_hints["openid_connect_config"])
            check_type(argname="argument user_pool_config", value=user_pool_config, expected_type=type_hints["user_pool_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authentication_type": authentication_type,
        }
        if lambda_authorizer_config is not None:
            self._values["lambda_authorizer_config"] = lambda_authorizer_config
        if openid_connect_config is not None:
            self._values["openid_connect_config"] = openid_connect_config
        if user_pool_config is not None:
            self._values["user_pool_config"] = user_pool_config

    @builtins.property
    def authentication_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#authentication_type AppsyncGraphqlApi#authentication_type}.'''
        result = self._values.get("authentication_type")
        assert result is not None, "Required property 'authentication_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lambda_authorizer_config(
        self,
    ) -> typing.Optional["AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfig"]:
        '''lambda_authorizer_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#lambda_authorizer_config AppsyncGraphqlApi#lambda_authorizer_config}
        '''
        result = self._values.get("lambda_authorizer_config")
        return typing.cast(typing.Optional["AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfig"], result)

    @builtins.property
    def openid_connect_config(
        self,
    ) -> typing.Optional["AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfig"]:
        '''openid_connect_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#openid_connect_config AppsyncGraphqlApi#openid_connect_config}
        '''
        result = self._values.get("openid_connect_config")
        return typing.cast(typing.Optional["AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfig"], result)

    @builtins.property
    def user_pool_config(
        self,
    ) -> typing.Optional["AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfig"]:
        '''user_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#user_pool_config AppsyncGraphqlApi#user_pool_config}
        '''
        result = self._values.get("user_pool_config")
        return typing.cast(typing.Optional["AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncGraphqlApiAdditionalAuthenticationProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "authorizer_uri": "authorizerUri",
        "authorizer_result_ttl_in_seconds": "authorizerResultTtlInSeconds",
        "identity_validation_expression": "identityValidationExpression",
    },
)
class AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfig:
    def __init__(
        self,
        *,
        authorizer_uri: builtins.str,
        authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number] = None,
        identity_validation_expression: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#authorizer_uri AppsyncGraphqlApi#authorizer_uri}.
        :param authorizer_result_ttl_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#authorizer_result_ttl_in_seconds AppsyncGraphqlApi#authorizer_result_ttl_in_seconds}.
        :param identity_validation_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#identity_validation_expression AppsyncGraphqlApi#identity_validation_expression}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bc8abac4127d95b7620ff5b62e3bb46b4a6adc31e008de5a8a0850929eb365e)
            check_type(argname="argument authorizer_uri", value=authorizer_uri, expected_type=type_hints["authorizer_uri"])
            check_type(argname="argument authorizer_result_ttl_in_seconds", value=authorizer_result_ttl_in_seconds, expected_type=type_hints["authorizer_result_ttl_in_seconds"])
            check_type(argname="argument identity_validation_expression", value=identity_validation_expression, expected_type=type_hints["identity_validation_expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorizer_uri": authorizer_uri,
        }
        if authorizer_result_ttl_in_seconds is not None:
            self._values["authorizer_result_ttl_in_seconds"] = authorizer_result_ttl_in_seconds
        if identity_validation_expression is not None:
            self._values["identity_validation_expression"] = identity_validation_expression

    @builtins.property
    def authorizer_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#authorizer_uri AppsyncGraphqlApi#authorizer_uri}.'''
        result = self._values.get("authorizer_uri")
        assert result is not None, "Required property 'authorizer_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorizer_result_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#authorizer_result_ttl_in_seconds AppsyncGraphqlApi#authorizer_result_ttl_in_seconds}.'''
        result = self._values.get("authorizer_result_ttl_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def identity_validation_expression(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#identity_validation_expression AppsyncGraphqlApi#identity_validation_expression}.'''
        result = self._values.get("identity_validation_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cfb7bf8a111167389ca38ae3be7cf5b152df8c4405b735df0e37dd7241f8bd8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthorizerResultTtlInSeconds")
    def reset_authorizer_result_ttl_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizerResultTtlInSeconds", []))

    @jsii.member(jsii_name="resetIdentityValidationExpression")
    def reset_identity_validation_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityValidationExpression", []))

    @builtins.property
    @jsii.member(jsii_name="authorizerResultTtlInSecondsInput")
    def authorizer_result_ttl_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "authorizerResultTtlInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizerUriInput")
    def authorizer_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizerUriInput"))

    @builtins.property
    @jsii.member(jsii_name="identityValidationExpressionInput")
    def identity_validation_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityValidationExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizerResultTtlInSeconds")
    def authorizer_result_ttl_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "authorizerResultTtlInSeconds"))

    @authorizer_result_ttl_in_seconds.setter
    def authorizer_result_ttl_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2053cec2ea5d89b2e1b10c078e48b8193dff52fd85c2b38130e72165e176d09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizerResultTtlInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authorizerUri")
    def authorizer_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizerUri"))

    @authorizer_uri.setter
    def authorizer_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7050244d36d193089ce6dcf75d87e7b05c8fe9a62eee195b3d4876380d4170be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizerUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityValidationExpression")
    def identity_validation_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityValidationExpression"))

    @identity_validation_expression.setter
    def identity_validation_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1126386fe269b64ab1b49326ab255d871c5e12a56dd36f13e76515e4cd7fef3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityValidationExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfig]:
        return typing.cast(typing.Optional[AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__906dc42286129bf9c874cf8eaddfd1114d45f9e905031b462362110868e9074e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncGraphqlApiAdditionalAuthenticationProviderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApiAdditionalAuthenticationProviderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2761a28b256e4d16850ac34f10d5fda435171a2942a7f7b5b19229f0b3e5e97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppsyncGraphqlApiAdditionalAuthenticationProviderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1f44cfb906117db79a2209b915b0f118335737570dffc4cd16808bc71d11775)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsyncGraphqlApiAdditionalAuthenticationProviderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d742fb2ba54a34ce5bd947914c43df1989ace0af6b2253b52db0f7e6a2b0bfd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbbc7f3967bb7a408330f3b679d46cb5d6a658ec831316138781a52843f020ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07d39385df4cfa9a61988b8cc1bde38d2dede8898eec720df1a8ade640a050bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncGraphqlApiAdditionalAuthenticationProvider]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncGraphqlApiAdditionalAuthenticationProvider]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncGraphqlApiAdditionalAuthenticationProvider]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba7c834efc22b2f4c10eb06f5de41a1f764eb0e3b1f036407f598daeb068c9e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfig",
    jsii_struct_bases=[],
    name_mapping={
        "issuer": "issuer",
        "auth_ttl": "authTtl",
        "client_id": "clientId",
        "iat_ttl": "iatTtl",
    },
)
class AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfig:
    def __init__(
        self,
        *,
        issuer: builtins.str,
        auth_ttl: typing.Optional[jsii.Number] = None,
        client_id: typing.Optional[builtins.str] = None,
        iat_ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param issuer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#issuer AppsyncGraphqlApi#issuer}.
        :param auth_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#auth_ttl AppsyncGraphqlApi#auth_ttl}.
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#client_id AppsyncGraphqlApi#client_id}.
        :param iat_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#iat_ttl AppsyncGraphqlApi#iat_ttl}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c123de334fd1608a6abab54a3a969f17a0d6928b70a4f9fd676c247afb936004)
            check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            check_type(argname="argument auth_ttl", value=auth_ttl, expected_type=type_hints["auth_ttl"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument iat_ttl", value=iat_ttl, expected_type=type_hints["iat_ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "issuer": issuer,
        }
        if auth_ttl is not None:
            self._values["auth_ttl"] = auth_ttl
        if client_id is not None:
            self._values["client_id"] = client_id
        if iat_ttl is not None:
            self._values["iat_ttl"] = iat_ttl

    @builtins.property
    def issuer(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#issuer AppsyncGraphqlApi#issuer}.'''
        result = self._values.get("issuer")
        assert result is not None, "Required property 'issuer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#auth_ttl AppsyncGraphqlApi#auth_ttl}.'''
        result = self._values.get("auth_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#client_id AppsyncGraphqlApi#client_id}.'''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iat_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#iat_ttl AppsyncGraphqlApi#iat_ttl}.'''
        result = self._values.get("iat_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95deaec752f9f8c8f73257a22e49a5fe42a61b4a193b1dd3aec464ff87ab9e2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthTtl")
    def reset_auth_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthTtl", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetIatTtl")
    def reset_iat_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIatTtl", []))

    @builtins.property
    @jsii.member(jsii_name="authTtlInput")
    def auth_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "authTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="iatTtlInput")
    def iat_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "iatTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerInput")
    def issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerInput"))

    @builtins.property
    @jsii.member(jsii_name="authTtl")
    def auth_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "authTtl"))

    @auth_ttl.setter
    def auth_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e1f6a6a0dd53e872a227aeed7ea8d0ccd89f17aed2ddd2cc68981b899fbceba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bf18d88a15033601df50845352ae2dfc42945ddceb0336b1744a13dfbfa754a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iatTtl")
    def iat_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "iatTtl"))

    @iat_ttl.setter
    def iat_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d89016c2ce303acf59e278296049837aefc9600b88f6847f2d496693a5e75a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iatTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2530dbd35c1d7133e2e2da2f8835dd26c7ef7b4f0821fb42712749949328855d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfig]:
        return typing.cast(typing.Optional[AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec5156af47305f9028dc8c4fe17f33c6ad2121ea1e735d0e60d16ad2254fda25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncGraphqlApiAdditionalAuthenticationProviderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApiAdditionalAuthenticationProviderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d8671e2d9d4cdd87a3570bfee85508ef3622e873033b1f49b23ae089c3d70cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putLambdaAuthorizerConfig")
    def put_lambda_authorizer_config(
        self,
        *,
        authorizer_uri: builtins.str,
        authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number] = None,
        identity_validation_expression: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#authorizer_uri AppsyncGraphqlApi#authorizer_uri}.
        :param authorizer_result_ttl_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#authorizer_result_ttl_in_seconds AppsyncGraphqlApi#authorizer_result_ttl_in_seconds}.
        :param identity_validation_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#identity_validation_expression AppsyncGraphqlApi#identity_validation_expression}.
        '''
        value = AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfig(
            authorizer_uri=authorizer_uri,
            authorizer_result_ttl_in_seconds=authorizer_result_ttl_in_seconds,
            identity_validation_expression=identity_validation_expression,
        )

        return typing.cast(None, jsii.invoke(self, "putLambdaAuthorizerConfig", [value]))

    @jsii.member(jsii_name="putOpenidConnectConfig")
    def put_openid_connect_config(
        self,
        *,
        issuer: builtins.str,
        auth_ttl: typing.Optional[jsii.Number] = None,
        client_id: typing.Optional[builtins.str] = None,
        iat_ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param issuer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#issuer AppsyncGraphqlApi#issuer}.
        :param auth_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#auth_ttl AppsyncGraphqlApi#auth_ttl}.
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#client_id AppsyncGraphqlApi#client_id}.
        :param iat_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#iat_ttl AppsyncGraphqlApi#iat_ttl}.
        '''
        value = AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfig(
            issuer=issuer, auth_ttl=auth_ttl, client_id=client_id, iat_ttl=iat_ttl
        )

        return typing.cast(None, jsii.invoke(self, "putOpenidConnectConfig", [value]))

    @jsii.member(jsii_name="putUserPoolConfig")
    def put_user_pool_config(
        self,
        *,
        user_pool_id: builtins.str,
        app_id_client_regex: typing.Optional[builtins.str] = None,
        aws_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param user_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#user_pool_id AppsyncGraphqlApi#user_pool_id}.
        :param app_id_client_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#app_id_client_regex AppsyncGraphqlApi#app_id_client_regex}.
        :param aws_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#aws_region AppsyncGraphqlApi#aws_region}.
        '''
        value = AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfig(
            user_pool_id=user_pool_id,
            app_id_client_regex=app_id_client_regex,
            aws_region=aws_region,
        )

        return typing.cast(None, jsii.invoke(self, "putUserPoolConfig", [value]))

    @jsii.member(jsii_name="resetLambdaAuthorizerConfig")
    def reset_lambda_authorizer_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaAuthorizerConfig", []))

    @jsii.member(jsii_name="resetOpenidConnectConfig")
    def reset_openid_connect_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOpenidConnectConfig", []))

    @jsii.member(jsii_name="resetUserPoolConfig")
    def reset_user_pool_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserPoolConfig", []))

    @builtins.property
    @jsii.member(jsii_name="lambdaAuthorizerConfig")
    def lambda_authorizer_config(
        self,
    ) -> AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfigOutputReference:
        return typing.cast(AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfigOutputReference, jsii.get(self, "lambdaAuthorizerConfig"))

    @builtins.property
    @jsii.member(jsii_name="openidConnectConfig")
    def openid_connect_config(
        self,
    ) -> AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfigOutputReference:
        return typing.cast(AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfigOutputReference, jsii.get(self, "openidConnectConfig"))

    @builtins.property
    @jsii.member(jsii_name="userPoolConfig")
    def user_pool_config(
        self,
    ) -> "AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfigOutputReference":
        return typing.cast("AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfigOutputReference", jsii.get(self, "userPoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="authenticationTypeInput")
    def authentication_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaAuthorizerConfigInput")
    def lambda_authorizer_config_input(
        self,
    ) -> typing.Optional[AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfig]:
        return typing.cast(typing.Optional[AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfig], jsii.get(self, "lambdaAuthorizerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="openidConnectConfigInput")
    def openid_connect_config_input(
        self,
    ) -> typing.Optional[AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfig]:
        return typing.cast(typing.Optional[AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfig], jsii.get(self, "openidConnectConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="userPoolConfigInput")
    def user_pool_config_input(
        self,
    ) -> typing.Optional["AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfig"]:
        return typing.cast(typing.Optional["AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfig"], jsii.get(self, "userPoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationType")
    def authentication_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationType"))

    @authentication_type.setter
    def authentication_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ca33bda24f222c46fba24fe6f662a7d6971c5cbc4809269fb90ef6ffc09dc22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncGraphqlApiAdditionalAuthenticationProvider]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncGraphqlApiAdditionalAuthenticationProvider]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncGraphqlApiAdditionalAuthenticationProvider]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc9b4c054bae79a064540a9d7649799ef39dede4ce3d43b7a80bd95034fd532)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfig",
    jsii_struct_bases=[],
    name_mapping={
        "user_pool_id": "userPoolId",
        "app_id_client_regex": "appIdClientRegex",
        "aws_region": "awsRegion",
    },
)
class AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfig:
    def __init__(
        self,
        *,
        user_pool_id: builtins.str,
        app_id_client_regex: typing.Optional[builtins.str] = None,
        aws_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param user_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#user_pool_id AppsyncGraphqlApi#user_pool_id}.
        :param app_id_client_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#app_id_client_regex AppsyncGraphqlApi#app_id_client_regex}.
        :param aws_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#aws_region AppsyncGraphqlApi#aws_region}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef1e17be9218493429f6dfec52c900de16b832effc837589b0b0ac4dc8fa9dfe)
            check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
            check_type(argname="argument app_id_client_regex", value=app_id_client_regex, expected_type=type_hints["app_id_client_regex"])
            check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_pool_id": user_pool_id,
        }
        if app_id_client_regex is not None:
            self._values["app_id_client_regex"] = app_id_client_regex
        if aws_region is not None:
            self._values["aws_region"] = aws_region

    @builtins.property
    def user_pool_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#user_pool_id AppsyncGraphqlApi#user_pool_id}.'''
        result = self._values.get("user_pool_id")
        assert result is not None, "Required property 'user_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_id_client_regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#app_id_client_regex AppsyncGraphqlApi#app_id_client_regex}.'''
        result = self._values.get("app_id_client_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#aws_region AppsyncGraphqlApi#aws_region}.'''
        result = self._values.get("aws_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb7afa2921ad8d8d08f5be504ece4a039227e1c1dde4790cb3b7216fe476e03d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAppIdClientRegex")
    def reset_app_id_client_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppIdClientRegex", []))

    @jsii.member(jsii_name="resetAwsRegion")
    def reset_aws_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegion", []))

    @builtins.property
    @jsii.member(jsii_name="appIdClientRegexInput")
    def app_id_client_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appIdClientRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegionInput")
    def aws_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="userPoolIdInput")
    def user_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="appIdClientRegex")
    def app_id_client_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appIdClientRegex"))

    @app_id_client_regex.setter
    def app_id_client_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fc9b40242672fad321cb6fc98d796a0df4825bfa8240265fdd1dfa59a4d1997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appIdClientRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsRegion"))

    @aws_region.setter
    def aws_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1026e6f52966e51ae2d5456f34e0844a273289e714cb2603ffd1cbd3f1281d07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPoolId"))

    @user_pool_id.setter
    def user_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177bc1242cfefc7deed48a02d4ac91fddde1d1cdaddd146b60238c83feb853fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfig]:
        return typing.cast(typing.Optional[AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04af9fea421d843f7210b15bfd3b9a7729c35085265d59799e29892b1fcc2856)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApiConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "authentication_type": "authenticationType",
        "name": "name",
        "additional_authentication_provider": "additionalAuthenticationProvider",
        "api_type": "apiType",
        "enhanced_metrics_config": "enhancedMetricsConfig",
        "id": "id",
        "introspection_config": "introspectionConfig",
        "lambda_authorizer_config": "lambdaAuthorizerConfig",
        "log_config": "logConfig",
        "merged_api_execution_role_arn": "mergedApiExecutionRoleArn",
        "openid_connect_config": "openidConnectConfig",
        "query_depth_limit": "queryDepthLimit",
        "region": "region",
        "resolver_count_limit": "resolverCountLimit",
        "schema": "schema",
        "tags": "tags",
        "tags_all": "tagsAll",
        "user_pool_config": "userPoolConfig",
        "visibility": "visibility",
        "xray_enabled": "xrayEnabled",
    },
)
class AppsyncGraphqlApiConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        authentication_type: builtins.str,
        name: builtins.str,
        additional_authentication_provider: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncGraphqlApiAdditionalAuthenticationProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
        api_type: typing.Optional[builtins.str] = None,
        enhanced_metrics_config: typing.Optional[typing.Union["AppsyncGraphqlApiEnhancedMetricsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        introspection_config: typing.Optional[builtins.str] = None,
        lambda_authorizer_config: typing.Optional[typing.Union["AppsyncGraphqlApiLambdaAuthorizerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        log_config: typing.Optional[typing.Union["AppsyncGraphqlApiLogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        merged_api_execution_role_arn: typing.Optional[builtins.str] = None,
        openid_connect_config: typing.Optional[typing.Union["AppsyncGraphqlApiOpenidConnectConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        query_depth_limit: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        resolver_count_limit: typing.Optional[jsii.Number] = None,
        schema: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        user_pool_config: typing.Optional[typing.Union["AppsyncGraphqlApiUserPoolConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        visibility: typing.Optional[builtins.str] = None,
        xray_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#authentication_type AppsyncGraphqlApi#authentication_type}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#name AppsyncGraphqlApi#name}.
        :param additional_authentication_provider: additional_authentication_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#additional_authentication_provider AppsyncGraphqlApi#additional_authentication_provider}
        :param api_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#api_type AppsyncGraphqlApi#api_type}.
        :param enhanced_metrics_config: enhanced_metrics_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#enhanced_metrics_config AppsyncGraphqlApi#enhanced_metrics_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#id AppsyncGraphqlApi#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param introspection_config: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#introspection_config AppsyncGraphqlApi#introspection_config}.
        :param lambda_authorizer_config: lambda_authorizer_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#lambda_authorizer_config AppsyncGraphqlApi#lambda_authorizer_config}
        :param log_config: log_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#log_config AppsyncGraphqlApi#log_config}
        :param merged_api_execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#merged_api_execution_role_arn AppsyncGraphqlApi#merged_api_execution_role_arn}.
        :param openid_connect_config: openid_connect_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#openid_connect_config AppsyncGraphqlApi#openid_connect_config}
        :param query_depth_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#query_depth_limit AppsyncGraphqlApi#query_depth_limit}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#region AppsyncGraphqlApi#region}
        :param resolver_count_limit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#resolver_count_limit AppsyncGraphqlApi#resolver_count_limit}.
        :param schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#schema AppsyncGraphqlApi#schema}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#tags AppsyncGraphqlApi#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#tags_all AppsyncGraphqlApi#tags_all}.
        :param user_pool_config: user_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#user_pool_config AppsyncGraphqlApi#user_pool_config}
        :param visibility: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#visibility AppsyncGraphqlApi#visibility}.
        :param xray_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#xray_enabled AppsyncGraphqlApi#xray_enabled}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(enhanced_metrics_config, dict):
            enhanced_metrics_config = AppsyncGraphqlApiEnhancedMetricsConfig(**enhanced_metrics_config)
        if isinstance(lambda_authorizer_config, dict):
            lambda_authorizer_config = AppsyncGraphqlApiLambdaAuthorizerConfig(**lambda_authorizer_config)
        if isinstance(log_config, dict):
            log_config = AppsyncGraphqlApiLogConfig(**log_config)
        if isinstance(openid_connect_config, dict):
            openid_connect_config = AppsyncGraphqlApiOpenidConnectConfig(**openid_connect_config)
        if isinstance(user_pool_config, dict):
            user_pool_config = AppsyncGraphqlApiUserPoolConfig(**user_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51deee9ad81cc55b243eaee6b8e78b437949e7ec85edcd2696b14fd0781d1262)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument additional_authentication_provider", value=additional_authentication_provider, expected_type=type_hints["additional_authentication_provider"])
            check_type(argname="argument api_type", value=api_type, expected_type=type_hints["api_type"])
            check_type(argname="argument enhanced_metrics_config", value=enhanced_metrics_config, expected_type=type_hints["enhanced_metrics_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument introspection_config", value=introspection_config, expected_type=type_hints["introspection_config"])
            check_type(argname="argument lambda_authorizer_config", value=lambda_authorizer_config, expected_type=type_hints["lambda_authorizer_config"])
            check_type(argname="argument log_config", value=log_config, expected_type=type_hints["log_config"])
            check_type(argname="argument merged_api_execution_role_arn", value=merged_api_execution_role_arn, expected_type=type_hints["merged_api_execution_role_arn"])
            check_type(argname="argument openid_connect_config", value=openid_connect_config, expected_type=type_hints["openid_connect_config"])
            check_type(argname="argument query_depth_limit", value=query_depth_limit, expected_type=type_hints["query_depth_limit"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument resolver_count_limit", value=resolver_count_limit, expected_type=type_hints["resolver_count_limit"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument user_pool_config", value=user_pool_config, expected_type=type_hints["user_pool_config"])
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
            check_type(argname="argument xray_enabled", value=xray_enabled, expected_type=type_hints["xray_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authentication_type": authentication_type,
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
        if additional_authentication_provider is not None:
            self._values["additional_authentication_provider"] = additional_authentication_provider
        if api_type is not None:
            self._values["api_type"] = api_type
        if enhanced_metrics_config is not None:
            self._values["enhanced_metrics_config"] = enhanced_metrics_config
        if id is not None:
            self._values["id"] = id
        if introspection_config is not None:
            self._values["introspection_config"] = introspection_config
        if lambda_authorizer_config is not None:
            self._values["lambda_authorizer_config"] = lambda_authorizer_config
        if log_config is not None:
            self._values["log_config"] = log_config
        if merged_api_execution_role_arn is not None:
            self._values["merged_api_execution_role_arn"] = merged_api_execution_role_arn
        if openid_connect_config is not None:
            self._values["openid_connect_config"] = openid_connect_config
        if query_depth_limit is not None:
            self._values["query_depth_limit"] = query_depth_limit
        if region is not None:
            self._values["region"] = region
        if resolver_count_limit is not None:
            self._values["resolver_count_limit"] = resolver_count_limit
        if schema is not None:
            self._values["schema"] = schema
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if user_pool_config is not None:
            self._values["user_pool_config"] = user_pool_config
        if visibility is not None:
            self._values["visibility"] = visibility
        if xray_enabled is not None:
            self._values["xray_enabled"] = xray_enabled

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
    def authentication_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#authentication_type AppsyncGraphqlApi#authentication_type}.'''
        result = self._values.get("authentication_type")
        assert result is not None, "Required property 'authentication_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#name AppsyncGraphqlApi#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_authentication_provider(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncGraphqlApiAdditionalAuthenticationProvider]]]:
        '''additional_authentication_provider block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#additional_authentication_provider AppsyncGraphqlApi#additional_authentication_provider}
        '''
        result = self._values.get("additional_authentication_provider")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncGraphqlApiAdditionalAuthenticationProvider]]], result)

    @builtins.property
    def api_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#api_type AppsyncGraphqlApi#api_type}.'''
        result = self._values.get("api_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enhanced_metrics_config(
        self,
    ) -> typing.Optional["AppsyncGraphqlApiEnhancedMetricsConfig"]:
        '''enhanced_metrics_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#enhanced_metrics_config AppsyncGraphqlApi#enhanced_metrics_config}
        '''
        result = self._values.get("enhanced_metrics_config")
        return typing.cast(typing.Optional["AppsyncGraphqlApiEnhancedMetricsConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#id AppsyncGraphqlApi#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def introspection_config(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#introspection_config AppsyncGraphqlApi#introspection_config}.'''
        result = self._values.get("introspection_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_authorizer_config(
        self,
    ) -> typing.Optional["AppsyncGraphqlApiLambdaAuthorizerConfig"]:
        '''lambda_authorizer_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#lambda_authorizer_config AppsyncGraphqlApi#lambda_authorizer_config}
        '''
        result = self._values.get("lambda_authorizer_config")
        return typing.cast(typing.Optional["AppsyncGraphqlApiLambdaAuthorizerConfig"], result)

    @builtins.property
    def log_config(self) -> typing.Optional["AppsyncGraphqlApiLogConfig"]:
        '''log_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#log_config AppsyncGraphqlApi#log_config}
        '''
        result = self._values.get("log_config")
        return typing.cast(typing.Optional["AppsyncGraphqlApiLogConfig"], result)

    @builtins.property
    def merged_api_execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#merged_api_execution_role_arn AppsyncGraphqlApi#merged_api_execution_role_arn}.'''
        result = self._values.get("merged_api_execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def openid_connect_config(
        self,
    ) -> typing.Optional["AppsyncGraphqlApiOpenidConnectConfig"]:
        '''openid_connect_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#openid_connect_config AppsyncGraphqlApi#openid_connect_config}
        '''
        result = self._values.get("openid_connect_config")
        return typing.cast(typing.Optional["AppsyncGraphqlApiOpenidConnectConfig"], result)

    @builtins.property
    def query_depth_limit(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#query_depth_limit AppsyncGraphqlApi#query_depth_limit}.'''
        result = self._values.get("query_depth_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#region AppsyncGraphqlApi#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resolver_count_limit(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#resolver_count_limit AppsyncGraphqlApi#resolver_count_limit}.'''
        result = self._values.get("resolver_count_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#schema AppsyncGraphqlApi#schema}.'''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#tags AppsyncGraphqlApi#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#tags_all AppsyncGraphqlApi#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def user_pool_config(self) -> typing.Optional["AppsyncGraphqlApiUserPoolConfig"]:
        '''user_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#user_pool_config AppsyncGraphqlApi#user_pool_config}
        '''
        result = self._values.get("user_pool_config")
        return typing.cast(typing.Optional["AppsyncGraphqlApiUserPoolConfig"], result)

    @builtins.property
    def visibility(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#visibility AppsyncGraphqlApi#visibility}.'''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def xray_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#xray_enabled AppsyncGraphqlApi#xray_enabled}.'''
        result = self._values.get("xray_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncGraphqlApiConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApiEnhancedMetricsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "data_source_level_metrics_behavior": "dataSourceLevelMetricsBehavior",
        "operation_level_metrics_config": "operationLevelMetricsConfig",
        "resolver_level_metrics_behavior": "resolverLevelMetricsBehavior",
    },
)
class AppsyncGraphqlApiEnhancedMetricsConfig:
    def __init__(
        self,
        *,
        data_source_level_metrics_behavior: builtins.str,
        operation_level_metrics_config: builtins.str,
        resolver_level_metrics_behavior: builtins.str,
    ) -> None:
        '''
        :param data_source_level_metrics_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#data_source_level_metrics_behavior AppsyncGraphqlApi#data_source_level_metrics_behavior}.
        :param operation_level_metrics_config: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#operation_level_metrics_config AppsyncGraphqlApi#operation_level_metrics_config}.
        :param resolver_level_metrics_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#resolver_level_metrics_behavior AppsyncGraphqlApi#resolver_level_metrics_behavior}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe9c6955e1cd425dc18fea600e6716aa3c241d28e22ed194b3905114a7e7fccb)
            check_type(argname="argument data_source_level_metrics_behavior", value=data_source_level_metrics_behavior, expected_type=type_hints["data_source_level_metrics_behavior"])
            check_type(argname="argument operation_level_metrics_config", value=operation_level_metrics_config, expected_type=type_hints["operation_level_metrics_config"])
            check_type(argname="argument resolver_level_metrics_behavior", value=resolver_level_metrics_behavior, expected_type=type_hints["resolver_level_metrics_behavior"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_source_level_metrics_behavior": data_source_level_metrics_behavior,
            "operation_level_metrics_config": operation_level_metrics_config,
            "resolver_level_metrics_behavior": resolver_level_metrics_behavior,
        }

    @builtins.property
    def data_source_level_metrics_behavior(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#data_source_level_metrics_behavior AppsyncGraphqlApi#data_source_level_metrics_behavior}.'''
        result = self._values.get("data_source_level_metrics_behavior")
        assert result is not None, "Required property 'data_source_level_metrics_behavior' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operation_level_metrics_config(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#operation_level_metrics_config AppsyncGraphqlApi#operation_level_metrics_config}.'''
        result = self._values.get("operation_level_metrics_config")
        assert result is not None, "Required property 'operation_level_metrics_config' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resolver_level_metrics_behavior(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#resolver_level_metrics_behavior AppsyncGraphqlApi#resolver_level_metrics_behavior}.'''
        result = self._values.get("resolver_level_metrics_behavior")
        assert result is not None, "Required property 'resolver_level_metrics_behavior' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncGraphqlApiEnhancedMetricsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncGraphqlApiEnhancedMetricsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApiEnhancedMetricsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb9128324ef0f1d0898fe3fc194f6696933b978b3725a464587fb07d6f188bc7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dataSourceLevelMetricsBehaviorInput")
    def data_source_level_metrics_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceLevelMetricsBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="operationLevelMetricsConfigInput")
    def operation_level_metrics_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationLevelMetricsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="resolverLevelMetricsBehaviorInput")
    def resolver_level_metrics_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resolverLevelMetricsBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceLevelMetricsBehavior")
    def data_source_level_metrics_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSourceLevelMetricsBehavior"))

    @data_source_level_metrics_behavior.setter
    def data_source_level_metrics_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8531038238c436331241ccb0df45c1d79942f18e55402921d770d3bed5c3b009)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceLevelMetricsBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operationLevelMetricsConfig")
    def operation_level_metrics_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operationLevelMetricsConfig"))

    @operation_level_metrics_config.setter
    def operation_level_metrics_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__638cd4ff4773af1b844f62e349e9bae496925904c6c469112832e07c0bb5a0be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationLevelMetricsConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resolverLevelMetricsBehavior")
    def resolver_level_metrics_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resolverLevelMetricsBehavior"))

    @resolver_level_metrics_behavior.setter
    def resolver_level_metrics_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__645849918023b4bf3880d8a3e6cc0dc24089bf0a8ec371be919db0a069ddeeb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resolverLevelMetricsBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppsyncGraphqlApiEnhancedMetricsConfig]:
        return typing.cast(typing.Optional[AppsyncGraphqlApiEnhancedMetricsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppsyncGraphqlApiEnhancedMetricsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cc1a8ef997471a78e6682d81d0e56f534f841b99ec7bacb33f73c48fd0fbc12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApiLambdaAuthorizerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "authorizer_uri": "authorizerUri",
        "authorizer_result_ttl_in_seconds": "authorizerResultTtlInSeconds",
        "identity_validation_expression": "identityValidationExpression",
    },
)
class AppsyncGraphqlApiLambdaAuthorizerConfig:
    def __init__(
        self,
        *,
        authorizer_uri: builtins.str,
        authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number] = None,
        identity_validation_expression: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorizer_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#authorizer_uri AppsyncGraphqlApi#authorizer_uri}.
        :param authorizer_result_ttl_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#authorizer_result_ttl_in_seconds AppsyncGraphqlApi#authorizer_result_ttl_in_seconds}.
        :param identity_validation_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#identity_validation_expression AppsyncGraphqlApi#identity_validation_expression}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb1dbdd2c03362bd1adb79c86d8a0e439c464210738346c827f3624dd2e5f419)
            check_type(argname="argument authorizer_uri", value=authorizer_uri, expected_type=type_hints["authorizer_uri"])
            check_type(argname="argument authorizer_result_ttl_in_seconds", value=authorizer_result_ttl_in_seconds, expected_type=type_hints["authorizer_result_ttl_in_seconds"])
            check_type(argname="argument identity_validation_expression", value=identity_validation_expression, expected_type=type_hints["identity_validation_expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorizer_uri": authorizer_uri,
        }
        if authorizer_result_ttl_in_seconds is not None:
            self._values["authorizer_result_ttl_in_seconds"] = authorizer_result_ttl_in_seconds
        if identity_validation_expression is not None:
            self._values["identity_validation_expression"] = identity_validation_expression

    @builtins.property
    def authorizer_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#authorizer_uri AppsyncGraphqlApi#authorizer_uri}.'''
        result = self._values.get("authorizer_uri")
        assert result is not None, "Required property 'authorizer_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorizer_result_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#authorizer_result_ttl_in_seconds AppsyncGraphqlApi#authorizer_result_ttl_in_seconds}.'''
        result = self._values.get("authorizer_result_ttl_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def identity_validation_expression(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#identity_validation_expression AppsyncGraphqlApi#identity_validation_expression}.'''
        result = self._values.get("identity_validation_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncGraphqlApiLambdaAuthorizerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncGraphqlApiLambdaAuthorizerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApiLambdaAuthorizerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89f62159ae8c8724359353739ef5fbfc15139e588db65e045b86adc5d57e5289)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthorizerResultTtlInSeconds")
    def reset_authorizer_result_ttl_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizerResultTtlInSeconds", []))

    @jsii.member(jsii_name="resetIdentityValidationExpression")
    def reset_identity_validation_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityValidationExpression", []))

    @builtins.property
    @jsii.member(jsii_name="authorizerResultTtlInSecondsInput")
    def authorizer_result_ttl_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "authorizerResultTtlInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizerUriInput")
    def authorizer_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizerUriInput"))

    @builtins.property
    @jsii.member(jsii_name="identityValidationExpressionInput")
    def identity_validation_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityValidationExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizerResultTtlInSeconds")
    def authorizer_result_ttl_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "authorizerResultTtlInSeconds"))

    @authorizer_result_ttl_in_seconds.setter
    def authorizer_result_ttl_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__227dd1a83ead9247ff3e50a1b3fb4edd87edbda1621cdf8c4af53e70dddf757f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizerResultTtlInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authorizerUri")
    def authorizer_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizerUri"))

    @authorizer_uri.setter
    def authorizer_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__566324855b17b2107fa06f053f503c1e6021503bf3923230a33d170510fcc416)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizerUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityValidationExpression")
    def identity_validation_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityValidationExpression"))

    @identity_validation_expression.setter
    def identity_validation_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc97689e288ae75580e5f71fdf2879dd77b773f2d1b1da3e1f98782f54ae90ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityValidationExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppsyncGraphqlApiLambdaAuthorizerConfig]:
        return typing.cast(typing.Optional[AppsyncGraphqlApiLambdaAuthorizerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppsyncGraphqlApiLambdaAuthorizerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1199afc4503807e6a6284a93906ce660bf69f6db87dd8f0f09130614852669ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApiLogConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cloudwatch_logs_role_arn": "cloudwatchLogsRoleArn",
        "field_log_level": "fieldLogLevel",
        "exclude_verbose_content": "excludeVerboseContent",
    },
)
class AppsyncGraphqlApiLogConfig:
    def __init__(
        self,
        *,
        cloudwatch_logs_role_arn: builtins.str,
        field_log_level: builtins.str,
        exclude_verbose_content: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cloudwatch_logs_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#cloudwatch_logs_role_arn AppsyncGraphqlApi#cloudwatch_logs_role_arn}.
        :param field_log_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#field_log_level AppsyncGraphqlApi#field_log_level}.
        :param exclude_verbose_content: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#exclude_verbose_content AppsyncGraphqlApi#exclude_verbose_content}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f62d38c1189a6663b3c9aee58912777f5d06e30bea4acc3062e0fef798ea5e8e)
            check_type(argname="argument cloudwatch_logs_role_arn", value=cloudwatch_logs_role_arn, expected_type=type_hints["cloudwatch_logs_role_arn"])
            check_type(argname="argument field_log_level", value=field_log_level, expected_type=type_hints["field_log_level"])
            check_type(argname="argument exclude_verbose_content", value=exclude_verbose_content, expected_type=type_hints["exclude_verbose_content"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloudwatch_logs_role_arn": cloudwatch_logs_role_arn,
            "field_log_level": field_log_level,
        }
        if exclude_verbose_content is not None:
            self._values["exclude_verbose_content"] = exclude_verbose_content

    @builtins.property
    def cloudwatch_logs_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#cloudwatch_logs_role_arn AppsyncGraphqlApi#cloudwatch_logs_role_arn}.'''
        result = self._values.get("cloudwatch_logs_role_arn")
        assert result is not None, "Required property 'cloudwatch_logs_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def field_log_level(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#field_log_level AppsyncGraphqlApi#field_log_level}.'''
        result = self._values.get("field_log_level")
        assert result is not None, "Required property 'field_log_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exclude_verbose_content(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#exclude_verbose_content AppsyncGraphqlApi#exclude_verbose_content}.'''
        result = self._values.get("exclude_verbose_content")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncGraphqlApiLogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncGraphqlApiLogConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApiLogConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__636adcd597b2bc2e2bcd3286bb97352fc89e89942f7c7f9d055925beb7f9c6b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludeVerboseContent")
    def reset_exclude_verbose_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeVerboseContent", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogsRoleArnInput")
    def cloudwatch_logs_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudwatchLogsRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeVerboseContentInput")
    def exclude_verbose_content_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "excludeVerboseContentInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldLogLevelInput")
    def field_log_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldLogLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogsRoleArn")
    def cloudwatch_logs_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudwatchLogsRoleArn"))

    @cloudwatch_logs_role_arn.setter
    def cloudwatch_logs_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99965b766aebd2b93d39e3cf6f547657decc9fd80c0c9711c97f17fc83c1ae60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudwatchLogsRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeVerboseContent")
    def exclude_verbose_content(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "excludeVerboseContent"))

    @exclude_verbose_content.setter
    def exclude_verbose_content(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd17ada5da2e7b995f826a4580ec9a4c03759a4a0a961189ad1e519098e7cdce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeVerboseContent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fieldLogLevel")
    def field_log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldLogLevel"))

    @field_log_level.setter
    def field_log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd7ae5c09c2ca6b57b2308b3546b2a921ab1f1b67b50b16448ca6fecdedb84db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldLogLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppsyncGraphqlApiLogConfig]:
        return typing.cast(typing.Optional[AppsyncGraphqlApiLogConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppsyncGraphqlApiLogConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9fff441aaf09a627bdee07ffe4dc254991b1611deb28659c11f818102e219e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApiOpenidConnectConfig",
    jsii_struct_bases=[],
    name_mapping={
        "issuer": "issuer",
        "auth_ttl": "authTtl",
        "client_id": "clientId",
        "iat_ttl": "iatTtl",
    },
)
class AppsyncGraphqlApiOpenidConnectConfig:
    def __init__(
        self,
        *,
        issuer: builtins.str,
        auth_ttl: typing.Optional[jsii.Number] = None,
        client_id: typing.Optional[builtins.str] = None,
        iat_ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param issuer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#issuer AppsyncGraphqlApi#issuer}.
        :param auth_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#auth_ttl AppsyncGraphqlApi#auth_ttl}.
        :param client_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#client_id AppsyncGraphqlApi#client_id}.
        :param iat_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#iat_ttl AppsyncGraphqlApi#iat_ttl}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a71f50c64f0691e4ff58f7609b3415a064a97391f8d50a4824aa570125fff79)
            check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            check_type(argname="argument auth_ttl", value=auth_ttl, expected_type=type_hints["auth_ttl"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument iat_ttl", value=iat_ttl, expected_type=type_hints["iat_ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "issuer": issuer,
        }
        if auth_ttl is not None:
            self._values["auth_ttl"] = auth_ttl
        if client_id is not None:
            self._values["client_id"] = client_id
        if iat_ttl is not None:
            self._values["iat_ttl"] = iat_ttl

    @builtins.property
    def issuer(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#issuer AppsyncGraphqlApi#issuer}.'''
        result = self._values.get("issuer")
        assert result is not None, "Required property 'issuer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#auth_ttl AppsyncGraphqlApi#auth_ttl}.'''
        result = self._values.get("auth_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#client_id AppsyncGraphqlApi#client_id}.'''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iat_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#iat_ttl AppsyncGraphqlApi#iat_ttl}.'''
        result = self._values.get("iat_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncGraphqlApiOpenidConnectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncGraphqlApiOpenidConnectConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApiOpenidConnectConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f4acab4179ac7eafc8e69c85eda8546282e83dffc8fc59d1d4a486f83fb528a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthTtl")
    def reset_auth_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthTtl", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetIatTtl")
    def reset_iat_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIatTtl", []))

    @builtins.property
    @jsii.member(jsii_name="authTtlInput")
    def auth_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "authTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="iatTtlInput")
    def iat_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "iatTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerInput")
    def issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerInput"))

    @builtins.property
    @jsii.member(jsii_name="authTtl")
    def auth_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "authTtl"))

    @auth_ttl.setter
    def auth_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d17d0b56158f819a2a22a558f43256648f949e22947a01151a979fc2ad4b1f5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5875961a453aa26f923653eb2face894cc53e365bbd193ec82319152fa893ed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iatTtl")
    def iat_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "iatTtl"))

    @iat_ttl.setter
    def iat_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97790c4620c80ed96ed77846664d9e00c6904c2261d5a08e4045430fdfc00e4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iatTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cec2e69c00c6a6a8ad92aac167900ef9c6cdb7b934b7985b5aca206f9601527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppsyncGraphqlApiOpenidConnectConfig]:
        return typing.cast(typing.Optional[AppsyncGraphqlApiOpenidConnectConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppsyncGraphqlApiOpenidConnectConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__704a927cc4f426545703470b559623341abdd5def9ddce3fe29b760ef899101b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApiUserPoolConfig",
    jsii_struct_bases=[],
    name_mapping={
        "default_action": "defaultAction",
        "user_pool_id": "userPoolId",
        "app_id_client_regex": "appIdClientRegex",
        "aws_region": "awsRegion",
    },
)
class AppsyncGraphqlApiUserPoolConfig:
    def __init__(
        self,
        *,
        default_action: builtins.str,
        user_pool_id: builtins.str,
        app_id_client_regex: typing.Optional[builtins.str] = None,
        aws_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#default_action AppsyncGraphqlApi#default_action}.
        :param user_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#user_pool_id AppsyncGraphqlApi#user_pool_id}.
        :param app_id_client_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#app_id_client_regex AppsyncGraphqlApi#app_id_client_regex}.
        :param aws_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#aws_region AppsyncGraphqlApi#aws_region}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81de0e3d9ae5a5e93f83d8a4e74466cc216b9fd4cc0b6d489738032d0f4781c1)
            check_type(argname="argument default_action", value=default_action, expected_type=type_hints["default_action"])
            check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
            check_type(argname="argument app_id_client_regex", value=app_id_client_regex, expected_type=type_hints["app_id_client_regex"])
            check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_action": default_action,
            "user_pool_id": user_pool_id,
        }
        if app_id_client_regex is not None:
            self._values["app_id_client_regex"] = app_id_client_regex
        if aws_region is not None:
            self._values["aws_region"] = aws_region

    @builtins.property
    def default_action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#default_action AppsyncGraphqlApi#default_action}.'''
        result = self._values.get("default_action")
        assert result is not None, "Required property 'default_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_pool_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#user_pool_id AppsyncGraphqlApi#user_pool_id}.'''
        result = self._values.get("user_pool_id")
        assert result is not None, "Required property 'user_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_id_client_regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#app_id_client_regex AppsyncGraphqlApi#app_id_client_regex}.'''
        result = self._values.get("app_id_client_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/appsync_graphql_api#aws_region AppsyncGraphqlApi#aws_region}.'''
        result = self._values.get("aws_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncGraphqlApiUserPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncGraphqlApiUserPoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.appsyncGraphqlApi.AppsyncGraphqlApiUserPoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5338f63023b671157f6c6ebabfea933588d753bf96f61ede04638be7a497e29f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAppIdClientRegex")
    def reset_app_id_client_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppIdClientRegex", []))

    @jsii.member(jsii_name="resetAwsRegion")
    def reset_aws_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegion", []))

    @builtins.property
    @jsii.member(jsii_name="appIdClientRegexInput")
    def app_id_client_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appIdClientRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegionInput")
    def aws_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultActionInput")
    def default_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultActionInput"))

    @builtins.property
    @jsii.member(jsii_name="userPoolIdInput")
    def user_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="appIdClientRegex")
    def app_id_client_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appIdClientRegex"))

    @app_id_client_regex.setter
    def app_id_client_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5621becac317f142c2939161d38d00a3c8fd553d8fc321947855c41a879f5cf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appIdClientRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsRegion"))

    @aws_region.setter
    def aws_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8065bbc35999bfc9181dcb9af47ac1934ed754c70d00163ca25cbc49c6f77d09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultAction")
    def default_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultAction"))

    @default_action.setter
    def default_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37cfdf8e4658605084c4bead1cb88796d24c9c178dde923e456fa8b9a98e53f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPoolId"))

    @user_pool_id.setter
    def user_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f4cd01931e5e9d07a322e34a325f59378b8806307bc1891c3e1804c28e11a69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppsyncGraphqlApiUserPoolConfig]:
        return typing.cast(typing.Optional[AppsyncGraphqlApiUserPoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppsyncGraphqlApiUserPoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56fe37b6583cdd04797bfdc8679f64e2d011b9fa186a6b15b1ca1fff33f17677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AppsyncGraphqlApi",
    "AppsyncGraphqlApiAdditionalAuthenticationProvider",
    "AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfig",
    "AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfigOutputReference",
    "AppsyncGraphqlApiAdditionalAuthenticationProviderList",
    "AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfig",
    "AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfigOutputReference",
    "AppsyncGraphqlApiAdditionalAuthenticationProviderOutputReference",
    "AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfig",
    "AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfigOutputReference",
    "AppsyncGraphqlApiConfig",
    "AppsyncGraphqlApiEnhancedMetricsConfig",
    "AppsyncGraphqlApiEnhancedMetricsConfigOutputReference",
    "AppsyncGraphqlApiLambdaAuthorizerConfig",
    "AppsyncGraphqlApiLambdaAuthorizerConfigOutputReference",
    "AppsyncGraphqlApiLogConfig",
    "AppsyncGraphqlApiLogConfigOutputReference",
    "AppsyncGraphqlApiOpenidConnectConfig",
    "AppsyncGraphqlApiOpenidConnectConfigOutputReference",
    "AppsyncGraphqlApiUserPoolConfig",
    "AppsyncGraphqlApiUserPoolConfigOutputReference",
]

publication.publish()

def _typecheckingstub__cc9175da39096934ba7623d1c246b4ec73608c6b36c3249181dda3e2f2b0ff09(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    authentication_type: builtins.str,
    name: builtins.str,
    additional_authentication_provider: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncGraphqlApiAdditionalAuthenticationProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    api_type: typing.Optional[builtins.str] = None,
    enhanced_metrics_config: typing.Optional[typing.Union[AppsyncGraphqlApiEnhancedMetricsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    introspection_config: typing.Optional[builtins.str] = None,
    lambda_authorizer_config: typing.Optional[typing.Union[AppsyncGraphqlApiLambdaAuthorizerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    log_config: typing.Optional[typing.Union[AppsyncGraphqlApiLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    merged_api_execution_role_arn: typing.Optional[builtins.str] = None,
    openid_connect_config: typing.Optional[typing.Union[AppsyncGraphqlApiOpenidConnectConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    query_depth_limit: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    resolver_count_limit: typing.Optional[jsii.Number] = None,
    schema: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    user_pool_config: typing.Optional[typing.Union[AppsyncGraphqlApiUserPoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    visibility: typing.Optional[builtins.str] = None,
    xray_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__0639819eb56169019ce7509b0c9082ba7ef3209285ff0b2f8e4b115684808fa1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__601d2d542c2b0292524707b9183d28c2f07980200568a769c0db6fc77232356f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncGraphqlApiAdditionalAuthenticationProvider, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d400a06d8bb56cbdf7987121c3daa9130e81545889a129b4152b7b99cbe2375(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7753ca040691a60a2a102926160b546d17062b5cf4624ec4b6cd3ff360e4fdca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ffec4f2205b37bf274138a2271c58239ae2377ed3f40a1a5dc44d3f7a793f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3799196a3b35809f1b50f77da73fe59fd48770f0d3c0e1ca6569f4fa0c6ac11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc7900583a37d016079026ef79e4232efdef6ef4d3c0708ad8bcf8454f8a910(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5d4acb3fa816800e413e87e45d56df530468caa04a4e187a8a1b2a26c60298(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea15b73e22539a888b03da8b7daa027987dd0289ca48f8c34c2c56f1c1923d61(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4bc9942e1f9ce19411d61df895b262fd10c0a5f7de004e1443c72f9c1999d0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3412c48ec591fcff6c2e395211694fce13d15a85e9018d6eaf86ad7c8b103f46(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0bf62a5f6411ae3d80f5d1ff0e89743e3e46ec802c96b90aecde144aec8bdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__533d8a36a26d2c6454dc5ccd09caf02419993df232bee2986f8aed0f26e6f1d0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c951b0ecc58a915b8084f36db34619232bf3d342ab831f74f959c5808d91fb54(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7fe64ccfd886823556bbf86ecc904b25b48a4c058e41cb592cc08175609f851(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271bb52fb0734623121f640f8b30f134a8a46e9a5a718e6b24849672f495b40c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb3399357ffec344794abda81c2e3ff520af237da5fe50bb0ac06ceb7357049(
    *,
    authentication_type: builtins.str,
    lambda_authorizer_config: typing.Optional[typing.Union[AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    openid_connect_config: typing.Optional[typing.Union[AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    user_pool_config: typing.Optional[typing.Union[AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc8abac4127d95b7620ff5b62e3bb46b4a6adc31e008de5a8a0850929eb365e(
    *,
    authorizer_uri: builtins.str,
    authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number] = None,
    identity_validation_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cfb7bf8a111167389ca38ae3be7cf5b152df8c4405b735df0e37dd7241f8bd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2053cec2ea5d89b2e1b10c078e48b8193dff52fd85c2b38130e72165e176d09(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7050244d36d193089ce6dcf75d87e7b05c8fe9a62eee195b3d4876380d4170be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1126386fe269b64ab1b49326ab255d871c5e12a56dd36f13e76515e4cd7fef3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906dc42286129bf9c874cf8eaddfd1114d45f9e905031b462362110868e9074e(
    value: typing.Optional[AppsyncGraphqlApiAdditionalAuthenticationProviderLambdaAuthorizerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2761a28b256e4d16850ac34f10d5fda435171a2942a7f7b5b19229f0b3e5e97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1f44cfb906117db79a2209b915b0f118335737570dffc4cd16808bc71d11775(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d742fb2ba54a34ce5bd947914c43df1989ace0af6b2253b52db0f7e6a2b0bfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbbc7f3967bb7a408330f3b679d46cb5d6a658ec831316138781a52843f020ca(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d39385df4cfa9a61988b8cc1bde38d2dede8898eec720df1a8ade640a050bf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba7c834efc22b2f4c10eb06f5de41a1f764eb0e3b1f036407f598daeb068c9e6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsyncGraphqlApiAdditionalAuthenticationProvider]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c123de334fd1608a6abab54a3a969f17a0d6928b70a4f9fd676c247afb936004(
    *,
    issuer: builtins.str,
    auth_ttl: typing.Optional[jsii.Number] = None,
    client_id: typing.Optional[builtins.str] = None,
    iat_ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95deaec752f9f8c8f73257a22e49a5fe42a61b4a193b1dd3aec464ff87ab9e2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e1f6a6a0dd53e872a227aeed7ea8d0ccd89f17aed2ddd2cc68981b899fbceba(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf18d88a15033601df50845352ae2dfc42945ddceb0336b1744a13dfbfa754a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d89016c2ce303acf59e278296049837aefc9600b88f6847f2d496693a5e75a1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2530dbd35c1d7133e2e2da2f8835dd26c7ef7b4f0821fb42712749949328855d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec5156af47305f9028dc8c4fe17f33c6ad2121ea1e735d0e60d16ad2254fda25(
    value: typing.Optional[AppsyncGraphqlApiAdditionalAuthenticationProviderOpenidConnectConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d8671e2d9d4cdd87a3570bfee85508ef3622e873033b1f49b23ae089c3d70cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca33bda24f222c46fba24fe6f662a7d6971c5cbc4809269fb90ef6ffc09dc22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc9b4c054bae79a064540a9d7649799ef39dede4ce3d43b7a80bd95034fd532(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsyncGraphqlApiAdditionalAuthenticationProvider]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef1e17be9218493429f6dfec52c900de16b832effc837589b0b0ac4dc8fa9dfe(
    *,
    user_pool_id: builtins.str,
    app_id_client_regex: typing.Optional[builtins.str] = None,
    aws_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb7afa2921ad8d8d08f5be504ece4a039227e1c1dde4790cb3b7216fe476e03d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc9b40242672fad321cb6fc98d796a0df4825bfa8240265fdd1dfa59a4d1997(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1026e6f52966e51ae2d5456f34e0844a273289e714cb2603ffd1cbd3f1281d07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177bc1242cfefc7deed48a02d4ac91fddde1d1cdaddd146b60238c83feb853fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04af9fea421d843f7210b15bfd3b9a7729c35085265d59799e29892b1fcc2856(
    value: typing.Optional[AppsyncGraphqlApiAdditionalAuthenticationProviderUserPoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51deee9ad81cc55b243eaee6b8e78b437949e7ec85edcd2696b14fd0781d1262(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    authentication_type: builtins.str,
    name: builtins.str,
    additional_authentication_provider: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsyncGraphqlApiAdditionalAuthenticationProvider, typing.Dict[builtins.str, typing.Any]]]]] = None,
    api_type: typing.Optional[builtins.str] = None,
    enhanced_metrics_config: typing.Optional[typing.Union[AppsyncGraphqlApiEnhancedMetricsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    introspection_config: typing.Optional[builtins.str] = None,
    lambda_authorizer_config: typing.Optional[typing.Union[AppsyncGraphqlApiLambdaAuthorizerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    log_config: typing.Optional[typing.Union[AppsyncGraphqlApiLogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    merged_api_execution_role_arn: typing.Optional[builtins.str] = None,
    openid_connect_config: typing.Optional[typing.Union[AppsyncGraphqlApiOpenidConnectConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    query_depth_limit: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    resolver_count_limit: typing.Optional[jsii.Number] = None,
    schema: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    user_pool_config: typing.Optional[typing.Union[AppsyncGraphqlApiUserPoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    visibility: typing.Optional[builtins.str] = None,
    xray_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe9c6955e1cd425dc18fea600e6716aa3c241d28e22ed194b3905114a7e7fccb(
    *,
    data_source_level_metrics_behavior: builtins.str,
    operation_level_metrics_config: builtins.str,
    resolver_level_metrics_behavior: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb9128324ef0f1d0898fe3fc194f6696933b978b3725a464587fb07d6f188bc7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8531038238c436331241ccb0df45c1d79942f18e55402921d770d3bed5c3b009(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__638cd4ff4773af1b844f62e349e9bae496925904c6c469112832e07c0bb5a0be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645849918023b4bf3880d8a3e6cc0dc24089bf0a8ec371be919db0a069ddeeb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc1a8ef997471a78e6682d81d0e56f534f841b99ec7bacb33f73c48fd0fbc12(
    value: typing.Optional[AppsyncGraphqlApiEnhancedMetricsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb1dbdd2c03362bd1adb79c86d8a0e439c464210738346c827f3624dd2e5f419(
    *,
    authorizer_uri: builtins.str,
    authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number] = None,
    identity_validation_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f62159ae8c8724359353739ef5fbfc15139e588db65e045b86adc5d57e5289(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__227dd1a83ead9247ff3e50a1b3fb4edd87edbda1621cdf8c4af53e70dddf757f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__566324855b17b2107fa06f053f503c1e6021503bf3923230a33d170510fcc416(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc97689e288ae75580e5f71fdf2879dd77b773f2d1b1da3e1f98782f54ae90ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1199afc4503807e6a6284a93906ce660bf69f6db87dd8f0f09130614852669ca(
    value: typing.Optional[AppsyncGraphqlApiLambdaAuthorizerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62d38c1189a6663b3c9aee58912777f5d06e30bea4acc3062e0fef798ea5e8e(
    *,
    cloudwatch_logs_role_arn: builtins.str,
    field_log_level: builtins.str,
    exclude_verbose_content: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__636adcd597b2bc2e2bcd3286bb97352fc89e89942f7c7f9d055925beb7f9c6b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99965b766aebd2b93d39e3cf6f547657decc9fd80c0c9711c97f17fc83c1ae60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd17ada5da2e7b995f826a4580ec9a4c03759a4a0a961189ad1e519098e7cdce(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd7ae5c09c2ca6b57b2308b3546b2a921ab1f1b67b50b16448ca6fecdedb84db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fff441aaf09a627bdee07ffe4dc254991b1611deb28659c11f818102e219e3(
    value: typing.Optional[AppsyncGraphqlApiLogConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a71f50c64f0691e4ff58f7609b3415a064a97391f8d50a4824aa570125fff79(
    *,
    issuer: builtins.str,
    auth_ttl: typing.Optional[jsii.Number] = None,
    client_id: typing.Optional[builtins.str] = None,
    iat_ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4acab4179ac7eafc8e69c85eda8546282e83dffc8fc59d1d4a486f83fb528a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17d0b56158f819a2a22a558f43256648f949e22947a01151a979fc2ad4b1f5d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5875961a453aa26f923653eb2face894cc53e365bbd193ec82319152fa893ed0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97790c4620c80ed96ed77846664d9e00c6904c2261d5a08e4045430fdfc00e4b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cec2e69c00c6a6a8ad92aac167900ef9c6cdb7b934b7985b5aca206f9601527(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__704a927cc4f426545703470b559623341abdd5def9ddce3fe29b760ef899101b(
    value: typing.Optional[AppsyncGraphqlApiOpenidConnectConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81de0e3d9ae5a5e93f83d8a4e74466cc216b9fd4cc0b6d489738032d0f4781c1(
    *,
    default_action: builtins.str,
    user_pool_id: builtins.str,
    app_id_client_regex: typing.Optional[builtins.str] = None,
    aws_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5338f63023b671157f6c6ebabfea933588d753bf96f61ede04638be7a497e29f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5621becac317f142c2939161d38d00a3c8fd553d8fc321947855c41a879f5cf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8065bbc35999bfc9181dcb9af47ac1934ed754c70d00163ca25cbc49c6f77d09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37cfdf8e4658605084c4bead1cb88796d24c9c178dde923e456fa8b9a98e53f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4cd01931e5e9d07a322e34a325f59378b8806307bc1891c3e1804c28e11a69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56fe37b6583cdd04797bfdc8679f64e2d011b9fa186a6b15b1ca1fff33f17677(
    value: typing.Optional[AppsyncGraphqlApiUserPoolConfig],
) -> None:
    """Type checking stubs"""
    pass
