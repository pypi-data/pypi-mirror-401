r'''
# `aws_cloudfront_distribution`

Refer to the Terraform Registry for docs: [`aws_cloudfront_distribution`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution).
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


class CloudfrontDistribution(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistribution",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution aws_cloudfront_distribution}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_cache_behavior: typing.Union["CloudfrontDistributionDefaultCacheBehavior", typing.Dict[builtins.str, typing.Any]],
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        origin: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontDistributionOrigin", typing.Dict[builtins.str, typing.Any]]]],
        restrictions: typing.Union["CloudfrontDistributionRestrictions", typing.Dict[builtins.str, typing.Any]],
        viewer_certificate: typing.Union["CloudfrontDistributionViewerCertificate", typing.Dict[builtins.str, typing.Any]],
        aliases: typing.Optional[typing.Sequence[builtins.str]] = None,
        anycast_ip_list_id: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        connection_function_association: typing.Optional[typing.Union["CloudfrontDistributionConnectionFunctionAssociation", typing.Dict[builtins.str, typing.Any]]] = None,
        continuous_deployment_policy_id: typing.Optional[builtins.str] = None,
        custom_error_response: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontDistributionCustomErrorResponse", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_root_object: typing.Optional[builtins.str] = None,
        http_version: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_ipv6_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        logging_config: typing.Optional[typing.Union["CloudfrontDistributionLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ordered_cache_behavior: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontDistributionOrderedCacheBehavior", typing.Dict[builtins.str, typing.Any]]]]] = None,
        origin_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontDistributionOriginGroup", typing.Dict[builtins.str, typing.Any]]]]] = None,
        price_class: typing.Optional[builtins.str] = None,
        retain_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        staging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        viewer_mtls_config: typing.Optional[typing.Union["CloudfrontDistributionViewerMtlsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        wait_for_deployment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        web_acl_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution aws_cloudfront_distribution} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_cache_behavior: default_cache_behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#default_cache_behavior CloudfrontDistribution#default_cache_behavior}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#enabled CloudfrontDistribution#enabled}.
        :param origin: origin block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin CloudfrontDistribution#origin}
        :param restrictions: restrictions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#restrictions CloudfrontDistribution#restrictions}
        :param viewer_certificate: viewer_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#viewer_certificate CloudfrontDistribution#viewer_certificate}
        :param aliases: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#aliases CloudfrontDistribution#aliases}.
        :param anycast_ip_list_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#anycast_ip_list_id CloudfrontDistribution#anycast_ip_list_id}.
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#comment CloudfrontDistribution#comment}.
        :param connection_function_association: connection_function_association block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#connection_function_association CloudfrontDistribution#connection_function_association}
        :param continuous_deployment_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#continuous_deployment_policy_id CloudfrontDistribution#continuous_deployment_policy_id}.
        :param custom_error_response: custom_error_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#custom_error_response CloudfrontDistribution#custom_error_response}
        :param default_root_object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#default_root_object CloudfrontDistribution#default_root_object}.
        :param http_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#http_version CloudfrontDistribution#http_version}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#id CloudfrontDistribution#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_ipv6_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#is_ipv6_enabled CloudfrontDistribution#is_ipv6_enabled}.
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#logging_config CloudfrontDistribution#logging_config}
        :param ordered_cache_behavior: ordered_cache_behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#ordered_cache_behavior CloudfrontDistribution#ordered_cache_behavior}
        :param origin_group: origin_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_group CloudfrontDistribution#origin_group}
        :param price_class: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#price_class CloudfrontDistribution#price_class}.
        :param retain_on_delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#retain_on_delete CloudfrontDistribution#retain_on_delete}.
        :param staging: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#staging CloudfrontDistribution#staging}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#tags CloudfrontDistribution#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#tags_all CloudfrontDistribution#tags_all}.
        :param viewer_mtls_config: viewer_mtls_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#viewer_mtls_config CloudfrontDistribution#viewer_mtls_config}
        :param wait_for_deployment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#wait_for_deployment CloudfrontDistribution#wait_for_deployment}.
        :param web_acl_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#web_acl_id CloudfrontDistribution#web_acl_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ba742e51779c85665248759cf5fb9e3d4e87f3afa826c08aeac0664bf0c8236)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudfrontDistributionConfig(
            default_cache_behavior=default_cache_behavior,
            enabled=enabled,
            origin=origin,
            restrictions=restrictions,
            viewer_certificate=viewer_certificate,
            aliases=aliases,
            anycast_ip_list_id=anycast_ip_list_id,
            comment=comment,
            connection_function_association=connection_function_association,
            continuous_deployment_policy_id=continuous_deployment_policy_id,
            custom_error_response=custom_error_response,
            default_root_object=default_root_object,
            http_version=http_version,
            id=id,
            is_ipv6_enabled=is_ipv6_enabled,
            logging_config=logging_config,
            ordered_cache_behavior=ordered_cache_behavior,
            origin_group=origin_group,
            price_class=price_class,
            retain_on_delete=retain_on_delete,
            staging=staging,
            tags=tags,
            tags_all=tags_all,
            viewer_mtls_config=viewer_mtls_config,
            wait_for_deployment=wait_for_deployment,
            web_acl_id=web_acl_id,
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
        '''Generates CDKTF code for importing a CloudfrontDistribution resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudfrontDistribution to import.
        :param import_from_id: The id of the existing CloudfrontDistribution that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudfrontDistribution to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f74acc3271f151e835bc4f31df589a52ef94af01e57658ea6e37d5b1193643ed)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConnectionFunctionAssociation")
    def put_connection_function_association(self, *, id: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#id CloudfrontDistribution#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        value = CloudfrontDistributionConnectionFunctionAssociation(id=id)

        return typing.cast(None, jsii.invoke(self, "putConnectionFunctionAssociation", [value]))

    @jsii.member(jsii_name="putCustomErrorResponse")
    def put_custom_error_response(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontDistributionCustomErrorResponse", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1551c62d004dc3dd25c1766b000d02b23cf79d4fd31fbfd61dd7f73b4794c9e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomErrorResponse", [value]))

    @jsii.member(jsii_name="putDefaultCacheBehavior")
    def put_default_cache_behavior(
        self,
        *,
        allowed_methods: typing.Sequence[builtins.str],
        cached_methods: typing.Sequence[builtins.str],
        target_origin_id: builtins.str,
        viewer_protocol_policy: builtins.str,
        cache_policy_id: typing.Optional[builtins.str] = None,
        compress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        field_level_encryption_id: typing.Optional[builtins.str] = None,
        forwarded_values: typing.Optional[typing.Union["CloudfrontDistributionDefaultCacheBehaviorForwardedValues", typing.Dict[builtins.str, typing.Any]]] = None,
        function_association: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        grpc_config: typing.Optional[typing.Union["CloudfrontDistributionDefaultCacheBehaviorGrpcConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_function_association: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_ttl: typing.Optional[jsii.Number] = None,
        min_ttl: typing.Optional[jsii.Number] = None,
        origin_request_policy_id: typing.Optional[builtins.str] = None,
        realtime_log_config_arn: typing.Optional[builtins.str] = None,
        response_headers_policy_id: typing.Optional[builtins.str] = None,
        smooth_streaming: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        trusted_key_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        trusted_signers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#allowed_methods CloudfrontDistribution#allowed_methods}.
        :param cached_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#cached_methods CloudfrontDistribution#cached_methods}.
        :param target_origin_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#target_origin_id CloudfrontDistribution#target_origin_id}.
        :param viewer_protocol_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#viewer_protocol_policy CloudfrontDistribution#viewer_protocol_policy}.
        :param cache_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#cache_policy_id CloudfrontDistribution#cache_policy_id}.
        :param compress: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#compress CloudfrontDistribution#compress}.
        :param default_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#default_ttl CloudfrontDistribution#default_ttl}.
        :param field_level_encryption_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#field_level_encryption_id CloudfrontDistribution#field_level_encryption_id}.
        :param forwarded_values: forwarded_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#forwarded_values CloudfrontDistribution#forwarded_values}
        :param function_association: function_association block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#function_association CloudfrontDistribution#function_association}
        :param grpc_config: grpc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#grpc_config CloudfrontDistribution#grpc_config}
        :param lambda_function_association: lambda_function_association block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#lambda_function_association CloudfrontDistribution#lambda_function_association}
        :param max_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#max_ttl CloudfrontDistribution#max_ttl}.
        :param min_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#min_ttl CloudfrontDistribution#min_ttl}.
        :param origin_request_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_request_policy_id CloudfrontDistribution#origin_request_policy_id}.
        :param realtime_log_config_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#realtime_log_config_arn CloudfrontDistribution#realtime_log_config_arn}.
        :param response_headers_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#response_headers_policy_id CloudfrontDistribution#response_headers_policy_id}.
        :param smooth_streaming: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#smooth_streaming CloudfrontDistribution#smooth_streaming}.
        :param trusted_key_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#trusted_key_groups CloudfrontDistribution#trusted_key_groups}.
        :param trusted_signers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#trusted_signers CloudfrontDistribution#trusted_signers}.
        '''
        value = CloudfrontDistributionDefaultCacheBehavior(
            allowed_methods=allowed_methods,
            cached_methods=cached_methods,
            target_origin_id=target_origin_id,
            viewer_protocol_policy=viewer_protocol_policy,
            cache_policy_id=cache_policy_id,
            compress=compress,
            default_ttl=default_ttl,
            field_level_encryption_id=field_level_encryption_id,
            forwarded_values=forwarded_values,
            function_association=function_association,
            grpc_config=grpc_config,
            lambda_function_association=lambda_function_association,
            max_ttl=max_ttl,
            min_ttl=min_ttl,
            origin_request_policy_id=origin_request_policy_id,
            realtime_log_config_arn=realtime_log_config_arn,
            response_headers_policy_id=response_headers_policy_id,
            smooth_streaming=smooth_streaming,
            trusted_key_groups=trusted_key_groups,
            trusted_signers=trusted_signers,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultCacheBehavior", [value]))

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        include_cookies: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#bucket CloudfrontDistribution#bucket}.
        :param include_cookies: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#include_cookies CloudfrontDistribution#include_cookies}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#prefix CloudfrontDistribution#prefix}.
        '''
        value = CloudfrontDistributionLoggingConfig(
            bucket=bucket, include_cookies=include_cookies, prefix=prefix
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="putOrderedCacheBehavior")
    def put_ordered_cache_behavior(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontDistributionOrderedCacheBehavior", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce75e0f4b5143d55e6b8ae6535534e9a937b7ce522a198007737262e2b0cdd25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOrderedCacheBehavior", [value]))

    @jsii.member(jsii_name="putOrigin")
    def put_origin(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontDistributionOrigin", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ebe65b6476340c6f4fed99fd305accc27e6f1231fc7f0b469f6fef4daee5f5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOrigin", [value]))

    @jsii.member(jsii_name="putOriginGroup")
    def put_origin_group(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontDistributionOriginGroup", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84359cef9500b744d8f11519d9e977b9e81a4e13349772ace34173d5242614a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOriginGroup", [value]))

    @jsii.member(jsii_name="putRestrictions")
    def put_restrictions(
        self,
        *,
        geo_restriction: typing.Union["CloudfrontDistributionRestrictionsGeoRestriction", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param geo_restriction: geo_restriction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#geo_restriction CloudfrontDistribution#geo_restriction}
        '''
        value = CloudfrontDistributionRestrictions(geo_restriction=geo_restriction)

        return typing.cast(None, jsii.invoke(self, "putRestrictions", [value]))

    @jsii.member(jsii_name="putViewerCertificate")
    def put_viewer_certificate(
        self,
        *,
        acm_certificate_arn: typing.Optional[builtins.str] = None,
        cloudfront_default_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        iam_certificate_id: typing.Optional[builtins.str] = None,
        minimum_protocol_version: typing.Optional[builtins.str] = None,
        ssl_support_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param acm_certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#acm_certificate_arn CloudfrontDistribution#acm_certificate_arn}.
        :param cloudfront_default_certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#cloudfront_default_certificate CloudfrontDistribution#cloudfront_default_certificate}.
        :param iam_certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#iam_certificate_id CloudfrontDistribution#iam_certificate_id}.
        :param minimum_protocol_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#minimum_protocol_version CloudfrontDistribution#minimum_protocol_version}.
        :param ssl_support_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#ssl_support_method CloudfrontDistribution#ssl_support_method}.
        '''
        value = CloudfrontDistributionViewerCertificate(
            acm_certificate_arn=acm_certificate_arn,
            cloudfront_default_certificate=cloudfront_default_certificate,
            iam_certificate_id=iam_certificate_id,
            minimum_protocol_version=minimum_protocol_version,
            ssl_support_method=ssl_support_method,
        )

        return typing.cast(None, jsii.invoke(self, "putViewerCertificate", [value]))

    @jsii.member(jsii_name="putViewerMtlsConfig")
    def put_viewer_mtls_config(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        trust_store_config: typing.Optional[typing.Union["CloudfrontDistributionViewerMtlsConfigTrustStoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#mode CloudfrontDistribution#mode}.
        :param trust_store_config: trust_store_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#trust_store_config CloudfrontDistribution#trust_store_config}
        '''
        value = CloudfrontDistributionViewerMtlsConfig(
            mode=mode, trust_store_config=trust_store_config
        )

        return typing.cast(None, jsii.invoke(self, "putViewerMtlsConfig", [value]))

    @jsii.member(jsii_name="resetAliases")
    def reset_aliases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAliases", []))

    @jsii.member(jsii_name="resetAnycastIpListId")
    def reset_anycast_ip_list_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnycastIpListId", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetConnectionFunctionAssociation")
    def reset_connection_function_association(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionFunctionAssociation", []))

    @jsii.member(jsii_name="resetContinuousDeploymentPolicyId")
    def reset_continuous_deployment_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContinuousDeploymentPolicyId", []))

    @jsii.member(jsii_name="resetCustomErrorResponse")
    def reset_custom_error_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomErrorResponse", []))

    @jsii.member(jsii_name="resetDefaultRootObject")
    def reset_default_root_object(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultRootObject", []))

    @jsii.member(jsii_name="resetHttpVersion")
    def reset_http_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpVersion", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsIpv6Enabled")
    def reset_is_ipv6_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsIpv6Enabled", []))

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @jsii.member(jsii_name="resetOrderedCacheBehavior")
    def reset_ordered_cache_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrderedCacheBehavior", []))

    @jsii.member(jsii_name="resetOriginGroup")
    def reset_origin_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginGroup", []))

    @jsii.member(jsii_name="resetPriceClass")
    def reset_price_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriceClass", []))

    @jsii.member(jsii_name="resetRetainOnDelete")
    def reset_retain_on_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetainOnDelete", []))

    @jsii.member(jsii_name="resetStaging")
    def reset_staging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStaging", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetViewerMtlsConfig")
    def reset_viewer_mtls_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetViewerMtlsConfig", []))

    @jsii.member(jsii_name="resetWaitForDeployment")
    def reset_wait_for_deployment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWaitForDeployment", []))

    @jsii.member(jsii_name="resetWebAclId")
    def reset_web_acl_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebAclId", []))

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
    @jsii.member(jsii_name="callerReference")
    def caller_reference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "callerReference"))

    @builtins.property
    @jsii.member(jsii_name="connectionFunctionAssociation")
    def connection_function_association(
        self,
    ) -> "CloudfrontDistributionConnectionFunctionAssociationOutputReference":
        return typing.cast("CloudfrontDistributionConnectionFunctionAssociationOutputReference", jsii.get(self, "connectionFunctionAssociation"))

    @builtins.property
    @jsii.member(jsii_name="customErrorResponse")
    def custom_error_response(self) -> "CloudfrontDistributionCustomErrorResponseList":
        return typing.cast("CloudfrontDistributionCustomErrorResponseList", jsii.get(self, "customErrorResponse"))

    @builtins.property
    @jsii.member(jsii_name="defaultCacheBehavior")
    def default_cache_behavior(
        self,
    ) -> "CloudfrontDistributionDefaultCacheBehaviorOutputReference":
        return typing.cast("CloudfrontDistributionDefaultCacheBehaviorOutputReference", jsii.get(self, "defaultCacheBehavior"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="hostedZoneId")
    def hosted_zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostedZoneId"))

    @builtins.property
    @jsii.member(jsii_name="inProgressValidationBatches")
    def in_progress_validation_batches(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "inProgressValidationBatches"))

    @builtins.property
    @jsii.member(jsii_name="lastModifiedTime")
    def last_modified_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModifiedTime"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(self) -> "CloudfrontDistributionLoggingConfigOutputReference":
        return typing.cast("CloudfrontDistributionLoggingConfigOutputReference", jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="loggingV1Enabled")
    def logging_v1_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "loggingV1Enabled"))

    @builtins.property
    @jsii.member(jsii_name="orderedCacheBehavior")
    def ordered_cache_behavior(
        self,
    ) -> "CloudfrontDistributionOrderedCacheBehaviorList":
        return typing.cast("CloudfrontDistributionOrderedCacheBehaviorList", jsii.get(self, "orderedCacheBehavior"))

    @builtins.property
    @jsii.member(jsii_name="origin")
    def origin(self) -> "CloudfrontDistributionOriginList":
        return typing.cast("CloudfrontDistributionOriginList", jsii.get(self, "origin"))

    @builtins.property
    @jsii.member(jsii_name="originGroup")
    def origin_group(self) -> "CloudfrontDistributionOriginGroupList":
        return typing.cast("CloudfrontDistributionOriginGroupList", jsii.get(self, "originGroup"))

    @builtins.property
    @jsii.member(jsii_name="restrictions")
    def restrictions(self) -> "CloudfrontDistributionRestrictionsOutputReference":
        return typing.cast("CloudfrontDistributionRestrictionsOutputReference", jsii.get(self, "restrictions"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="trustedKeyGroups")
    def trusted_key_groups(self) -> "CloudfrontDistributionTrustedKeyGroupsList":
        return typing.cast("CloudfrontDistributionTrustedKeyGroupsList", jsii.get(self, "trustedKeyGroups"))

    @builtins.property
    @jsii.member(jsii_name="trustedSigners")
    def trusted_signers(self) -> "CloudfrontDistributionTrustedSignersList":
        return typing.cast("CloudfrontDistributionTrustedSignersList", jsii.get(self, "trustedSigners"))

    @builtins.property
    @jsii.member(jsii_name="viewerCertificate")
    def viewer_certificate(
        self,
    ) -> "CloudfrontDistributionViewerCertificateOutputReference":
        return typing.cast("CloudfrontDistributionViewerCertificateOutputReference", jsii.get(self, "viewerCertificate"))

    @builtins.property
    @jsii.member(jsii_name="viewerMtlsConfig")
    def viewer_mtls_config(
        self,
    ) -> "CloudfrontDistributionViewerMtlsConfigOutputReference":
        return typing.cast("CloudfrontDistributionViewerMtlsConfigOutputReference", jsii.get(self, "viewerMtlsConfig"))

    @builtins.property
    @jsii.member(jsii_name="aliasesInput")
    def aliases_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "aliasesInput"))

    @builtins.property
    @jsii.member(jsii_name="anycastIpListIdInput")
    def anycast_ip_list_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "anycastIpListIdInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionFunctionAssociationInput")
    def connection_function_association_input(
        self,
    ) -> typing.Optional["CloudfrontDistributionConnectionFunctionAssociation"]:
        return typing.cast(typing.Optional["CloudfrontDistributionConnectionFunctionAssociation"], jsii.get(self, "connectionFunctionAssociationInput"))

    @builtins.property
    @jsii.member(jsii_name="continuousDeploymentPolicyIdInput")
    def continuous_deployment_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "continuousDeploymentPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="customErrorResponseInput")
    def custom_error_response_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionCustomErrorResponse"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionCustomErrorResponse"]]], jsii.get(self, "customErrorResponseInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultCacheBehaviorInput")
    def default_cache_behavior_input(
        self,
    ) -> typing.Optional["CloudfrontDistributionDefaultCacheBehavior"]:
        return typing.cast(typing.Optional["CloudfrontDistributionDefaultCacheBehavior"], jsii.get(self, "defaultCacheBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultRootObjectInput")
    def default_root_object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultRootObjectInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="httpVersionInput")
    def http_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isIpv6EnabledInput")
    def is_ipv6_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isIpv6EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional["CloudfrontDistributionLoggingConfig"]:
        return typing.cast(typing.Optional["CloudfrontDistributionLoggingConfig"], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="orderedCacheBehaviorInput")
    def ordered_cache_behavior_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionOrderedCacheBehavior"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionOrderedCacheBehavior"]]], jsii.get(self, "orderedCacheBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="originGroupInput")
    def origin_group_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionOriginGroup"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionOriginGroup"]]], jsii.get(self, "originGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="originInput")
    def origin_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionOrigin"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionOrigin"]]], jsii.get(self, "originInput"))

    @builtins.property
    @jsii.member(jsii_name="priceClassInput")
    def price_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "priceClassInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictionsInput")
    def restrictions_input(
        self,
    ) -> typing.Optional["CloudfrontDistributionRestrictions"]:
        return typing.cast(typing.Optional["CloudfrontDistributionRestrictions"], jsii.get(self, "restrictionsInput"))

    @builtins.property
    @jsii.member(jsii_name="retainOnDeleteInput")
    def retain_on_delete_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "retainOnDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="stagingInput")
    def staging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "stagingInput"))

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
    @jsii.member(jsii_name="viewerCertificateInput")
    def viewer_certificate_input(
        self,
    ) -> typing.Optional["CloudfrontDistributionViewerCertificate"]:
        return typing.cast(typing.Optional["CloudfrontDistributionViewerCertificate"], jsii.get(self, "viewerCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="viewerMtlsConfigInput")
    def viewer_mtls_config_input(
        self,
    ) -> typing.Optional["CloudfrontDistributionViewerMtlsConfig"]:
        return typing.cast(typing.Optional["CloudfrontDistributionViewerMtlsConfig"], jsii.get(self, "viewerMtlsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="waitForDeploymentInput")
    def wait_for_deployment_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "waitForDeploymentInput"))

    @builtins.property
    @jsii.member(jsii_name="webAclIdInput")
    def web_acl_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webAclIdInput"))

    @builtins.property
    @jsii.member(jsii_name="aliases")
    def aliases(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "aliases"))

    @aliases.setter
    def aliases(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b340a15dbf11078679c86eaa19c488ec8096d436ff58ad0ed7530bd38d376ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aliases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="anycastIpListId")
    def anycast_ip_list_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "anycastIpListId"))

    @anycast_ip_list_id.setter
    def anycast_ip_list_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c89c3d17e3b49394c293512d57f8282b71086bb7fc16975010c50f3817e9c3ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "anycastIpListId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ebe827d0ca2711cfe1bd051aa344e52c77eda4b2284aeb50382c82d7b60efec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="continuousDeploymentPolicyId")
    def continuous_deployment_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "continuousDeploymentPolicyId"))

    @continuous_deployment_policy_id.setter
    def continuous_deployment_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e30728b8fff46b0264ede736a3c68c3dc6eac68d079a3aa0f5677df3fdc4249b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "continuousDeploymentPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultRootObject")
    def default_root_object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultRootObject"))

    @default_root_object.setter
    def default_root_object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0de6b02061ba8d66451350bfe8499de91dac7ff3db62de9db991e0296dbb96f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRootObject", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__fae0792e2f5c7e114b1a2f19be78a6ba447b27f0aae73b3cafa2162baca9624d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpVersion")
    def http_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpVersion"))

    @http_version.setter
    def http_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00e4d8d6d79f8bfedabc21229ba541e02f8dfedcfc840e51c4d66987c55b0164)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f449cc7c227d4cd798b526cba8deee75b8118f1f7103c7ea9773c281d3c75850)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isIpv6Enabled")
    def is_ipv6_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isIpv6Enabled"))

    @is_ipv6_enabled.setter
    def is_ipv6_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79bf75639d76db494258c2e1620b4a4e9d7480a918aa0f08d615aba13961c89d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isIpv6Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priceClass")
    def price_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "priceClass"))

    @price_class.setter
    def price_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7189538c4dc11bb641d3f56306c4bf136e69a48bafba15db88c66bfc862deb4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priceClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retainOnDelete")
    def retain_on_delete(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "retainOnDelete"))

    @retain_on_delete.setter
    def retain_on_delete(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf59b0ab6783d3b18d49d6ff1684348a9f3ada2ea8902d833bef757950c7c555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retainOnDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="staging")
    def staging(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "staging"))

    @staging.setter
    def staging(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7fef9703e5a46cb736cd916f7503584b5c585c9cd2fca143f4d6ee00688ac1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "staging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2dea6b3eb9f072bcf8a05415213884e79292da51e88b53677fa6a5cc698ebd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2bb0329bffdf88c112ca2e418d9f512a220909f5526ef0f5fc60c4e8d383cea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitForDeployment")
    def wait_for_deployment(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "waitForDeployment"))

    @wait_for_deployment.setter
    def wait_for_deployment(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ad14abc8660cfcafe79c40248b111c8f96aec62853062050feea927765c0fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForDeployment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webAclId")
    def web_acl_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webAclId"))

    @web_acl_id.setter
    def web_acl_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65aee952aa4e651a1f45f349d5dad08a84bbd616478bf42029950b0eb120aee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webAclId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "default_cache_behavior": "defaultCacheBehavior",
        "enabled": "enabled",
        "origin": "origin",
        "restrictions": "restrictions",
        "viewer_certificate": "viewerCertificate",
        "aliases": "aliases",
        "anycast_ip_list_id": "anycastIpListId",
        "comment": "comment",
        "connection_function_association": "connectionFunctionAssociation",
        "continuous_deployment_policy_id": "continuousDeploymentPolicyId",
        "custom_error_response": "customErrorResponse",
        "default_root_object": "defaultRootObject",
        "http_version": "httpVersion",
        "id": "id",
        "is_ipv6_enabled": "isIpv6Enabled",
        "logging_config": "loggingConfig",
        "ordered_cache_behavior": "orderedCacheBehavior",
        "origin_group": "originGroup",
        "price_class": "priceClass",
        "retain_on_delete": "retainOnDelete",
        "staging": "staging",
        "tags": "tags",
        "tags_all": "tagsAll",
        "viewer_mtls_config": "viewerMtlsConfig",
        "wait_for_deployment": "waitForDeployment",
        "web_acl_id": "webAclId",
    },
)
class CloudfrontDistributionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        default_cache_behavior: typing.Union["CloudfrontDistributionDefaultCacheBehavior", typing.Dict[builtins.str, typing.Any]],
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        origin: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontDistributionOrigin", typing.Dict[builtins.str, typing.Any]]]],
        restrictions: typing.Union["CloudfrontDistributionRestrictions", typing.Dict[builtins.str, typing.Any]],
        viewer_certificate: typing.Union["CloudfrontDistributionViewerCertificate", typing.Dict[builtins.str, typing.Any]],
        aliases: typing.Optional[typing.Sequence[builtins.str]] = None,
        anycast_ip_list_id: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        connection_function_association: typing.Optional[typing.Union["CloudfrontDistributionConnectionFunctionAssociation", typing.Dict[builtins.str, typing.Any]]] = None,
        continuous_deployment_policy_id: typing.Optional[builtins.str] = None,
        custom_error_response: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontDistributionCustomErrorResponse", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_root_object: typing.Optional[builtins.str] = None,
        http_version: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_ipv6_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        logging_config: typing.Optional[typing.Union["CloudfrontDistributionLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        ordered_cache_behavior: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontDistributionOrderedCacheBehavior", typing.Dict[builtins.str, typing.Any]]]]] = None,
        origin_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontDistributionOriginGroup", typing.Dict[builtins.str, typing.Any]]]]] = None,
        price_class: typing.Optional[builtins.str] = None,
        retain_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        staging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        viewer_mtls_config: typing.Optional[typing.Union["CloudfrontDistributionViewerMtlsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        wait_for_deployment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        web_acl_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param default_cache_behavior: default_cache_behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#default_cache_behavior CloudfrontDistribution#default_cache_behavior}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#enabled CloudfrontDistribution#enabled}.
        :param origin: origin block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin CloudfrontDistribution#origin}
        :param restrictions: restrictions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#restrictions CloudfrontDistribution#restrictions}
        :param viewer_certificate: viewer_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#viewer_certificate CloudfrontDistribution#viewer_certificate}
        :param aliases: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#aliases CloudfrontDistribution#aliases}.
        :param anycast_ip_list_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#anycast_ip_list_id CloudfrontDistribution#anycast_ip_list_id}.
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#comment CloudfrontDistribution#comment}.
        :param connection_function_association: connection_function_association block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#connection_function_association CloudfrontDistribution#connection_function_association}
        :param continuous_deployment_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#continuous_deployment_policy_id CloudfrontDistribution#continuous_deployment_policy_id}.
        :param custom_error_response: custom_error_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#custom_error_response CloudfrontDistribution#custom_error_response}
        :param default_root_object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#default_root_object CloudfrontDistribution#default_root_object}.
        :param http_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#http_version CloudfrontDistribution#http_version}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#id CloudfrontDistribution#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_ipv6_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#is_ipv6_enabled CloudfrontDistribution#is_ipv6_enabled}.
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#logging_config CloudfrontDistribution#logging_config}
        :param ordered_cache_behavior: ordered_cache_behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#ordered_cache_behavior CloudfrontDistribution#ordered_cache_behavior}
        :param origin_group: origin_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_group CloudfrontDistribution#origin_group}
        :param price_class: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#price_class CloudfrontDistribution#price_class}.
        :param retain_on_delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#retain_on_delete CloudfrontDistribution#retain_on_delete}.
        :param staging: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#staging CloudfrontDistribution#staging}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#tags CloudfrontDistribution#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#tags_all CloudfrontDistribution#tags_all}.
        :param viewer_mtls_config: viewer_mtls_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#viewer_mtls_config CloudfrontDistribution#viewer_mtls_config}
        :param wait_for_deployment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#wait_for_deployment CloudfrontDistribution#wait_for_deployment}.
        :param web_acl_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#web_acl_id CloudfrontDistribution#web_acl_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(default_cache_behavior, dict):
            default_cache_behavior = CloudfrontDistributionDefaultCacheBehavior(**default_cache_behavior)
        if isinstance(restrictions, dict):
            restrictions = CloudfrontDistributionRestrictions(**restrictions)
        if isinstance(viewer_certificate, dict):
            viewer_certificate = CloudfrontDistributionViewerCertificate(**viewer_certificate)
        if isinstance(connection_function_association, dict):
            connection_function_association = CloudfrontDistributionConnectionFunctionAssociation(**connection_function_association)
        if isinstance(logging_config, dict):
            logging_config = CloudfrontDistributionLoggingConfig(**logging_config)
        if isinstance(viewer_mtls_config, dict):
            viewer_mtls_config = CloudfrontDistributionViewerMtlsConfig(**viewer_mtls_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a778aae6002d6970e024f74b8e96456d5d8a6131c12682a408186c7edee3f0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument default_cache_behavior", value=default_cache_behavior, expected_type=type_hints["default_cache_behavior"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
            check_type(argname="argument restrictions", value=restrictions, expected_type=type_hints["restrictions"])
            check_type(argname="argument viewer_certificate", value=viewer_certificate, expected_type=type_hints["viewer_certificate"])
            check_type(argname="argument aliases", value=aliases, expected_type=type_hints["aliases"])
            check_type(argname="argument anycast_ip_list_id", value=anycast_ip_list_id, expected_type=type_hints["anycast_ip_list_id"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument connection_function_association", value=connection_function_association, expected_type=type_hints["connection_function_association"])
            check_type(argname="argument continuous_deployment_policy_id", value=continuous_deployment_policy_id, expected_type=type_hints["continuous_deployment_policy_id"])
            check_type(argname="argument custom_error_response", value=custom_error_response, expected_type=type_hints["custom_error_response"])
            check_type(argname="argument default_root_object", value=default_root_object, expected_type=type_hints["default_root_object"])
            check_type(argname="argument http_version", value=http_version, expected_type=type_hints["http_version"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_ipv6_enabled", value=is_ipv6_enabled, expected_type=type_hints["is_ipv6_enabled"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument ordered_cache_behavior", value=ordered_cache_behavior, expected_type=type_hints["ordered_cache_behavior"])
            check_type(argname="argument origin_group", value=origin_group, expected_type=type_hints["origin_group"])
            check_type(argname="argument price_class", value=price_class, expected_type=type_hints["price_class"])
            check_type(argname="argument retain_on_delete", value=retain_on_delete, expected_type=type_hints["retain_on_delete"])
            check_type(argname="argument staging", value=staging, expected_type=type_hints["staging"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument viewer_mtls_config", value=viewer_mtls_config, expected_type=type_hints["viewer_mtls_config"])
            check_type(argname="argument wait_for_deployment", value=wait_for_deployment, expected_type=type_hints["wait_for_deployment"])
            check_type(argname="argument web_acl_id", value=web_acl_id, expected_type=type_hints["web_acl_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_cache_behavior": default_cache_behavior,
            "enabled": enabled,
            "origin": origin,
            "restrictions": restrictions,
            "viewer_certificate": viewer_certificate,
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
        if aliases is not None:
            self._values["aliases"] = aliases
        if anycast_ip_list_id is not None:
            self._values["anycast_ip_list_id"] = anycast_ip_list_id
        if comment is not None:
            self._values["comment"] = comment
        if connection_function_association is not None:
            self._values["connection_function_association"] = connection_function_association
        if continuous_deployment_policy_id is not None:
            self._values["continuous_deployment_policy_id"] = continuous_deployment_policy_id
        if custom_error_response is not None:
            self._values["custom_error_response"] = custom_error_response
        if default_root_object is not None:
            self._values["default_root_object"] = default_root_object
        if http_version is not None:
            self._values["http_version"] = http_version
        if id is not None:
            self._values["id"] = id
        if is_ipv6_enabled is not None:
            self._values["is_ipv6_enabled"] = is_ipv6_enabled
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if ordered_cache_behavior is not None:
            self._values["ordered_cache_behavior"] = ordered_cache_behavior
        if origin_group is not None:
            self._values["origin_group"] = origin_group
        if price_class is not None:
            self._values["price_class"] = price_class
        if retain_on_delete is not None:
            self._values["retain_on_delete"] = retain_on_delete
        if staging is not None:
            self._values["staging"] = staging
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if viewer_mtls_config is not None:
            self._values["viewer_mtls_config"] = viewer_mtls_config
        if wait_for_deployment is not None:
            self._values["wait_for_deployment"] = wait_for_deployment
        if web_acl_id is not None:
            self._values["web_acl_id"] = web_acl_id

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
    def default_cache_behavior(self) -> "CloudfrontDistributionDefaultCacheBehavior":
        '''default_cache_behavior block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#default_cache_behavior CloudfrontDistribution#default_cache_behavior}
        '''
        result = self._values.get("default_cache_behavior")
        assert result is not None, "Required property 'default_cache_behavior' is missing"
        return typing.cast("CloudfrontDistributionDefaultCacheBehavior", result)

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#enabled CloudfrontDistribution#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def origin(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionOrigin"]]:
        '''origin block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin CloudfrontDistribution#origin}
        '''
        result = self._values.get("origin")
        assert result is not None, "Required property 'origin' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionOrigin"]], result)

    @builtins.property
    def restrictions(self) -> "CloudfrontDistributionRestrictions":
        '''restrictions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#restrictions CloudfrontDistribution#restrictions}
        '''
        result = self._values.get("restrictions")
        assert result is not None, "Required property 'restrictions' is missing"
        return typing.cast("CloudfrontDistributionRestrictions", result)

    @builtins.property
    def viewer_certificate(self) -> "CloudfrontDistributionViewerCertificate":
        '''viewer_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#viewer_certificate CloudfrontDistribution#viewer_certificate}
        '''
        result = self._values.get("viewer_certificate")
        assert result is not None, "Required property 'viewer_certificate' is missing"
        return typing.cast("CloudfrontDistributionViewerCertificate", result)

    @builtins.property
    def aliases(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#aliases CloudfrontDistribution#aliases}.'''
        result = self._values.get("aliases")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def anycast_ip_list_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#anycast_ip_list_id CloudfrontDistribution#anycast_ip_list_id}.'''
        result = self._values.get("anycast_ip_list_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#comment CloudfrontDistribution#comment}.'''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_function_association(
        self,
    ) -> typing.Optional["CloudfrontDistributionConnectionFunctionAssociation"]:
        '''connection_function_association block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#connection_function_association CloudfrontDistribution#connection_function_association}
        '''
        result = self._values.get("connection_function_association")
        return typing.cast(typing.Optional["CloudfrontDistributionConnectionFunctionAssociation"], result)

    @builtins.property
    def continuous_deployment_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#continuous_deployment_policy_id CloudfrontDistribution#continuous_deployment_policy_id}.'''
        result = self._values.get("continuous_deployment_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_error_response(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionCustomErrorResponse"]]]:
        '''custom_error_response block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#custom_error_response CloudfrontDistribution#custom_error_response}
        '''
        result = self._values.get("custom_error_response")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionCustomErrorResponse"]]], result)

    @builtins.property
    def default_root_object(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#default_root_object CloudfrontDistribution#default_root_object}.'''
        result = self._values.get("default_root_object")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#http_version CloudfrontDistribution#http_version}.'''
        result = self._values.get("http_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#id CloudfrontDistribution#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_ipv6_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#is_ipv6_enabled CloudfrontDistribution#is_ipv6_enabled}.'''
        result = self._values.get("is_ipv6_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def logging_config(self) -> typing.Optional["CloudfrontDistributionLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#logging_config CloudfrontDistribution#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["CloudfrontDistributionLoggingConfig"], result)

    @builtins.property
    def ordered_cache_behavior(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionOrderedCacheBehavior"]]]:
        '''ordered_cache_behavior block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#ordered_cache_behavior CloudfrontDistribution#ordered_cache_behavior}
        '''
        result = self._values.get("ordered_cache_behavior")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionOrderedCacheBehavior"]]], result)

    @builtins.property
    def origin_group(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionOriginGroup"]]]:
        '''origin_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_group CloudfrontDistribution#origin_group}
        '''
        result = self._values.get("origin_group")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionOriginGroup"]]], result)

    @builtins.property
    def price_class(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#price_class CloudfrontDistribution#price_class}.'''
        result = self._values.get("price_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retain_on_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#retain_on_delete CloudfrontDistribution#retain_on_delete}.'''
        result = self._values.get("retain_on_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def staging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#staging CloudfrontDistribution#staging}.'''
        result = self._values.get("staging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#tags CloudfrontDistribution#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#tags_all CloudfrontDistribution#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def viewer_mtls_config(
        self,
    ) -> typing.Optional["CloudfrontDistributionViewerMtlsConfig"]:
        '''viewer_mtls_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#viewer_mtls_config CloudfrontDistribution#viewer_mtls_config}
        '''
        result = self._values.get("viewer_mtls_config")
        return typing.cast(typing.Optional["CloudfrontDistributionViewerMtlsConfig"], result)

    @builtins.property
    def wait_for_deployment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#wait_for_deployment CloudfrontDistribution#wait_for_deployment}.'''
        result = self._values.get("wait_for_deployment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def web_acl_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#web_acl_id CloudfrontDistribution#web_acl_id}.'''
        result = self._values.get("web_acl_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionConnectionFunctionAssociation",
    jsii_struct_bases=[],
    name_mapping={"id": "id"},
)
class CloudfrontDistributionConnectionFunctionAssociation:
    def __init__(self, *, id: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#id CloudfrontDistribution#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ec01a0f107577b42c6500a2d43498ef5051e408e2e10c2a1faef000f6d5ed2d)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#id CloudfrontDistribution#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionConnectionFunctionAssociation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionConnectionFunctionAssociationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionConnectionFunctionAssociationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__def3d2362b7934484ffc8ce4bee8e1ba8e34ae8c5b4da3c116b7399fc3190b77)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8332f6ed7ad0fcb68bdf9a1330c9654298188d4249570cafab7d91e5dc6fa79c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontDistributionConnectionFunctionAssociation]:
        return typing.cast(typing.Optional[CloudfrontDistributionConnectionFunctionAssociation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionConnectionFunctionAssociation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b77d7948c6b71751aaf06f77bf01a090103d317bbaa7fc72aec8a10645651978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionCustomErrorResponse",
    jsii_struct_bases=[],
    name_mapping={
        "error_code": "errorCode",
        "error_caching_min_ttl": "errorCachingMinTtl",
        "response_code": "responseCode",
        "response_page_path": "responsePagePath",
    },
)
class CloudfrontDistributionCustomErrorResponse:
    def __init__(
        self,
        *,
        error_code: jsii.Number,
        error_caching_min_ttl: typing.Optional[jsii.Number] = None,
        response_code: typing.Optional[jsii.Number] = None,
        response_page_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param error_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#error_code CloudfrontDistribution#error_code}.
        :param error_caching_min_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#error_caching_min_ttl CloudfrontDistribution#error_caching_min_ttl}.
        :param response_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#response_code CloudfrontDistribution#response_code}.
        :param response_page_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#response_page_path CloudfrontDistribution#response_page_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50bb8b09d5eca03761314f8c035e825b140439adbe7e1c49bdb2e2e6008c0315)
            check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
            check_type(argname="argument error_caching_min_ttl", value=error_caching_min_ttl, expected_type=type_hints["error_caching_min_ttl"])
            check_type(argname="argument response_code", value=response_code, expected_type=type_hints["response_code"])
            check_type(argname="argument response_page_path", value=response_page_path, expected_type=type_hints["response_page_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "error_code": error_code,
        }
        if error_caching_min_ttl is not None:
            self._values["error_caching_min_ttl"] = error_caching_min_ttl
        if response_code is not None:
            self._values["response_code"] = response_code
        if response_page_path is not None:
            self._values["response_page_path"] = response_page_path

    @builtins.property
    def error_code(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#error_code CloudfrontDistribution#error_code}.'''
        result = self._values.get("error_code")
        assert result is not None, "Required property 'error_code' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def error_caching_min_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#error_caching_min_ttl CloudfrontDistribution#error_caching_min_ttl}.'''
        result = self._values.get("error_caching_min_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def response_code(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#response_code CloudfrontDistribution#response_code}.'''
        result = self._values.get("response_code")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def response_page_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#response_page_path CloudfrontDistribution#response_page_path}.'''
        result = self._values.get("response_page_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionCustomErrorResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionCustomErrorResponseList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionCustomErrorResponseList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60e659840541bf513c9447554d9f272da59b1659311fc46db53d7c8722aa6320)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontDistributionCustomErrorResponseOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1edbd73850098b9a0f80e698215b227fb0dafe4099f24bb6f7947a85df94544)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontDistributionCustomErrorResponseOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16dfeb79bf3805b4b688f9f0a1c98a812724cea30673255fd6a940d05cd1c7a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b51f0299bd82a28a5106877d1c9fb479a2109bd95b4acabbd331045609063089)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d0bdec176bbe3c8765b16c4f5e630f3c6b5a55240b4a148d8d2e23b78fc476e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionCustomErrorResponse]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionCustomErrorResponse]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionCustomErrorResponse]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da9610df82580608387da55c262b14f2401dd05324709d0473dd304148270809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionCustomErrorResponseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionCustomErrorResponseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__957c4b65d403d5f3464928b31f537c56fec953905a08b425083fb6e5044d5617)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetErrorCachingMinTtl")
    def reset_error_caching_min_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorCachingMinTtl", []))

    @jsii.member(jsii_name="resetResponseCode")
    def reset_response_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseCode", []))

    @jsii.member(jsii_name="resetResponsePagePath")
    def reset_response_page_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponsePagePath", []))

    @builtins.property
    @jsii.member(jsii_name="errorCachingMinTtlInput")
    def error_caching_min_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "errorCachingMinTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="errorCodeInput")
    def error_code_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "errorCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="responseCodeInput")
    def response_code_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "responseCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="responsePagePathInput")
    def response_page_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responsePagePathInput"))

    @builtins.property
    @jsii.member(jsii_name="errorCachingMinTtl")
    def error_caching_min_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "errorCachingMinTtl"))

    @error_caching_min_ttl.setter
    def error_caching_min_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70f7284a800ac0f16d55f8b5bf7e7db19df255a86cee205b0a0046a052e9274a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorCachingMinTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="errorCode")
    def error_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "errorCode"))

    @error_code.setter
    def error_code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f7ac291b8c9e099aacb2a294fd19b4e1585c0c6d85fedf044b155383f032a36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseCode")
    def response_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "responseCode"))

    @response_code.setter
    def response_code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae2146406b989cee68d5950a84dcb685b2b3a8fb9dd5d5eed8d91865154596ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responsePagePath")
    def response_page_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responsePagePath"))

    @response_page_path.setter
    def response_page_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adc1d5110f923705e22e0cf694268c26e45e87359621a322aeef850d7b4412d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responsePagePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionCustomErrorResponse]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionCustomErrorResponse]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionCustomErrorResponse]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f10de61fa6c418d2f3eea1657ae2b7885833aa7ef547df2d184d6eb0df74f6bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionDefaultCacheBehavior",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_methods": "allowedMethods",
        "cached_methods": "cachedMethods",
        "target_origin_id": "targetOriginId",
        "viewer_protocol_policy": "viewerProtocolPolicy",
        "cache_policy_id": "cachePolicyId",
        "compress": "compress",
        "default_ttl": "defaultTtl",
        "field_level_encryption_id": "fieldLevelEncryptionId",
        "forwarded_values": "forwardedValues",
        "function_association": "functionAssociation",
        "grpc_config": "grpcConfig",
        "lambda_function_association": "lambdaFunctionAssociation",
        "max_ttl": "maxTtl",
        "min_ttl": "minTtl",
        "origin_request_policy_id": "originRequestPolicyId",
        "realtime_log_config_arn": "realtimeLogConfigArn",
        "response_headers_policy_id": "responseHeadersPolicyId",
        "smooth_streaming": "smoothStreaming",
        "trusted_key_groups": "trustedKeyGroups",
        "trusted_signers": "trustedSigners",
    },
)
class CloudfrontDistributionDefaultCacheBehavior:
    def __init__(
        self,
        *,
        allowed_methods: typing.Sequence[builtins.str],
        cached_methods: typing.Sequence[builtins.str],
        target_origin_id: builtins.str,
        viewer_protocol_policy: builtins.str,
        cache_policy_id: typing.Optional[builtins.str] = None,
        compress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        field_level_encryption_id: typing.Optional[builtins.str] = None,
        forwarded_values: typing.Optional[typing.Union["CloudfrontDistributionDefaultCacheBehaviorForwardedValues", typing.Dict[builtins.str, typing.Any]]] = None,
        function_association: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        grpc_config: typing.Optional[typing.Union["CloudfrontDistributionDefaultCacheBehaviorGrpcConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_function_association: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_ttl: typing.Optional[jsii.Number] = None,
        min_ttl: typing.Optional[jsii.Number] = None,
        origin_request_policy_id: typing.Optional[builtins.str] = None,
        realtime_log_config_arn: typing.Optional[builtins.str] = None,
        response_headers_policy_id: typing.Optional[builtins.str] = None,
        smooth_streaming: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        trusted_key_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        trusted_signers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#allowed_methods CloudfrontDistribution#allowed_methods}.
        :param cached_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#cached_methods CloudfrontDistribution#cached_methods}.
        :param target_origin_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#target_origin_id CloudfrontDistribution#target_origin_id}.
        :param viewer_protocol_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#viewer_protocol_policy CloudfrontDistribution#viewer_protocol_policy}.
        :param cache_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#cache_policy_id CloudfrontDistribution#cache_policy_id}.
        :param compress: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#compress CloudfrontDistribution#compress}.
        :param default_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#default_ttl CloudfrontDistribution#default_ttl}.
        :param field_level_encryption_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#field_level_encryption_id CloudfrontDistribution#field_level_encryption_id}.
        :param forwarded_values: forwarded_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#forwarded_values CloudfrontDistribution#forwarded_values}
        :param function_association: function_association block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#function_association CloudfrontDistribution#function_association}
        :param grpc_config: grpc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#grpc_config CloudfrontDistribution#grpc_config}
        :param lambda_function_association: lambda_function_association block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#lambda_function_association CloudfrontDistribution#lambda_function_association}
        :param max_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#max_ttl CloudfrontDistribution#max_ttl}.
        :param min_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#min_ttl CloudfrontDistribution#min_ttl}.
        :param origin_request_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_request_policy_id CloudfrontDistribution#origin_request_policy_id}.
        :param realtime_log_config_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#realtime_log_config_arn CloudfrontDistribution#realtime_log_config_arn}.
        :param response_headers_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#response_headers_policy_id CloudfrontDistribution#response_headers_policy_id}.
        :param smooth_streaming: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#smooth_streaming CloudfrontDistribution#smooth_streaming}.
        :param trusted_key_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#trusted_key_groups CloudfrontDistribution#trusted_key_groups}.
        :param trusted_signers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#trusted_signers CloudfrontDistribution#trusted_signers}.
        '''
        if isinstance(forwarded_values, dict):
            forwarded_values = CloudfrontDistributionDefaultCacheBehaviorForwardedValues(**forwarded_values)
        if isinstance(grpc_config, dict):
            grpc_config = CloudfrontDistributionDefaultCacheBehaviorGrpcConfig(**grpc_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8da0babe2622ca73b92bd536cb65d3054373a9e50240c7ae5e960eccd8a82c84)
            check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
            check_type(argname="argument cached_methods", value=cached_methods, expected_type=type_hints["cached_methods"])
            check_type(argname="argument target_origin_id", value=target_origin_id, expected_type=type_hints["target_origin_id"])
            check_type(argname="argument viewer_protocol_policy", value=viewer_protocol_policy, expected_type=type_hints["viewer_protocol_policy"])
            check_type(argname="argument cache_policy_id", value=cache_policy_id, expected_type=type_hints["cache_policy_id"])
            check_type(argname="argument compress", value=compress, expected_type=type_hints["compress"])
            check_type(argname="argument default_ttl", value=default_ttl, expected_type=type_hints["default_ttl"])
            check_type(argname="argument field_level_encryption_id", value=field_level_encryption_id, expected_type=type_hints["field_level_encryption_id"])
            check_type(argname="argument forwarded_values", value=forwarded_values, expected_type=type_hints["forwarded_values"])
            check_type(argname="argument function_association", value=function_association, expected_type=type_hints["function_association"])
            check_type(argname="argument grpc_config", value=grpc_config, expected_type=type_hints["grpc_config"])
            check_type(argname="argument lambda_function_association", value=lambda_function_association, expected_type=type_hints["lambda_function_association"])
            check_type(argname="argument max_ttl", value=max_ttl, expected_type=type_hints["max_ttl"])
            check_type(argname="argument min_ttl", value=min_ttl, expected_type=type_hints["min_ttl"])
            check_type(argname="argument origin_request_policy_id", value=origin_request_policy_id, expected_type=type_hints["origin_request_policy_id"])
            check_type(argname="argument realtime_log_config_arn", value=realtime_log_config_arn, expected_type=type_hints["realtime_log_config_arn"])
            check_type(argname="argument response_headers_policy_id", value=response_headers_policy_id, expected_type=type_hints["response_headers_policy_id"])
            check_type(argname="argument smooth_streaming", value=smooth_streaming, expected_type=type_hints["smooth_streaming"])
            check_type(argname="argument trusted_key_groups", value=trusted_key_groups, expected_type=type_hints["trusted_key_groups"])
            check_type(argname="argument trusted_signers", value=trusted_signers, expected_type=type_hints["trusted_signers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_methods": allowed_methods,
            "cached_methods": cached_methods,
            "target_origin_id": target_origin_id,
            "viewer_protocol_policy": viewer_protocol_policy,
        }
        if cache_policy_id is not None:
            self._values["cache_policy_id"] = cache_policy_id
        if compress is not None:
            self._values["compress"] = compress
        if default_ttl is not None:
            self._values["default_ttl"] = default_ttl
        if field_level_encryption_id is not None:
            self._values["field_level_encryption_id"] = field_level_encryption_id
        if forwarded_values is not None:
            self._values["forwarded_values"] = forwarded_values
        if function_association is not None:
            self._values["function_association"] = function_association
        if grpc_config is not None:
            self._values["grpc_config"] = grpc_config
        if lambda_function_association is not None:
            self._values["lambda_function_association"] = lambda_function_association
        if max_ttl is not None:
            self._values["max_ttl"] = max_ttl
        if min_ttl is not None:
            self._values["min_ttl"] = min_ttl
        if origin_request_policy_id is not None:
            self._values["origin_request_policy_id"] = origin_request_policy_id
        if realtime_log_config_arn is not None:
            self._values["realtime_log_config_arn"] = realtime_log_config_arn
        if response_headers_policy_id is not None:
            self._values["response_headers_policy_id"] = response_headers_policy_id
        if smooth_streaming is not None:
            self._values["smooth_streaming"] = smooth_streaming
        if trusted_key_groups is not None:
            self._values["trusted_key_groups"] = trusted_key_groups
        if trusted_signers is not None:
            self._values["trusted_signers"] = trusted_signers

    @builtins.property
    def allowed_methods(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#allowed_methods CloudfrontDistribution#allowed_methods}.'''
        result = self._values.get("allowed_methods")
        assert result is not None, "Required property 'allowed_methods' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cached_methods(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#cached_methods CloudfrontDistribution#cached_methods}.'''
        result = self._values.get("cached_methods")
        assert result is not None, "Required property 'cached_methods' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def target_origin_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#target_origin_id CloudfrontDistribution#target_origin_id}.'''
        result = self._values.get("target_origin_id")
        assert result is not None, "Required property 'target_origin_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def viewer_protocol_policy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#viewer_protocol_policy CloudfrontDistribution#viewer_protocol_policy}.'''
        result = self._values.get("viewer_protocol_policy")
        assert result is not None, "Required property 'viewer_protocol_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cache_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#cache_policy_id CloudfrontDistribution#cache_policy_id}.'''
        result = self._values.get("cache_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compress(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#compress CloudfrontDistribution#compress}.'''
        result = self._values.get("compress")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def default_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#default_ttl CloudfrontDistribution#default_ttl}.'''
        result = self._values.get("default_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def field_level_encryption_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#field_level_encryption_id CloudfrontDistribution#field_level_encryption_id}.'''
        result = self._values.get("field_level_encryption_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forwarded_values(
        self,
    ) -> typing.Optional["CloudfrontDistributionDefaultCacheBehaviorForwardedValues"]:
        '''forwarded_values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#forwarded_values CloudfrontDistribution#forwarded_values}
        '''
        result = self._values.get("forwarded_values")
        return typing.cast(typing.Optional["CloudfrontDistributionDefaultCacheBehaviorForwardedValues"], result)

    @builtins.property
    def function_association(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation"]]]:
        '''function_association block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#function_association CloudfrontDistribution#function_association}
        '''
        result = self._values.get("function_association")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation"]]], result)

    @builtins.property
    def grpc_config(
        self,
    ) -> typing.Optional["CloudfrontDistributionDefaultCacheBehaviorGrpcConfig"]:
        '''grpc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#grpc_config CloudfrontDistribution#grpc_config}
        '''
        result = self._values.get("grpc_config")
        return typing.cast(typing.Optional["CloudfrontDistributionDefaultCacheBehaviorGrpcConfig"], result)

    @builtins.property
    def lambda_function_association(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation"]]]:
        '''lambda_function_association block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#lambda_function_association CloudfrontDistribution#lambda_function_association}
        '''
        result = self._values.get("lambda_function_association")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation"]]], result)

    @builtins.property
    def max_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#max_ttl CloudfrontDistribution#max_ttl}.'''
        result = self._values.get("max_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#min_ttl CloudfrontDistribution#min_ttl}.'''
        result = self._values.get("min_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def origin_request_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_request_policy_id CloudfrontDistribution#origin_request_policy_id}.'''
        result = self._values.get("origin_request_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def realtime_log_config_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#realtime_log_config_arn CloudfrontDistribution#realtime_log_config_arn}.'''
        result = self._values.get("realtime_log_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_headers_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#response_headers_policy_id CloudfrontDistribution#response_headers_policy_id}.'''
        result = self._values.get("response_headers_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def smooth_streaming(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#smooth_streaming CloudfrontDistribution#smooth_streaming}.'''
        result = self._values.get("smooth_streaming")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def trusted_key_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#trusted_key_groups CloudfrontDistribution#trusted_key_groups}.'''
        result = self._values.get("trusted_key_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def trusted_signers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#trusted_signers CloudfrontDistribution#trusted_signers}.'''
        result = self._values.get("trusted_signers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionDefaultCacheBehavior(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionDefaultCacheBehaviorForwardedValues",
    jsii_struct_bases=[],
    name_mapping={
        "cookies": "cookies",
        "query_string": "queryString",
        "headers": "headers",
        "query_string_cache_keys": "queryStringCacheKeys",
    },
)
class CloudfrontDistributionDefaultCacheBehaviorForwardedValues:
    def __init__(
        self,
        *,
        cookies: typing.Union["CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies", typing.Dict[builtins.str, typing.Any]],
        query_string: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_cache_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cookies: cookies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#cookies CloudfrontDistribution#cookies}
        :param query_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#query_string CloudfrontDistribution#query_string}.
        :param headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#headers CloudfrontDistribution#headers}.
        :param query_string_cache_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#query_string_cache_keys CloudfrontDistribution#query_string_cache_keys}.
        '''
        if isinstance(cookies, dict):
            cookies = CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies(**cookies)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2958489a8ad983fd9752df72108d42306a99c56d0e015f9b8b3ed4f594d83593)
            check_type(argname="argument cookies", value=cookies, expected_type=type_hints["cookies"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument query_string_cache_keys", value=query_string_cache_keys, expected_type=type_hints["query_string_cache_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cookies": cookies,
            "query_string": query_string,
        }
        if headers is not None:
            self._values["headers"] = headers
        if query_string_cache_keys is not None:
            self._values["query_string_cache_keys"] = query_string_cache_keys

    @builtins.property
    def cookies(
        self,
    ) -> "CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies":
        '''cookies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#cookies CloudfrontDistribution#cookies}
        '''
        result = self._values.get("cookies")
        assert result is not None, "Required property 'cookies' is missing"
        return typing.cast("CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies", result)

    @builtins.property
    def query_string(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#query_string CloudfrontDistribution#query_string}.'''
        result = self._values.get("query_string")
        assert result is not None, "Required property 'query_string' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#headers CloudfrontDistribution#headers}.'''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def query_string_cache_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#query_string_cache_keys CloudfrontDistribution#query_string_cache_keys}.'''
        result = self._values.get("query_string_cache_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionDefaultCacheBehaviorForwardedValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies",
    jsii_struct_bases=[],
    name_mapping={"forward": "forward", "whitelisted_names": "whitelistedNames"},
)
class CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies:
    def __init__(
        self,
        *,
        forward: builtins.str,
        whitelisted_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param forward: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#forward CloudfrontDistribution#forward}.
        :param whitelisted_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#whitelisted_names CloudfrontDistribution#whitelisted_names}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afdd8ef36313698961fc250b283111d2c3e7a6822ddf7e7f6766727ed07769c8)
            check_type(argname="argument forward", value=forward, expected_type=type_hints["forward"])
            check_type(argname="argument whitelisted_names", value=whitelisted_names, expected_type=type_hints["whitelisted_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "forward": forward,
        }
        if whitelisted_names is not None:
            self._values["whitelisted_names"] = whitelisted_names

    @builtins.property
    def forward(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#forward CloudfrontDistribution#forward}.'''
        result = self._values.get("forward")
        assert result is not None, "Required property 'forward' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def whitelisted_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#whitelisted_names CloudfrontDistribution#whitelisted_names}.'''
        result = self._values.get("whitelisted_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__977d7efc21860bf92b3dd2241b39379b4d6489bf201b198c2f5f7da65d4995a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetWhitelistedNames")
    def reset_whitelisted_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWhitelistedNames", []))

    @builtins.property
    @jsii.member(jsii_name="forwardInput")
    def forward_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forwardInput"))

    @builtins.property
    @jsii.member(jsii_name="whitelistedNamesInput")
    def whitelisted_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "whitelistedNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="forward")
    def forward(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forward"))

    @forward.setter
    def forward(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c8ce14bf5d299b86427552c34fbee8dcb7d06de948821a129b45f17f87ccda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forward", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="whitelistedNames")
    def whitelisted_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "whitelistedNames"))

    @whitelisted_names.setter
    def whitelisted_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74d758c8f9cc4b23b18cd6c2f6bafb86e384cfd42ff06309e60600ca43267f30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "whitelistedNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies]:
        return typing.cast(typing.Optional[CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e3c2821f5f87c2a0f28e53108ddbb8679951585ceeb4bbd55d527016a4ea989)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionDefaultCacheBehaviorForwardedValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionDefaultCacheBehaviorForwardedValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb88192d3b855dc3d0ef5e18e40035a0ffcf8f110daca25d479911dead093723)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCookies")
    def put_cookies(
        self,
        *,
        forward: builtins.str,
        whitelisted_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param forward: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#forward CloudfrontDistribution#forward}.
        :param whitelisted_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#whitelisted_names CloudfrontDistribution#whitelisted_names}.
        '''
        value = CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies(
            forward=forward, whitelisted_names=whitelisted_names
        )

        return typing.cast(None, jsii.invoke(self, "putCookies", [value]))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @jsii.member(jsii_name="resetQueryStringCacheKeys")
    def reset_query_string_cache_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryStringCacheKeys", []))

    @builtins.property
    @jsii.member(jsii_name="cookies")
    def cookies(
        self,
    ) -> CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookiesOutputReference:
        return typing.cast(CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookiesOutputReference, jsii.get(self, "cookies"))

    @builtins.property
    @jsii.member(jsii_name="cookiesInput")
    def cookies_input(
        self,
    ) -> typing.Optional[CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies]:
        return typing.cast(typing.Optional[CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies], jsii.get(self, "cookiesInput"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringCacheKeysInput")
    def query_string_cache_keys_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queryStringCacheKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringInput")
    def query_string_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "queryStringInput"))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "headers"))

    @headers.setter
    def headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e55ae64592d6e33d7710eb1904e2c2ac6b3eb6a46619c364a33017ce690f72c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryString")
    def query_string(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "queryString"))

    @query_string.setter
    def query_string(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__885f45347497938eca1436141f7ab0d8ee4ece620ca902997bc7f40c0521c38a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringCacheKeys")
    def query_string_cache_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queryStringCacheKeys"))

    @query_string_cache_keys.setter
    def query_string_cache_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ab4cfc3e1c98353965dc5d3798102b696a86cb4f6ab50651f8b15696ce53443)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringCacheKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontDistributionDefaultCacheBehaviorForwardedValues]:
        return typing.cast(typing.Optional[CloudfrontDistributionDefaultCacheBehaviorForwardedValues], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionDefaultCacheBehaviorForwardedValues],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__310189ae4609a68a1893d31b062c7456533ff802b8c4d1c22cb67c02394faa98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation",
    jsii_struct_bases=[],
    name_mapping={"event_type": "eventType", "function_arn": "functionArn"},
)
class CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation:
    def __init__(self, *, event_type: builtins.str, function_arn: builtins.str) -> None:
        '''
        :param event_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#event_type CloudfrontDistribution#event_type}.
        :param function_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#function_arn CloudfrontDistribution#function_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65da29b8d3d2bf3d03b6ae00dbc177f563bd35a04b03c1a0cd1eec048ba87f85)
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_type": event_type,
            "function_arn": function_arn,
        }

    @builtins.property
    def event_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#event_type CloudfrontDistribution#event_type}.'''
        result = self._values.get("event_type")
        assert result is not None, "Required property 'event_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def function_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#function_arn CloudfrontDistribution#function_arn}.'''
        result = self._values.get("function_arn")
        assert result is not None, "Required property 'function_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionDefaultCacheBehaviorFunctionAssociationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionDefaultCacheBehaviorFunctionAssociationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b9a1cd80f1b06d93e300c6c23d62b702cd096bcfc4f2d8da9762ee1441052e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontDistributionDefaultCacheBehaviorFunctionAssociationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8014e0fd903b33fa23e9efdd31fe96e9595bbf58c8ab685ea81e944d4b59cc51)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontDistributionDefaultCacheBehaviorFunctionAssociationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd06e86fafee34197e0e9f3a55f0a29233c63807e5eb4c4a420830f086b9d4e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b92e8f795480bb2da5e83e4d3f62013d4a4b20c0def938f5484f2a3871f88212)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a387a37bff151eee6e9590ca8bbf55215eb0195d46d35bf3f23d2b5cad4017f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fe8212e43fa5a1512638e711eed8c0fc5ead243cefa5cb3002035fa18b60faf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionDefaultCacheBehaviorFunctionAssociationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionDefaultCacheBehaviorFunctionAssociationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e82723574d83b6f8ffc06718b5260286b3fcebf3fa342613f65759298aa563c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="eventTypeInput")
    def event_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="functionArnInput")
    def function_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="eventType")
    def event_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventType"))

    @event_type.setter
    def event_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c35bf5fecef7b676006fee586097defc9276166527706d021b82193f3a9c1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionArn"))

    @function_arn.setter
    def function_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3dfeebbe6d22b638fed685ad0f5854121901a1f32e84331021cc2a0f9ae06ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3621e70c2baae7a5be4029a0e29cc46c536e837719e5ea2df6b133c475cc0958)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionDefaultCacheBehaviorGrpcConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class CloudfrontDistributionDefaultCacheBehaviorGrpcConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#enabled CloudfrontDistribution#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bfa838e5b0ba28cafe1f68733e2c281923c81963745f8ed3c171c8236032125)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#enabled CloudfrontDistribution#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionDefaultCacheBehaviorGrpcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionDefaultCacheBehaviorGrpcConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionDefaultCacheBehaviorGrpcConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d63461a283761e6615101ec89435e3bdd166d2d92976fb4b6c4120d4b62fc34a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__69a7df54d92f349cd445a6d03a3191b3dad76e5f21a87c6dea445a933e188fcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontDistributionDefaultCacheBehaviorGrpcConfig]:
        return typing.cast(typing.Optional[CloudfrontDistributionDefaultCacheBehaviorGrpcConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionDefaultCacheBehaviorGrpcConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee97fd16d3dea579890a8499c227e42245eebcf04c6e49376799e7229bcacd5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation",
    jsii_struct_bases=[],
    name_mapping={
        "event_type": "eventType",
        "lambda_arn": "lambdaArn",
        "include_body": "includeBody",
    },
)
class CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation:
    def __init__(
        self,
        *,
        event_type: builtins.str,
        lambda_arn: builtins.str,
        include_body: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param event_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#event_type CloudfrontDistribution#event_type}.
        :param lambda_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#lambda_arn CloudfrontDistribution#lambda_arn}.
        :param include_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#include_body CloudfrontDistribution#include_body}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ed01d8eb9beb1253ea561d8466da04f6efdae02a848c3259e50dcf02b9a9e7)
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
            check_type(argname="argument include_body", value=include_body, expected_type=type_hints["include_body"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_type": event_type,
            "lambda_arn": lambda_arn,
        }
        if include_body is not None:
            self._values["include_body"] = include_body

    @builtins.property
    def event_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#event_type CloudfrontDistribution#event_type}.'''
        result = self._values.get("event_type")
        assert result is not None, "Required property 'event_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lambda_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#lambda_arn CloudfrontDistribution#lambda_arn}.'''
        result = self._values.get("lambda_arn")
        assert result is not None, "Required property 'lambda_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include_body(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#include_body CloudfrontDistribution#include_body}.'''
        result = self._values.get("include_body")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1947cf193ecd3e22d31f810e1cd52c05c24df683d5d9efcecb2a5da754266293)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b0866eba6159126b477c1b7d20afe12778b287f387f56bd7ca7586b6b6d60c9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e03acade586ca12737d4108b157e827620eca670a0f55773cc42de65af8a1045)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c43406a952d564a0b056c4d7c2a6367dab8d7a93b0b52cd7e33268cfb3a46a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e19a18a7396f207407b1abe26f42bd243a6d69937b6429b338dbaf5b2e010e71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051db0f0e9c2df45238b0c9ae49893cf0f186e599732a4c84e4fc76fcea9fdea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70b9dd2b29db3e910b91909396af4b283ed9e67fcfa311efaf06d21613d9dea0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIncludeBody")
    def reset_include_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeBody", []))

    @builtins.property
    @jsii.member(jsii_name="eventTypeInput")
    def event_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="includeBodyInput")
    def include_body_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaArnInput")
    def lambda_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lambdaArnInput"))

    @builtins.property
    @jsii.member(jsii_name="eventType")
    def event_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventType"))

    @event_type.setter
    def event_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ee51287f8bdc38d8a85fd77484a61d264fbe819c00836401cbe7ed356187d49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeBody")
    def include_body(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeBody"))

    @include_body.setter
    def include_body(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__457866f3fab2303502e29d146b661bcd567c381e57115563913d9ffe583d82bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lambdaArn")
    def lambda_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lambdaArn"))

    @lambda_arn.setter
    def lambda_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b1ad34c863f822d330c45d047c2a8efa2848b9a4a6ab9de08f8f4213575eae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99c753ab2d1236a884e86c9b693611614f7453a654a6a11e2998b3f327caef40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionDefaultCacheBehaviorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionDefaultCacheBehaviorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b4e38f2c4050a5cf2241d4488a1fd87f1ed66d012fe7ae41cf997b120f760d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putForwardedValues")
    def put_forwarded_values(
        self,
        *,
        cookies: typing.Union[CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies, typing.Dict[builtins.str, typing.Any]],
        query_string: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_cache_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cookies: cookies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#cookies CloudfrontDistribution#cookies}
        :param query_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#query_string CloudfrontDistribution#query_string}.
        :param headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#headers CloudfrontDistribution#headers}.
        :param query_string_cache_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#query_string_cache_keys CloudfrontDistribution#query_string_cache_keys}.
        '''
        value = CloudfrontDistributionDefaultCacheBehaviorForwardedValues(
            cookies=cookies,
            query_string=query_string,
            headers=headers,
            query_string_cache_keys=query_string_cache_keys,
        )

        return typing.cast(None, jsii.invoke(self, "putForwardedValues", [value]))

    @jsii.member(jsii_name="putFunctionAssociation")
    def put_function_association(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9366100fbcc7734185b03eb5fde859225e6036fbf96f7a73315a424c8ccac17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFunctionAssociation", [value]))

    @jsii.member(jsii_name="putGrpcConfig")
    def put_grpc_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#enabled CloudfrontDistribution#enabled}.
        '''
        value = CloudfrontDistributionDefaultCacheBehaviorGrpcConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putGrpcConfig", [value]))

    @jsii.member(jsii_name="putLambdaFunctionAssociation")
    def put_lambda_function_association(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__224c6a63827f2e67981ab40775bf69fdbca7ccf07994fd88ebfac4ed96c478a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLambdaFunctionAssociation", [value]))

    @jsii.member(jsii_name="resetCachePolicyId")
    def reset_cache_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCachePolicyId", []))

    @jsii.member(jsii_name="resetCompress")
    def reset_compress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompress", []))

    @jsii.member(jsii_name="resetDefaultTtl")
    def reset_default_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTtl", []))

    @jsii.member(jsii_name="resetFieldLevelEncryptionId")
    def reset_field_level_encryption_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldLevelEncryptionId", []))

    @jsii.member(jsii_name="resetForwardedValues")
    def reset_forwarded_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardedValues", []))

    @jsii.member(jsii_name="resetFunctionAssociation")
    def reset_function_association(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunctionAssociation", []))

    @jsii.member(jsii_name="resetGrpcConfig")
    def reset_grpc_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpcConfig", []))

    @jsii.member(jsii_name="resetLambdaFunctionAssociation")
    def reset_lambda_function_association(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaFunctionAssociation", []))

    @jsii.member(jsii_name="resetMaxTtl")
    def reset_max_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxTtl", []))

    @jsii.member(jsii_name="resetMinTtl")
    def reset_min_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinTtl", []))

    @jsii.member(jsii_name="resetOriginRequestPolicyId")
    def reset_origin_request_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginRequestPolicyId", []))

    @jsii.member(jsii_name="resetRealtimeLogConfigArn")
    def reset_realtime_log_config_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRealtimeLogConfigArn", []))

    @jsii.member(jsii_name="resetResponseHeadersPolicyId")
    def reset_response_headers_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseHeadersPolicyId", []))

    @jsii.member(jsii_name="resetSmoothStreaming")
    def reset_smooth_streaming(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmoothStreaming", []))

    @jsii.member(jsii_name="resetTrustedKeyGroups")
    def reset_trusted_key_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedKeyGroups", []))

    @jsii.member(jsii_name="resetTrustedSigners")
    def reset_trusted_signers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedSigners", []))

    @builtins.property
    @jsii.member(jsii_name="forwardedValues")
    def forwarded_values(
        self,
    ) -> CloudfrontDistributionDefaultCacheBehaviorForwardedValuesOutputReference:
        return typing.cast(CloudfrontDistributionDefaultCacheBehaviorForwardedValuesOutputReference, jsii.get(self, "forwardedValues"))

    @builtins.property
    @jsii.member(jsii_name="functionAssociation")
    def function_association(
        self,
    ) -> CloudfrontDistributionDefaultCacheBehaviorFunctionAssociationList:
        return typing.cast(CloudfrontDistributionDefaultCacheBehaviorFunctionAssociationList, jsii.get(self, "functionAssociation"))

    @builtins.property
    @jsii.member(jsii_name="grpcConfig")
    def grpc_config(
        self,
    ) -> CloudfrontDistributionDefaultCacheBehaviorGrpcConfigOutputReference:
        return typing.cast(CloudfrontDistributionDefaultCacheBehaviorGrpcConfigOutputReference, jsii.get(self, "grpcConfig"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionAssociation")
    def lambda_function_association(
        self,
    ) -> CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociationList:
        return typing.cast(CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociationList, jsii.get(self, "lambdaFunctionAssociation"))

    @builtins.property
    @jsii.member(jsii_name="allowedMethodsInput")
    def allowed_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="cachedMethodsInput")
    def cached_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cachedMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="cachePolicyIdInput")
    def cache_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cachePolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="compressInput")
    def compress_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "compressInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTtlInput")
    def default_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldLevelEncryptionIdInput")
    def field_level_encryption_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldLevelEncryptionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardedValuesInput")
    def forwarded_values_input(
        self,
    ) -> typing.Optional[CloudfrontDistributionDefaultCacheBehaviorForwardedValues]:
        return typing.cast(typing.Optional[CloudfrontDistributionDefaultCacheBehaviorForwardedValues], jsii.get(self, "forwardedValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="functionAssociationInput")
    def function_association_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation]]], jsii.get(self, "functionAssociationInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcConfigInput")
    def grpc_config_input(
        self,
    ) -> typing.Optional[CloudfrontDistributionDefaultCacheBehaviorGrpcConfig]:
        return typing.cast(typing.Optional[CloudfrontDistributionDefaultCacheBehaviorGrpcConfig], jsii.get(self, "grpcConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionAssociationInput")
    def lambda_function_association_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation]]], jsii.get(self, "lambdaFunctionAssociationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxTtlInput")
    def max_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="minTtlInput")
    def min_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="originRequestPolicyIdInput")
    def origin_request_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originRequestPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="realtimeLogConfigArnInput")
    def realtime_log_config_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "realtimeLogConfigArnInput"))

    @builtins.property
    @jsii.member(jsii_name="responseHeadersPolicyIdInput")
    def response_headers_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseHeadersPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="smoothStreamingInput")
    def smooth_streaming_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "smoothStreamingInput"))

    @builtins.property
    @jsii.member(jsii_name="targetOriginIdInput")
    def target_origin_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetOriginIdInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedKeyGroupsInput")
    def trusted_key_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "trustedKeyGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedSignersInput")
    def trusted_signers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "trustedSignersInput"))

    @builtins.property
    @jsii.member(jsii_name="viewerProtocolPolicyInput")
    def viewer_protocol_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "viewerProtocolPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedMethods")
    def allowed_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedMethods"))

    @allowed_methods.setter
    def allowed_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb681a4e747c920b374a24c0a1e8564958ce5c5d49d0f78596ca6ccfd912e20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cachedMethods")
    def cached_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cachedMethods"))

    @cached_methods.setter
    def cached_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab847365125ec359a4e36a4527377e10a409e85d511e1e373516f2aaf2e961f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cachedMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cachePolicyId")
    def cache_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cachePolicyId"))

    @cache_policy_id.setter
    def cache_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f72fab6ed020275604802901b9a51e32744190983c09e7a0159419a94f40deb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cachePolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="compress")
    def compress(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "compress"))

    @compress.setter
    def compress(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26397b5f40ac3fb32365514cb54c736277f56e62ec3157805a02529364cf3d2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTtl")
    def default_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultTtl"))

    @default_ttl.setter
    def default_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3bdb986a6ea7b252ca3fa0c7d013a06bc9b0066b13671c827b88b71d74bca1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fieldLevelEncryptionId")
    def field_level_encryption_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldLevelEncryptionId"))

    @field_level_encryption_id.setter
    def field_level_encryption_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c305007ee769cfafb6d2099e1a87d4968266d411e288da929e0115a9086e63f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldLevelEncryptionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxTtl")
    def max_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxTtl"))

    @max_ttl.setter
    def max_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e675552b61bfa75e398748f0860fbea9de9031cdb3d5afd398b79547ddebc86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minTtl")
    def min_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minTtl"))

    @min_ttl.setter
    def min_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10ff939293494b12fc38e4d1e1ed79fd72aff425409d6a99d84c6b9df7f44853)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originRequestPolicyId")
    def origin_request_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originRequestPolicyId"))

    @origin_request_policy_id.setter
    def origin_request_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec57c7aea7de5c9fab628fb2de6f4ac012308b91515fb024dda44d1100a4f79e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originRequestPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="realtimeLogConfigArn")
    def realtime_log_config_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "realtimeLogConfigArn"))

    @realtime_log_config_arn.setter
    def realtime_log_config_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fea5adaf39e3a19d2c4dca958083d5f67697cf5d2d2cb81e5b0b4a79f57c46f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "realtimeLogConfigArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseHeadersPolicyId")
    def response_headers_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseHeadersPolicyId"))

    @response_headers_policy_id.setter
    def response_headers_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e1621f459e3522f90083d3488962d14f724eac4cf41140525e127edce2fa8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseHeadersPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="smoothStreaming")
    def smooth_streaming(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "smoothStreaming"))

    @smooth_streaming.setter
    def smooth_streaming(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02d7c70dfde84c1ad0b7a10192a363dd96f98a793e2fcc8907a36ba78a0b99fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smoothStreaming", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetOriginId")
    def target_origin_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetOriginId"))

    @target_origin_id.setter
    def target_origin_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__986ffd05b8ba5e86055d86908504810136da10ed205fc7ab4639ac58f982e394)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetOriginId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustedKeyGroups")
    def trusted_key_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "trustedKeyGroups"))

    @trusted_key_groups.setter
    def trusted_key_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c17e7f37c871458a6780dadf04ee2b4659981315c589e060b965ae0623ba8a38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedKeyGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustedSigners")
    def trusted_signers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "trustedSigners"))

    @trusted_signers.setter
    def trusted_signers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e3886725a0512fa4880630da7838add020f1853e472ad4490b55e06e3a05a45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedSigners", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="viewerProtocolPolicy")
    def viewer_protocol_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "viewerProtocolPolicy"))

    @viewer_protocol_policy.setter
    def viewer_protocol_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfe3f2193d9314ea754e3ec461db0d5c62dbb5467d47f029454ad7631d1eecd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "viewerProtocolPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontDistributionDefaultCacheBehavior]:
        return typing.cast(typing.Optional[CloudfrontDistributionDefaultCacheBehavior], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionDefaultCacheBehavior],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b78c0025ceaacb8a86f0693fb59345ddea6945e87cf1ca81e59e089d85eb840e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "include_cookies": "includeCookies",
        "prefix": "prefix",
    },
)
class CloudfrontDistributionLoggingConfig:
    def __init__(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        include_cookies: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#bucket CloudfrontDistribution#bucket}.
        :param include_cookies: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#include_cookies CloudfrontDistribution#include_cookies}.
        :param prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#prefix CloudfrontDistribution#prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__836d73ffe7c9e47a9daaec8b9194430d6da21f1150a066afbd4da3d229456c62)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument include_cookies", value=include_cookies, expected_type=type_hints["include_cookies"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket
        if include_cookies is not None:
            self._values["include_cookies"] = include_cookies
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#bucket CloudfrontDistribution#bucket}.'''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_cookies(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#include_cookies CloudfrontDistribution#include_cookies}.'''
        result = self._values.get("include_cookies")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#prefix CloudfrontDistribution#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99142b0782db984627518fd6daed8a91c704702a03681b175fc22be37843ffc5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucket")
    def reset_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucket", []))

    @jsii.member(jsii_name="resetIncludeCookies")
    def reset_include_cookies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeCookies", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="includeCookiesInput")
    def include_cookies_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeCookiesInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__336fb057503f0dd85b1cde0a896d5df858053ce2c3501c1aa37334a5c9dfbeba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeCookies")
    def include_cookies(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeCookies"))

    @include_cookies.setter
    def include_cookies(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02718a4ea5309e329c02391109f382afd1ba3b37137ad8f520d44818088b11dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeCookies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86069df8ad95c2f9ecab8056aa20216b269d1b47348a108c1ff05c1b1f6814b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudfrontDistributionLoggingConfig]:
        return typing.cast(typing.Optional[CloudfrontDistributionLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cee46a6db9455f5fd1e5e7f21009434ce58f547e65cde8f3873cecdfb736f1cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOrderedCacheBehavior",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_methods": "allowedMethods",
        "cached_methods": "cachedMethods",
        "path_pattern": "pathPattern",
        "target_origin_id": "targetOriginId",
        "viewer_protocol_policy": "viewerProtocolPolicy",
        "cache_policy_id": "cachePolicyId",
        "compress": "compress",
        "default_ttl": "defaultTtl",
        "field_level_encryption_id": "fieldLevelEncryptionId",
        "forwarded_values": "forwardedValues",
        "function_association": "functionAssociation",
        "grpc_config": "grpcConfig",
        "lambda_function_association": "lambdaFunctionAssociation",
        "max_ttl": "maxTtl",
        "min_ttl": "minTtl",
        "origin_request_policy_id": "originRequestPolicyId",
        "realtime_log_config_arn": "realtimeLogConfigArn",
        "response_headers_policy_id": "responseHeadersPolicyId",
        "smooth_streaming": "smoothStreaming",
        "trusted_key_groups": "trustedKeyGroups",
        "trusted_signers": "trustedSigners",
    },
)
class CloudfrontDistributionOrderedCacheBehavior:
    def __init__(
        self,
        *,
        allowed_methods: typing.Sequence[builtins.str],
        cached_methods: typing.Sequence[builtins.str],
        path_pattern: builtins.str,
        target_origin_id: builtins.str,
        viewer_protocol_policy: builtins.str,
        cache_policy_id: typing.Optional[builtins.str] = None,
        compress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        field_level_encryption_id: typing.Optional[builtins.str] = None,
        forwarded_values: typing.Optional[typing.Union["CloudfrontDistributionOrderedCacheBehaviorForwardedValues", typing.Dict[builtins.str, typing.Any]]] = None,
        function_association: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontDistributionOrderedCacheBehaviorFunctionAssociation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        grpc_config: typing.Optional[typing.Union["CloudfrontDistributionOrderedCacheBehaviorGrpcConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_function_association: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_ttl: typing.Optional[jsii.Number] = None,
        min_ttl: typing.Optional[jsii.Number] = None,
        origin_request_policy_id: typing.Optional[builtins.str] = None,
        realtime_log_config_arn: typing.Optional[builtins.str] = None,
        response_headers_policy_id: typing.Optional[builtins.str] = None,
        smooth_streaming: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        trusted_key_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        trusted_signers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#allowed_methods CloudfrontDistribution#allowed_methods}.
        :param cached_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#cached_methods CloudfrontDistribution#cached_methods}.
        :param path_pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#path_pattern CloudfrontDistribution#path_pattern}.
        :param target_origin_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#target_origin_id CloudfrontDistribution#target_origin_id}.
        :param viewer_protocol_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#viewer_protocol_policy CloudfrontDistribution#viewer_protocol_policy}.
        :param cache_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#cache_policy_id CloudfrontDistribution#cache_policy_id}.
        :param compress: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#compress CloudfrontDistribution#compress}.
        :param default_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#default_ttl CloudfrontDistribution#default_ttl}.
        :param field_level_encryption_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#field_level_encryption_id CloudfrontDistribution#field_level_encryption_id}.
        :param forwarded_values: forwarded_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#forwarded_values CloudfrontDistribution#forwarded_values}
        :param function_association: function_association block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#function_association CloudfrontDistribution#function_association}
        :param grpc_config: grpc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#grpc_config CloudfrontDistribution#grpc_config}
        :param lambda_function_association: lambda_function_association block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#lambda_function_association CloudfrontDistribution#lambda_function_association}
        :param max_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#max_ttl CloudfrontDistribution#max_ttl}.
        :param min_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#min_ttl CloudfrontDistribution#min_ttl}.
        :param origin_request_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_request_policy_id CloudfrontDistribution#origin_request_policy_id}.
        :param realtime_log_config_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#realtime_log_config_arn CloudfrontDistribution#realtime_log_config_arn}.
        :param response_headers_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#response_headers_policy_id CloudfrontDistribution#response_headers_policy_id}.
        :param smooth_streaming: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#smooth_streaming CloudfrontDistribution#smooth_streaming}.
        :param trusted_key_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#trusted_key_groups CloudfrontDistribution#trusted_key_groups}.
        :param trusted_signers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#trusted_signers CloudfrontDistribution#trusted_signers}.
        '''
        if isinstance(forwarded_values, dict):
            forwarded_values = CloudfrontDistributionOrderedCacheBehaviorForwardedValues(**forwarded_values)
        if isinstance(grpc_config, dict):
            grpc_config = CloudfrontDistributionOrderedCacheBehaviorGrpcConfig(**grpc_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__744e39b86cfc9fc2539f6e35cfafee5066f21b076ad262b2ebc780936fd45286)
            check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
            check_type(argname="argument cached_methods", value=cached_methods, expected_type=type_hints["cached_methods"])
            check_type(argname="argument path_pattern", value=path_pattern, expected_type=type_hints["path_pattern"])
            check_type(argname="argument target_origin_id", value=target_origin_id, expected_type=type_hints["target_origin_id"])
            check_type(argname="argument viewer_protocol_policy", value=viewer_protocol_policy, expected_type=type_hints["viewer_protocol_policy"])
            check_type(argname="argument cache_policy_id", value=cache_policy_id, expected_type=type_hints["cache_policy_id"])
            check_type(argname="argument compress", value=compress, expected_type=type_hints["compress"])
            check_type(argname="argument default_ttl", value=default_ttl, expected_type=type_hints["default_ttl"])
            check_type(argname="argument field_level_encryption_id", value=field_level_encryption_id, expected_type=type_hints["field_level_encryption_id"])
            check_type(argname="argument forwarded_values", value=forwarded_values, expected_type=type_hints["forwarded_values"])
            check_type(argname="argument function_association", value=function_association, expected_type=type_hints["function_association"])
            check_type(argname="argument grpc_config", value=grpc_config, expected_type=type_hints["grpc_config"])
            check_type(argname="argument lambda_function_association", value=lambda_function_association, expected_type=type_hints["lambda_function_association"])
            check_type(argname="argument max_ttl", value=max_ttl, expected_type=type_hints["max_ttl"])
            check_type(argname="argument min_ttl", value=min_ttl, expected_type=type_hints["min_ttl"])
            check_type(argname="argument origin_request_policy_id", value=origin_request_policy_id, expected_type=type_hints["origin_request_policy_id"])
            check_type(argname="argument realtime_log_config_arn", value=realtime_log_config_arn, expected_type=type_hints["realtime_log_config_arn"])
            check_type(argname="argument response_headers_policy_id", value=response_headers_policy_id, expected_type=type_hints["response_headers_policy_id"])
            check_type(argname="argument smooth_streaming", value=smooth_streaming, expected_type=type_hints["smooth_streaming"])
            check_type(argname="argument trusted_key_groups", value=trusted_key_groups, expected_type=type_hints["trusted_key_groups"])
            check_type(argname="argument trusted_signers", value=trusted_signers, expected_type=type_hints["trusted_signers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_methods": allowed_methods,
            "cached_methods": cached_methods,
            "path_pattern": path_pattern,
            "target_origin_id": target_origin_id,
            "viewer_protocol_policy": viewer_protocol_policy,
        }
        if cache_policy_id is not None:
            self._values["cache_policy_id"] = cache_policy_id
        if compress is not None:
            self._values["compress"] = compress
        if default_ttl is not None:
            self._values["default_ttl"] = default_ttl
        if field_level_encryption_id is not None:
            self._values["field_level_encryption_id"] = field_level_encryption_id
        if forwarded_values is not None:
            self._values["forwarded_values"] = forwarded_values
        if function_association is not None:
            self._values["function_association"] = function_association
        if grpc_config is not None:
            self._values["grpc_config"] = grpc_config
        if lambda_function_association is not None:
            self._values["lambda_function_association"] = lambda_function_association
        if max_ttl is not None:
            self._values["max_ttl"] = max_ttl
        if min_ttl is not None:
            self._values["min_ttl"] = min_ttl
        if origin_request_policy_id is not None:
            self._values["origin_request_policy_id"] = origin_request_policy_id
        if realtime_log_config_arn is not None:
            self._values["realtime_log_config_arn"] = realtime_log_config_arn
        if response_headers_policy_id is not None:
            self._values["response_headers_policy_id"] = response_headers_policy_id
        if smooth_streaming is not None:
            self._values["smooth_streaming"] = smooth_streaming
        if trusted_key_groups is not None:
            self._values["trusted_key_groups"] = trusted_key_groups
        if trusted_signers is not None:
            self._values["trusted_signers"] = trusted_signers

    @builtins.property
    def allowed_methods(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#allowed_methods CloudfrontDistribution#allowed_methods}.'''
        result = self._values.get("allowed_methods")
        assert result is not None, "Required property 'allowed_methods' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cached_methods(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#cached_methods CloudfrontDistribution#cached_methods}.'''
        result = self._values.get("cached_methods")
        assert result is not None, "Required property 'cached_methods' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def path_pattern(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#path_pattern CloudfrontDistribution#path_pattern}.'''
        result = self._values.get("path_pattern")
        assert result is not None, "Required property 'path_pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_origin_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#target_origin_id CloudfrontDistribution#target_origin_id}.'''
        result = self._values.get("target_origin_id")
        assert result is not None, "Required property 'target_origin_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def viewer_protocol_policy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#viewer_protocol_policy CloudfrontDistribution#viewer_protocol_policy}.'''
        result = self._values.get("viewer_protocol_policy")
        assert result is not None, "Required property 'viewer_protocol_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cache_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#cache_policy_id CloudfrontDistribution#cache_policy_id}.'''
        result = self._values.get("cache_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compress(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#compress CloudfrontDistribution#compress}.'''
        result = self._values.get("compress")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def default_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#default_ttl CloudfrontDistribution#default_ttl}.'''
        result = self._values.get("default_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def field_level_encryption_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#field_level_encryption_id CloudfrontDistribution#field_level_encryption_id}.'''
        result = self._values.get("field_level_encryption_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forwarded_values(
        self,
    ) -> typing.Optional["CloudfrontDistributionOrderedCacheBehaviorForwardedValues"]:
        '''forwarded_values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#forwarded_values CloudfrontDistribution#forwarded_values}
        '''
        result = self._values.get("forwarded_values")
        return typing.cast(typing.Optional["CloudfrontDistributionOrderedCacheBehaviorForwardedValues"], result)

    @builtins.property
    def function_association(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionOrderedCacheBehaviorFunctionAssociation"]]]:
        '''function_association block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#function_association CloudfrontDistribution#function_association}
        '''
        result = self._values.get("function_association")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionOrderedCacheBehaviorFunctionAssociation"]]], result)

    @builtins.property
    def grpc_config(
        self,
    ) -> typing.Optional["CloudfrontDistributionOrderedCacheBehaviorGrpcConfig"]:
        '''grpc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#grpc_config CloudfrontDistribution#grpc_config}
        '''
        result = self._values.get("grpc_config")
        return typing.cast(typing.Optional["CloudfrontDistributionOrderedCacheBehaviorGrpcConfig"], result)

    @builtins.property
    def lambda_function_association(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociation"]]]:
        '''lambda_function_association block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#lambda_function_association CloudfrontDistribution#lambda_function_association}
        '''
        result = self._values.get("lambda_function_association")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociation"]]], result)

    @builtins.property
    def max_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#max_ttl CloudfrontDistribution#max_ttl}.'''
        result = self._values.get("max_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#min_ttl CloudfrontDistribution#min_ttl}.'''
        result = self._values.get("min_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def origin_request_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_request_policy_id CloudfrontDistribution#origin_request_policy_id}.'''
        result = self._values.get("origin_request_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def realtime_log_config_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#realtime_log_config_arn CloudfrontDistribution#realtime_log_config_arn}.'''
        result = self._values.get("realtime_log_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_headers_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#response_headers_policy_id CloudfrontDistribution#response_headers_policy_id}.'''
        result = self._values.get("response_headers_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def smooth_streaming(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#smooth_streaming CloudfrontDistribution#smooth_streaming}.'''
        result = self._values.get("smooth_streaming")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def trusted_key_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#trusted_key_groups CloudfrontDistribution#trusted_key_groups}.'''
        result = self._values.get("trusted_key_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def trusted_signers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#trusted_signers CloudfrontDistribution#trusted_signers}.'''
        result = self._values.get("trusted_signers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionOrderedCacheBehavior(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOrderedCacheBehaviorForwardedValues",
    jsii_struct_bases=[],
    name_mapping={
        "cookies": "cookies",
        "query_string": "queryString",
        "headers": "headers",
        "query_string_cache_keys": "queryStringCacheKeys",
    },
)
class CloudfrontDistributionOrderedCacheBehaviorForwardedValues:
    def __init__(
        self,
        *,
        cookies: typing.Union["CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookies", typing.Dict[builtins.str, typing.Any]],
        query_string: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_cache_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cookies: cookies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#cookies CloudfrontDistribution#cookies}
        :param query_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#query_string CloudfrontDistribution#query_string}.
        :param headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#headers CloudfrontDistribution#headers}.
        :param query_string_cache_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#query_string_cache_keys CloudfrontDistribution#query_string_cache_keys}.
        '''
        if isinstance(cookies, dict):
            cookies = CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookies(**cookies)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a4698074d9ecab848380adc22e78d5659d4babe7fe0405a0058bbbd723487c8)
            check_type(argname="argument cookies", value=cookies, expected_type=type_hints["cookies"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument query_string_cache_keys", value=query_string_cache_keys, expected_type=type_hints["query_string_cache_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cookies": cookies,
            "query_string": query_string,
        }
        if headers is not None:
            self._values["headers"] = headers
        if query_string_cache_keys is not None:
            self._values["query_string_cache_keys"] = query_string_cache_keys

    @builtins.property
    def cookies(
        self,
    ) -> "CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookies":
        '''cookies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#cookies CloudfrontDistribution#cookies}
        '''
        result = self._values.get("cookies")
        assert result is not None, "Required property 'cookies' is missing"
        return typing.cast("CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookies", result)

    @builtins.property
    def query_string(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#query_string CloudfrontDistribution#query_string}.'''
        result = self._values.get("query_string")
        assert result is not None, "Required property 'query_string' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#headers CloudfrontDistribution#headers}.'''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def query_string_cache_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#query_string_cache_keys CloudfrontDistribution#query_string_cache_keys}.'''
        result = self._values.get("query_string_cache_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionOrderedCacheBehaviorForwardedValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookies",
    jsii_struct_bases=[],
    name_mapping={"forward": "forward", "whitelisted_names": "whitelistedNames"},
)
class CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookies:
    def __init__(
        self,
        *,
        forward: builtins.str,
        whitelisted_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param forward: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#forward CloudfrontDistribution#forward}.
        :param whitelisted_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#whitelisted_names CloudfrontDistribution#whitelisted_names}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a50fd00614acdf1eeefc9e1d5bf73fc2cabd0422e1d0ceb204c6433c6df94cb)
            check_type(argname="argument forward", value=forward, expected_type=type_hints["forward"])
            check_type(argname="argument whitelisted_names", value=whitelisted_names, expected_type=type_hints["whitelisted_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "forward": forward,
        }
        if whitelisted_names is not None:
            self._values["whitelisted_names"] = whitelisted_names

    @builtins.property
    def forward(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#forward CloudfrontDistribution#forward}.'''
        result = self._values.get("forward")
        assert result is not None, "Required property 'forward' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def whitelisted_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#whitelisted_names CloudfrontDistribution#whitelisted_names}.'''
        result = self._values.get("whitelisted_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ac2499b0171f47e122fafbcbcadb19848f588695b4837d266ae23a4d9aaf853)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetWhitelistedNames")
    def reset_whitelisted_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWhitelistedNames", []))

    @builtins.property
    @jsii.member(jsii_name="forwardInput")
    def forward_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forwardInput"))

    @builtins.property
    @jsii.member(jsii_name="whitelistedNamesInput")
    def whitelisted_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "whitelistedNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="forward")
    def forward(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forward"))

    @forward.setter
    def forward(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55e0c2ad64362dc329b9ae8121baf072d1754cba7faf19c1f4aaa5ba7e04214c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forward", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="whitelistedNames")
    def whitelisted_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "whitelistedNames"))

    @whitelisted_names.setter
    def whitelisted_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad06b2ae020c30b939dc0986b953c093b3e09f204af232bbe10767895f2b6558)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "whitelistedNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookies]:
        return typing.cast(typing.Optional[CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookies], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookies],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3c82fbf8b294691c91f3c33cade46ed47c316177b18ee73620b4c5e6a1bc035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionOrderedCacheBehaviorForwardedValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOrderedCacheBehaviorForwardedValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31f33be41dd57629be8a2d3d6bdc4364958d88de8cf615e25d08a9e60c9e34f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCookies")
    def put_cookies(
        self,
        *,
        forward: builtins.str,
        whitelisted_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param forward: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#forward CloudfrontDistribution#forward}.
        :param whitelisted_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#whitelisted_names CloudfrontDistribution#whitelisted_names}.
        '''
        value = CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookies(
            forward=forward, whitelisted_names=whitelisted_names
        )

        return typing.cast(None, jsii.invoke(self, "putCookies", [value]))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @jsii.member(jsii_name="resetQueryStringCacheKeys")
    def reset_query_string_cache_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryStringCacheKeys", []))

    @builtins.property
    @jsii.member(jsii_name="cookies")
    def cookies(
        self,
    ) -> CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookiesOutputReference:
        return typing.cast(CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookiesOutputReference, jsii.get(self, "cookies"))

    @builtins.property
    @jsii.member(jsii_name="cookiesInput")
    def cookies_input(
        self,
    ) -> typing.Optional[CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookies]:
        return typing.cast(typing.Optional[CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookies], jsii.get(self, "cookiesInput"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringCacheKeysInput")
    def query_string_cache_keys_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queryStringCacheKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringInput")
    def query_string_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "queryStringInput"))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "headers"))

    @headers.setter
    def headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebae7c929a1d7dc9c3f5fb7b9b6a791b8ab9f22181cee8654f7ab3a0bf439400)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryString")
    def query_string(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "queryString"))

    @query_string.setter
    def query_string(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a08c56a8257af6eb1687be3e8ffa6a484401ec2fb04afe28678822743106146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringCacheKeys")
    def query_string_cache_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queryStringCacheKeys"))

    @query_string_cache_keys.setter
    def query_string_cache_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2222eeb0eef5f9b1fbe35a829db72ef954cb35225cd8ea9ecf7a5a2bd06cb52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringCacheKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontDistributionOrderedCacheBehaviorForwardedValues]:
        return typing.cast(typing.Optional[CloudfrontDistributionOrderedCacheBehaviorForwardedValues], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionOrderedCacheBehaviorForwardedValues],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7888500d4158ac7801531012f1e83a38bdf3099f3796788f8c94d8ab139a76c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOrderedCacheBehaviorFunctionAssociation",
    jsii_struct_bases=[],
    name_mapping={"event_type": "eventType", "function_arn": "functionArn"},
)
class CloudfrontDistributionOrderedCacheBehaviorFunctionAssociation:
    def __init__(self, *, event_type: builtins.str, function_arn: builtins.str) -> None:
        '''
        :param event_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#event_type CloudfrontDistribution#event_type}.
        :param function_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#function_arn CloudfrontDistribution#function_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c1de4a27340508dcfd07461ccbcae5c46b9df71ec5ae3aed84c917aa5a9f1b7)
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_type": event_type,
            "function_arn": function_arn,
        }

    @builtins.property
    def event_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#event_type CloudfrontDistribution#event_type}.'''
        result = self._values.get("event_type")
        assert result is not None, "Required property 'event_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def function_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#function_arn CloudfrontDistribution#function_arn}.'''
        result = self._values.get("function_arn")
        assert result is not None, "Required property 'function_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionOrderedCacheBehaviorFunctionAssociation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionOrderedCacheBehaviorFunctionAssociationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOrderedCacheBehaviorFunctionAssociationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8c69d4946da36770726dbf5ed9bb53f5d88d311aa33e836a0819e121213cc2e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontDistributionOrderedCacheBehaviorFunctionAssociationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28b89cc61eb8e929d2751d04756429f31803e1f4b3812eccd426b3c5ffade9de)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontDistributionOrderedCacheBehaviorFunctionAssociationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc96c19d2a7acfbdb6582abbdffdc2de37ea82d54f11958c13fbe34349714336)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38d77c5ba037980f6fcca9c94375cd3a2eac0da79237af235fad1e990166907f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdc2d30948d2501171cd0c8ae352591ad4173345eba5945b1144e388c02e0240)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOrderedCacheBehaviorFunctionAssociation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOrderedCacheBehaviorFunctionAssociation]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOrderedCacheBehaviorFunctionAssociation]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7bb36380e9f003586a7e8cd57e9cc2ba344f48f6f497d375d408c10d743e19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionOrderedCacheBehaviorFunctionAssociationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOrderedCacheBehaviorFunctionAssociationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fb45f09375a534e5de21a3985c57b868df014bba5c6e197a24fb0a796cb7d7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="eventTypeInput")
    def event_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="functionArnInput")
    def function_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="eventType")
    def event_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventType"))

    @event_type.setter
    def event_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2283ad81a1fb66b2f2195d72dec6682ac826e817946b6f7f96275a249de2195)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionArn"))

    @function_arn.setter
    def function_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4543cb53f3a2b510cbe938f369337d50a5e4362cf16f5179c4d6b12987d12bf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOrderedCacheBehaviorFunctionAssociation]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOrderedCacheBehaviorFunctionAssociation]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOrderedCacheBehaviorFunctionAssociation]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eecedbbc1825fb5719b3680b685cfa9248937baed56dcd74f7de2b02f8946c11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOrderedCacheBehaviorGrpcConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class CloudfrontDistributionOrderedCacheBehaviorGrpcConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#enabled CloudfrontDistribution#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1071d92d7a88ce077d25af6d32af9d6f90e642a62f446df0e11a87c419547e0)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#enabled CloudfrontDistribution#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionOrderedCacheBehaviorGrpcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionOrderedCacheBehaviorGrpcConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOrderedCacheBehaviorGrpcConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f342a92bf8a5b45d202c4f543c7d8c86d40c5e6c789cb6ee52082c3542984b17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6a1c5d48a1370faf0aed23f700f43697cca8a8501fd882077ae7bed9143fa3e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontDistributionOrderedCacheBehaviorGrpcConfig]:
        return typing.cast(typing.Optional[CloudfrontDistributionOrderedCacheBehaviorGrpcConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionOrderedCacheBehaviorGrpcConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__342996609c8f0adf3eddff2d0b36d1b003760acb7c84974668b062632790a9b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociation",
    jsii_struct_bases=[],
    name_mapping={
        "event_type": "eventType",
        "lambda_arn": "lambdaArn",
        "include_body": "includeBody",
    },
)
class CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociation:
    def __init__(
        self,
        *,
        event_type: builtins.str,
        lambda_arn: builtins.str,
        include_body: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param event_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#event_type CloudfrontDistribution#event_type}.
        :param lambda_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#lambda_arn CloudfrontDistribution#lambda_arn}.
        :param include_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#include_body CloudfrontDistribution#include_body}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42a16cb1ea31aa22899fbf50a01ff701c57a02e713ae83b24858dbb5ea49b10f)
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
            check_type(argname="argument include_body", value=include_body, expected_type=type_hints["include_body"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_type": event_type,
            "lambda_arn": lambda_arn,
        }
        if include_body is not None:
            self._values["include_body"] = include_body

    @builtins.property
    def event_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#event_type CloudfrontDistribution#event_type}.'''
        result = self._values.get("event_type")
        assert result is not None, "Required property 'event_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lambda_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#lambda_arn CloudfrontDistribution#lambda_arn}.'''
        result = self._values.get("lambda_arn")
        assert result is not None, "Required property 'lambda_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include_body(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#include_body CloudfrontDistribution#include_body}.'''
        result = self._values.get("include_body")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f160ab48a8b1f8a198c897c06b10bbfdc61261b24560cb143cc86c081a59aba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__139c6ff2e0c6f2f5985c648d66b98a6cfdc5d1d6e44e69e9b2c684b144966ab3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__615999b5f3cbb508441b2ffff9f69d7856779925b75bc9062d89a7c7efd5331b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a276f8d078e0ed20c7b7f28c36b13a2a9efc4dd138ffb2df33332dbb05cf5e4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e16de40c01c241fc1c70bdd78a9a4af32d2b57e1341d4aaf5c820dba5cbb2b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociation]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociation]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2747678f1c6d72ff107a61b5927ccd008cb9b4e64c27189668e6a78994f84d47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d41e4bdd1b4a7df139f863e7c02028ac6f3ba2cd8eb4c859f11cbedf30bdfed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIncludeBody")
    def reset_include_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeBody", []))

    @builtins.property
    @jsii.member(jsii_name="eventTypeInput")
    def event_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="includeBodyInput")
    def include_body_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaArnInput")
    def lambda_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lambdaArnInput"))

    @builtins.property
    @jsii.member(jsii_name="eventType")
    def event_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventType"))

    @event_type.setter
    def event_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc55a3f1fa9a0672102affcc757f35852bf9f33aaf82c2f4f4a1b87c5a7f9dea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeBody")
    def include_body(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeBody"))

    @include_body.setter
    def include_body(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f156d517f8cb4ecbbd3b1208441ead4314f81d94f50abca29b7c438c8f453dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lambdaArn")
    def lambda_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lambdaArn"))

    @lambda_arn.setter
    def lambda_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea8e9fb7f6cb7576736a982644a1cca2dd1452b2dbee5cea77b8c2c9d42ccdec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociation]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociation]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociation]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63c5d26a9af401aec04bd9e92044c3e3717fbb03680ef5c3f23ef363061c2738)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionOrderedCacheBehaviorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOrderedCacheBehaviorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86afacc7d5b05412992a8b01a8d152e0e2a58155a4c5aa5d01c55bbea4223b82)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontDistributionOrderedCacheBehaviorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466ab320fe7ff51db95de0f2f9e523a4791255ee1e153f4ea1df7523297589a9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontDistributionOrderedCacheBehaviorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a720dc34f5f71abc6e21b552147e2fae4b17fea133c642c3504514654949bc6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dba448b026a1f62883606218cfe08f31adabec3c57bcff2789ea2ae76398ff83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a8e028d6543632e996ab4d6584d80c4ba1f8dcdc2309a83a4620253fa06fb9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOrderedCacheBehavior]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOrderedCacheBehavior]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOrderedCacheBehavior]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbe570985ba78f0b917ed180d3b9e95bc7d2f909e5d33c1eeea9934fb30daa1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionOrderedCacheBehaviorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOrderedCacheBehaviorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c73c15c04b71404321f80f95eb2af99356c3a1ea29b3589c3e81e8477a5610c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putForwardedValues")
    def put_forwarded_values(
        self,
        *,
        cookies: typing.Union[CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookies, typing.Dict[builtins.str, typing.Any]],
        query_string: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_cache_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cookies: cookies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#cookies CloudfrontDistribution#cookies}
        :param query_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#query_string CloudfrontDistribution#query_string}.
        :param headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#headers CloudfrontDistribution#headers}.
        :param query_string_cache_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#query_string_cache_keys CloudfrontDistribution#query_string_cache_keys}.
        '''
        value = CloudfrontDistributionOrderedCacheBehaviorForwardedValues(
            cookies=cookies,
            query_string=query_string,
            headers=headers,
            query_string_cache_keys=query_string_cache_keys,
        )

        return typing.cast(None, jsii.invoke(self, "putForwardedValues", [value]))

    @jsii.member(jsii_name="putFunctionAssociation")
    def put_function_association(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOrderedCacheBehaviorFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e630f6950842fd4c0c9f9d9486fbdad3afb036b8c29ca1d1952e8b1236a03fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFunctionAssociation", [value]))

    @jsii.member(jsii_name="putGrpcConfig")
    def put_grpc_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#enabled CloudfrontDistribution#enabled}.
        '''
        value = CloudfrontDistributionOrderedCacheBehaviorGrpcConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putGrpcConfig", [value]))

    @jsii.member(jsii_name="putLambdaFunctionAssociation")
    def put_lambda_function_association(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd8273bf6718d3bd52eb7649e14118a32c1937c1bf19ed4b04f8e0f4e4e594c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLambdaFunctionAssociation", [value]))

    @jsii.member(jsii_name="resetCachePolicyId")
    def reset_cache_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCachePolicyId", []))

    @jsii.member(jsii_name="resetCompress")
    def reset_compress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompress", []))

    @jsii.member(jsii_name="resetDefaultTtl")
    def reset_default_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTtl", []))

    @jsii.member(jsii_name="resetFieldLevelEncryptionId")
    def reset_field_level_encryption_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldLevelEncryptionId", []))

    @jsii.member(jsii_name="resetForwardedValues")
    def reset_forwarded_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardedValues", []))

    @jsii.member(jsii_name="resetFunctionAssociation")
    def reset_function_association(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunctionAssociation", []))

    @jsii.member(jsii_name="resetGrpcConfig")
    def reset_grpc_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpcConfig", []))

    @jsii.member(jsii_name="resetLambdaFunctionAssociation")
    def reset_lambda_function_association(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaFunctionAssociation", []))

    @jsii.member(jsii_name="resetMaxTtl")
    def reset_max_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxTtl", []))

    @jsii.member(jsii_name="resetMinTtl")
    def reset_min_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinTtl", []))

    @jsii.member(jsii_name="resetOriginRequestPolicyId")
    def reset_origin_request_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginRequestPolicyId", []))

    @jsii.member(jsii_name="resetRealtimeLogConfigArn")
    def reset_realtime_log_config_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRealtimeLogConfigArn", []))

    @jsii.member(jsii_name="resetResponseHeadersPolicyId")
    def reset_response_headers_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseHeadersPolicyId", []))

    @jsii.member(jsii_name="resetSmoothStreaming")
    def reset_smooth_streaming(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmoothStreaming", []))

    @jsii.member(jsii_name="resetTrustedKeyGroups")
    def reset_trusted_key_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedKeyGroups", []))

    @jsii.member(jsii_name="resetTrustedSigners")
    def reset_trusted_signers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedSigners", []))

    @builtins.property
    @jsii.member(jsii_name="forwardedValues")
    def forwarded_values(
        self,
    ) -> CloudfrontDistributionOrderedCacheBehaviorForwardedValuesOutputReference:
        return typing.cast(CloudfrontDistributionOrderedCacheBehaviorForwardedValuesOutputReference, jsii.get(self, "forwardedValues"))

    @builtins.property
    @jsii.member(jsii_name="functionAssociation")
    def function_association(
        self,
    ) -> CloudfrontDistributionOrderedCacheBehaviorFunctionAssociationList:
        return typing.cast(CloudfrontDistributionOrderedCacheBehaviorFunctionAssociationList, jsii.get(self, "functionAssociation"))

    @builtins.property
    @jsii.member(jsii_name="grpcConfig")
    def grpc_config(
        self,
    ) -> CloudfrontDistributionOrderedCacheBehaviorGrpcConfigOutputReference:
        return typing.cast(CloudfrontDistributionOrderedCacheBehaviorGrpcConfigOutputReference, jsii.get(self, "grpcConfig"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionAssociation")
    def lambda_function_association(
        self,
    ) -> CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociationList:
        return typing.cast(CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociationList, jsii.get(self, "lambdaFunctionAssociation"))

    @builtins.property
    @jsii.member(jsii_name="allowedMethodsInput")
    def allowed_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="cachedMethodsInput")
    def cached_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cachedMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="cachePolicyIdInput")
    def cache_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cachePolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="compressInput")
    def compress_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "compressInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTtlInput")
    def default_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldLevelEncryptionIdInput")
    def field_level_encryption_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldLevelEncryptionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardedValuesInput")
    def forwarded_values_input(
        self,
    ) -> typing.Optional[CloudfrontDistributionOrderedCacheBehaviorForwardedValues]:
        return typing.cast(typing.Optional[CloudfrontDistributionOrderedCacheBehaviorForwardedValues], jsii.get(self, "forwardedValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="functionAssociationInput")
    def function_association_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOrderedCacheBehaviorFunctionAssociation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOrderedCacheBehaviorFunctionAssociation]]], jsii.get(self, "functionAssociationInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcConfigInput")
    def grpc_config_input(
        self,
    ) -> typing.Optional[CloudfrontDistributionOrderedCacheBehaviorGrpcConfig]:
        return typing.cast(typing.Optional[CloudfrontDistributionOrderedCacheBehaviorGrpcConfig], jsii.get(self, "grpcConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionAssociationInput")
    def lambda_function_association_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociation]]], jsii.get(self, "lambdaFunctionAssociationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxTtlInput")
    def max_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="minTtlInput")
    def min_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="originRequestPolicyIdInput")
    def origin_request_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originRequestPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="pathPatternInput")
    def path_pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathPatternInput"))

    @builtins.property
    @jsii.member(jsii_name="realtimeLogConfigArnInput")
    def realtime_log_config_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "realtimeLogConfigArnInput"))

    @builtins.property
    @jsii.member(jsii_name="responseHeadersPolicyIdInput")
    def response_headers_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseHeadersPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="smoothStreamingInput")
    def smooth_streaming_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "smoothStreamingInput"))

    @builtins.property
    @jsii.member(jsii_name="targetOriginIdInput")
    def target_origin_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetOriginIdInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedKeyGroupsInput")
    def trusted_key_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "trustedKeyGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedSignersInput")
    def trusted_signers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "trustedSignersInput"))

    @builtins.property
    @jsii.member(jsii_name="viewerProtocolPolicyInput")
    def viewer_protocol_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "viewerProtocolPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedMethods")
    def allowed_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedMethods"))

    @allowed_methods.setter
    def allowed_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c4613be14e544d067c2caa941ad6b1cee48823ef5f85ad885c79b04a9323e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cachedMethods")
    def cached_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cachedMethods"))

    @cached_methods.setter
    def cached_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e9a9d114ec3b8f3177d6cf870d68327a09036a0e20efc2cab3c77e859f1ff3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cachedMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cachePolicyId")
    def cache_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cachePolicyId"))

    @cache_policy_id.setter
    def cache_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c712dbd21049ad92ee958a08e2d7b03f0aaedb24bb521ecf9abdfacd904c04f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cachePolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="compress")
    def compress(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "compress"))

    @compress.setter
    def compress(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7592c9b08d3e863d634368ba8fdf4e97fc17938c5fb469b633376e06bd5d3dbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTtl")
    def default_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultTtl"))

    @default_ttl.setter
    def default_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98ec444be5e38b30a5ab1cb2811497f074f1f7122fd74ce31febd7559e2f2aa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fieldLevelEncryptionId")
    def field_level_encryption_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldLevelEncryptionId"))

    @field_level_encryption_id.setter
    def field_level_encryption_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e9b1c90aab0e3bea249fe9600452ce382e39ded84e4ebd75e69f873982e49dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldLevelEncryptionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxTtl")
    def max_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxTtl"))

    @max_ttl.setter
    def max_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea03542db755abbc39a1dd6f4703e9245b7a4056c21a5ce0127a407dc1e20a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minTtl")
    def min_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minTtl"))

    @min_ttl.setter
    def min_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d1c328d8793237f37e5299551f17dc5997559cf048c1ea831f488b4e05d7218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originRequestPolicyId")
    def origin_request_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originRequestPolicyId"))

    @origin_request_policy_id.setter
    def origin_request_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5214c2aba9ee5a269d34701b43b0371c68a0b9a334a1d10abff524d92d6a7b4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originRequestPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathPattern")
    def path_pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathPattern"))

    @path_pattern.setter
    def path_pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27ece3b566c0ff665b3d127fed18cd367e6d1ffb6109d8a325533b173466ec59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathPattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="realtimeLogConfigArn")
    def realtime_log_config_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "realtimeLogConfigArn"))

    @realtime_log_config_arn.setter
    def realtime_log_config_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f98f3c6d3eba29df91c7af127ef521cb784f17d37693d05d09f884e73eb6a86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "realtimeLogConfigArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseHeadersPolicyId")
    def response_headers_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseHeadersPolicyId"))

    @response_headers_policy_id.setter
    def response_headers_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be7ec773669ac8c67850762c61dec2de685c59f6ea64d23dad089af159a6c92d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseHeadersPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="smoothStreaming")
    def smooth_streaming(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "smoothStreaming"))

    @smooth_streaming.setter
    def smooth_streaming(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b42e9bef9c02f3534662b4eb04222c18e4f99b555c728411985dd77c19726eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smoothStreaming", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetOriginId")
    def target_origin_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetOriginId"))

    @target_origin_id.setter
    def target_origin_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a633c395b5b3c9650679020adc22bca1424feb942f961ea5782d28e2b3fa50fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetOriginId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustedKeyGroups")
    def trusted_key_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "trustedKeyGroups"))

    @trusted_key_groups.setter
    def trusted_key_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4bb9fdd55c1cf35d9c02d3b141ec9eb2ac86ccae42f4eaa2b69be94700d5be1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedKeyGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustedSigners")
    def trusted_signers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "trustedSigners"))

    @trusted_signers.setter
    def trusted_signers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa05d966696ce12854dc156f8c7a0bc4d868f40dde3c5221acaf4084af0ef2d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedSigners", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="viewerProtocolPolicy")
    def viewer_protocol_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "viewerProtocolPolicy"))

    @viewer_protocol_policy.setter
    def viewer_protocol_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a5599cca94582829db84e45febfb7cb6a64ad683fc2f047920453527131af81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "viewerProtocolPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOrderedCacheBehavior]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOrderedCacheBehavior]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOrderedCacheBehavior]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__853089461b27529531924afc5971c838136be7ae8b870f868814aefbb21b5482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOrigin",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "origin_id": "originId",
        "connection_attempts": "connectionAttempts",
        "connection_timeout": "connectionTimeout",
        "custom_header": "customHeader",
        "custom_origin_config": "customOriginConfig",
        "origin_access_control_id": "originAccessControlId",
        "origin_path": "originPath",
        "origin_shield": "originShield",
        "response_completion_timeout": "responseCompletionTimeout",
        "s3_origin_config": "s3OriginConfig",
        "vpc_origin_config": "vpcOriginConfig",
    },
)
class CloudfrontDistributionOrigin:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        origin_id: builtins.str,
        connection_attempts: typing.Optional[jsii.Number] = None,
        connection_timeout: typing.Optional[jsii.Number] = None,
        custom_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontDistributionOriginCustomHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_origin_config: typing.Optional[typing.Union["CloudfrontDistributionOriginCustomOriginConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        origin_access_control_id: typing.Optional[builtins.str] = None,
        origin_path: typing.Optional[builtins.str] = None,
        origin_shield: typing.Optional[typing.Union["CloudfrontDistributionOriginOriginShield", typing.Dict[builtins.str, typing.Any]]] = None,
        response_completion_timeout: typing.Optional[jsii.Number] = None,
        s3_origin_config: typing.Optional[typing.Union["CloudfrontDistributionOriginS3OriginConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_origin_config: typing.Optional[typing.Union["CloudfrontDistributionOriginVpcOriginConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#domain_name CloudfrontDistribution#domain_name}.
        :param origin_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_id CloudfrontDistribution#origin_id}.
        :param connection_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#connection_attempts CloudfrontDistribution#connection_attempts}.
        :param connection_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#connection_timeout CloudfrontDistribution#connection_timeout}.
        :param custom_header: custom_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#custom_header CloudfrontDistribution#custom_header}
        :param custom_origin_config: custom_origin_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#custom_origin_config CloudfrontDistribution#custom_origin_config}
        :param origin_access_control_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_access_control_id CloudfrontDistribution#origin_access_control_id}.
        :param origin_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_path CloudfrontDistribution#origin_path}.
        :param origin_shield: origin_shield block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_shield CloudfrontDistribution#origin_shield}
        :param response_completion_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#response_completion_timeout CloudfrontDistribution#response_completion_timeout}.
        :param s3_origin_config: s3_origin_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#s3_origin_config CloudfrontDistribution#s3_origin_config}
        :param vpc_origin_config: vpc_origin_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#vpc_origin_config CloudfrontDistribution#vpc_origin_config}
        '''
        if isinstance(custom_origin_config, dict):
            custom_origin_config = CloudfrontDistributionOriginCustomOriginConfig(**custom_origin_config)
        if isinstance(origin_shield, dict):
            origin_shield = CloudfrontDistributionOriginOriginShield(**origin_shield)
        if isinstance(s3_origin_config, dict):
            s3_origin_config = CloudfrontDistributionOriginS3OriginConfig(**s3_origin_config)
        if isinstance(vpc_origin_config, dict):
            vpc_origin_config = CloudfrontDistributionOriginVpcOriginConfig(**vpc_origin_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8c04669ab32ac2265f9574cc11d512177a84ff5e4a49eff644c11625c189499)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument origin_id", value=origin_id, expected_type=type_hints["origin_id"])
            check_type(argname="argument connection_attempts", value=connection_attempts, expected_type=type_hints["connection_attempts"])
            check_type(argname="argument connection_timeout", value=connection_timeout, expected_type=type_hints["connection_timeout"])
            check_type(argname="argument custom_header", value=custom_header, expected_type=type_hints["custom_header"])
            check_type(argname="argument custom_origin_config", value=custom_origin_config, expected_type=type_hints["custom_origin_config"])
            check_type(argname="argument origin_access_control_id", value=origin_access_control_id, expected_type=type_hints["origin_access_control_id"])
            check_type(argname="argument origin_path", value=origin_path, expected_type=type_hints["origin_path"])
            check_type(argname="argument origin_shield", value=origin_shield, expected_type=type_hints["origin_shield"])
            check_type(argname="argument response_completion_timeout", value=response_completion_timeout, expected_type=type_hints["response_completion_timeout"])
            check_type(argname="argument s3_origin_config", value=s3_origin_config, expected_type=type_hints["s3_origin_config"])
            check_type(argname="argument vpc_origin_config", value=vpc_origin_config, expected_type=type_hints["vpc_origin_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
            "origin_id": origin_id,
        }
        if connection_attempts is not None:
            self._values["connection_attempts"] = connection_attempts
        if connection_timeout is not None:
            self._values["connection_timeout"] = connection_timeout
        if custom_header is not None:
            self._values["custom_header"] = custom_header
        if custom_origin_config is not None:
            self._values["custom_origin_config"] = custom_origin_config
        if origin_access_control_id is not None:
            self._values["origin_access_control_id"] = origin_access_control_id
        if origin_path is not None:
            self._values["origin_path"] = origin_path
        if origin_shield is not None:
            self._values["origin_shield"] = origin_shield
        if response_completion_timeout is not None:
            self._values["response_completion_timeout"] = response_completion_timeout
        if s3_origin_config is not None:
            self._values["s3_origin_config"] = s3_origin_config
        if vpc_origin_config is not None:
            self._values["vpc_origin_config"] = vpc_origin_config

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#domain_name CloudfrontDistribution#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origin_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_id CloudfrontDistribution#origin_id}.'''
        result = self._values.get("origin_id")
        assert result is not None, "Required property 'origin_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connection_attempts(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#connection_attempts CloudfrontDistribution#connection_attempts}.'''
        result = self._values.get("connection_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def connection_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#connection_timeout CloudfrontDistribution#connection_timeout}.'''
        result = self._values.get("connection_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def custom_header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionOriginCustomHeader"]]]:
        '''custom_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#custom_header CloudfrontDistribution#custom_header}
        '''
        result = self._values.get("custom_header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionOriginCustomHeader"]]], result)

    @builtins.property
    def custom_origin_config(
        self,
    ) -> typing.Optional["CloudfrontDistributionOriginCustomOriginConfig"]:
        '''custom_origin_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#custom_origin_config CloudfrontDistribution#custom_origin_config}
        '''
        result = self._values.get("custom_origin_config")
        return typing.cast(typing.Optional["CloudfrontDistributionOriginCustomOriginConfig"], result)

    @builtins.property
    def origin_access_control_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_access_control_id CloudfrontDistribution#origin_access_control_id}.'''
        result = self._values.get("origin_access_control_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origin_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_path CloudfrontDistribution#origin_path}.'''
        result = self._values.get("origin_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origin_shield(
        self,
    ) -> typing.Optional["CloudfrontDistributionOriginOriginShield"]:
        '''origin_shield block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_shield CloudfrontDistribution#origin_shield}
        '''
        result = self._values.get("origin_shield")
        return typing.cast(typing.Optional["CloudfrontDistributionOriginOriginShield"], result)

    @builtins.property
    def response_completion_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#response_completion_timeout CloudfrontDistribution#response_completion_timeout}.'''
        result = self._values.get("response_completion_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def s3_origin_config(
        self,
    ) -> typing.Optional["CloudfrontDistributionOriginS3OriginConfig"]:
        '''s3_origin_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#s3_origin_config CloudfrontDistribution#s3_origin_config}
        '''
        result = self._values.get("s3_origin_config")
        return typing.cast(typing.Optional["CloudfrontDistributionOriginS3OriginConfig"], result)

    @builtins.property
    def vpc_origin_config(
        self,
    ) -> typing.Optional["CloudfrontDistributionOriginVpcOriginConfig"]:
        '''vpc_origin_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#vpc_origin_config CloudfrontDistribution#vpc_origin_config}
        '''
        result = self._values.get("vpc_origin_config")
        return typing.cast(typing.Optional["CloudfrontDistributionOriginVpcOriginConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionOrigin(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginCustomHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class CloudfrontDistributionOriginCustomHeader:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#name CloudfrontDistribution#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#value CloudfrontDistribution#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d170d3d0d677eefc7d2d592475b85bf2fbd875783bdab005967149707ab2e242)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#name CloudfrontDistribution#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#value CloudfrontDistribution#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionOriginCustomHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionOriginCustomHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginCustomHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2afa0a7db74255c43ced6a740fae4c4dab92d3eeba8eacb20e59b6b55db2afbe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontDistributionOriginCustomHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec1da5891ec90c5b1c8d9ba7ffc1873e3b388cf820a2bbd95158d08e987585d2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontDistributionOriginCustomHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68a0ae924d67d981caf0954dd8827aa2b4170cc7f9644b8f4b1482e2caa3a11d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f616d87e59a38bb1a1b5858642b79c728cb8ebce93c021a02ca20c0b1d9a6a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__457f846392373179c62026e421e03e302d82d0163fa2fdcdbaec6a6295b48e06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOriginCustomHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOriginCustomHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOriginCustomHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__637f1defc6f4cd3b54d72820363cf0e3b41de89da991e3104acae81c06b10282)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionOriginCustomHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginCustomHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6dbe53bff37c0cbe32b3ff2454181c45258de86f6eff163e485f441e7f71c55)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62976c8edbf0dde192f90d8d16fcfe4e29d61abd3ef3214e492ae50d783d30b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__718c0190709dca852784c84bf8ec0d2b05b035cbe780ef28c3a4315211e0e542)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOriginCustomHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOriginCustomHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOriginCustomHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e1f0594df4268e4c1ad811bd1adba5a312637a6dcaef585725d8f2a03a6a197)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginCustomOriginConfig",
    jsii_struct_bases=[],
    name_mapping={
        "http_port": "httpPort",
        "https_port": "httpsPort",
        "origin_protocol_policy": "originProtocolPolicy",
        "origin_ssl_protocols": "originSslProtocols",
        "ip_address_type": "ipAddressType",
        "origin_keepalive_timeout": "originKeepaliveTimeout",
        "origin_read_timeout": "originReadTimeout",
    },
)
class CloudfrontDistributionOriginCustomOriginConfig:
    def __init__(
        self,
        *,
        http_port: jsii.Number,
        https_port: jsii.Number,
        origin_protocol_policy: builtins.str,
        origin_ssl_protocols: typing.Sequence[builtins.str],
        ip_address_type: typing.Optional[builtins.str] = None,
        origin_keepalive_timeout: typing.Optional[jsii.Number] = None,
        origin_read_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#http_port CloudfrontDistribution#http_port}.
        :param https_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#https_port CloudfrontDistribution#https_port}.
        :param origin_protocol_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_protocol_policy CloudfrontDistribution#origin_protocol_policy}.
        :param origin_ssl_protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_ssl_protocols CloudfrontDistribution#origin_ssl_protocols}.
        :param ip_address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#ip_address_type CloudfrontDistribution#ip_address_type}.
        :param origin_keepalive_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_keepalive_timeout CloudfrontDistribution#origin_keepalive_timeout}.
        :param origin_read_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_read_timeout CloudfrontDistribution#origin_read_timeout}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c26e133c02c7e5899651f8568987d382a785c06b7283eecadc93d77ea5c2f47b)
            check_type(argname="argument http_port", value=http_port, expected_type=type_hints["http_port"])
            check_type(argname="argument https_port", value=https_port, expected_type=type_hints["https_port"])
            check_type(argname="argument origin_protocol_policy", value=origin_protocol_policy, expected_type=type_hints["origin_protocol_policy"])
            check_type(argname="argument origin_ssl_protocols", value=origin_ssl_protocols, expected_type=type_hints["origin_ssl_protocols"])
            check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
            check_type(argname="argument origin_keepalive_timeout", value=origin_keepalive_timeout, expected_type=type_hints["origin_keepalive_timeout"])
            check_type(argname="argument origin_read_timeout", value=origin_read_timeout, expected_type=type_hints["origin_read_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "http_port": http_port,
            "https_port": https_port,
            "origin_protocol_policy": origin_protocol_policy,
            "origin_ssl_protocols": origin_ssl_protocols,
        }
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type
        if origin_keepalive_timeout is not None:
            self._values["origin_keepalive_timeout"] = origin_keepalive_timeout
        if origin_read_timeout is not None:
            self._values["origin_read_timeout"] = origin_read_timeout

    @builtins.property
    def http_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#http_port CloudfrontDistribution#http_port}.'''
        result = self._values.get("http_port")
        assert result is not None, "Required property 'http_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def https_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#https_port CloudfrontDistribution#https_port}.'''
        result = self._values.get("https_port")
        assert result is not None, "Required property 'https_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def origin_protocol_policy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_protocol_policy CloudfrontDistribution#origin_protocol_policy}.'''
        result = self._values.get("origin_protocol_policy")
        assert result is not None, "Required property 'origin_protocol_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origin_ssl_protocols(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_ssl_protocols CloudfrontDistribution#origin_ssl_protocols}.'''
        result = self._values.get("origin_ssl_protocols")
        assert result is not None, "Required property 'origin_ssl_protocols' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#ip_address_type CloudfrontDistribution#ip_address_type}.'''
        result = self._values.get("ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origin_keepalive_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_keepalive_timeout CloudfrontDistribution#origin_keepalive_timeout}.'''
        result = self._values.get("origin_keepalive_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def origin_read_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_read_timeout CloudfrontDistribution#origin_read_timeout}.'''
        result = self._values.get("origin_read_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionOriginCustomOriginConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionOriginCustomOriginConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginCustomOriginConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1051854fac4249b59f6cf4d061211d150e3e6a1f1fde964b7a8a5780d8c54d80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIpAddressType")
    def reset_ip_address_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddressType", []))

    @jsii.member(jsii_name="resetOriginKeepaliveTimeout")
    def reset_origin_keepalive_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginKeepaliveTimeout", []))

    @jsii.member(jsii_name="resetOriginReadTimeout")
    def reset_origin_read_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginReadTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="httpPortInput")
    def http_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpPortInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsPortInput")
    def https_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpsPortInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressTypeInput")
    def ip_address_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="originKeepaliveTimeoutInput")
    def origin_keepalive_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "originKeepaliveTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="originProtocolPolicyInput")
    def origin_protocol_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originProtocolPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="originReadTimeoutInput")
    def origin_read_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "originReadTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="originSslProtocolsInput")
    def origin_ssl_protocols_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "originSslProtocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="httpPort")
    def http_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "httpPort"))

    @http_port.setter
    def http_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4db362b08cddb21aaa1affae6312685a355b6dfc2ab3e33bcb63776417df7eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsPort")
    def https_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "httpsPort"))

    @https_port.setter
    def https_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e30b83668b0d900081f70ec66622da3069d78263f89742511ff37c9b5be7090)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddressType")
    def ip_address_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddressType"))

    @ip_address_type.setter
    def ip_address_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f09021c90cc96b3682eacfcf45814efa58d73251ba37a71b617746f1679960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddressType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originKeepaliveTimeout")
    def origin_keepalive_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "originKeepaliveTimeout"))

    @origin_keepalive_timeout.setter
    def origin_keepalive_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74e0b47ee490a9f8d15e837dc0124e8f1f3d09a548e57701651cf1e62580f3a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originKeepaliveTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originProtocolPolicy")
    def origin_protocol_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originProtocolPolicy"))

    @origin_protocol_policy.setter
    def origin_protocol_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b452fc9f225e6948b7eaba9d67320cdf2bdd395f3072163ba7ebe809c7b90e7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originProtocolPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originReadTimeout")
    def origin_read_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "originReadTimeout"))

    @origin_read_timeout.setter
    def origin_read_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b1011231312d939832868e76f2ce69098cd4b9be10d334dc815768285025065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originReadTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originSslProtocols")
    def origin_ssl_protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "originSslProtocols"))

    @origin_ssl_protocols.setter
    def origin_ssl_protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46898499ea952c358bc51b5c297310c877ac162d55376af917075c5f8fc651b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originSslProtocols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontDistributionOriginCustomOriginConfig]:
        return typing.cast(typing.Optional[CloudfrontDistributionOriginCustomOriginConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionOriginCustomOriginConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b2823fa2be1053a6e1dbda19fcd780af047d008cba0c0442fce1fa1e39ee8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginGroup",
    jsii_struct_bases=[],
    name_mapping={
        "failover_criteria": "failoverCriteria",
        "member": "member",
        "origin_id": "originId",
    },
)
class CloudfrontDistributionOriginGroup:
    def __init__(
        self,
        *,
        failover_criteria: typing.Union["CloudfrontDistributionOriginGroupFailoverCriteria", typing.Dict[builtins.str, typing.Any]],
        member: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontDistributionOriginGroupMember", typing.Dict[builtins.str, typing.Any]]]],
        origin_id: builtins.str,
    ) -> None:
        '''
        :param failover_criteria: failover_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#failover_criteria CloudfrontDistribution#failover_criteria}
        :param member: member block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#member CloudfrontDistribution#member}
        :param origin_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_id CloudfrontDistribution#origin_id}.
        '''
        if isinstance(failover_criteria, dict):
            failover_criteria = CloudfrontDistributionOriginGroupFailoverCriteria(**failover_criteria)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d45cc4ec445a740ea95f24a58c0e9ef1b1f28f02802fb4a99af598800d1f19e4)
            check_type(argname="argument failover_criteria", value=failover_criteria, expected_type=type_hints["failover_criteria"])
            check_type(argname="argument member", value=member, expected_type=type_hints["member"])
            check_type(argname="argument origin_id", value=origin_id, expected_type=type_hints["origin_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "failover_criteria": failover_criteria,
            "member": member,
            "origin_id": origin_id,
        }

    @builtins.property
    def failover_criteria(self) -> "CloudfrontDistributionOriginGroupFailoverCriteria":
        '''failover_criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#failover_criteria CloudfrontDistribution#failover_criteria}
        '''
        result = self._values.get("failover_criteria")
        assert result is not None, "Required property 'failover_criteria' is missing"
        return typing.cast("CloudfrontDistributionOriginGroupFailoverCriteria", result)

    @builtins.property
    def member(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionOriginGroupMember"]]:
        '''member block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#member CloudfrontDistribution#member}
        '''
        result = self._values.get("member")
        assert result is not None, "Required property 'member' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontDistributionOriginGroupMember"]], result)

    @builtins.property
    def origin_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_id CloudfrontDistribution#origin_id}.'''
        result = self._values.get("origin_id")
        assert result is not None, "Required property 'origin_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionOriginGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginGroupFailoverCriteria",
    jsii_struct_bases=[],
    name_mapping={"status_codes": "statusCodes"},
)
class CloudfrontDistributionOriginGroupFailoverCriteria:
    def __init__(self, *, status_codes: typing.Sequence[jsii.Number]) -> None:
        '''
        :param status_codes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#status_codes CloudfrontDistribution#status_codes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f410973ca4d5c38fa26c154c8a7d4659bd9b5586bc22a14c235c82a96266a0ea)
            check_type(argname="argument status_codes", value=status_codes, expected_type=type_hints["status_codes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status_codes": status_codes,
        }

    @builtins.property
    def status_codes(self) -> typing.List[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#status_codes CloudfrontDistribution#status_codes}.'''
        result = self._values.get("status_codes")
        assert result is not None, "Required property 'status_codes' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionOriginGroupFailoverCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionOriginGroupFailoverCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginGroupFailoverCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6820e4b88be3848f56cddd960395556a66efb9b6a6f1ea085f8010d3196882ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="statusCodesInput")
    def status_codes_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "statusCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="statusCodes")
    def status_codes(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "statusCodes"))

    @status_codes.setter
    def status_codes(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c298897fb722d7e10595d783e89421a5a4ae059caac484e9212f6b6a35d7cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontDistributionOriginGroupFailoverCriteria]:
        return typing.cast(typing.Optional[CloudfrontDistributionOriginGroupFailoverCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionOriginGroupFailoverCriteria],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0b289a5e15752d3a2384c2faf53946aeefa665659711b3f9a61d2c0abfea110)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionOriginGroupList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginGroupList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2d178fc83943220a28dd400aa5aa06a099a6ad9d974f374156aa2980ec4b6a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontDistributionOriginGroupOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7976c9d54a8055d70b73ac480d943342e835ef08676cf2bc6d635e498165eab3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontDistributionOriginGroupOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d17f04957afc36ec06e77cbf5600ec420af26352b9d5e65bdbe578e9d8ac06b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9428a5ab1dc5d82520cc255cc6e0dee16d150315b302f5f82b0111d6737bfd86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea2b9c1350e90484e3d39996b17e99237af8f96766d4f983cc4c879a6f5478f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOriginGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOriginGroup]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOriginGroup]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a5d83dfa14c9466d74e3afd03d5745a440fa93a844678dee7f5243830b56bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginGroupMember",
    jsii_struct_bases=[],
    name_mapping={"origin_id": "originId"},
)
class CloudfrontDistributionOriginGroupMember:
    def __init__(self, *, origin_id: builtins.str) -> None:
        '''
        :param origin_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_id CloudfrontDistribution#origin_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d53b4b53ae7713365657be8080a0ba7dff1634d54e92d7fc494ab1beecbebe1)
            check_type(argname="argument origin_id", value=origin_id, expected_type=type_hints["origin_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "origin_id": origin_id,
        }

    @builtins.property
    def origin_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_id CloudfrontDistribution#origin_id}.'''
        result = self._values.get("origin_id")
        assert result is not None, "Required property 'origin_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionOriginGroupMember(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionOriginGroupMemberList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginGroupMemberList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d791e8d99c4abb77956374aa94f37380ba5865443615617685800f7bc801bad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontDistributionOriginGroupMemberOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ca68eab62d4194ee34f5e3f547683f23af9a11610c221364886f8a8c3c9708)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontDistributionOriginGroupMemberOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea912299e98d20c23d4c9b35265d743fb4ca2950a2c2ca09184acd3f3c755b90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9fc4aaab33ed97ee409f3924fa7ecbca0b42e8c80ff60908a66d59b3b674420)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f1dbde4811a19f96cc2adcc82652ba00998d3ad49f310aaaaccadd8ad027d1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOriginGroupMember]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOriginGroupMember]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOriginGroupMember]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab0e782b9bfadd85ca52f999be2c6e73ed889945ebd1b742b44fd762cc040743)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionOriginGroupMemberOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginGroupMemberOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6408a117b5da685d32a2e5c338dceb8747a7dc225cb1e26eaf15cd53053d72d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="originIdInput")
    def origin_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originIdInput"))

    @builtins.property
    @jsii.member(jsii_name="originId")
    def origin_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originId"))

    @origin_id.setter
    def origin_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e39f74c3e469c47264d9c63dd9a03d24836afe9e1aa72626e6c75ec7547505a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOriginGroupMember]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOriginGroupMember]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOriginGroupMember]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcb86215355a6f5b1a52d1bb6870681fd84bb8f216082e908ce83ee7bcdafefc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionOriginGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9b3fe416a00b22145bc013f1a162ba6d650fa70860304e1d944f3f59401c0aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFailoverCriteria")
    def put_failover_criteria(
        self,
        *,
        status_codes: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param status_codes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#status_codes CloudfrontDistribution#status_codes}.
        '''
        value = CloudfrontDistributionOriginGroupFailoverCriteria(
            status_codes=status_codes
        )

        return typing.cast(None, jsii.invoke(self, "putFailoverCriteria", [value]))

    @jsii.member(jsii_name="putMember")
    def put_member(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOriginGroupMember, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b7aad23219f42e9e39d0886d676358f8ed0104126b4be27fb08aca4383a870f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMember", [value]))

    @builtins.property
    @jsii.member(jsii_name="failoverCriteria")
    def failover_criteria(
        self,
    ) -> CloudfrontDistributionOriginGroupFailoverCriteriaOutputReference:
        return typing.cast(CloudfrontDistributionOriginGroupFailoverCriteriaOutputReference, jsii.get(self, "failoverCriteria"))

    @builtins.property
    @jsii.member(jsii_name="member")
    def member(self) -> CloudfrontDistributionOriginGroupMemberList:
        return typing.cast(CloudfrontDistributionOriginGroupMemberList, jsii.get(self, "member"))

    @builtins.property
    @jsii.member(jsii_name="failoverCriteriaInput")
    def failover_criteria_input(
        self,
    ) -> typing.Optional[CloudfrontDistributionOriginGroupFailoverCriteria]:
        return typing.cast(typing.Optional[CloudfrontDistributionOriginGroupFailoverCriteria], jsii.get(self, "failoverCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="memberInput")
    def member_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOriginGroupMember]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOriginGroupMember]]], jsii.get(self, "memberInput"))

    @builtins.property
    @jsii.member(jsii_name="originIdInput")
    def origin_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originIdInput"))

    @builtins.property
    @jsii.member(jsii_name="originId")
    def origin_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originId"))

    @origin_id.setter
    def origin_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a38f9a269f6748479aa6893482be621bc76f39c5c0af59393b3de72367dc9f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOriginGroup]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOriginGroup]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOriginGroup]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__055485c8b7d08914c431946381ac18dbeb83adcc9b3134421b77cd7d11c4136e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionOriginList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f57aaa916f83b4dea59bb55013f3aa3ffd574dcc671c4f3b43bf619c877b31a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CloudfrontDistributionOriginOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cb2258af00e60eb5fa8ab35c5bb01d3f2843f43fe8ea91878e7e0e3ee4174e3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontDistributionOriginOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98a56d69efda63db98bca6dc8d19f79c06a6ba74ec693b1b4d32fc4d0698b7a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd7c155f04af18eba90ba8a4c43f9f792a8a9d5939f474153e30d9ceefa28b2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a294b3e484df55778b8c2de3910556d8b90709cee16310974803866cba75d2c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOrigin]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOrigin]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOrigin]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c515f32a8434f2acffa8e83b3c59b02f5fba3a82d45771c4b27cf70562bf06d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginOriginShield",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "origin_shield_region": "originShieldRegion"},
)
class CloudfrontDistributionOriginOriginShield:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        origin_shield_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#enabled CloudfrontDistribution#enabled}.
        :param origin_shield_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_shield_region CloudfrontDistribution#origin_shield_region}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79183e516f93dcbea116a16c74402941f93504e2ad0b4ecf29b728a9fe1dd4cc)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument origin_shield_region", value=origin_shield_region, expected_type=type_hints["origin_shield_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if origin_shield_region is not None:
            self._values["origin_shield_region"] = origin_shield_region

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#enabled CloudfrontDistribution#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def origin_shield_region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_shield_region CloudfrontDistribution#origin_shield_region}.'''
        result = self._values.get("origin_shield_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionOriginOriginShield(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionOriginOriginShieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginOriginShieldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__278c2cfbd5ef79c40ec0f2a2709063800f3bc71c557024d4b13e91611f7ccb7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOriginShieldRegion")
    def reset_origin_shield_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginShieldRegion", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="originShieldRegionInput")
    def origin_shield_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originShieldRegionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__031e8b377318b8c96c29282a6411b46b2ace438c1a0bc87eba7a3a4cddaf0d36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originShieldRegion")
    def origin_shield_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originShieldRegion"))

    @origin_shield_region.setter
    def origin_shield_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34f2eb69dae2cd88571da72f1c0293eb8451607dad0a2d6eda33244d464d784d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originShieldRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontDistributionOriginOriginShield]:
        return typing.cast(typing.Optional[CloudfrontDistributionOriginOriginShield], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionOriginOriginShield],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49c46f0b15f2456605d4a7756a823c58e682adaec574137650bc1dbbfd9e63c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionOriginOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__381642faf9a425d3c8081409f7ef57a75dddbbee3a24fb05c958e1adc872be7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCustomHeader")
    def put_custom_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOriginCustomHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23643948988ceca1fc33dad64ed8bdc6d0f4af2cd24c339aee80c4ca237d026f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomHeader", [value]))

    @jsii.member(jsii_name="putCustomOriginConfig")
    def put_custom_origin_config(
        self,
        *,
        http_port: jsii.Number,
        https_port: jsii.Number,
        origin_protocol_policy: builtins.str,
        origin_ssl_protocols: typing.Sequence[builtins.str],
        ip_address_type: typing.Optional[builtins.str] = None,
        origin_keepalive_timeout: typing.Optional[jsii.Number] = None,
        origin_read_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#http_port CloudfrontDistribution#http_port}.
        :param https_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#https_port CloudfrontDistribution#https_port}.
        :param origin_protocol_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_protocol_policy CloudfrontDistribution#origin_protocol_policy}.
        :param origin_ssl_protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_ssl_protocols CloudfrontDistribution#origin_ssl_protocols}.
        :param ip_address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#ip_address_type CloudfrontDistribution#ip_address_type}.
        :param origin_keepalive_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_keepalive_timeout CloudfrontDistribution#origin_keepalive_timeout}.
        :param origin_read_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_read_timeout CloudfrontDistribution#origin_read_timeout}.
        '''
        value = CloudfrontDistributionOriginCustomOriginConfig(
            http_port=http_port,
            https_port=https_port,
            origin_protocol_policy=origin_protocol_policy,
            origin_ssl_protocols=origin_ssl_protocols,
            ip_address_type=ip_address_type,
            origin_keepalive_timeout=origin_keepalive_timeout,
            origin_read_timeout=origin_read_timeout,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomOriginConfig", [value]))

    @jsii.member(jsii_name="putOriginShield")
    def put_origin_shield(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        origin_shield_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#enabled CloudfrontDistribution#enabled}.
        :param origin_shield_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_shield_region CloudfrontDistribution#origin_shield_region}.
        '''
        value = CloudfrontDistributionOriginOriginShield(
            enabled=enabled, origin_shield_region=origin_shield_region
        )

        return typing.cast(None, jsii.invoke(self, "putOriginShield", [value]))

    @jsii.member(jsii_name="putS3OriginConfig")
    def put_s3_origin_config(self, *, origin_access_identity: builtins.str) -> None:
        '''
        :param origin_access_identity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_access_identity CloudfrontDistribution#origin_access_identity}.
        '''
        value = CloudfrontDistributionOriginS3OriginConfig(
            origin_access_identity=origin_access_identity
        )

        return typing.cast(None, jsii.invoke(self, "putS3OriginConfig", [value]))

    @jsii.member(jsii_name="putVpcOriginConfig")
    def put_vpc_origin_config(
        self,
        *,
        vpc_origin_id: builtins.str,
        origin_keepalive_timeout: typing.Optional[jsii.Number] = None,
        origin_read_timeout: typing.Optional[jsii.Number] = None,
        owner_account_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param vpc_origin_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#vpc_origin_id CloudfrontDistribution#vpc_origin_id}.
        :param origin_keepalive_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_keepalive_timeout CloudfrontDistribution#origin_keepalive_timeout}.
        :param origin_read_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_read_timeout CloudfrontDistribution#origin_read_timeout}.
        :param owner_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#owner_account_id CloudfrontDistribution#owner_account_id}.
        '''
        value = CloudfrontDistributionOriginVpcOriginConfig(
            vpc_origin_id=vpc_origin_id,
            origin_keepalive_timeout=origin_keepalive_timeout,
            origin_read_timeout=origin_read_timeout,
            owner_account_id=owner_account_id,
        )

        return typing.cast(None, jsii.invoke(self, "putVpcOriginConfig", [value]))

    @jsii.member(jsii_name="resetConnectionAttempts")
    def reset_connection_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionAttempts", []))

    @jsii.member(jsii_name="resetConnectionTimeout")
    def reset_connection_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionTimeout", []))

    @jsii.member(jsii_name="resetCustomHeader")
    def reset_custom_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomHeader", []))

    @jsii.member(jsii_name="resetCustomOriginConfig")
    def reset_custom_origin_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomOriginConfig", []))

    @jsii.member(jsii_name="resetOriginAccessControlId")
    def reset_origin_access_control_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginAccessControlId", []))

    @jsii.member(jsii_name="resetOriginPath")
    def reset_origin_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginPath", []))

    @jsii.member(jsii_name="resetOriginShield")
    def reset_origin_shield(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginShield", []))

    @jsii.member(jsii_name="resetResponseCompletionTimeout")
    def reset_response_completion_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseCompletionTimeout", []))

    @jsii.member(jsii_name="resetS3OriginConfig")
    def reset_s3_origin_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3OriginConfig", []))

    @jsii.member(jsii_name="resetVpcOriginConfig")
    def reset_vpc_origin_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcOriginConfig", []))

    @builtins.property
    @jsii.member(jsii_name="customHeader")
    def custom_header(self) -> CloudfrontDistributionOriginCustomHeaderList:
        return typing.cast(CloudfrontDistributionOriginCustomHeaderList, jsii.get(self, "customHeader"))

    @builtins.property
    @jsii.member(jsii_name="customOriginConfig")
    def custom_origin_config(
        self,
    ) -> CloudfrontDistributionOriginCustomOriginConfigOutputReference:
        return typing.cast(CloudfrontDistributionOriginCustomOriginConfigOutputReference, jsii.get(self, "customOriginConfig"))

    @builtins.property
    @jsii.member(jsii_name="originShield")
    def origin_shield(self) -> CloudfrontDistributionOriginOriginShieldOutputReference:
        return typing.cast(CloudfrontDistributionOriginOriginShieldOutputReference, jsii.get(self, "originShield"))

    @builtins.property
    @jsii.member(jsii_name="s3OriginConfig")
    def s3_origin_config(
        self,
    ) -> "CloudfrontDistributionOriginS3OriginConfigOutputReference":
        return typing.cast("CloudfrontDistributionOriginS3OriginConfigOutputReference", jsii.get(self, "s3OriginConfig"))

    @builtins.property
    @jsii.member(jsii_name="vpcOriginConfig")
    def vpc_origin_config(
        self,
    ) -> "CloudfrontDistributionOriginVpcOriginConfigOutputReference":
        return typing.cast("CloudfrontDistributionOriginVpcOriginConfigOutputReference", jsii.get(self, "vpcOriginConfig"))

    @builtins.property
    @jsii.member(jsii_name="connectionAttemptsInput")
    def connection_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "connectionAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionTimeoutInput")
    def connection_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "connectionTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="customHeaderInput")
    def custom_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOriginCustomHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOriginCustomHeader]]], jsii.get(self, "customHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="customOriginConfigInput")
    def custom_origin_config_input(
        self,
    ) -> typing.Optional[CloudfrontDistributionOriginCustomOriginConfig]:
        return typing.cast(typing.Optional[CloudfrontDistributionOriginCustomOriginConfig], jsii.get(self, "customOriginConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="originAccessControlIdInput")
    def origin_access_control_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originAccessControlIdInput"))

    @builtins.property
    @jsii.member(jsii_name="originIdInput")
    def origin_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originIdInput"))

    @builtins.property
    @jsii.member(jsii_name="originPathInput")
    def origin_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originPathInput"))

    @builtins.property
    @jsii.member(jsii_name="originShieldInput")
    def origin_shield_input(
        self,
    ) -> typing.Optional[CloudfrontDistributionOriginOriginShield]:
        return typing.cast(typing.Optional[CloudfrontDistributionOriginOriginShield], jsii.get(self, "originShieldInput"))

    @builtins.property
    @jsii.member(jsii_name="responseCompletionTimeoutInput")
    def response_completion_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "responseCompletionTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="s3OriginConfigInput")
    def s3_origin_config_input(
        self,
    ) -> typing.Optional["CloudfrontDistributionOriginS3OriginConfig"]:
        return typing.cast(typing.Optional["CloudfrontDistributionOriginS3OriginConfig"], jsii.get(self, "s3OriginConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcOriginConfigInput")
    def vpc_origin_config_input(
        self,
    ) -> typing.Optional["CloudfrontDistributionOriginVpcOriginConfig"]:
        return typing.cast(typing.Optional["CloudfrontDistributionOriginVpcOriginConfig"], jsii.get(self, "vpcOriginConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionAttempts")
    def connection_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "connectionAttempts"))

    @connection_attempts.setter
    def connection_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb94f958e1115ca0bd89cef9a70fb869936066232ed8502fe3255027709a934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectionTimeout")
    def connection_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "connectionTimeout"))

    @connection_timeout.setter
    def connection_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b223fb60f2e31179dc12e2c45e84d3bf3376ae303e3e6f80db7bd5496959504)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f97f7356f3837aff7a8a1a9fd0be95113751c6097eeffecae750221b29b4dec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originAccessControlId")
    def origin_access_control_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originAccessControlId"))

    @origin_access_control_id.setter
    def origin_access_control_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0b8d6a8e14a6da72778406eb2eb57c4c651537492b6e71eb5385efc023c1b63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originAccessControlId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originId")
    def origin_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originId"))

    @origin_id.setter
    def origin_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db30fdd5a9ce779de43c54c94de3a42902bd44a1fc404500557ba35352d5e31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originPath")
    def origin_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originPath"))

    @origin_path.setter
    def origin_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa06c9a1770246c6d84b11c16b24235fc931a1b4e43b150b5216ced81261b35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseCompletionTimeout")
    def response_completion_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "responseCompletionTimeout"))

    @response_completion_timeout.setter
    def response_completion_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d2d23d79d24dafcb4a4f48e205c87d07bb689cf039a6b0a14bfff830916a5b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseCompletionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOrigin]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOrigin]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOrigin]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b47c375d254d42678716df3663f1d9e3672c568ff8be461b4d4b5a928e14b93f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginS3OriginConfig",
    jsii_struct_bases=[],
    name_mapping={"origin_access_identity": "originAccessIdentity"},
)
class CloudfrontDistributionOriginS3OriginConfig:
    def __init__(self, *, origin_access_identity: builtins.str) -> None:
        '''
        :param origin_access_identity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_access_identity CloudfrontDistribution#origin_access_identity}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b08301c46c3f7326d9d31c7c2acefa73ae2c0f1d1bb9ff3f4ff179e5112f136c)
            check_type(argname="argument origin_access_identity", value=origin_access_identity, expected_type=type_hints["origin_access_identity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "origin_access_identity": origin_access_identity,
        }

    @builtins.property
    def origin_access_identity(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_access_identity CloudfrontDistribution#origin_access_identity}.'''
        result = self._values.get("origin_access_identity")
        assert result is not None, "Required property 'origin_access_identity' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionOriginS3OriginConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionOriginS3OriginConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginS3OriginConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__560757dcb36ce5ee18f1b84729c343aafaac51600ef2d1b41813d7eeaf98b3b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="originAccessIdentityInput")
    def origin_access_identity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originAccessIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="originAccessIdentity")
    def origin_access_identity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originAccessIdentity"))

    @origin_access_identity.setter
    def origin_access_identity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afc044ffffda056894a5c5f23edf50fd5abf8b46932cf1dea248bb4263f10571)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originAccessIdentity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontDistributionOriginS3OriginConfig]:
        return typing.cast(typing.Optional[CloudfrontDistributionOriginS3OriginConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionOriginS3OriginConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae557d9645975a39b3fc86c715419505fb0af24317cfdd4eff0645bf0ca6203c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginVpcOriginConfig",
    jsii_struct_bases=[],
    name_mapping={
        "vpc_origin_id": "vpcOriginId",
        "origin_keepalive_timeout": "originKeepaliveTimeout",
        "origin_read_timeout": "originReadTimeout",
        "owner_account_id": "ownerAccountId",
    },
)
class CloudfrontDistributionOriginVpcOriginConfig:
    def __init__(
        self,
        *,
        vpc_origin_id: builtins.str,
        origin_keepalive_timeout: typing.Optional[jsii.Number] = None,
        origin_read_timeout: typing.Optional[jsii.Number] = None,
        owner_account_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param vpc_origin_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#vpc_origin_id CloudfrontDistribution#vpc_origin_id}.
        :param origin_keepalive_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_keepalive_timeout CloudfrontDistribution#origin_keepalive_timeout}.
        :param origin_read_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_read_timeout CloudfrontDistribution#origin_read_timeout}.
        :param owner_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#owner_account_id CloudfrontDistribution#owner_account_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b965be7b2d93b5916a133e4331b226aa1c91e9aff69953cb9970bef30e5935a7)
            check_type(argname="argument vpc_origin_id", value=vpc_origin_id, expected_type=type_hints["vpc_origin_id"])
            check_type(argname="argument origin_keepalive_timeout", value=origin_keepalive_timeout, expected_type=type_hints["origin_keepalive_timeout"])
            check_type(argname="argument origin_read_timeout", value=origin_read_timeout, expected_type=type_hints["origin_read_timeout"])
            check_type(argname="argument owner_account_id", value=owner_account_id, expected_type=type_hints["owner_account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc_origin_id": vpc_origin_id,
        }
        if origin_keepalive_timeout is not None:
            self._values["origin_keepalive_timeout"] = origin_keepalive_timeout
        if origin_read_timeout is not None:
            self._values["origin_read_timeout"] = origin_read_timeout
        if owner_account_id is not None:
            self._values["owner_account_id"] = owner_account_id

    @builtins.property
    def vpc_origin_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#vpc_origin_id CloudfrontDistribution#vpc_origin_id}.'''
        result = self._values.get("vpc_origin_id")
        assert result is not None, "Required property 'vpc_origin_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origin_keepalive_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_keepalive_timeout CloudfrontDistribution#origin_keepalive_timeout}.'''
        result = self._values.get("origin_keepalive_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def origin_read_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#origin_read_timeout CloudfrontDistribution#origin_read_timeout}.'''
        result = self._values.get("origin_read_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def owner_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#owner_account_id CloudfrontDistribution#owner_account_id}.'''
        result = self._values.get("owner_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionOriginVpcOriginConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionOriginVpcOriginConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionOriginVpcOriginConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2030be70c9c455bce264024ee4476a0160a389fce2b5761f8f7f392f9863d540)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOriginKeepaliveTimeout")
    def reset_origin_keepalive_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginKeepaliveTimeout", []))

    @jsii.member(jsii_name="resetOriginReadTimeout")
    def reset_origin_read_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginReadTimeout", []))

    @jsii.member(jsii_name="resetOwnerAccountId")
    def reset_owner_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwnerAccountId", []))

    @builtins.property
    @jsii.member(jsii_name="originKeepaliveTimeoutInput")
    def origin_keepalive_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "originKeepaliveTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="originReadTimeoutInput")
    def origin_read_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "originReadTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="ownerAccountIdInput")
    def owner_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcOriginIdInput")
    def vpc_origin_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcOriginIdInput"))

    @builtins.property
    @jsii.member(jsii_name="originKeepaliveTimeout")
    def origin_keepalive_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "originKeepaliveTimeout"))

    @origin_keepalive_timeout.setter
    def origin_keepalive_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e69c70aff874c157aafff4f83edd1f12e90d4d3bd323b7cb139da861161d6428)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originKeepaliveTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originReadTimeout")
    def origin_read_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "originReadTimeout"))

    @origin_read_timeout.setter
    def origin_read_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c46ba831495d4d86cdcd977fb5ff8f84cbaf722e05b4b9cf8c0ca581243249f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originReadTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ownerAccountId")
    def owner_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownerAccountId"))

    @owner_account_id.setter
    def owner_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f225b622dce46f3d46f254b8f208cd103bbbcbecdb7b7837b9f4b2168fd4e5a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ownerAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcOriginId")
    def vpc_origin_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcOriginId"))

    @vpc_origin_id.setter
    def vpc_origin_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa7a61b6cf5bbb2d76b63ad04c719381cd15b96c373ab7c192dfde61536489f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcOriginId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontDistributionOriginVpcOriginConfig]:
        return typing.cast(typing.Optional[CloudfrontDistributionOriginVpcOriginConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionOriginVpcOriginConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c22503db29fcf978500948f79f6ce5ea9bff0f8aeecc9a32511edfd15d706b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionRestrictions",
    jsii_struct_bases=[],
    name_mapping={"geo_restriction": "geoRestriction"},
)
class CloudfrontDistributionRestrictions:
    def __init__(
        self,
        *,
        geo_restriction: typing.Union["CloudfrontDistributionRestrictionsGeoRestriction", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param geo_restriction: geo_restriction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#geo_restriction CloudfrontDistribution#geo_restriction}
        '''
        if isinstance(geo_restriction, dict):
            geo_restriction = CloudfrontDistributionRestrictionsGeoRestriction(**geo_restriction)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__803c0405770ab46aad53c8cf2e6c0942da1c468e141dded7a77eeda9e794fc68)
            check_type(argname="argument geo_restriction", value=geo_restriction, expected_type=type_hints["geo_restriction"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "geo_restriction": geo_restriction,
        }

    @builtins.property
    def geo_restriction(self) -> "CloudfrontDistributionRestrictionsGeoRestriction":
        '''geo_restriction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#geo_restriction CloudfrontDistribution#geo_restriction}
        '''
        result = self._values.get("geo_restriction")
        assert result is not None, "Required property 'geo_restriction' is missing"
        return typing.cast("CloudfrontDistributionRestrictionsGeoRestriction", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionRestrictions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionRestrictionsGeoRestriction",
    jsii_struct_bases=[],
    name_mapping={"restriction_type": "restrictionType", "locations": "locations"},
)
class CloudfrontDistributionRestrictionsGeoRestriction:
    def __init__(
        self,
        *,
        restriction_type: builtins.str,
        locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param restriction_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#restriction_type CloudfrontDistribution#restriction_type}.
        :param locations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#locations CloudfrontDistribution#locations}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ad6e68fcf393c092cf15cc17a7b7974c5803475ed09ba18911dd622c8a9bc6f)
            check_type(argname="argument restriction_type", value=restriction_type, expected_type=type_hints["restriction_type"])
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "restriction_type": restriction_type,
        }
        if locations is not None:
            self._values["locations"] = locations

    @builtins.property
    def restriction_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#restriction_type CloudfrontDistribution#restriction_type}.'''
        result = self._values.get("restriction_type")
        assert result is not None, "Required property 'restriction_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def locations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#locations CloudfrontDistribution#locations}.'''
        result = self._values.get("locations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionRestrictionsGeoRestriction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionRestrictionsGeoRestrictionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionRestrictionsGeoRestrictionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db3f407a47f75f28ab2c048c4d3e6e55565a0bd5fc1f297d2ab8da1d5db16adb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLocations")
    def reset_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocations", []))

    @builtins.property
    @jsii.member(jsii_name="locationsInput")
    def locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "locationsInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictionTypeInput")
    def restriction_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "restrictionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="locations")
    def locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "locations"))

    @locations.setter
    def locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__358ed744b47e1eafe82dffd6b2c8bd1766c012f4fe5973f30e51c7429164eb61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restrictionType")
    def restriction_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "restrictionType"))

    @restriction_type.setter
    def restriction_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__895e32b1b87c556af6c5d9e846ac8783f019a62b7f7de23511a1e68d571cb441)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restrictionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontDistributionRestrictionsGeoRestriction]:
        return typing.cast(typing.Optional[CloudfrontDistributionRestrictionsGeoRestriction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionRestrictionsGeoRestriction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba63f7320894f2bf8f1c8cebc65edcaf328d298fc7618b19073fe07117ffef18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionRestrictionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionRestrictionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91cda328b272ac0a5c0021ce4c113ff242af24757fe42dad7d8d92ba49788637)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGeoRestriction")
    def put_geo_restriction(
        self,
        *,
        restriction_type: builtins.str,
        locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param restriction_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#restriction_type CloudfrontDistribution#restriction_type}.
        :param locations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#locations CloudfrontDistribution#locations}.
        '''
        value = CloudfrontDistributionRestrictionsGeoRestriction(
            restriction_type=restriction_type, locations=locations
        )

        return typing.cast(None, jsii.invoke(self, "putGeoRestriction", [value]))

    @builtins.property
    @jsii.member(jsii_name="geoRestriction")
    def geo_restriction(
        self,
    ) -> CloudfrontDistributionRestrictionsGeoRestrictionOutputReference:
        return typing.cast(CloudfrontDistributionRestrictionsGeoRestrictionOutputReference, jsii.get(self, "geoRestriction"))

    @builtins.property
    @jsii.member(jsii_name="geoRestrictionInput")
    def geo_restriction_input(
        self,
    ) -> typing.Optional[CloudfrontDistributionRestrictionsGeoRestriction]:
        return typing.cast(typing.Optional[CloudfrontDistributionRestrictionsGeoRestriction], jsii.get(self, "geoRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudfrontDistributionRestrictions]:
        return typing.cast(typing.Optional[CloudfrontDistributionRestrictions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionRestrictions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54a45c36a07284c12a7a54d868f7ece9e1a58b513352e12b3d251e4298957fdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionTrustedKeyGroups",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudfrontDistributionTrustedKeyGroups:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionTrustedKeyGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionTrustedKeyGroupsItems",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudfrontDistributionTrustedKeyGroupsItems:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionTrustedKeyGroupsItems(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionTrustedKeyGroupsItemsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionTrustedKeyGroupsItemsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93fda38cbeb31a505987ee099e5c5eb690ecc9d59b8163732d9bd4de72edfba9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontDistributionTrustedKeyGroupsItemsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ffd572feb9c9328771a6685c304c677015388345a5a7e795236e6d11ca32b6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontDistributionTrustedKeyGroupsItemsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eed0bf40e432117b99e7ea8d473ebacd16998bb68ae73a142d86936409293282)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60711a1b600814105fd8c15abf719f5afb31044312e25f67da5b29cdcb5dcdbd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f5a31d73d99357481210ba1ba1cc1154281235bf6c0568a02efc9e005ad0f7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionTrustedKeyGroupsItemsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionTrustedKeyGroupsItemsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__664f3ebb7f5247b6b860e556e5bf32b794a63078df3aee4ac7ba97167b007b03)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyGroupId")
    def key_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyGroupId"))

    @builtins.property
    @jsii.member(jsii_name="keyPairIds")
    def key_pair_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "keyPairIds"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontDistributionTrustedKeyGroupsItems]:
        return typing.cast(typing.Optional[CloudfrontDistributionTrustedKeyGroupsItems], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionTrustedKeyGroupsItems],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15c9f3b5d96fd8eeb43bee8a7208a82224eb3fd6eb77b9fc1411c4395dc659d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionTrustedKeyGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionTrustedKeyGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3cbcc2520a18c50da7e03c520e0e3241feb386e1c254a8cad7e2b794fa43992)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontDistributionTrustedKeyGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32d05b99c7824feae666e4afc57d06c5dad2c9a89ce7366017b23f0d322033d5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontDistributionTrustedKeyGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4370f4a63f920502828211db51a5429cb9f0f3f26e6fa1423bd9de473fc20ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28e4c0fcc5e26d3edaeb53e9a3f72e78408fc89b73179a68230ec4c20f3cc73f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b84a9027b4818756db32ca0b6298a6bd7f9c3b497a08cd24f6e5f594d86d1cd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionTrustedKeyGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionTrustedKeyGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea1828fe2239c00d08e597f1e73539eccdb14db4644c73e5e9ca3fbc87c4def8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> CloudfrontDistributionTrustedKeyGroupsItemsList:
        return typing.cast(CloudfrontDistributionTrustedKeyGroupsItemsList, jsii.get(self, "items"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudfrontDistributionTrustedKeyGroups]:
        return typing.cast(typing.Optional[CloudfrontDistributionTrustedKeyGroups], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionTrustedKeyGroups],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f13e6152232fbb409294a45a8688dd9a6ea5000f7d372e034dbcf2fb7c57e8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionTrustedSigners",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudfrontDistributionTrustedSigners:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionTrustedSigners(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionTrustedSignersItems",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudfrontDistributionTrustedSignersItems:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionTrustedSignersItems(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionTrustedSignersItemsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionTrustedSignersItemsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebc4b967cfea7f4fee04e66db64299495bbcc4adf7e8450117550bb0028d0215)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontDistributionTrustedSignersItemsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bebb2d048d43996dfae8224629149ee89d6d7eed1a4da108bf51f5c56549e0d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontDistributionTrustedSignersItemsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79a3f2946a75b1787aa9a7e9cf784d4fac57098149cf9458124026e0ac25d6e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0581b6793524bc52a157d83935f2303a61223f3913222bd603de4122b45244f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dee1145d27319fc63c50dd272eac0acb785f77feca67dbe5fba50704e918b917)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionTrustedSignersItemsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionTrustedSignersItemsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92219547d5ae894c4bb2444656a44c5f75fc4c8d2d038ea0efec09fd6f9f81d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="awsAccountNumber")
    def aws_account_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsAccountNumber"))

    @builtins.property
    @jsii.member(jsii_name="keyPairIds")
    def key_pair_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "keyPairIds"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontDistributionTrustedSignersItems]:
        return typing.cast(typing.Optional[CloudfrontDistributionTrustedSignersItems], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionTrustedSignersItems],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e7031cbed5652f455373bfb661d26b56bd1bae33843058cdb715363e9819969)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionTrustedSignersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionTrustedSignersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fdd1d0341217720ae5d2ccbf91392a7f4e1ac4b53fc56c6a75d4a0049b82ae2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontDistributionTrustedSignersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a8b6ec37a5a917111f9658551d3f340f4ca7660654b1a267add8ef2adc9050d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontDistributionTrustedSignersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc9e37df4ae5f231ccbab05650d7d172dd13f84bac6082801a39228784bb26f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7731adcb315f2a477cdb98fd2898997dd730c11c8a7d3e45b00cf855afcbf8da)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a28c7e14b3b791acd9b0e2b40ed13a0b6a9ef28e6a82ac53b5159849f853e49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CloudfrontDistributionTrustedSignersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionTrustedSignersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18bdf34d4597f3d77026f29bb8be6df2a1244de1f4844613e3e7a8e5472c56b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> CloudfrontDistributionTrustedSignersItemsList:
        return typing.cast(CloudfrontDistributionTrustedSignersItemsList, jsii.get(self, "items"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudfrontDistributionTrustedSigners]:
        return typing.cast(typing.Optional[CloudfrontDistributionTrustedSigners], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionTrustedSigners],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__721ccbc269d3c6eb12aa0ec3ec911fd5fa53e6922a39f4a343631b57f4eaec01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionViewerCertificate",
    jsii_struct_bases=[],
    name_mapping={
        "acm_certificate_arn": "acmCertificateArn",
        "cloudfront_default_certificate": "cloudfrontDefaultCertificate",
        "iam_certificate_id": "iamCertificateId",
        "minimum_protocol_version": "minimumProtocolVersion",
        "ssl_support_method": "sslSupportMethod",
    },
)
class CloudfrontDistributionViewerCertificate:
    def __init__(
        self,
        *,
        acm_certificate_arn: typing.Optional[builtins.str] = None,
        cloudfront_default_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        iam_certificate_id: typing.Optional[builtins.str] = None,
        minimum_protocol_version: typing.Optional[builtins.str] = None,
        ssl_support_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param acm_certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#acm_certificate_arn CloudfrontDistribution#acm_certificate_arn}.
        :param cloudfront_default_certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#cloudfront_default_certificate CloudfrontDistribution#cloudfront_default_certificate}.
        :param iam_certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#iam_certificate_id CloudfrontDistribution#iam_certificate_id}.
        :param minimum_protocol_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#minimum_protocol_version CloudfrontDistribution#minimum_protocol_version}.
        :param ssl_support_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#ssl_support_method CloudfrontDistribution#ssl_support_method}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9af1378dd1337388d6af2a165aaa594b90f5fcbbbc3d8ce1f6d98800743f9cd)
            check_type(argname="argument acm_certificate_arn", value=acm_certificate_arn, expected_type=type_hints["acm_certificate_arn"])
            check_type(argname="argument cloudfront_default_certificate", value=cloudfront_default_certificate, expected_type=type_hints["cloudfront_default_certificate"])
            check_type(argname="argument iam_certificate_id", value=iam_certificate_id, expected_type=type_hints["iam_certificate_id"])
            check_type(argname="argument minimum_protocol_version", value=minimum_protocol_version, expected_type=type_hints["minimum_protocol_version"])
            check_type(argname="argument ssl_support_method", value=ssl_support_method, expected_type=type_hints["ssl_support_method"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if acm_certificate_arn is not None:
            self._values["acm_certificate_arn"] = acm_certificate_arn
        if cloudfront_default_certificate is not None:
            self._values["cloudfront_default_certificate"] = cloudfront_default_certificate
        if iam_certificate_id is not None:
            self._values["iam_certificate_id"] = iam_certificate_id
        if minimum_protocol_version is not None:
            self._values["minimum_protocol_version"] = minimum_protocol_version
        if ssl_support_method is not None:
            self._values["ssl_support_method"] = ssl_support_method

    @builtins.property
    def acm_certificate_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#acm_certificate_arn CloudfrontDistribution#acm_certificate_arn}.'''
        result = self._values.get("acm_certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudfront_default_certificate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#cloudfront_default_certificate CloudfrontDistribution#cloudfront_default_certificate}.'''
        result = self._values.get("cloudfront_default_certificate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def iam_certificate_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#iam_certificate_id CloudfrontDistribution#iam_certificate_id}.'''
        result = self._values.get("iam_certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum_protocol_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#minimum_protocol_version CloudfrontDistribution#minimum_protocol_version}.'''
        result = self._values.get("minimum_protocol_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_support_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#ssl_support_method CloudfrontDistribution#ssl_support_method}.'''
        result = self._values.get("ssl_support_method")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionViewerCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionViewerCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionViewerCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ecdc4b477aeca464d11450c89c15bcf1d9ceea24da7fe858a72ab53b5675fca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAcmCertificateArn")
    def reset_acm_certificate_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcmCertificateArn", []))

    @jsii.member(jsii_name="resetCloudfrontDefaultCertificate")
    def reset_cloudfront_default_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudfrontDefaultCertificate", []))

    @jsii.member(jsii_name="resetIamCertificateId")
    def reset_iam_certificate_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIamCertificateId", []))

    @jsii.member(jsii_name="resetMinimumProtocolVersion")
    def reset_minimum_protocol_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumProtocolVersion", []))

    @jsii.member(jsii_name="resetSslSupportMethod")
    def reset_ssl_support_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslSupportMethod", []))

    @builtins.property
    @jsii.member(jsii_name="acmCertificateArnInput")
    def acm_certificate_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acmCertificateArnInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudfrontDefaultCertificateInput")
    def cloudfront_default_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cloudfrontDefaultCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="iamCertificateIdInput")
    def iam_certificate_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamCertificateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumProtocolVersionInput")
    def minimum_protocol_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimumProtocolVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="sslSupportMethodInput")
    def ssl_support_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslSupportMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="acmCertificateArn")
    def acm_certificate_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acmCertificateArn"))

    @acm_certificate_arn.setter
    def acm_certificate_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36bee1a33dd504a2af8b6b29f9ed949f8e058bb02c1e6b54ef759d29edd0aa7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acmCertificateArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudfrontDefaultCertificate")
    def cloudfront_default_certificate(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cloudfrontDefaultCertificate"))

    @cloudfront_default_certificate.setter
    def cloudfront_default_certificate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b526802d4386f85f7504e09da2c846ec5cfbcf955def33f4ec36b70abc396c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudfrontDefaultCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iamCertificateId")
    def iam_certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iamCertificateId"))

    @iam_certificate_id.setter
    def iam_certificate_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aca7fbda846bb08a2b9b7aa0b401152a6884951f6fd24f1321587ef4bfa9a457)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamCertificateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumProtocolVersion")
    def minimum_protocol_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumProtocolVersion"))

    @minimum_protocol_version.setter
    def minimum_protocol_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b998046a190e130640ea3018cc99b9aee039cffd4d86f8f04bac0a308f42b943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumProtocolVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslSupportMethod")
    def ssl_support_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslSupportMethod"))

    @ssl_support_method.setter
    def ssl_support_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__469ce6ae0743b6ae0b60b5801ce0b8a47e3bc650e950ba86aa331699bc4e08f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslSupportMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontDistributionViewerCertificate]:
        return typing.cast(typing.Optional[CloudfrontDistributionViewerCertificate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionViewerCertificate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e502655f10a5874862bb22f02229e90eca3c0760669492c7baf3ff475896ed64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionViewerMtlsConfig",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "trust_store_config": "trustStoreConfig"},
)
class CloudfrontDistributionViewerMtlsConfig:
    def __init__(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        trust_store_config: typing.Optional[typing.Union["CloudfrontDistributionViewerMtlsConfigTrustStoreConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#mode CloudfrontDistribution#mode}.
        :param trust_store_config: trust_store_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#trust_store_config CloudfrontDistribution#trust_store_config}
        '''
        if isinstance(trust_store_config, dict):
            trust_store_config = CloudfrontDistributionViewerMtlsConfigTrustStoreConfig(**trust_store_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc70452d524abca3193d85a556ea1932b00f6268dbf4e29074587ee3b3055d9a)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument trust_store_config", value=trust_store_config, expected_type=type_hints["trust_store_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode
        if trust_store_config is not None:
            self._values["trust_store_config"] = trust_store_config

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#mode CloudfrontDistribution#mode}.'''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trust_store_config(
        self,
    ) -> typing.Optional["CloudfrontDistributionViewerMtlsConfigTrustStoreConfig"]:
        '''trust_store_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#trust_store_config CloudfrontDistribution#trust_store_config}
        '''
        result = self._values.get("trust_store_config")
        return typing.cast(typing.Optional["CloudfrontDistributionViewerMtlsConfigTrustStoreConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionViewerMtlsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionViewerMtlsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionViewerMtlsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcd9e85cc2916304dd04cdef209094463a66623671ee939d5bbcc549d4cd42ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTrustStoreConfig")
    def put_trust_store_config(
        self,
        *,
        trust_store_id: builtins.str,
        advertise_trust_store_ca_names: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ignore_certificate_expiry: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param trust_store_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#trust_store_id CloudfrontDistribution#trust_store_id}.
        :param advertise_trust_store_ca_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#advertise_trust_store_ca_names CloudfrontDistribution#advertise_trust_store_ca_names}.
        :param ignore_certificate_expiry: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#ignore_certificate_expiry CloudfrontDistribution#ignore_certificate_expiry}.
        '''
        value = CloudfrontDistributionViewerMtlsConfigTrustStoreConfig(
            trust_store_id=trust_store_id,
            advertise_trust_store_ca_names=advertise_trust_store_ca_names,
            ignore_certificate_expiry=ignore_certificate_expiry,
        )

        return typing.cast(None, jsii.invoke(self, "putTrustStoreConfig", [value]))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetTrustStoreConfig")
    def reset_trust_store_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustStoreConfig", []))

    @builtins.property
    @jsii.member(jsii_name="trustStoreConfig")
    def trust_store_config(
        self,
    ) -> "CloudfrontDistributionViewerMtlsConfigTrustStoreConfigOutputReference":
        return typing.cast("CloudfrontDistributionViewerMtlsConfigTrustStoreConfigOutputReference", jsii.get(self, "trustStoreConfig"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="trustStoreConfigInput")
    def trust_store_config_input(
        self,
    ) -> typing.Optional["CloudfrontDistributionViewerMtlsConfigTrustStoreConfig"]:
        return typing.cast(typing.Optional["CloudfrontDistributionViewerMtlsConfigTrustStoreConfig"], jsii.get(self, "trustStoreConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6f3b6c78bb800b35b59bc19dca3b8b12a958c2e854c03305017cc0fb26986e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudfrontDistributionViewerMtlsConfig]:
        return typing.cast(typing.Optional[CloudfrontDistributionViewerMtlsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionViewerMtlsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59071d5302c1da301e45f49a084b389da5ff497ab2f8ec63c12bdd7b081f5a95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionViewerMtlsConfigTrustStoreConfig",
    jsii_struct_bases=[],
    name_mapping={
        "trust_store_id": "trustStoreId",
        "advertise_trust_store_ca_names": "advertiseTrustStoreCaNames",
        "ignore_certificate_expiry": "ignoreCertificateExpiry",
    },
)
class CloudfrontDistributionViewerMtlsConfigTrustStoreConfig:
    def __init__(
        self,
        *,
        trust_store_id: builtins.str,
        advertise_trust_store_ca_names: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ignore_certificate_expiry: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param trust_store_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#trust_store_id CloudfrontDistribution#trust_store_id}.
        :param advertise_trust_store_ca_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#advertise_trust_store_ca_names CloudfrontDistribution#advertise_trust_store_ca_names}.
        :param ignore_certificate_expiry: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#ignore_certificate_expiry CloudfrontDistribution#ignore_certificate_expiry}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25acc82073f65146fd36428a6d1ae2f69dc245ae1a535cf07b5cce42c77983df)
            check_type(argname="argument trust_store_id", value=trust_store_id, expected_type=type_hints["trust_store_id"])
            check_type(argname="argument advertise_trust_store_ca_names", value=advertise_trust_store_ca_names, expected_type=type_hints["advertise_trust_store_ca_names"])
            check_type(argname="argument ignore_certificate_expiry", value=ignore_certificate_expiry, expected_type=type_hints["ignore_certificate_expiry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "trust_store_id": trust_store_id,
        }
        if advertise_trust_store_ca_names is not None:
            self._values["advertise_trust_store_ca_names"] = advertise_trust_store_ca_names
        if ignore_certificate_expiry is not None:
            self._values["ignore_certificate_expiry"] = ignore_certificate_expiry

    @builtins.property
    def trust_store_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#trust_store_id CloudfrontDistribution#trust_store_id}.'''
        result = self._values.get("trust_store_id")
        assert result is not None, "Required property 'trust_store_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advertise_trust_store_ca_names(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#advertise_trust_store_ca_names CloudfrontDistribution#advertise_trust_store_ca_names}.'''
        result = self._values.get("advertise_trust_store_ca_names")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ignore_certificate_expiry(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_distribution#ignore_certificate_expiry CloudfrontDistribution#ignore_certificate_expiry}.'''
        result = self._values.get("ignore_certificate_expiry")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontDistributionViewerMtlsConfigTrustStoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontDistributionViewerMtlsConfigTrustStoreConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontDistribution.CloudfrontDistributionViewerMtlsConfigTrustStoreConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b53c9cf7eb10532c2a59b53f050474641b5f4624d695ad265c5561a774209cc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdvertiseTrustStoreCaNames")
    def reset_advertise_trust_store_ca_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvertiseTrustStoreCaNames", []))

    @jsii.member(jsii_name="resetIgnoreCertificateExpiry")
    def reset_ignore_certificate_expiry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreCertificateExpiry", []))

    @builtins.property
    @jsii.member(jsii_name="advertiseTrustStoreCaNamesInput")
    def advertise_trust_store_ca_names_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "advertiseTrustStoreCaNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreCertificateExpiryInput")
    def ignore_certificate_expiry_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreCertificateExpiryInput"))

    @builtins.property
    @jsii.member(jsii_name="trustStoreIdInput")
    def trust_store_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trustStoreIdInput"))

    @builtins.property
    @jsii.member(jsii_name="advertiseTrustStoreCaNames")
    def advertise_trust_store_ca_names(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "advertiseTrustStoreCaNames"))

    @advertise_trust_store_ca_names.setter
    def advertise_trust_store_ca_names(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f411c93f9b9ce338b50c580c3bd21acdea862a2cfb5486e1d7f2e132060671b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advertiseTrustStoreCaNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreCertificateExpiry")
    def ignore_certificate_expiry(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreCertificateExpiry"))

    @ignore_certificate_expiry.setter
    def ignore_certificate_expiry(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfbb6c94955aed28894a6b66758b892ad653889c54bfcbdd2dfb00887cad0d42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCertificateExpiry", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trustStoreId")
    def trust_store_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trustStoreId"))

    @trust_store_id.setter
    def trust_store_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7994be8498cf07f99a5dc73e476f1bfbe2a6f3f71036c8049dd4d4c6e478741d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustStoreId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudfrontDistributionViewerMtlsConfigTrustStoreConfig]:
        return typing.cast(typing.Optional[CloudfrontDistributionViewerMtlsConfigTrustStoreConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudfrontDistributionViewerMtlsConfigTrustStoreConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14bf4ccc0e2ab4183a46fa6c3b9288931b510db68a75362b9302af5087b464a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudfrontDistribution",
    "CloudfrontDistributionConfig",
    "CloudfrontDistributionConnectionFunctionAssociation",
    "CloudfrontDistributionConnectionFunctionAssociationOutputReference",
    "CloudfrontDistributionCustomErrorResponse",
    "CloudfrontDistributionCustomErrorResponseList",
    "CloudfrontDistributionCustomErrorResponseOutputReference",
    "CloudfrontDistributionDefaultCacheBehavior",
    "CloudfrontDistributionDefaultCacheBehaviorForwardedValues",
    "CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies",
    "CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookiesOutputReference",
    "CloudfrontDistributionDefaultCacheBehaviorForwardedValuesOutputReference",
    "CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation",
    "CloudfrontDistributionDefaultCacheBehaviorFunctionAssociationList",
    "CloudfrontDistributionDefaultCacheBehaviorFunctionAssociationOutputReference",
    "CloudfrontDistributionDefaultCacheBehaviorGrpcConfig",
    "CloudfrontDistributionDefaultCacheBehaviorGrpcConfigOutputReference",
    "CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation",
    "CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociationList",
    "CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociationOutputReference",
    "CloudfrontDistributionDefaultCacheBehaviorOutputReference",
    "CloudfrontDistributionLoggingConfig",
    "CloudfrontDistributionLoggingConfigOutputReference",
    "CloudfrontDistributionOrderedCacheBehavior",
    "CloudfrontDistributionOrderedCacheBehaviorForwardedValues",
    "CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookies",
    "CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookiesOutputReference",
    "CloudfrontDistributionOrderedCacheBehaviorForwardedValuesOutputReference",
    "CloudfrontDistributionOrderedCacheBehaviorFunctionAssociation",
    "CloudfrontDistributionOrderedCacheBehaviorFunctionAssociationList",
    "CloudfrontDistributionOrderedCacheBehaviorFunctionAssociationOutputReference",
    "CloudfrontDistributionOrderedCacheBehaviorGrpcConfig",
    "CloudfrontDistributionOrderedCacheBehaviorGrpcConfigOutputReference",
    "CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociation",
    "CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociationList",
    "CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociationOutputReference",
    "CloudfrontDistributionOrderedCacheBehaviorList",
    "CloudfrontDistributionOrderedCacheBehaviorOutputReference",
    "CloudfrontDistributionOrigin",
    "CloudfrontDistributionOriginCustomHeader",
    "CloudfrontDistributionOriginCustomHeaderList",
    "CloudfrontDistributionOriginCustomHeaderOutputReference",
    "CloudfrontDistributionOriginCustomOriginConfig",
    "CloudfrontDistributionOriginCustomOriginConfigOutputReference",
    "CloudfrontDistributionOriginGroup",
    "CloudfrontDistributionOriginGroupFailoverCriteria",
    "CloudfrontDistributionOriginGroupFailoverCriteriaOutputReference",
    "CloudfrontDistributionOriginGroupList",
    "CloudfrontDistributionOriginGroupMember",
    "CloudfrontDistributionOriginGroupMemberList",
    "CloudfrontDistributionOriginGroupMemberOutputReference",
    "CloudfrontDistributionOriginGroupOutputReference",
    "CloudfrontDistributionOriginList",
    "CloudfrontDistributionOriginOriginShield",
    "CloudfrontDistributionOriginOriginShieldOutputReference",
    "CloudfrontDistributionOriginOutputReference",
    "CloudfrontDistributionOriginS3OriginConfig",
    "CloudfrontDistributionOriginS3OriginConfigOutputReference",
    "CloudfrontDistributionOriginVpcOriginConfig",
    "CloudfrontDistributionOriginVpcOriginConfigOutputReference",
    "CloudfrontDistributionRestrictions",
    "CloudfrontDistributionRestrictionsGeoRestriction",
    "CloudfrontDistributionRestrictionsGeoRestrictionOutputReference",
    "CloudfrontDistributionRestrictionsOutputReference",
    "CloudfrontDistributionTrustedKeyGroups",
    "CloudfrontDistributionTrustedKeyGroupsItems",
    "CloudfrontDistributionTrustedKeyGroupsItemsList",
    "CloudfrontDistributionTrustedKeyGroupsItemsOutputReference",
    "CloudfrontDistributionTrustedKeyGroupsList",
    "CloudfrontDistributionTrustedKeyGroupsOutputReference",
    "CloudfrontDistributionTrustedSigners",
    "CloudfrontDistributionTrustedSignersItems",
    "CloudfrontDistributionTrustedSignersItemsList",
    "CloudfrontDistributionTrustedSignersItemsOutputReference",
    "CloudfrontDistributionTrustedSignersList",
    "CloudfrontDistributionTrustedSignersOutputReference",
    "CloudfrontDistributionViewerCertificate",
    "CloudfrontDistributionViewerCertificateOutputReference",
    "CloudfrontDistributionViewerMtlsConfig",
    "CloudfrontDistributionViewerMtlsConfigOutputReference",
    "CloudfrontDistributionViewerMtlsConfigTrustStoreConfig",
    "CloudfrontDistributionViewerMtlsConfigTrustStoreConfigOutputReference",
]

publication.publish()

def _typecheckingstub__9ba742e51779c85665248759cf5fb9e3d4e87f3afa826c08aeac0664bf0c8236(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_cache_behavior: typing.Union[CloudfrontDistributionDefaultCacheBehavior, typing.Dict[builtins.str, typing.Any]],
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    origin: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOrigin, typing.Dict[builtins.str, typing.Any]]]],
    restrictions: typing.Union[CloudfrontDistributionRestrictions, typing.Dict[builtins.str, typing.Any]],
    viewer_certificate: typing.Union[CloudfrontDistributionViewerCertificate, typing.Dict[builtins.str, typing.Any]],
    aliases: typing.Optional[typing.Sequence[builtins.str]] = None,
    anycast_ip_list_id: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    connection_function_association: typing.Optional[typing.Union[CloudfrontDistributionConnectionFunctionAssociation, typing.Dict[builtins.str, typing.Any]]] = None,
    continuous_deployment_policy_id: typing.Optional[builtins.str] = None,
    custom_error_response: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionCustomErrorResponse, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_root_object: typing.Optional[builtins.str] = None,
    http_version: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_ipv6_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    logging_config: typing.Optional[typing.Union[CloudfrontDistributionLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ordered_cache_behavior: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOrderedCacheBehavior, typing.Dict[builtins.str, typing.Any]]]]] = None,
    origin_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOriginGroup, typing.Dict[builtins.str, typing.Any]]]]] = None,
    price_class: typing.Optional[builtins.str] = None,
    retain_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    staging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    viewer_mtls_config: typing.Optional[typing.Union[CloudfrontDistributionViewerMtlsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    wait_for_deployment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    web_acl_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__f74acc3271f151e835bc4f31df589a52ef94af01e57658ea6e37d5b1193643ed(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1551c62d004dc3dd25c1766b000d02b23cf79d4fd31fbfd61dd7f73b4794c9e4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionCustomErrorResponse, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce75e0f4b5143d55e6b8ae6535534e9a937b7ce522a198007737262e2b0cdd25(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOrderedCacheBehavior, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ebe65b6476340c6f4fed99fd305accc27e6f1231fc7f0b469f6fef4daee5f5d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOrigin, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84359cef9500b744d8f11519d9e977b9e81a4e13349772ace34173d5242614a1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOriginGroup, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b340a15dbf11078679c86eaa19c488ec8096d436ff58ad0ed7530bd38d376ebf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c89c3d17e3b49394c293512d57f8282b71086bb7fc16975010c50f3817e9c3ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ebe827d0ca2711cfe1bd051aa344e52c77eda4b2284aeb50382c82d7b60efec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e30728b8fff46b0264ede736a3c68c3dc6eac68d079a3aa0f5677df3fdc4249b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0de6b02061ba8d66451350bfe8499de91dac7ff3db62de9db991e0296dbb96f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae0792e2f5c7e114b1a2f19be78a6ba447b27f0aae73b3cafa2162baca9624d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e4d8d6d79f8bfedabc21229ba541e02f8dfedcfc840e51c4d66987c55b0164(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f449cc7c227d4cd798b526cba8deee75b8118f1f7103c7ea9773c281d3c75850(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79bf75639d76db494258c2e1620b4a4e9d7480a918aa0f08d615aba13961c89d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7189538c4dc11bb641d3f56306c4bf136e69a48bafba15db88c66bfc862deb4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf59b0ab6783d3b18d49d6ff1684348a9f3ada2ea8902d833bef757950c7c555(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7fef9703e5a46cb736cd916f7503584b5c585c9cd2fca143f4d6ee00688ac1b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2dea6b3eb9f072bcf8a05415213884e79292da51e88b53677fa6a5cc698ebd9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2bb0329bffdf88c112ca2e418d9f512a220909f5526ef0f5fc60c4e8d383cea(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ad14abc8660cfcafe79c40248b111c8f96aec62853062050feea927765c0fd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65aee952aa4e651a1f45f349d5dad08a84bbd616478bf42029950b0eb120aee9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a778aae6002d6970e024f74b8e96456d5d8a6131c12682a408186c7edee3f0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_cache_behavior: typing.Union[CloudfrontDistributionDefaultCacheBehavior, typing.Dict[builtins.str, typing.Any]],
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    origin: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOrigin, typing.Dict[builtins.str, typing.Any]]]],
    restrictions: typing.Union[CloudfrontDistributionRestrictions, typing.Dict[builtins.str, typing.Any]],
    viewer_certificate: typing.Union[CloudfrontDistributionViewerCertificate, typing.Dict[builtins.str, typing.Any]],
    aliases: typing.Optional[typing.Sequence[builtins.str]] = None,
    anycast_ip_list_id: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    connection_function_association: typing.Optional[typing.Union[CloudfrontDistributionConnectionFunctionAssociation, typing.Dict[builtins.str, typing.Any]]] = None,
    continuous_deployment_policy_id: typing.Optional[builtins.str] = None,
    custom_error_response: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionCustomErrorResponse, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_root_object: typing.Optional[builtins.str] = None,
    http_version: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_ipv6_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    logging_config: typing.Optional[typing.Union[CloudfrontDistributionLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ordered_cache_behavior: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOrderedCacheBehavior, typing.Dict[builtins.str, typing.Any]]]]] = None,
    origin_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOriginGroup, typing.Dict[builtins.str, typing.Any]]]]] = None,
    price_class: typing.Optional[builtins.str] = None,
    retain_on_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    staging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    viewer_mtls_config: typing.Optional[typing.Union[CloudfrontDistributionViewerMtlsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    wait_for_deployment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    web_acl_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ec01a0f107577b42c6500a2d43498ef5051e408e2e10c2a1faef000f6d5ed2d(
    *,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def3d2362b7934484ffc8ce4bee8e1ba8e34ae8c5b4da3c116b7399fc3190b77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8332f6ed7ad0fcb68bdf9a1330c9654298188d4249570cafab7d91e5dc6fa79c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77d7948c6b71751aaf06f77bf01a090103d317bbaa7fc72aec8a10645651978(
    value: typing.Optional[CloudfrontDistributionConnectionFunctionAssociation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50bb8b09d5eca03761314f8c035e825b140439adbe7e1c49bdb2e2e6008c0315(
    *,
    error_code: jsii.Number,
    error_caching_min_ttl: typing.Optional[jsii.Number] = None,
    response_code: typing.Optional[jsii.Number] = None,
    response_page_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e659840541bf513c9447554d9f272da59b1659311fc46db53d7c8722aa6320(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1edbd73850098b9a0f80e698215b227fb0dafe4099f24bb6f7947a85df94544(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16dfeb79bf3805b4b688f9f0a1c98a812724cea30673255fd6a940d05cd1c7a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51f0299bd82a28a5106877d1c9fb479a2109bd95b4acabbd331045609063089(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d0bdec176bbe3c8765b16c4f5e630f3c6b5a55240b4a148d8d2e23b78fc476e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da9610df82580608387da55c262b14f2401dd05324709d0473dd304148270809(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionCustomErrorResponse]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__957c4b65d403d5f3464928b31f537c56fec953905a08b425083fb6e5044d5617(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f7284a800ac0f16d55f8b5bf7e7db19df255a86cee205b0a0046a052e9274a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7ac291b8c9e099aacb2a294fd19b4e1585c0c6d85fedf044b155383f032a36(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae2146406b989cee68d5950a84dcb685b2b3a8fb9dd5d5eed8d91865154596ec(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adc1d5110f923705e22e0cf694268c26e45e87359621a322aeef850d7b4412d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10de61fa6c418d2f3eea1657ae2b7885833aa7ef547df2d184d6eb0df74f6bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionCustomErrorResponse]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da0babe2622ca73b92bd536cb65d3054373a9e50240c7ae5e960eccd8a82c84(
    *,
    allowed_methods: typing.Sequence[builtins.str],
    cached_methods: typing.Sequence[builtins.str],
    target_origin_id: builtins.str,
    viewer_protocol_policy: builtins.str,
    cache_policy_id: typing.Optional[builtins.str] = None,
    compress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_ttl: typing.Optional[jsii.Number] = None,
    field_level_encryption_id: typing.Optional[builtins.str] = None,
    forwarded_values: typing.Optional[typing.Union[CloudfrontDistributionDefaultCacheBehaviorForwardedValues, typing.Dict[builtins.str, typing.Any]]] = None,
    function_association: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]]] = None,
    grpc_config: typing.Optional[typing.Union[CloudfrontDistributionDefaultCacheBehaviorGrpcConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    lambda_function_association: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_ttl: typing.Optional[jsii.Number] = None,
    min_ttl: typing.Optional[jsii.Number] = None,
    origin_request_policy_id: typing.Optional[builtins.str] = None,
    realtime_log_config_arn: typing.Optional[builtins.str] = None,
    response_headers_policy_id: typing.Optional[builtins.str] = None,
    smooth_streaming: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    trusted_key_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    trusted_signers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2958489a8ad983fd9752df72108d42306a99c56d0e015f9b8b3ed4f594d83593(
    *,
    cookies: typing.Union[CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies, typing.Dict[builtins.str, typing.Any]],
    query_string: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_string_cache_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afdd8ef36313698961fc250b283111d2c3e7a6822ddf7e7f6766727ed07769c8(
    *,
    forward: builtins.str,
    whitelisted_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__977d7efc21860bf92b3dd2241b39379b4d6489bf201b198c2f5f7da65d4995a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c8ce14bf5d299b86427552c34fbee8dcb7d06de948821a129b45f17f87ccda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d758c8f9cc4b23b18cd6c2f6bafb86e384cfd42ff06309e60600ca43267f30(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e3c2821f5f87c2a0f28e53108ddbb8679951585ceeb4bbd55d527016a4ea989(
    value: typing.Optional[CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb88192d3b855dc3d0ef5e18e40035a0ffcf8f110daca25d479911dead093723(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e55ae64592d6e33d7710eb1904e2c2ac6b3eb6a46619c364a33017ce690f72c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__885f45347497938eca1436141f7ab0d8ee4ece620ca902997bc7f40c0521c38a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab4cfc3e1c98353965dc5d3798102b696a86cb4f6ab50651f8b15696ce53443(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310189ae4609a68a1893d31b062c7456533ff802b8c4d1c22cb67c02394faa98(
    value: typing.Optional[CloudfrontDistributionDefaultCacheBehaviorForwardedValues],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65da29b8d3d2bf3d03b6ae00dbc177f563bd35a04b03c1a0cd1eec048ba87f85(
    *,
    event_type: builtins.str,
    function_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9a1cd80f1b06d93e300c6c23d62b702cd096bcfc4f2d8da9762ee1441052e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8014e0fd903b33fa23e9efdd31fe96e9595bbf58c8ab685ea81e944d4b59cc51(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd06e86fafee34197e0e9f3a55f0a29233c63807e5eb4c4a420830f086b9d4e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b92e8f795480bb2da5e83e4d3f62013d4a4b20c0def938f5484f2a3871f88212(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a387a37bff151eee6e9590ca8bbf55215eb0195d46d35bf3f23d2b5cad4017f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe8212e43fa5a1512638e711eed8c0fc5ead243cefa5cb3002035fa18b60faf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e82723574d83b6f8ffc06718b5260286b3fcebf3fa342613f65759298aa563c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c35bf5fecef7b676006fee586097defc9276166527706d021b82193f3a9c1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3dfeebbe6d22b638fed685ad0f5854121901a1f32e84331021cc2a0f9ae06ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3621e70c2baae7a5be4029a0e29cc46c536e837719e5ea2df6b133c475cc0958(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bfa838e5b0ba28cafe1f68733e2c281923c81963745f8ed3c171c8236032125(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63461a283761e6615101ec89435e3bdd166d2d92976fb4b6c4120d4b62fc34a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a7df54d92f349cd445a6d03a3191b3dad76e5f21a87c6dea445a933e188fcd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee97fd16d3dea579890a8499c227e42245eebcf04c6e49376799e7229bcacd5a(
    value: typing.Optional[CloudfrontDistributionDefaultCacheBehaviorGrpcConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ed01d8eb9beb1253ea561d8466da04f6efdae02a848c3259e50dcf02b9a9e7(
    *,
    event_type: builtins.str,
    lambda_arn: builtins.str,
    include_body: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1947cf193ecd3e22d31f810e1cd52c05c24df683d5d9efcecb2a5da754266293(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0866eba6159126b477c1b7d20afe12778b287f387f56bd7ca7586b6b6d60c9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e03acade586ca12737d4108b157e827620eca670a0f55773cc42de65af8a1045(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c43406a952d564a0b056c4d7c2a6367dab8d7a93b0b52cd7e33268cfb3a46a8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e19a18a7396f207407b1abe26f42bd243a6d69937b6429b338dbaf5b2e010e71(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051db0f0e9c2df45238b0c9ae49893cf0f186e599732a4c84e4fc76fcea9fdea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b9dd2b29db3e910b91909396af4b283ed9e67fcfa311efaf06d21613d9dea0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee51287f8bdc38d8a85fd77484a61d264fbe819c00836401cbe7ed356187d49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457866f3fab2303502e29d146b661bcd567c381e57115563913d9ffe583d82bb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b1ad34c863f822d330c45d047c2a8efa2848b9a4a6ab9de08f8f4213575eae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c753ab2d1236a884e86c9b693611614f7453a654a6a11e2998b3f327caef40(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b4e38f2c4050a5cf2241d4488a1fd87f1ed66d012fe7ae41cf997b120f760d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9366100fbcc7734185b03eb5fde859225e6036fbf96f7a73315a424c8ccac17(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionDefaultCacheBehaviorFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__224c6a63827f2e67981ab40775bf69fdbca7ccf07994fd88ebfac4ed96c478a1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionDefaultCacheBehaviorLambdaFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb681a4e747c920b374a24c0a1e8564958ce5c5d49d0f78596ca6ccfd912e20(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab847365125ec359a4e36a4527377e10a409e85d511e1e373516f2aaf2e961f4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f72fab6ed020275604802901b9a51e32744190983c09e7a0159419a94f40deb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26397b5f40ac3fb32365514cb54c736277f56e62ec3157805a02529364cf3d2b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3bdb986a6ea7b252ca3fa0c7d013a06bc9b0066b13671c827b88b71d74bca1a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c305007ee769cfafb6d2099e1a87d4968266d411e288da929e0115a9086e63f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e675552b61bfa75e398748f0860fbea9de9031cdb3d5afd398b79547ddebc86(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ff939293494b12fc38e4d1e1ed79fd72aff425409d6a99d84c6b9df7f44853(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec57c7aea7de5c9fab628fb2de6f4ac012308b91515fb024dda44d1100a4f79e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fea5adaf39e3a19d2c4dca958083d5f67697cf5d2d2cb81e5b0b4a79f57c46f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e1621f459e3522f90083d3488962d14f724eac4cf41140525e127edce2fa8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d7c70dfde84c1ad0b7a10192a363dd96f98a793e2fcc8907a36ba78a0b99fc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__986ffd05b8ba5e86055d86908504810136da10ed205fc7ab4639ac58f982e394(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c17e7f37c871458a6780dadf04ee2b4659981315c589e060b965ae0623ba8a38(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e3886725a0512fa4880630da7838add020f1853e472ad4490b55e06e3a05a45(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe3f2193d9314ea754e3ec461db0d5c62dbb5467d47f029454ad7631d1eecd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78c0025ceaacb8a86f0693fb59345ddea6945e87cf1ca81e59e089d85eb840e(
    value: typing.Optional[CloudfrontDistributionDefaultCacheBehavior],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836d73ffe7c9e47a9daaec8b9194430d6da21f1150a066afbd4da3d229456c62(
    *,
    bucket: typing.Optional[builtins.str] = None,
    include_cookies: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99142b0782db984627518fd6daed8a91c704702a03681b175fc22be37843ffc5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__336fb057503f0dd85b1cde0a896d5df858053ce2c3501c1aa37334a5c9dfbeba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02718a4ea5309e329c02391109f382afd1ba3b37137ad8f520d44818088b11dc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86069df8ad95c2f9ecab8056aa20216b269d1b47348a108c1ff05c1b1f6814b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee46a6db9455f5fd1e5e7f21009434ce58f547e65cde8f3873cecdfb736f1cb(
    value: typing.Optional[CloudfrontDistributionLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__744e39b86cfc9fc2539f6e35cfafee5066f21b076ad262b2ebc780936fd45286(
    *,
    allowed_methods: typing.Sequence[builtins.str],
    cached_methods: typing.Sequence[builtins.str],
    path_pattern: builtins.str,
    target_origin_id: builtins.str,
    viewer_protocol_policy: builtins.str,
    cache_policy_id: typing.Optional[builtins.str] = None,
    compress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_ttl: typing.Optional[jsii.Number] = None,
    field_level_encryption_id: typing.Optional[builtins.str] = None,
    forwarded_values: typing.Optional[typing.Union[CloudfrontDistributionOrderedCacheBehaviorForwardedValues, typing.Dict[builtins.str, typing.Any]]] = None,
    function_association: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOrderedCacheBehaviorFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]]] = None,
    grpc_config: typing.Optional[typing.Union[CloudfrontDistributionOrderedCacheBehaviorGrpcConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    lambda_function_association: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_ttl: typing.Optional[jsii.Number] = None,
    min_ttl: typing.Optional[jsii.Number] = None,
    origin_request_policy_id: typing.Optional[builtins.str] = None,
    realtime_log_config_arn: typing.Optional[builtins.str] = None,
    response_headers_policy_id: typing.Optional[builtins.str] = None,
    smooth_streaming: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    trusted_key_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    trusted_signers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a4698074d9ecab848380adc22e78d5659d4babe7fe0405a0058bbbd723487c8(
    *,
    cookies: typing.Union[CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookies, typing.Dict[builtins.str, typing.Any]],
    query_string: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_string_cache_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a50fd00614acdf1eeefc9e1d5bf73fc2cabd0422e1d0ceb204c6433c6df94cb(
    *,
    forward: builtins.str,
    whitelisted_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac2499b0171f47e122fafbcbcadb19848f588695b4837d266ae23a4d9aaf853(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e0c2ad64362dc329b9ae8121baf072d1754cba7faf19c1f4aaa5ba7e04214c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad06b2ae020c30b939dc0986b953c093b3e09f204af232bbe10767895f2b6558(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3c82fbf8b294691c91f3c33cade46ed47c316177b18ee73620b4c5e6a1bc035(
    value: typing.Optional[CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookies],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f33be41dd57629be8a2d3d6bdc4364958d88de8cf615e25d08a9e60c9e34f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebae7c929a1d7dc9c3f5fb7b9b6a791b8ab9f22181cee8654f7ab3a0bf439400(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a08c56a8257af6eb1687be3e8ffa6a484401ec2fb04afe28678822743106146(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2222eeb0eef5f9b1fbe35a829db72ef954cb35225cd8ea9ecf7a5a2bd06cb52(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7888500d4158ac7801531012f1e83a38bdf3099f3796788f8c94d8ab139a76c(
    value: typing.Optional[CloudfrontDistributionOrderedCacheBehaviorForwardedValues],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1de4a27340508dcfd07461ccbcae5c46b9df71ec5ae3aed84c917aa5a9f1b7(
    *,
    event_type: builtins.str,
    function_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c69d4946da36770726dbf5ed9bb53f5d88d311aa33e836a0819e121213cc2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b89cc61eb8e929d2751d04756429f31803e1f4b3812eccd426b3c5ffade9de(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc96c19d2a7acfbdb6582abbdffdc2de37ea82d54f11958c13fbe34349714336(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38d77c5ba037980f6fcca9c94375cd3a2eac0da79237af235fad1e990166907f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc2d30948d2501171cd0c8ae352591ad4173345eba5945b1144e388c02e0240(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7bb36380e9f003586a7e8cd57e9cc2ba344f48f6f497d375d408c10d743e19(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOrderedCacheBehaviorFunctionAssociation]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb45f09375a534e5de21a3985c57b868df014bba5c6e197a24fb0a796cb7d7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2283ad81a1fb66b2f2195d72dec6682ac826e817946b6f7f96275a249de2195(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4543cb53f3a2b510cbe938f369337d50a5e4362cf16f5179c4d6b12987d12bf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eecedbbc1825fb5719b3680b685cfa9248937baed56dcd74f7de2b02f8946c11(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOrderedCacheBehaviorFunctionAssociation]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1071d92d7a88ce077d25af6d32af9d6f90e642a62f446df0e11a87c419547e0(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f342a92bf8a5b45d202c4f543c7d8c86d40c5e6c789cb6ee52082c3542984b17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a1c5d48a1370faf0aed23f700f43697cca8a8501fd882077ae7bed9143fa3e4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342996609c8f0adf3eddff2d0b36d1b003760acb7c84974668b062632790a9b1(
    value: typing.Optional[CloudfrontDistributionOrderedCacheBehaviorGrpcConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a16cb1ea31aa22899fbf50a01ff701c57a02e713ae83b24858dbb5ea49b10f(
    *,
    event_type: builtins.str,
    lambda_arn: builtins.str,
    include_body: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f160ab48a8b1f8a198c897c06b10bbfdc61261b24560cb143cc86c081a59aba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__139c6ff2e0c6f2f5985c648d66b98a6cfdc5d1d6e44e69e9b2c684b144966ab3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__615999b5f3cbb508441b2ffff9f69d7856779925b75bc9062d89a7c7efd5331b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a276f8d078e0ed20c7b7f28c36b13a2a9efc4dd138ffb2df33332dbb05cf5e4f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e16de40c01c241fc1c70bdd78a9a4af32d2b57e1341d4aaf5c820dba5cbb2b8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2747678f1c6d72ff107a61b5927ccd008cb9b4e64c27189668e6a78994f84d47(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociation]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d41e4bdd1b4a7df139f863e7c02028ac6f3ba2cd8eb4c859f11cbedf30bdfed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc55a3f1fa9a0672102affcc757f35852bf9f33aaf82c2f4f4a1b87c5a7f9dea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f156d517f8cb4ecbbd3b1208441ead4314f81d94f50abca29b7c438c8f453dd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea8e9fb7f6cb7576736a982644a1cca2dd1452b2dbee5cea77b8c2c9d42ccdec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c5d26a9af401aec04bd9e92044c3e3717fbb03680ef5c3f23ef363061c2738(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociation]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86afacc7d5b05412992a8b01a8d152e0e2a58155a4c5aa5d01c55bbea4223b82(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466ab320fe7ff51db95de0f2f9e523a4791255ee1e153f4ea1df7523297589a9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a720dc34f5f71abc6e21b552147e2fae4b17fea133c642c3504514654949bc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dba448b026a1f62883606218cfe08f31adabec3c57bcff2789ea2ae76398ff83(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a8e028d6543632e996ab4d6584d80c4ba1f8dcdc2309a83a4620253fa06fb9d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe570985ba78f0b917ed180d3b9e95bc7d2f909e5d33c1eeea9934fb30daa1b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOrderedCacheBehavior]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73c15c04b71404321f80f95eb2af99356c3a1ea29b3589c3e81e8477a5610c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e630f6950842fd4c0c9f9d9486fbdad3afb036b8c29ca1d1952e8b1236a03fb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOrderedCacheBehaviorFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8273bf6718d3bd52eb7649e14118a32c1937c1bf19ed4b04f8e0f4e4e594c8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOrderedCacheBehaviorLambdaFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c4613be14e544d067c2caa941ad6b1cee48823ef5f85ad885c79b04a9323e95(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e9a9d114ec3b8f3177d6cf870d68327a09036a0e20efc2cab3c77e859f1ff3e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c712dbd21049ad92ee958a08e2d7b03f0aaedb24bb521ecf9abdfacd904c04f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7592c9b08d3e863d634368ba8fdf4e97fc17938c5fb469b633376e06bd5d3dbf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ec444be5e38b30a5ab1cb2811497f074f1f7122fd74ce31febd7559e2f2aa0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e9b1c90aab0e3bea249fe9600452ce382e39ded84e4ebd75e69f873982e49dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea03542db755abbc39a1dd6f4703e9245b7a4056c21a5ce0127a407dc1e20a8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d1c328d8793237f37e5299551f17dc5997559cf048c1ea831f488b4e05d7218(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5214c2aba9ee5a269d34701b43b0371c68a0b9a334a1d10abff524d92d6a7b4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ece3b566c0ff665b3d127fed18cd367e6d1ffb6109d8a325533b173466ec59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f98f3c6d3eba29df91c7af127ef521cb784f17d37693d05d09f884e73eb6a86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be7ec773669ac8c67850762c61dec2de685c59f6ea64d23dad089af159a6c92d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b42e9bef9c02f3534662b4eb04222c18e4f99b555c728411985dd77c19726eb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a633c395b5b3c9650679020adc22bca1424feb942f961ea5782d28e2b3fa50fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4bb9fdd55c1cf35d9c02d3b141ec9eb2ac86ccae42f4eaa2b69be94700d5be1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa05d966696ce12854dc156f8c7a0bc4d868f40dde3c5221acaf4084af0ef2d7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a5599cca94582829db84e45febfb7cb6a64ad683fc2f047920453527131af81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853089461b27529531924afc5971c838136be7ae8b870f868814aefbb21b5482(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOrderedCacheBehavior]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c04669ab32ac2265f9574cc11d512177a84ff5e4a49eff644c11625c189499(
    *,
    domain_name: builtins.str,
    origin_id: builtins.str,
    connection_attempts: typing.Optional[jsii.Number] = None,
    connection_timeout: typing.Optional[jsii.Number] = None,
    custom_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOriginCustomHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_origin_config: typing.Optional[typing.Union[CloudfrontDistributionOriginCustomOriginConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    origin_access_control_id: typing.Optional[builtins.str] = None,
    origin_path: typing.Optional[builtins.str] = None,
    origin_shield: typing.Optional[typing.Union[CloudfrontDistributionOriginOriginShield, typing.Dict[builtins.str, typing.Any]]] = None,
    response_completion_timeout: typing.Optional[jsii.Number] = None,
    s3_origin_config: typing.Optional[typing.Union[CloudfrontDistributionOriginS3OriginConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_origin_config: typing.Optional[typing.Union[CloudfrontDistributionOriginVpcOriginConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d170d3d0d677eefc7d2d592475b85bf2fbd875783bdab005967149707ab2e242(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2afa0a7db74255c43ced6a740fae4c4dab92d3eeba8eacb20e59b6b55db2afbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1da5891ec90c5b1c8d9ba7ffc1873e3b388cf820a2bbd95158d08e987585d2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68a0ae924d67d981caf0954dd8827aa2b4170cc7f9644b8f4b1482e2caa3a11d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f616d87e59a38bb1a1b5858642b79c728cb8ebce93c021a02ca20c0b1d9a6a7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457f846392373179c62026e421e03e302d82d0163fa2fdcdbaec6a6295b48e06(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637f1defc6f4cd3b54d72820363cf0e3b41de89da991e3104acae81c06b10282(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOriginCustomHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6dbe53bff37c0cbe32b3ff2454181c45258de86f6eff163e485f441e7f71c55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62976c8edbf0dde192f90d8d16fcfe4e29d61abd3ef3214e492ae50d783d30b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718c0190709dca852784c84bf8ec0d2b05b035cbe780ef28c3a4315211e0e542(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1f0594df4268e4c1ad811bd1adba5a312637a6dcaef585725d8f2a03a6a197(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOriginCustomHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c26e133c02c7e5899651f8568987d382a785c06b7283eecadc93d77ea5c2f47b(
    *,
    http_port: jsii.Number,
    https_port: jsii.Number,
    origin_protocol_policy: builtins.str,
    origin_ssl_protocols: typing.Sequence[builtins.str],
    ip_address_type: typing.Optional[builtins.str] = None,
    origin_keepalive_timeout: typing.Optional[jsii.Number] = None,
    origin_read_timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1051854fac4249b59f6cf4d061211d150e3e6a1f1fde964b7a8a5780d8c54d80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4db362b08cddb21aaa1affae6312685a355b6dfc2ab3e33bcb63776417df7eb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e30b83668b0d900081f70ec66622da3069d78263f89742511ff37c9b5be7090(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f09021c90cc96b3682eacfcf45814efa58d73251ba37a71b617746f1679960(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e0b47ee490a9f8d15e837dc0124e8f1f3d09a548e57701651cf1e62580f3a5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b452fc9f225e6948b7eaba9d67320cdf2bdd395f3072163ba7ebe809c7b90e7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b1011231312d939832868e76f2ce69098cd4b9be10d334dc815768285025065(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46898499ea952c358bc51b5c297310c877ac162d55376af917075c5f8fc651b2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b2823fa2be1053a6e1dbda19fcd780af047d008cba0c0442fce1fa1e39ee8e(
    value: typing.Optional[CloudfrontDistributionOriginCustomOriginConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45cc4ec445a740ea95f24a58c0e9ef1b1f28f02802fb4a99af598800d1f19e4(
    *,
    failover_criteria: typing.Union[CloudfrontDistributionOriginGroupFailoverCriteria, typing.Dict[builtins.str, typing.Any]],
    member: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOriginGroupMember, typing.Dict[builtins.str, typing.Any]]]],
    origin_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f410973ca4d5c38fa26c154c8a7d4659bd9b5586bc22a14c235c82a96266a0ea(
    *,
    status_codes: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6820e4b88be3848f56cddd960395556a66efb9b6a6f1ea085f8010d3196882ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c298897fb722d7e10595d783e89421a5a4ae059caac484e9212f6b6a35d7cd(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b289a5e15752d3a2384c2faf53946aeefa665659711b3f9a61d2c0abfea110(
    value: typing.Optional[CloudfrontDistributionOriginGroupFailoverCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2d178fc83943220a28dd400aa5aa06a099a6ad9d974f374156aa2980ec4b6a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7976c9d54a8055d70b73ac480d943342e835ef08676cf2bc6d635e498165eab3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17f04957afc36ec06e77cbf5600ec420af26352b9d5e65bdbe578e9d8ac06b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9428a5ab1dc5d82520cc255cc6e0dee16d150315b302f5f82b0111d6737bfd86(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2b9c1350e90484e3d39996b17e99237af8f96766d4f983cc4c879a6f5478f7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a5d83dfa14c9466d74e3afd03d5745a440fa93a844678dee7f5243830b56bb4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOriginGroup]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d53b4b53ae7713365657be8080a0ba7dff1634d54e92d7fc494ab1beecbebe1(
    *,
    origin_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d791e8d99c4abb77956374aa94f37380ba5865443615617685800f7bc801bad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ca68eab62d4194ee34f5e3f547683f23af9a11610c221364886f8a8c3c9708(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea912299e98d20c23d4c9b35265d743fb4ca2950a2c2ca09184acd3f3c755b90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9fc4aaab33ed97ee409f3924fa7ecbca0b42e8c80ff60908a66d59b3b674420(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1dbde4811a19f96cc2adcc82652ba00998d3ad49f310aaaaccadd8ad027d1e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab0e782b9bfadd85ca52f999be2c6e73ed889945ebd1b742b44fd762cc040743(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOriginGroupMember]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6408a117b5da685d32a2e5c338dceb8747a7dc225cb1e26eaf15cd53053d72d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e39f74c3e469c47264d9c63dd9a03d24836afe9e1aa72626e6c75ec7547505a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb86215355a6f5b1a52d1bb6870681fd84bb8f216082e908ce83ee7bcdafefc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOriginGroupMember]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b3fe416a00b22145bc013f1a162ba6d650fa70860304e1d944f3f59401c0aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7aad23219f42e9e39d0886d676358f8ed0104126b4be27fb08aca4383a870f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOriginGroupMember, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a38f9a269f6748479aa6893482be621bc76f39c5c0af59393b3de72367dc9f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__055485c8b7d08914c431946381ac18dbeb83adcc9b3134421b77cd7d11c4136e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOriginGroup]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f57aaa916f83b4dea59bb55013f3aa3ffd574dcc671c4f3b43bf619c877b31a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cb2258af00e60eb5fa8ab35c5bb01d3f2843f43fe8ea91878e7e0e3ee4174e3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a56d69efda63db98bca6dc8d19f79c06a6ba74ec693b1b4d32fc4d0698b7a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7c155f04af18eba90ba8a4c43f9f792a8a9d5939f474153e30d9ceefa28b2b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a294b3e484df55778b8c2de3910556d8b90709cee16310974803866cba75d2c3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c515f32a8434f2acffa8e83b3c59b02f5fba3a82d45771c4b27cf70562bf06d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontDistributionOrigin]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79183e516f93dcbea116a16c74402941f93504e2ad0b4ecf29b728a9fe1dd4cc(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    origin_shield_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__278c2cfbd5ef79c40ec0f2a2709063800f3bc71c557024d4b13e91611f7ccb7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__031e8b377318b8c96c29282a6411b46b2ace438c1a0bc87eba7a3a4cddaf0d36(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f2eb69dae2cd88571da72f1c0293eb8451607dad0a2d6eda33244d464d784d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49c46f0b15f2456605d4a7756a823c58e682adaec574137650bc1dbbfd9e63c6(
    value: typing.Optional[CloudfrontDistributionOriginOriginShield],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381642faf9a425d3c8081409f7ef57a75dddbbee3a24fb05c958e1adc872be7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23643948988ceca1fc33dad64ed8bdc6d0f4af2cd24c339aee80c4ca237d026f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontDistributionOriginCustomHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb94f958e1115ca0bd89cef9a70fb869936066232ed8502fe3255027709a934(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b223fb60f2e31179dc12e2c45e84d3bf3376ae303e3e6f80db7bd5496959504(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f97f7356f3837aff7a8a1a9fd0be95113751c6097eeffecae750221b29b4dec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0b8d6a8e14a6da72778406eb2eb57c4c651537492b6e71eb5385efc023c1b63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db30fdd5a9ce779de43c54c94de3a42902bd44a1fc404500557ba35352d5e31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa06c9a1770246c6d84b11c16b24235fc931a1b4e43b150b5216ced81261b35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d2d23d79d24dafcb4a4f48e205c87d07bb689cf039a6b0a14bfff830916a5b5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47c375d254d42678716df3663f1d9e3672c568ff8be461b4d4b5a928e14b93f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontDistributionOrigin]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b08301c46c3f7326d9d31c7c2acefa73ae2c0f1d1bb9ff3f4ff179e5112f136c(
    *,
    origin_access_identity: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560757dcb36ce5ee18f1b84729c343aafaac51600ef2d1b41813d7eeaf98b3b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afc044ffffda056894a5c5f23edf50fd5abf8b46932cf1dea248bb4263f10571(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae557d9645975a39b3fc86c715419505fb0af24317cfdd4eff0645bf0ca6203c(
    value: typing.Optional[CloudfrontDistributionOriginS3OriginConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b965be7b2d93b5916a133e4331b226aa1c91e9aff69953cb9970bef30e5935a7(
    *,
    vpc_origin_id: builtins.str,
    origin_keepalive_timeout: typing.Optional[jsii.Number] = None,
    origin_read_timeout: typing.Optional[jsii.Number] = None,
    owner_account_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2030be70c9c455bce264024ee4476a0160a389fce2b5761f8f7f392f9863d540(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e69c70aff874c157aafff4f83edd1f12e90d4d3bd323b7cb139da861161d6428(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c46ba831495d4d86cdcd977fb5ff8f84cbaf722e05b4b9cf8c0ca581243249f8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f225b622dce46f3d46f254b8f208cd103bbbcbecdb7b7837b9f4b2168fd4e5a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa7a61b6cf5bbb2d76b63ad04c719381cd15b96c373ab7c192dfde61536489f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c22503db29fcf978500948f79f6ce5ea9bff0f8aeecc9a32511edfd15d706b7(
    value: typing.Optional[CloudfrontDistributionOriginVpcOriginConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__803c0405770ab46aad53c8cf2e6c0942da1c468e141dded7a77eeda9e794fc68(
    *,
    geo_restriction: typing.Union[CloudfrontDistributionRestrictionsGeoRestriction, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad6e68fcf393c092cf15cc17a7b7974c5803475ed09ba18911dd622c8a9bc6f(
    *,
    restriction_type: builtins.str,
    locations: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db3f407a47f75f28ab2c048c4d3e6e55565a0bd5fc1f297d2ab8da1d5db16adb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358ed744b47e1eafe82dffd6b2c8bd1766c012f4fe5973f30e51c7429164eb61(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895e32b1b87c556af6c5d9e846ac8783f019a62b7f7de23511a1e68d571cb441(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba63f7320894f2bf8f1c8cebc65edcaf328d298fc7618b19073fe07117ffef18(
    value: typing.Optional[CloudfrontDistributionRestrictionsGeoRestriction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91cda328b272ac0a5c0021ce4c113ff242af24757fe42dad7d8d92ba49788637(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a45c36a07284c12a7a54d868f7ece9e1a58b513352e12b3d251e4298957fdc(
    value: typing.Optional[CloudfrontDistributionRestrictions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93fda38cbeb31a505987ee099e5c5eb690ecc9d59b8163732d9bd4de72edfba9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ffd572feb9c9328771a6685c304c677015388345a5a7e795236e6d11ca32b6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eed0bf40e432117b99e7ea8d473ebacd16998bb68ae73a142d86936409293282(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60711a1b600814105fd8c15abf719f5afb31044312e25f67da5b29cdcb5dcdbd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5a31d73d99357481210ba1ba1cc1154281235bf6c0568a02efc9e005ad0f7f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__664f3ebb7f5247b6b860e556e5bf32b794a63078df3aee4ac7ba97167b007b03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c9f3b5d96fd8eeb43bee8a7208a82224eb3fd6eb77b9fc1411c4395dc659d2(
    value: typing.Optional[CloudfrontDistributionTrustedKeyGroupsItems],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3cbcc2520a18c50da7e03c520e0e3241feb386e1c254a8cad7e2b794fa43992(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d05b99c7824feae666e4afc57d06c5dad2c9a89ce7366017b23f0d322033d5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4370f4a63f920502828211db51a5429cb9f0f3f26e6fa1423bd9de473fc20ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e4c0fcc5e26d3edaeb53e9a3f72e78408fc89b73179a68230ec4c20f3cc73f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b84a9027b4818756db32ca0b6298a6bd7f9c3b497a08cd24f6e5f594d86d1cd1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea1828fe2239c00d08e597f1e73539eccdb14db4644c73e5e9ca3fbc87c4def8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f13e6152232fbb409294a45a8688dd9a6ea5000f7d372e034dbcf2fb7c57e8d(
    value: typing.Optional[CloudfrontDistributionTrustedKeyGroups],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebc4b967cfea7f4fee04e66db64299495bbcc4adf7e8450117550bb0028d0215(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bebb2d048d43996dfae8224629149ee89d6d7eed1a4da108bf51f5c56549e0d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79a3f2946a75b1787aa9a7e9cf784d4fac57098149cf9458124026e0ac25d6e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0581b6793524bc52a157d83935f2303a61223f3913222bd603de4122b45244f6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dee1145d27319fc63c50dd272eac0acb785f77feca67dbe5fba50704e918b917(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92219547d5ae894c4bb2444656a44c5f75fc4c8d2d038ea0efec09fd6f9f81d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7031cbed5652f455373bfb661d26b56bd1bae33843058cdb715363e9819969(
    value: typing.Optional[CloudfrontDistributionTrustedSignersItems],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fdd1d0341217720ae5d2ccbf91392a7f4e1ac4b53fc56c6a75d4a0049b82ae2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a8b6ec37a5a917111f9658551d3f340f4ca7660654b1a267add8ef2adc9050d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc9e37df4ae5f231ccbab05650d7d172dd13f84bac6082801a39228784bb26f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7731adcb315f2a477cdb98fd2898997dd730c11c8a7d3e45b00cf855afcbf8da(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a28c7e14b3b791acd9b0e2b40ed13a0b6a9ef28e6a82ac53b5159849f853e49(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18bdf34d4597f3d77026f29bb8be6df2a1244de1f4844613e3e7a8e5472c56b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721ccbc269d3c6eb12aa0ec3ec911fd5fa53e6922a39f4a343631b57f4eaec01(
    value: typing.Optional[CloudfrontDistributionTrustedSigners],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9af1378dd1337388d6af2a165aaa594b90f5fcbbbc3d8ce1f6d98800743f9cd(
    *,
    acm_certificate_arn: typing.Optional[builtins.str] = None,
    cloudfront_default_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    iam_certificate_id: typing.Optional[builtins.str] = None,
    minimum_protocol_version: typing.Optional[builtins.str] = None,
    ssl_support_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ecdc4b477aeca464d11450c89c15bcf1d9ceea24da7fe858a72ab53b5675fca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36bee1a33dd504a2af8b6b29f9ed949f8e058bb02c1e6b54ef759d29edd0aa7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b526802d4386f85f7504e09da2c846ec5cfbcf955def33f4ec36b70abc396c2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca7fbda846bb08a2b9b7aa0b401152a6884951f6fd24f1321587ef4bfa9a457(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b998046a190e130640ea3018cc99b9aee039cffd4d86f8f04bac0a308f42b943(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__469ce6ae0743b6ae0b60b5801ce0b8a47e3bc650e950ba86aa331699bc4e08f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e502655f10a5874862bb22f02229e90eca3c0760669492c7baf3ff475896ed64(
    value: typing.Optional[CloudfrontDistributionViewerCertificate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc70452d524abca3193d85a556ea1932b00f6268dbf4e29074587ee3b3055d9a(
    *,
    mode: typing.Optional[builtins.str] = None,
    trust_store_config: typing.Optional[typing.Union[CloudfrontDistributionViewerMtlsConfigTrustStoreConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd9e85cc2916304dd04cdef209094463a66623671ee939d5bbcc549d4cd42ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f3b6c78bb800b35b59bc19dca3b8b12a958c2e854c03305017cc0fb26986e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59071d5302c1da301e45f49a084b389da5ff497ab2f8ec63c12bdd7b081f5a95(
    value: typing.Optional[CloudfrontDistributionViewerMtlsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25acc82073f65146fd36428a6d1ae2f69dc245ae1a535cf07b5cce42c77983df(
    *,
    trust_store_id: builtins.str,
    advertise_trust_store_ca_names: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ignore_certificate_expiry: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b53c9cf7eb10532c2a59b53f050474641b5f4624d695ad265c5561a774209cc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f411c93f9b9ce338b50c580c3bd21acdea862a2cfb5486e1d7f2e132060671b6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfbb6c94955aed28894a6b66758b892ad653889c54bfcbdd2dfb00887cad0d42(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7994be8498cf07f99a5dc73e476f1bfbe2a6f3f71036c8049dd4d4c6e478741d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14bf4ccc0e2ab4183a46fa6c3b9288931b510db68a75362b9302af5087b464a6(
    value: typing.Optional[CloudfrontDistributionViewerMtlsConfigTrustStoreConfig],
) -> None:
    """Type checking stubs"""
    pass
