r'''
# `aws_cloudfront_multitenant_distribution`

Refer to the Terraform Registry for docs: [`aws_cloudfront_multitenant_distribution`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution).
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


class CloudfrontMultitenantDistribution(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistribution",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution aws_cloudfront_multitenant_distribution}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        comment: builtins.str,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        active_trusted_key_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionActiveTrustedKeyGroups", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cache_behavior: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionCacheBehavior", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_error_response: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionCustomErrorResponse", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_cache_behavior: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionDefaultCacheBehavior", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_root_object: typing.Optional[builtins.str] = None,
        http_version: typing.Optional[builtins.str] = None,
        origin: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionOrigin", typing.Dict[builtins.str, typing.Any]]]]] = None,
        origin_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionOriginGroup", typing.Dict[builtins.str, typing.Any]]]]] = None,
        restrictions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionRestrictions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tenant_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionTenantConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["CloudfrontMultitenantDistributionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        viewer_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionViewerCertificate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        web_acl_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution aws_cloudfront_multitenant_distribution} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#comment CloudfrontMultitenantDistribution#comment}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#enabled CloudfrontMultitenantDistribution#enabled}.
        :param active_trusted_key_groups: active_trusted_key_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#active_trusted_key_groups CloudfrontMultitenantDistribution#active_trusted_key_groups}
        :param cache_behavior: cache_behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#cache_behavior CloudfrontMultitenantDistribution#cache_behavior}
        :param custom_error_response: custom_error_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#custom_error_response CloudfrontMultitenantDistribution#custom_error_response}
        :param default_cache_behavior: default_cache_behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#default_cache_behavior CloudfrontMultitenantDistribution#default_cache_behavior}
        :param default_root_object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#default_root_object CloudfrontMultitenantDistribution#default_root_object}.
        :param http_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#http_version CloudfrontMultitenantDistribution#http_version}.
        :param origin: origin block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin CloudfrontMultitenantDistribution#origin}
        :param origin_group: origin_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_group CloudfrontMultitenantDistribution#origin_group}
        :param restrictions: restrictions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#restrictions CloudfrontMultitenantDistribution#restrictions}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#tags CloudfrontMultitenantDistribution#tags}.
        :param tenant_config: tenant_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#tenant_config CloudfrontMultitenantDistribution#tenant_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#timeouts CloudfrontMultitenantDistribution#timeouts}
        :param viewer_certificate: viewer_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#viewer_certificate CloudfrontMultitenantDistribution#viewer_certificate}
        :param web_acl_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#web_acl_id CloudfrontMultitenantDistribution#web_acl_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e30f44d9a1c3ca9305d2f7bc4fe4f1fe821b016da6055961394bd8c976d4a874)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = CloudfrontMultitenantDistributionConfig(
            comment=comment,
            enabled=enabled,
            active_trusted_key_groups=active_trusted_key_groups,
            cache_behavior=cache_behavior,
            custom_error_response=custom_error_response,
            default_cache_behavior=default_cache_behavior,
            default_root_object=default_root_object,
            http_version=http_version,
            origin=origin,
            origin_group=origin_group,
            restrictions=restrictions,
            tags=tags,
            tenant_config=tenant_config,
            timeouts=timeouts,
            viewer_certificate=viewer_certificate,
            web_acl_id=web_acl_id,
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
        '''Generates CDKTF code for importing a CloudfrontMultitenantDistribution resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudfrontMultitenantDistribution to import.
        :param import_from_id: The id of the existing CloudfrontMultitenantDistribution that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudfrontMultitenantDistribution to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba7f52c2fa44ba35415e3002150235d92987d7e13d0f79348dfd707bb2c6009f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putActiveTrustedKeyGroups")
    def put_active_trusted_key_groups(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionActiveTrustedKeyGroups", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe7550b51fcdd3a11a85ec95dcff9d0da4e2094a33135aff9a64e46f836561e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putActiveTrustedKeyGroups", [value]))

    @jsii.member(jsii_name="putCacheBehavior")
    def put_cache_behavior(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionCacheBehavior", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b126bfb733d27affb0b6db427f12c5db1dfbeeadcab093e73c1334c6289850f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCacheBehavior", [value]))

    @jsii.member(jsii_name="putCustomErrorResponse")
    def put_custom_error_response(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionCustomErrorResponse", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__272a450852cc1a6ff58be9324f36e7832bb594f6bfea754c123f91a6dd9ba5d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomErrorResponse", [value]))

    @jsii.member(jsii_name="putDefaultCacheBehavior")
    def put_default_cache_behavior(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionDefaultCacheBehavior", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4dd8467e20f12a93555c493d35743d9a71fd8672ad09b7cbcb1b454d9be5e83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDefaultCacheBehavior", [value]))

    @jsii.member(jsii_name="putOrigin")
    def put_origin(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionOrigin", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bb062dcfd361d30b2dd3714d1792483db233cd8f3518997efade2e720b844de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOrigin", [value]))

    @jsii.member(jsii_name="putOriginGroup")
    def put_origin_group(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionOriginGroup", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e83039afda0b67a8bbae9767872be82c48dac5debbd0b515e21ac89079e6fd81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOriginGroup", [value]))

    @jsii.member(jsii_name="putRestrictions")
    def put_restrictions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionRestrictions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea68a4f694bd32e0f9ef27ebd0b19e98920d559da2098cbdde9b0c8e048bb563)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRestrictions", [value]))

    @jsii.member(jsii_name="putTenantConfig")
    def put_tenant_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionTenantConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3b7f3523b3be3ce452e701395e79c5919cee6acd783bef44e56e52c337f7ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTenantConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#create CloudfrontMultitenantDistribution#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#delete CloudfrontMultitenantDistribution#delete}
        :param update: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#update CloudfrontMultitenantDistribution#update}
        '''
        value = CloudfrontMultitenantDistributionTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putViewerCertificate")
    def put_viewer_certificate(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionViewerCertificate", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab9e068882796f390d094cdb36f4a7c79de2d5196076ba46b5494d7c80f04e7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putViewerCertificate", [value]))

    @jsii.member(jsii_name="resetActiveTrustedKeyGroups")
    def reset_active_trusted_key_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveTrustedKeyGroups", []))

    @jsii.member(jsii_name="resetCacheBehavior")
    def reset_cache_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheBehavior", []))

    @jsii.member(jsii_name="resetCustomErrorResponse")
    def reset_custom_error_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomErrorResponse", []))

    @jsii.member(jsii_name="resetDefaultCacheBehavior")
    def reset_default_cache_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultCacheBehavior", []))

    @jsii.member(jsii_name="resetDefaultRootObject")
    def reset_default_root_object(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultRootObject", []))

    @jsii.member(jsii_name="resetHttpVersion")
    def reset_http_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpVersion", []))

    @jsii.member(jsii_name="resetOrigin")
    def reset_origin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrigin", []))

    @jsii.member(jsii_name="resetOriginGroup")
    def reset_origin_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginGroup", []))

    @jsii.member(jsii_name="resetRestrictions")
    def reset_restrictions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictions", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTenantConfig")
    def reset_tenant_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantConfig", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetViewerCertificate")
    def reset_viewer_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetViewerCertificate", []))

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
    @jsii.member(jsii_name="activeTrustedKeyGroups")
    def active_trusted_key_groups(
        self,
    ) -> "CloudfrontMultitenantDistributionActiveTrustedKeyGroupsList":
        return typing.cast("CloudfrontMultitenantDistributionActiveTrustedKeyGroupsList", jsii.get(self, "activeTrustedKeyGroups"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="cacheBehavior")
    def cache_behavior(self) -> "CloudfrontMultitenantDistributionCacheBehaviorList":
        return typing.cast("CloudfrontMultitenantDistributionCacheBehaviorList", jsii.get(self, "cacheBehavior"))

    @builtins.property
    @jsii.member(jsii_name="callerReference")
    def caller_reference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "callerReference"))

    @builtins.property
    @jsii.member(jsii_name="connectionMode")
    def connection_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionMode"))

    @builtins.property
    @jsii.member(jsii_name="customErrorResponse")
    def custom_error_response(
        self,
    ) -> "CloudfrontMultitenantDistributionCustomErrorResponseList":
        return typing.cast("CloudfrontMultitenantDistributionCustomErrorResponseList", jsii.get(self, "customErrorResponse"))

    @builtins.property
    @jsii.member(jsii_name="defaultCacheBehavior")
    def default_cache_behavior(
        self,
    ) -> "CloudfrontMultitenantDistributionDefaultCacheBehaviorList":
        return typing.cast("CloudfrontMultitenantDistributionDefaultCacheBehaviorList", jsii.get(self, "defaultCacheBehavior"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="inProgressInvalidationBatches")
    def in_progress_invalidation_batches(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "inProgressInvalidationBatches"))

    @builtins.property
    @jsii.member(jsii_name="lastModifiedTime")
    def last_modified_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModifiedTime"))

    @builtins.property
    @jsii.member(jsii_name="origin")
    def origin(self) -> "CloudfrontMultitenantDistributionOriginList":
        return typing.cast("CloudfrontMultitenantDistributionOriginList", jsii.get(self, "origin"))

    @builtins.property
    @jsii.member(jsii_name="originGroup")
    def origin_group(self) -> "CloudfrontMultitenantDistributionOriginGroupList":
        return typing.cast("CloudfrontMultitenantDistributionOriginGroupList", jsii.get(self, "originGroup"))

    @builtins.property
    @jsii.member(jsii_name="restrictions")
    def restrictions(self) -> "CloudfrontMultitenantDistributionRestrictionsList":
        return typing.cast("CloudfrontMultitenantDistributionRestrictionsList", jsii.get(self, "restrictions"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tagsAll"))

    @builtins.property
    @jsii.member(jsii_name="tenantConfig")
    def tenant_config(self) -> "CloudfrontMultitenantDistributionTenantConfigList":
        return typing.cast("CloudfrontMultitenantDistributionTenantConfigList", jsii.get(self, "tenantConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CloudfrontMultitenantDistributionTimeoutsOutputReference":
        return typing.cast("CloudfrontMultitenantDistributionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="viewerCertificate")
    def viewer_certificate(
        self,
    ) -> "CloudfrontMultitenantDistributionViewerCertificateList":
        return typing.cast("CloudfrontMultitenantDistributionViewerCertificateList", jsii.get(self, "viewerCertificate"))

    @builtins.property
    @jsii.member(jsii_name="activeTrustedKeyGroupsInput")
    def active_trusted_key_groups_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionActiveTrustedKeyGroups"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionActiveTrustedKeyGroups"]]], jsii.get(self, "activeTrustedKeyGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheBehaviorInput")
    def cache_behavior_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionCacheBehavior"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionCacheBehavior"]]], jsii.get(self, "cacheBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="customErrorResponseInput")
    def custom_error_response_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionCustomErrorResponse"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionCustomErrorResponse"]]], jsii.get(self, "customErrorResponseInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultCacheBehaviorInput")
    def default_cache_behavior_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionDefaultCacheBehavior"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionDefaultCacheBehavior"]]], jsii.get(self, "defaultCacheBehaviorInput"))

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
    @jsii.member(jsii_name="originGroupInput")
    def origin_group_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOriginGroup"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOriginGroup"]]], jsii.get(self, "originGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="originInput")
    def origin_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOrigin"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOrigin"]]], jsii.get(self, "originInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictionsInput")
    def restrictions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionRestrictions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionRestrictions"]]], jsii.get(self, "restrictionsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantConfigInput")
    def tenant_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionTenantConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionTenantConfig"]]], jsii.get(self, "tenantConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudfrontMultitenantDistributionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudfrontMultitenantDistributionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="viewerCertificateInput")
    def viewer_certificate_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionViewerCertificate"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionViewerCertificate"]]], jsii.get(self, "viewerCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="webAclIdInput")
    def web_acl_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webAclIdInput"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da9135aa3383970b0da397e2efcba31d6649361cdb5c937376655f31eb0123f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultRootObject")
    def default_root_object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultRootObject"))

    @default_root_object.setter
    def default_root_object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b4140340551e069a87011378d0a13153c8a3f406568ac92c36237a916d0f95b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b051485483656642bd375157d6267161695053e1bd529031312d16e4e02c8509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpVersion")
    def http_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpVersion"))

    @http_version.setter
    def http_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddf8f590ab104ebb4e3d232401f5bd710d1a98640de714de8583d13808a0ea7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__994e046b35eebd71a9f10937a038d6a13ee1be5d83d77d25a5161292b68d5083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webAclId")
    def web_acl_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webAclId"))

    @web_acl_id.setter
    def web_acl_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c4ebf20ca8e14b8c61dfdab033eef16db624d361c4ff8bdc51ea2c5280c4b93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webAclId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionActiveTrustedKeyGroups",
    jsii_struct_bases=[],
    name_mapping={"items": "items"},
)
class CloudfrontMultitenantDistributionActiveTrustedKeyGroups:
    def __init__(
        self,
        *,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#items CloudfrontMultitenantDistribution#items}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__728c2b79de5f2f9b6829de921323891c77f01bbee0c69e13d900f6a0b2fdd695)
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if items is not None:
            self._values["items"] = items

    @builtins.property
    def items(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItems"]]]:
        '''items block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#items CloudfrontMultitenantDistribution#items}
        '''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItems"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionActiveTrustedKeyGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItems",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItems:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItems(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItemsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItemsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a91704f59fb5d638b938b40eef7d61004f63870700b809ec52d235453b1ec8d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItemsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4763e54509de7e03b4c8f80e163074d3a7771b8e16bbca19dc2caf77cd5010e5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItemsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60bcc7435db18426e41d60a224745a0529ba80ddb90128b0425d3230b5db3134)
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
            type_hints = typing.get_type_hints(_typecheckingstub__647f9e6747adb7de8a60a48ed2165b9c221a04c74904e9c4b4e1de09aa47caac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf5906f291ad8664ff4a2e73234f3a4df6c5add7ab0c4ed592908d3878191d54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItems]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItems]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cc2d2f540107e202cc7cc433cf8660ecc717f7719a93a1b15d55bf84021c9f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItemsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItemsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d45fc232ab743326415b923bf7d0dc5cd90a6355faa31113fcfdb138ed74452)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItems]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItems]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItems]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d5fc280cbb528e84935bd80e61a8cd92f91dc9dbc4035d1d959912570580ed2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionActiveTrustedKeyGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionActiveTrustedKeyGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffff850bab7634b5551d71877f8ccb2df95a0198e263368aa592cdc84f6ac582)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionActiveTrustedKeyGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cde858e18dabc21ab1bb74222650f4252eef141196c1add756e097fcdad4619)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionActiveTrustedKeyGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f15acf8eee261cc00bc15f7442548f2d8b0bf0f69dd6bc70376835a4291e4b8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f08a7c32114134e856dbc714540d41fc7ec54d9956c383f44dc018a520536a1d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d8486910568046eb0557f34c15a709315e5d48d504953e858a03fa04b220333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionActiveTrustedKeyGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionActiveTrustedKeyGroups]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionActiveTrustedKeyGroups]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363100cbea47cd501cdc676cc16f7f4a17e6e170d6341ed517ad4c2667e907e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionActiveTrustedKeyGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionActiveTrustedKeyGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4674536802181acea0804e92b660a177168a7d6c2d1260609db124266f98c09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putItems")
    def put_items(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItems, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3052f741c77080b375795909e226f03e38490939794cb1f483d69cf073d24fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putItems", [value]))

    @jsii.member(jsii_name="resetItems")
    def reset_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItems", []))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItemsList:
        return typing.cast(CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItemsList, jsii.get(self, "items"))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItems]]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionActiveTrustedKeyGroups]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionActiveTrustedKeyGroups]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionActiveTrustedKeyGroups]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54696b762951bfc50012fc3e6aed3d74403d8b967022bf355b683893275acdfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionCacheBehavior",
    jsii_struct_bases=[],
    name_mapping={
        "path_pattern": "pathPattern",
        "target_origin_id": "targetOriginId",
        "viewer_protocol_policy": "viewerProtocolPolicy",
        "allowed_methods": "allowedMethods",
        "cache_policy_id": "cachePolicyId",
        "compress": "compress",
        "field_level_encryption_id": "fieldLevelEncryptionId",
        "function_association": "functionAssociation",
        "lambda_function_association": "lambdaFunctionAssociation",
        "origin_request_policy_id": "originRequestPolicyId",
        "realtime_log_config_arn": "realtimeLogConfigArn",
        "response_headers_policy_id": "responseHeadersPolicyId",
        "trusted_key_groups": "trustedKeyGroups",
    },
)
class CloudfrontMultitenantDistributionCacheBehavior:
    def __init__(
        self,
        *,
        path_pattern: builtins.str,
        target_origin_id: builtins.str,
        viewer_protocol_policy: builtins.str,
        allowed_methods: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionCacheBehaviorAllowedMethods", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cache_policy_id: typing.Optional[builtins.str] = None,
        compress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        field_level_encryption_id: typing.Optional[builtins.str] = None,
        function_association: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lambda_function_association: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        origin_request_policy_id: typing.Optional[builtins.str] = None,
        realtime_log_config_arn: typing.Optional[builtins.str] = None,
        response_headers_policy_id: typing.Optional[builtins.str] = None,
        trusted_key_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroups", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param path_pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#path_pattern CloudfrontMultitenantDistribution#path_pattern}.
        :param target_origin_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#target_origin_id CloudfrontMultitenantDistribution#target_origin_id}.
        :param viewer_protocol_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#viewer_protocol_policy CloudfrontMultitenantDistribution#viewer_protocol_policy}.
        :param allowed_methods: allowed_methods block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#allowed_methods CloudfrontMultitenantDistribution#allowed_methods}
        :param cache_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#cache_policy_id CloudfrontMultitenantDistribution#cache_policy_id}.
        :param compress: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#compress CloudfrontMultitenantDistribution#compress}.
        :param field_level_encryption_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#field_level_encryption_id CloudfrontMultitenantDistribution#field_level_encryption_id}.
        :param function_association: function_association block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#function_association CloudfrontMultitenantDistribution#function_association}
        :param lambda_function_association: lambda_function_association block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#lambda_function_association CloudfrontMultitenantDistribution#lambda_function_association}
        :param origin_request_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_request_policy_id CloudfrontMultitenantDistribution#origin_request_policy_id}.
        :param realtime_log_config_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#realtime_log_config_arn CloudfrontMultitenantDistribution#realtime_log_config_arn}.
        :param response_headers_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#response_headers_policy_id CloudfrontMultitenantDistribution#response_headers_policy_id}.
        :param trusted_key_groups: trusted_key_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#trusted_key_groups CloudfrontMultitenantDistribution#trusted_key_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c3e119136eabbf910f606f77021b4100f2b3d8f3e3885db392c5bae810ae666)
            check_type(argname="argument path_pattern", value=path_pattern, expected_type=type_hints["path_pattern"])
            check_type(argname="argument target_origin_id", value=target_origin_id, expected_type=type_hints["target_origin_id"])
            check_type(argname="argument viewer_protocol_policy", value=viewer_protocol_policy, expected_type=type_hints["viewer_protocol_policy"])
            check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
            check_type(argname="argument cache_policy_id", value=cache_policy_id, expected_type=type_hints["cache_policy_id"])
            check_type(argname="argument compress", value=compress, expected_type=type_hints["compress"])
            check_type(argname="argument field_level_encryption_id", value=field_level_encryption_id, expected_type=type_hints["field_level_encryption_id"])
            check_type(argname="argument function_association", value=function_association, expected_type=type_hints["function_association"])
            check_type(argname="argument lambda_function_association", value=lambda_function_association, expected_type=type_hints["lambda_function_association"])
            check_type(argname="argument origin_request_policy_id", value=origin_request_policy_id, expected_type=type_hints["origin_request_policy_id"])
            check_type(argname="argument realtime_log_config_arn", value=realtime_log_config_arn, expected_type=type_hints["realtime_log_config_arn"])
            check_type(argname="argument response_headers_policy_id", value=response_headers_policy_id, expected_type=type_hints["response_headers_policy_id"])
            check_type(argname="argument trusted_key_groups", value=trusted_key_groups, expected_type=type_hints["trusted_key_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path_pattern": path_pattern,
            "target_origin_id": target_origin_id,
            "viewer_protocol_policy": viewer_protocol_policy,
        }
        if allowed_methods is not None:
            self._values["allowed_methods"] = allowed_methods
        if cache_policy_id is not None:
            self._values["cache_policy_id"] = cache_policy_id
        if compress is not None:
            self._values["compress"] = compress
        if field_level_encryption_id is not None:
            self._values["field_level_encryption_id"] = field_level_encryption_id
        if function_association is not None:
            self._values["function_association"] = function_association
        if lambda_function_association is not None:
            self._values["lambda_function_association"] = lambda_function_association
        if origin_request_policy_id is not None:
            self._values["origin_request_policy_id"] = origin_request_policy_id
        if realtime_log_config_arn is not None:
            self._values["realtime_log_config_arn"] = realtime_log_config_arn
        if response_headers_policy_id is not None:
            self._values["response_headers_policy_id"] = response_headers_policy_id
        if trusted_key_groups is not None:
            self._values["trusted_key_groups"] = trusted_key_groups

    @builtins.property
    def path_pattern(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#path_pattern CloudfrontMultitenantDistribution#path_pattern}.'''
        result = self._values.get("path_pattern")
        assert result is not None, "Required property 'path_pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_origin_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#target_origin_id CloudfrontMultitenantDistribution#target_origin_id}.'''
        result = self._values.get("target_origin_id")
        assert result is not None, "Required property 'target_origin_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def viewer_protocol_policy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#viewer_protocol_policy CloudfrontMultitenantDistribution#viewer_protocol_policy}.'''
        result = self._values.get("viewer_protocol_policy")
        assert result is not None, "Required property 'viewer_protocol_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_methods(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionCacheBehaviorAllowedMethods"]]]:
        '''allowed_methods block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#allowed_methods CloudfrontMultitenantDistribution#allowed_methods}
        '''
        result = self._values.get("allowed_methods")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionCacheBehaviorAllowedMethods"]]], result)

    @builtins.property
    def cache_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#cache_policy_id CloudfrontMultitenantDistribution#cache_policy_id}.'''
        result = self._values.get("cache_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compress(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#compress CloudfrontMultitenantDistribution#compress}.'''
        result = self._values.get("compress")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def field_level_encryption_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#field_level_encryption_id CloudfrontMultitenantDistribution#field_level_encryption_id}.'''
        result = self._values.get("field_level_encryption_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def function_association(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociation"]]]:
        '''function_association block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#function_association CloudfrontMultitenantDistribution#function_association}
        '''
        result = self._values.get("function_association")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociation"]]], result)

    @builtins.property
    def lambda_function_association(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociation"]]]:
        '''lambda_function_association block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#lambda_function_association CloudfrontMultitenantDistribution#lambda_function_association}
        '''
        result = self._values.get("lambda_function_association")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociation"]]], result)

    @builtins.property
    def origin_request_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_request_policy_id CloudfrontMultitenantDistribution#origin_request_policy_id}.'''
        result = self._values.get("origin_request_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def realtime_log_config_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#realtime_log_config_arn CloudfrontMultitenantDistribution#realtime_log_config_arn}.'''
        result = self._values.get("realtime_log_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_headers_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#response_headers_policy_id CloudfrontMultitenantDistribution#response_headers_policy_id}.'''
        result = self._values.get("response_headers_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trusted_key_groups(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroups"]]]:
        '''trusted_key_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#trusted_key_groups CloudfrontMultitenantDistribution#trusted_key_groups}
        '''
        result = self._values.get("trusted_key_groups")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroups"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionCacheBehavior(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionCacheBehaviorAllowedMethods",
    jsii_struct_bases=[],
    name_mapping={"cached_methods": "cachedMethods", "items": "items"},
)
class CloudfrontMultitenantDistributionCacheBehaviorAllowedMethods:
    def __init__(
        self,
        *,
        cached_methods: typing.Sequence[builtins.str],
        items: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param cached_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#cached_methods CloudfrontMultitenantDistribution#cached_methods}.
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#items CloudfrontMultitenantDistribution#items}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b0fe6072cd84719d9477a506bc20f3792ed4ae0bed3d4a8acef0d2d8c34cefb)
            check_type(argname="argument cached_methods", value=cached_methods, expected_type=type_hints["cached_methods"])
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cached_methods": cached_methods,
            "items": items,
        }

    @builtins.property
    def cached_methods(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#cached_methods CloudfrontMultitenantDistribution#cached_methods}.'''
        result = self._values.get("cached_methods")
        assert result is not None, "Required property 'cached_methods' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def items(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#items CloudfrontMultitenantDistribution#items}.'''
        result = self._values.get("items")
        assert result is not None, "Required property 'items' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionCacheBehaviorAllowedMethods(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionCacheBehaviorAllowedMethodsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionCacheBehaviorAllowedMethodsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__547bd74ce4036f6ce60250021a61cf04465e2d72e0f8d57b1644379b3c0057fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionCacheBehaviorAllowedMethodsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a28fcd77334f4c05bee8106679296f5bd8747a9a01c7cdc3799531b9251bb11)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionCacheBehaviorAllowedMethodsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77ff76c85a7bccb29acb00fc61bf33e05d98be8cf04d5eef854b3e12d802dda2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e44cc53d80a666daa54251eff41b7a42c8f42113af81365b57ce6280f671b108)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0dd1cc7f5390a3dbcd8114d5f59ede15151732345c9c5fc97289063831cf70dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorAllowedMethods]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorAllowedMethods]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorAllowedMethods]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4337114cff48a718b0a7856d799b21ae99d7f328d2e305600edfb99f30c41c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionCacheBehaviorAllowedMethodsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionCacheBehaviorAllowedMethodsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__950743de9ac27a94bdc3ae4410367f39d8e35a9a8a51cc37a6a862d2c4ee6b39)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="cachedMethodsInput")
    def cached_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cachedMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="cachedMethods")
    def cached_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cachedMethods"))

    @cached_methods.setter
    def cached_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2face7a433e055cf80a11f261d62be7c58a8cb91fc3262b652206856bceffe6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cachedMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "items"))

    @items.setter
    def items(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a9931041364ceab3fd211c02112818928fbd99a42787a52548ded26f57562ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "items", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCacheBehaviorAllowedMethods]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCacheBehaviorAllowedMethods]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCacheBehaviorAllowedMethods]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32826f4dca97aaeb07de08f25973c2982adfe95723a1c6df34bb82203d19eba1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociation",
    jsii_struct_bases=[],
    name_mapping={"event_type": "eventType", "function_arn": "functionArn"},
)
class CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociation:
    def __init__(self, *, event_type: builtins.str, function_arn: builtins.str) -> None:
        '''
        :param event_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#event_type CloudfrontMultitenantDistribution#event_type}.
        :param function_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#function_arn CloudfrontMultitenantDistribution#function_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aface80e582dde466ae9dbc74e7fc42be57e799af3ef5b38c68b6c1845f87097)
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_type": event_type,
            "function_arn": function_arn,
        }

    @builtins.property
    def event_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#event_type CloudfrontMultitenantDistribution#event_type}.'''
        result = self._values.get("event_type")
        assert result is not None, "Required property 'event_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def function_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#function_arn CloudfrontMultitenantDistribution#function_arn}.'''
        result = self._values.get("function_arn")
        assert result is not None, "Required property 'function_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2864d4238a74bdea9388c14a7238b9a6a936aa4b2a65ad8114ec531d2b281beb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3d17287056b8054bc9f7e97e93f0e9d80ed5a23377243846813591f896810d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f49cc596dadf0c6134f9446fce6a46b7acacc4c9c501f375aaf983e6c18c92d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75e16d9f6af7916e799c4884f82da4b41d87939fd6d0d6e140ed69e196933727)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39ac320b832efc604adfbd80369704c40a6e611ef9f6eb8f20bb88c31397f893)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociation]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociation]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e4a452104733a342a061ac08753cf94523a868e3074437d1de8f121ffb4d7f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__959b031aefb3e884403f3017ccf4c63afcc58a3e60ec1b5338a2e5a16522d107)
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
            type_hints = typing.get_type_hints(_typecheckingstub__952582ffad209518d41d40acdd414bb90ffa399f7a1b058d75c33e69ab2438b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionArn"))

    @function_arn.setter
    def function_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca8fe12b72e11a92f335b2d1a8dbaedeab82c93287d545b9847db7a47d99729c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociation]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociation]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociation]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25f8c0e3377a2607c4a889b3ee6ee4f97213f0987e2316e81812b9c97d51e491)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociation",
    jsii_struct_bases=[],
    name_mapping={
        "event_type": "eventType",
        "lambda_function_arn": "lambdaFunctionArn",
        "include_body": "includeBody",
    },
)
class CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociation:
    def __init__(
        self,
        *,
        event_type: builtins.str,
        lambda_function_arn: builtins.str,
        include_body: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param event_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#event_type CloudfrontMultitenantDistribution#event_type}.
        :param lambda_function_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#lambda_function_arn CloudfrontMultitenantDistribution#lambda_function_arn}.
        :param include_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#include_body CloudfrontMultitenantDistribution#include_body}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8da7c02fb8b1a53139bfef01ef010d384504814c88cb742db244c6f77fd4bee9)
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument lambda_function_arn", value=lambda_function_arn, expected_type=type_hints["lambda_function_arn"])
            check_type(argname="argument include_body", value=include_body, expected_type=type_hints["include_body"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_type": event_type,
            "lambda_function_arn": lambda_function_arn,
        }
        if include_body is not None:
            self._values["include_body"] = include_body

    @builtins.property
    def event_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#event_type CloudfrontMultitenantDistribution#event_type}.'''
        result = self._values.get("event_type")
        assert result is not None, "Required property 'event_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lambda_function_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#lambda_function_arn CloudfrontMultitenantDistribution#lambda_function_arn}.'''
        result = self._values.get("lambda_function_arn")
        assert result is not None, "Required property 'lambda_function_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include_body(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#include_body CloudfrontMultitenantDistribution#include_body}.'''
        result = self._values.get("include_body")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__236b01480ac7fb93e6fdf572cd2c20cf5d3b9c44a94c6c117ab44084ca6acc77)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__672d7faf18b277621568845b29e094e92337466051c902c1bec5b973aa10c4cd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__228512f25b7f4122afa2a0e290a94ffb2b9b35e0cd4acc3e94e42b00c725ff97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59bed4258dc09eb17b7b79341d19f2dc272e150a4d819d142eee74e8e3584b5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9613ac74f574da6a1b199b4fff6e546e51d345160ded85815eeca3905c95c7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociation]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociation]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d6b21b7e461a15e0bf5ebd1c9e25f15539b779ad944bab6b70fd6c70b4a1965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94e5764f4e41390d0820d2ebc67893a4d51903d9476f1adf7fd5691e5ec88e00)
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
    @jsii.member(jsii_name="lambdaFunctionArnInput")
    def lambda_function_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lambdaFunctionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="eventType")
    def event_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventType"))

    @event_type.setter
    def event_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f745b1f762afc3331898ea12ff2000e9f3e36f6343d82dd4fb4c6e9e2a4e9fc2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2844f81b463fc264ae789e0647127fc85dfc9716c8a87c2f52736a85774d071c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionArn")
    def lambda_function_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lambdaFunctionArn"))

    @lambda_function_arn.setter
    def lambda_function_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f842037517afaf3a35d345b95632a50b43269e34c0622c208d69add1c6370eb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaFunctionArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociation]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociation]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociation]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daa88dd39ac1878a6ab915a07503eff8eb3be81e4240cec1ee652499a215c808)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionCacheBehaviorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionCacheBehaviorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__386476adae5132ce001294508312708af524ecfbceb81f83ca97d7750d9d3085)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionCacheBehaviorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6846cac31d025b3576bfaa159a5cd8e26a9674084688dacd5f6b788453c109b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionCacheBehaviorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__940a48eba6e90a4cb8ae81f0f31e13585194c24ee4a87198fe8debeb94ab6e56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c5d8ec311dcb2ec2be2e1736ceb1f8aaa315a58f9673fc479e06e8a37d13bf9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b904b6a45ff5f25e51c1e4d154c2f4132f91ffe31de3002376d006d684af67d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehavior]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehavior]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehavior]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f04641138b2e2bb07cca8dc63cad1d0f1e241b010f47ff63ce84fd442a4e7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionCacheBehaviorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionCacheBehaviorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f37a83464f32add2fca550cd47a6f0c8c1233811b46f80bb8c3c684efb72ad5d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAllowedMethods")
    def put_allowed_methods(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionCacheBehaviorAllowedMethods, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3596606a0c2aa17d7c4deb2efb17e76299035408ae11de1755ae8607730b83e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowedMethods", [value]))

    @jsii.member(jsii_name="putFunctionAssociation")
    def put_function_association(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc6c085f2b94e4211e9307fbc51cd71fc22b99c1f5e63715e3dc915501bf8f75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFunctionAssociation", [value]))

    @jsii.member(jsii_name="putLambdaFunctionAssociation")
    def put_lambda_function_association(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d41df34232135ecb98cb1201743797673c739fc574642ee828423e25644d58e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLambdaFunctionAssociation", [value]))

    @jsii.member(jsii_name="putTrustedKeyGroups")
    def put_trusted_key_groups(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroups", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f46c7bbfcba8ccfceee964593051c4aed7957f96c3d201c6720e2c410b7b76fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTrustedKeyGroups", [value]))

    @jsii.member(jsii_name="resetAllowedMethods")
    def reset_allowed_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedMethods", []))

    @jsii.member(jsii_name="resetCachePolicyId")
    def reset_cache_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCachePolicyId", []))

    @jsii.member(jsii_name="resetCompress")
    def reset_compress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompress", []))

    @jsii.member(jsii_name="resetFieldLevelEncryptionId")
    def reset_field_level_encryption_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldLevelEncryptionId", []))

    @jsii.member(jsii_name="resetFunctionAssociation")
    def reset_function_association(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunctionAssociation", []))

    @jsii.member(jsii_name="resetLambdaFunctionAssociation")
    def reset_lambda_function_association(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaFunctionAssociation", []))

    @jsii.member(jsii_name="resetOriginRequestPolicyId")
    def reset_origin_request_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginRequestPolicyId", []))

    @jsii.member(jsii_name="resetRealtimeLogConfigArn")
    def reset_realtime_log_config_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRealtimeLogConfigArn", []))

    @jsii.member(jsii_name="resetResponseHeadersPolicyId")
    def reset_response_headers_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseHeadersPolicyId", []))

    @jsii.member(jsii_name="resetTrustedKeyGroups")
    def reset_trusted_key_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedKeyGroups", []))

    @builtins.property
    @jsii.member(jsii_name="allowedMethods")
    def allowed_methods(
        self,
    ) -> CloudfrontMultitenantDistributionCacheBehaviorAllowedMethodsList:
        return typing.cast(CloudfrontMultitenantDistributionCacheBehaviorAllowedMethodsList, jsii.get(self, "allowedMethods"))

    @builtins.property
    @jsii.member(jsii_name="functionAssociation")
    def function_association(
        self,
    ) -> CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociationList:
        return typing.cast(CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociationList, jsii.get(self, "functionAssociation"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionAssociation")
    def lambda_function_association(
        self,
    ) -> CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociationList:
        return typing.cast(CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociationList, jsii.get(self, "lambdaFunctionAssociation"))

    @builtins.property
    @jsii.member(jsii_name="trustedKeyGroups")
    def trusted_key_groups(
        self,
    ) -> "CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroupsList":
        return typing.cast("CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroupsList", jsii.get(self, "trustedKeyGroups"))

    @builtins.property
    @jsii.member(jsii_name="allowedMethodsInput")
    def allowed_methods_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorAllowedMethods]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorAllowedMethods]]], jsii.get(self, "allowedMethodsInput"))

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
    @jsii.member(jsii_name="fieldLevelEncryptionIdInput")
    def field_level_encryption_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldLevelEncryptionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="functionAssociationInput")
    def function_association_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociation]]], jsii.get(self, "functionAssociationInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionAssociationInput")
    def lambda_function_association_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociation]]], jsii.get(self, "lambdaFunctionAssociationInput"))

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
    @jsii.member(jsii_name="targetOriginIdInput")
    def target_origin_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetOriginIdInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedKeyGroupsInput")
    def trusted_key_groups_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroups"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroups"]]], jsii.get(self, "trustedKeyGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="viewerProtocolPolicyInput")
    def viewer_protocol_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "viewerProtocolPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="cachePolicyId")
    def cache_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cachePolicyId"))

    @cache_policy_id.setter
    def cache_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23cd0861886563d9ade5de9159aa8b5e2a833ee4d343ad75e99e4350e189c2a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__796063907baa8e8da058ea441c9c814883417b78a4ce51a52d90f4fc9c59dc07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fieldLevelEncryptionId")
    def field_level_encryption_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldLevelEncryptionId"))

    @field_level_encryption_id.setter
    def field_level_encryption_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d310000e673b115fdf57fb2053d6345f19b0872e01c9739020751105c4cff932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldLevelEncryptionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originRequestPolicyId")
    def origin_request_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originRequestPolicyId"))

    @origin_request_policy_id.setter
    def origin_request_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f820bf2c33693fffbecce800c483a62c9812fb628103d3a009dde5a719a4a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originRequestPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathPattern")
    def path_pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathPattern"))

    @path_pattern.setter
    def path_pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41aa9230ad31eb03c210c28f5ab02311bbb5085bc08520f5a42a53afee20c89f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathPattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="realtimeLogConfigArn")
    def realtime_log_config_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "realtimeLogConfigArn"))

    @realtime_log_config_arn.setter
    def realtime_log_config_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__055b5bb9a46ae8a21cd76c14921207ba48219997a24e750aa2851d055cc74118)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "realtimeLogConfigArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseHeadersPolicyId")
    def response_headers_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseHeadersPolicyId"))

    @response_headers_policy_id.setter
    def response_headers_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__228b84319e0bc0daaf6021c4af52f5c99c2e2223d41e55a190700f90f2935dd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseHeadersPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetOriginId")
    def target_origin_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetOriginId"))

    @target_origin_id.setter
    def target_origin_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5482ab88102f2161093aca936fa6f13baecaf6798e1959e8922ca6e4a684dab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetOriginId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="viewerProtocolPolicy")
    def viewer_protocol_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "viewerProtocolPolicy"))

    @viewer_protocol_policy.setter
    def viewer_protocol_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7471ed99ad0c0d79adae566c2b10ddc993f4e55f75a995253485b3740554ec5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "viewerProtocolPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCacheBehavior]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCacheBehavior]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCacheBehavior]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda1e63e5230e0377e2de0c0c437cd5ea391801cb5fc82da1187f96b20d30db9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroups",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "items": "items"},
)
class CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroups:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        items: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#enabled CloudfrontMultitenantDistribution#enabled}.
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#items CloudfrontMultitenantDistribution#items}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f0bbe2830fd5bd374e3c169b9fe7e5a66a3d1bf184735f2e04dfa32b7249ca2)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if items is not None:
            self._values["items"] = items

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#enabled CloudfrontMultitenantDistribution#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def items(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#items CloudfrontMultitenantDistribution#items}.'''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6fc21f94e4b58228b5af80752baf724496cb8c6aa2b1444d2d601e7401a4809)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86efd4ab4abd40662db0397edf4d8e64bda4a8328fa79183ea12ece71ee0915d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7ffc5b0b64b01b3822fd19aced15914e68beba6c6b8bbbff6a8eef1689f354a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c96b91546d5ecc2c44207083f334207be5a904a59ec710a6e779defa1c131c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87e07eb5a808c14c3d4baf440c30be08f0b2da11d898f680d9ae671ff95c5d7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroups]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroups]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c277b83e291c678cbf0144486643b70eed55782c51c65d88a9b2973f689bf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55364e5120691b19cb8dd855fc6031a7cced771cd1dee63e992512375cce35a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetItems")
    def reset_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItems", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "itemsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b036c2f5d85ff75f52c9a426a60ca35a42647f4cf64e15569a27233fb506c54e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "items"))

    @items.setter
    def items(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c5100058fe41287cf483656ee59ef79386921cf38bd9a6caf0a3291cea8ed20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "items", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroups]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroups]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroups]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73038b9f71143777589ea4a06a551cbd5d5acbfcd6acc4a37a6cab0fd036ebc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "comment": "comment",
        "enabled": "enabled",
        "active_trusted_key_groups": "activeTrustedKeyGroups",
        "cache_behavior": "cacheBehavior",
        "custom_error_response": "customErrorResponse",
        "default_cache_behavior": "defaultCacheBehavior",
        "default_root_object": "defaultRootObject",
        "http_version": "httpVersion",
        "origin": "origin",
        "origin_group": "originGroup",
        "restrictions": "restrictions",
        "tags": "tags",
        "tenant_config": "tenantConfig",
        "timeouts": "timeouts",
        "viewer_certificate": "viewerCertificate",
        "web_acl_id": "webAclId",
    },
)
class CloudfrontMultitenantDistributionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        comment: builtins.str,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        active_trusted_key_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionActiveTrustedKeyGroups, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cache_behavior: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionCacheBehavior, typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_error_response: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionCustomErrorResponse", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_cache_behavior: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionDefaultCacheBehavior", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_root_object: typing.Optional[builtins.str] = None,
        http_version: typing.Optional[builtins.str] = None,
        origin: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionOrigin", typing.Dict[builtins.str, typing.Any]]]]] = None,
        origin_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionOriginGroup", typing.Dict[builtins.str, typing.Any]]]]] = None,
        restrictions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionRestrictions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tenant_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionTenantConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["CloudfrontMultitenantDistributionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        viewer_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionViewerCertificate", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#comment CloudfrontMultitenantDistribution#comment}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#enabled CloudfrontMultitenantDistribution#enabled}.
        :param active_trusted_key_groups: active_trusted_key_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#active_trusted_key_groups CloudfrontMultitenantDistribution#active_trusted_key_groups}
        :param cache_behavior: cache_behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#cache_behavior CloudfrontMultitenantDistribution#cache_behavior}
        :param custom_error_response: custom_error_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#custom_error_response CloudfrontMultitenantDistribution#custom_error_response}
        :param default_cache_behavior: default_cache_behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#default_cache_behavior CloudfrontMultitenantDistribution#default_cache_behavior}
        :param default_root_object: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#default_root_object CloudfrontMultitenantDistribution#default_root_object}.
        :param http_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#http_version CloudfrontMultitenantDistribution#http_version}.
        :param origin: origin block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin CloudfrontMultitenantDistribution#origin}
        :param origin_group: origin_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_group CloudfrontMultitenantDistribution#origin_group}
        :param restrictions: restrictions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#restrictions CloudfrontMultitenantDistribution#restrictions}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#tags CloudfrontMultitenantDistribution#tags}.
        :param tenant_config: tenant_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#tenant_config CloudfrontMultitenantDistribution#tenant_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#timeouts CloudfrontMultitenantDistribution#timeouts}
        :param viewer_certificate: viewer_certificate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#viewer_certificate CloudfrontMultitenantDistribution#viewer_certificate}
        :param web_acl_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#web_acl_id CloudfrontMultitenantDistribution#web_acl_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = CloudfrontMultitenantDistributionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e1d893e03ab4358dc164b3862a31da88907930025a83954fcc1f6eef14b9ca1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument active_trusted_key_groups", value=active_trusted_key_groups, expected_type=type_hints["active_trusted_key_groups"])
            check_type(argname="argument cache_behavior", value=cache_behavior, expected_type=type_hints["cache_behavior"])
            check_type(argname="argument custom_error_response", value=custom_error_response, expected_type=type_hints["custom_error_response"])
            check_type(argname="argument default_cache_behavior", value=default_cache_behavior, expected_type=type_hints["default_cache_behavior"])
            check_type(argname="argument default_root_object", value=default_root_object, expected_type=type_hints["default_root_object"])
            check_type(argname="argument http_version", value=http_version, expected_type=type_hints["http_version"])
            check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
            check_type(argname="argument origin_group", value=origin_group, expected_type=type_hints["origin_group"])
            check_type(argname="argument restrictions", value=restrictions, expected_type=type_hints["restrictions"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tenant_config", value=tenant_config, expected_type=type_hints["tenant_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument viewer_certificate", value=viewer_certificate, expected_type=type_hints["viewer_certificate"])
            check_type(argname="argument web_acl_id", value=web_acl_id, expected_type=type_hints["web_acl_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "comment": comment,
            "enabled": enabled,
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
        if active_trusted_key_groups is not None:
            self._values["active_trusted_key_groups"] = active_trusted_key_groups
        if cache_behavior is not None:
            self._values["cache_behavior"] = cache_behavior
        if custom_error_response is not None:
            self._values["custom_error_response"] = custom_error_response
        if default_cache_behavior is not None:
            self._values["default_cache_behavior"] = default_cache_behavior
        if default_root_object is not None:
            self._values["default_root_object"] = default_root_object
        if http_version is not None:
            self._values["http_version"] = http_version
        if origin is not None:
            self._values["origin"] = origin
        if origin_group is not None:
            self._values["origin_group"] = origin_group
        if restrictions is not None:
            self._values["restrictions"] = restrictions
        if tags is not None:
            self._values["tags"] = tags
        if tenant_config is not None:
            self._values["tenant_config"] = tenant_config
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if viewer_certificate is not None:
            self._values["viewer_certificate"] = viewer_certificate
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
    def comment(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#comment CloudfrontMultitenantDistribution#comment}.'''
        result = self._values.get("comment")
        assert result is not None, "Required property 'comment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#enabled CloudfrontMultitenantDistribution#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def active_trusted_key_groups(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionActiveTrustedKeyGroups]]]:
        '''active_trusted_key_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#active_trusted_key_groups CloudfrontMultitenantDistribution#active_trusted_key_groups}
        '''
        result = self._values.get("active_trusted_key_groups")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionActiveTrustedKeyGroups]]], result)

    @builtins.property
    def cache_behavior(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehavior]]]:
        '''cache_behavior block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#cache_behavior CloudfrontMultitenantDistribution#cache_behavior}
        '''
        result = self._values.get("cache_behavior")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehavior]]], result)

    @builtins.property
    def custom_error_response(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionCustomErrorResponse"]]]:
        '''custom_error_response block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#custom_error_response CloudfrontMultitenantDistribution#custom_error_response}
        '''
        result = self._values.get("custom_error_response")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionCustomErrorResponse"]]], result)

    @builtins.property
    def default_cache_behavior(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionDefaultCacheBehavior"]]]:
        '''default_cache_behavior block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#default_cache_behavior CloudfrontMultitenantDistribution#default_cache_behavior}
        '''
        result = self._values.get("default_cache_behavior")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionDefaultCacheBehavior"]]], result)

    @builtins.property
    def default_root_object(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#default_root_object CloudfrontMultitenantDistribution#default_root_object}.'''
        result = self._values.get("default_root_object")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#http_version CloudfrontMultitenantDistribution#http_version}.'''
        result = self._values.get("http_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origin(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOrigin"]]]:
        '''origin block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin CloudfrontMultitenantDistribution#origin}
        '''
        result = self._values.get("origin")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOrigin"]]], result)

    @builtins.property
    def origin_group(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOriginGroup"]]]:
        '''origin_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_group CloudfrontMultitenantDistribution#origin_group}
        '''
        result = self._values.get("origin_group")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOriginGroup"]]], result)

    @builtins.property
    def restrictions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionRestrictions"]]]:
        '''restrictions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#restrictions CloudfrontMultitenantDistribution#restrictions}
        '''
        result = self._values.get("restrictions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionRestrictions"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#tags CloudfrontMultitenantDistribution#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tenant_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionTenantConfig"]]]:
        '''tenant_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#tenant_config CloudfrontMultitenantDistribution#tenant_config}
        '''
        result = self._values.get("tenant_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionTenantConfig"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CloudfrontMultitenantDistributionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#timeouts CloudfrontMultitenantDistribution#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CloudfrontMultitenantDistributionTimeouts"], result)

    @builtins.property
    def viewer_certificate(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionViewerCertificate"]]]:
        '''viewer_certificate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#viewer_certificate CloudfrontMultitenantDistribution#viewer_certificate}
        '''
        result = self._values.get("viewer_certificate")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionViewerCertificate"]]], result)

    @builtins.property
    def web_acl_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#web_acl_id CloudfrontMultitenantDistribution#web_acl_id}.'''
        result = self._values.get("web_acl_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionCustomErrorResponse",
    jsii_struct_bases=[],
    name_mapping={
        "error_code": "errorCode",
        "error_caching_min_ttl": "errorCachingMinTtl",
        "response_code": "responseCode",
        "response_page_path": "responsePagePath",
    },
)
class CloudfrontMultitenantDistributionCustomErrorResponse:
    def __init__(
        self,
        *,
        error_code: jsii.Number,
        error_caching_min_ttl: typing.Optional[jsii.Number] = None,
        response_code: typing.Optional[builtins.str] = None,
        response_page_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param error_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#error_code CloudfrontMultitenantDistribution#error_code}.
        :param error_caching_min_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#error_caching_min_ttl CloudfrontMultitenantDistribution#error_caching_min_ttl}.
        :param response_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#response_code CloudfrontMultitenantDistribution#response_code}.
        :param response_page_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#response_page_path CloudfrontMultitenantDistribution#response_page_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed058b937bfc8904d89cbea7b96145544a62170d6f81b64f49d08d9d93611dc6)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#error_code CloudfrontMultitenantDistribution#error_code}.'''
        result = self._values.get("error_code")
        assert result is not None, "Required property 'error_code' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def error_caching_min_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#error_caching_min_ttl CloudfrontMultitenantDistribution#error_caching_min_ttl}.'''
        result = self._values.get("error_caching_min_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def response_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#response_code CloudfrontMultitenantDistribution#response_code}.'''
        result = self._values.get("response_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_page_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#response_page_path CloudfrontMultitenantDistribution#response_page_path}.'''
        result = self._values.get("response_page_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionCustomErrorResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionCustomErrorResponseList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionCustomErrorResponseList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af480b1f274d8187b5b311e5a92c9df972bd37f7a5060ea9f458972aa3a0ff08)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionCustomErrorResponseOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b140747faf0c03e52612a6d467531fd087f6e597212795dc788300eb6d4790c0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionCustomErrorResponseOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88d8b5de344d2780b71f94bb7b9c243be4d236bd53e46dc9dc378b1d4885a46f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a212b6fba81a118d52703cc7f33bd9ba6e97038df1257482bf25c81892322a49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__399e5a141d5d381ca86baa1b941fb2c3b0545dba2704b08601a83e129a354313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCustomErrorResponse]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCustomErrorResponse]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCustomErrorResponse]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a518790f4cc689959628b04ca0f27db5f3d77b83ac64ede8496f5163d9706fe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionCustomErrorResponseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionCustomErrorResponseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71bd16d398ca50893a1a028d1287283e3e648fbc9d12015d8e4d2896d1092f21)
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
    def response_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseCodeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__cebb4c070181b8516e3a9cca50974b051afd8e9aafe652378e4050663f56a2be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorCachingMinTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="errorCode")
    def error_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "errorCode"))

    @error_code.setter
    def error_code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83859c764f643f373218cdb21482e36f1574c5669424c8f12c09eb0884764ec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseCode")
    def response_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseCode"))

    @response_code.setter
    def response_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa7df1b4ff69aaca26bf64b12a3f86bc30e8d723c7d375af80d657a176b4225)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responsePagePath")
    def response_page_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responsePagePath"))

    @response_page_path.setter
    def response_page_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cef942bb7d241bc2be1cf7fefbc0c7d524f225b20704b91ce07ff12d81de445a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responsePagePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCustomErrorResponse]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCustomErrorResponse]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCustomErrorResponse]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b921df196d33005ceaf8eedc9a1c2910aa882725e17ada0efe4ee92be629ff4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionDefaultCacheBehavior",
    jsii_struct_bases=[],
    name_mapping={
        "target_origin_id": "targetOriginId",
        "viewer_protocol_policy": "viewerProtocolPolicy",
        "allowed_methods": "allowedMethods",
        "cache_policy_id": "cachePolicyId",
        "compress": "compress",
        "field_level_encryption_id": "fieldLevelEncryptionId",
        "function_association": "functionAssociation",
        "lambda_function_association": "lambdaFunctionAssociation",
        "origin_request_policy_id": "originRequestPolicyId",
        "realtime_log_config_arn": "realtimeLogConfigArn",
        "response_headers_policy_id": "responseHeadersPolicyId",
        "trusted_key_groups": "trustedKeyGroups",
    },
)
class CloudfrontMultitenantDistributionDefaultCacheBehavior:
    def __init__(
        self,
        *,
        target_origin_id: builtins.str,
        viewer_protocol_policy: builtins.str,
        allowed_methods: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethods", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cache_policy_id: typing.Optional[builtins.str] = None,
        compress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        field_level_encryption_id: typing.Optional[builtins.str] = None,
        function_association: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lambda_function_association: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociation", typing.Dict[builtins.str, typing.Any]]]]] = None,
        origin_request_policy_id: typing.Optional[builtins.str] = None,
        realtime_log_config_arn: typing.Optional[builtins.str] = None,
        response_headers_policy_id: typing.Optional[builtins.str] = None,
        trusted_key_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroups", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param target_origin_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#target_origin_id CloudfrontMultitenantDistribution#target_origin_id}.
        :param viewer_protocol_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#viewer_protocol_policy CloudfrontMultitenantDistribution#viewer_protocol_policy}.
        :param allowed_methods: allowed_methods block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#allowed_methods CloudfrontMultitenantDistribution#allowed_methods}
        :param cache_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#cache_policy_id CloudfrontMultitenantDistribution#cache_policy_id}.
        :param compress: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#compress CloudfrontMultitenantDistribution#compress}.
        :param field_level_encryption_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#field_level_encryption_id CloudfrontMultitenantDistribution#field_level_encryption_id}.
        :param function_association: function_association block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#function_association CloudfrontMultitenantDistribution#function_association}
        :param lambda_function_association: lambda_function_association block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#lambda_function_association CloudfrontMultitenantDistribution#lambda_function_association}
        :param origin_request_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_request_policy_id CloudfrontMultitenantDistribution#origin_request_policy_id}.
        :param realtime_log_config_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#realtime_log_config_arn CloudfrontMultitenantDistribution#realtime_log_config_arn}.
        :param response_headers_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#response_headers_policy_id CloudfrontMultitenantDistribution#response_headers_policy_id}.
        :param trusted_key_groups: trusted_key_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#trusted_key_groups CloudfrontMultitenantDistribution#trusted_key_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba80b017f01fe7862ca29009c7f9ae179ccdc59de36a6c4a5e8b79ed1dcc21b0)
            check_type(argname="argument target_origin_id", value=target_origin_id, expected_type=type_hints["target_origin_id"])
            check_type(argname="argument viewer_protocol_policy", value=viewer_protocol_policy, expected_type=type_hints["viewer_protocol_policy"])
            check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
            check_type(argname="argument cache_policy_id", value=cache_policy_id, expected_type=type_hints["cache_policy_id"])
            check_type(argname="argument compress", value=compress, expected_type=type_hints["compress"])
            check_type(argname="argument field_level_encryption_id", value=field_level_encryption_id, expected_type=type_hints["field_level_encryption_id"])
            check_type(argname="argument function_association", value=function_association, expected_type=type_hints["function_association"])
            check_type(argname="argument lambda_function_association", value=lambda_function_association, expected_type=type_hints["lambda_function_association"])
            check_type(argname="argument origin_request_policy_id", value=origin_request_policy_id, expected_type=type_hints["origin_request_policy_id"])
            check_type(argname="argument realtime_log_config_arn", value=realtime_log_config_arn, expected_type=type_hints["realtime_log_config_arn"])
            check_type(argname="argument response_headers_policy_id", value=response_headers_policy_id, expected_type=type_hints["response_headers_policy_id"])
            check_type(argname="argument trusted_key_groups", value=trusted_key_groups, expected_type=type_hints["trusted_key_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_origin_id": target_origin_id,
            "viewer_protocol_policy": viewer_protocol_policy,
        }
        if allowed_methods is not None:
            self._values["allowed_methods"] = allowed_methods
        if cache_policy_id is not None:
            self._values["cache_policy_id"] = cache_policy_id
        if compress is not None:
            self._values["compress"] = compress
        if field_level_encryption_id is not None:
            self._values["field_level_encryption_id"] = field_level_encryption_id
        if function_association is not None:
            self._values["function_association"] = function_association
        if lambda_function_association is not None:
            self._values["lambda_function_association"] = lambda_function_association
        if origin_request_policy_id is not None:
            self._values["origin_request_policy_id"] = origin_request_policy_id
        if realtime_log_config_arn is not None:
            self._values["realtime_log_config_arn"] = realtime_log_config_arn
        if response_headers_policy_id is not None:
            self._values["response_headers_policy_id"] = response_headers_policy_id
        if trusted_key_groups is not None:
            self._values["trusted_key_groups"] = trusted_key_groups

    @builtins.property
    def target_origin_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#target_origin_id CloudfrontMultitenantDistribution#target_origin_id}.'''
        result = self._values.get("target_origin_id")
        assert result is not None, "Required property 'target_origin_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def viewer_protocol_policy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#viewer_protocol_policy CloudfrontMultitenantDistribution#viewer_protocol_policy}.'''
        result = self._values.get("viewer_protocol_policy")
        assert result is not None, "Required property 'viewer_protocol_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_methods(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethods"]]]:
        '''allowed_methods block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#allowed_methods CloudfrontMultitenantDistribution#allowed_methods}
        '''
        result = self._values.get("allowed_methods")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethods"]]], result)

    @builtins.property
    def cache_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#cache_policy_id CloudfrontMultitenantDistribution#cache_policy_id}.'''
        result = self._values.get("cache_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compress(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#compress CloudfrontMultitenantDistribution#compress}.'''
        result = self._values.get("compress")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def field_level_encryption_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#field_level_encryption_id CloudfrontMultitenantDistribution#field_level_encryption_id}.'''
        result = self._values.get("field_level_encryption_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def function_association(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociation"]]]:
        '''function_association block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#function_association CloudfrontMultitenantDistribution#function_association}
        '''
        result = self._values.get("function_association")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociation"]]], result)

    @builtins.property
    def lambda_function_association(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociation"]]]:
        '''lambda_function_association block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#lambda_function_association CloudfrontMultitenantDistribution#lambda_function_association}
        '''
        result = self._values.get("lambda_function_association")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociation"]]], result)

    @builtins.property
    def origin_request_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_request_policy_id CloudfrontMultitenantDistribution#origin_request_policy_id}.'''
        result = self._values.get("origin_request_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def realtime_log_config_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#realtime_log_config_arn CloudfrontMultitenantDistribution#realtime_log_config_arn}.'''
        result = self._values.get("realtime_log_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_headers_policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#response_headers_policy_id CloudfrontMultitenantDistribution#response_headers_policy_id}.'''
        result = self._values.get("response_headers_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trusted_key_groups(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroups"]]]:
        '''trusted_key_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#trusted_key_groups CloudfrontMultitenantDistribution#trusted_key_groups}
        '''
        result = self._values.get("trusted_key_groups")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroups"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionDefaultCacheBehavior(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethods",
    jsii_struct_bases=[],
    name_mapping={"cached_methods": "cachedMethods", "items": "items"},
)
class CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethods:
    def __init__(
        self,
        *,
        cached_methods: typing.Sequence[builtins.str],
        items: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param cached_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#cached_methods CloudfrontMultitenantDistribution#cached_methods}.
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#items CloudfrontMultitenantDistribution#items}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4262c433b52f5306c4c44a1b94067d971c17cb70763f0c09ecc1fdcf1512e038)
            check_type(argname="argument cached_methods", value=cached_methods, expected_type=type_hints["cached_methods"])
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cached_methods": cached_methods,
            "items": items,
        }

    @builtins.property
    def cached_methods(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#cached_methods CloudfrontMultitenantDistribution#cached_methods}.'''
        result = self._values.get("cached_methods")
        assert result is not None, "Required property 'cached_methods' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def items(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#items CloudfrontMultitenantDistribution#items}.'''
        result = self._values.get("items")
        assert result is not None, "Required property 'items' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethods(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethodsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethodsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6908e3b368431a36e3e13f3eef7dae7f8ccaf5880bc3c16d901f73c03234d9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethodsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b669e30d15c2475cc873ae661903220ced5c273929911d4b40df347f0572e6a7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethodsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__658882202ac20dff6be7b31c00710b88b366cdf073073b502a30df511105f8fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b764fbe87b0fd17e7e643321bebfff83c022c4349f061524feea0d691c86b05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd9c49482abb1233cf02511a1326e3ad0b3ea0d5462a22304320f9a4a22aebab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethods]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethods]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethods]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a46a45a87ea1fb4fc864ba99fe8a6b9f7cf8c33923b32cb226e55cc9f84f85d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethodsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethodsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3590ac8c0137098cbfb58a65757c070a2468a1463efa66e2cf7a6b804365f438)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="cachedMethodsInput")
    def cached_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cachedMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="cachedMethods")
    def cached_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cachedMethods"))

    @cached_methods.setter
    def cached_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae711513d90708e51a5f8f4c7f2b96c9d711253353da34d4735fde1764c2cd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cachedMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "items"))

    @items.setter
    def items(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e3bf4e5e89d6197da66a4a27d851210cc273337efa8dd8461869058ea9736a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "items", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethods]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethods]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethods]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66fdf06f32a3e5d14478f2651aae7c151c50da70471ebf54d708389a68564c49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociation",
    jsii_struct_bases=[],
    name_mapping={"event_type": "eventType", "function_arn": "functionArn"},
)
class CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociation:
    def __init__(self, *, event_type: builtins.str, function_arn: builtins.str) -> None:
        '''
        :param event_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#event_type CloudfrontMultitenantDistribution#event_type}.
        :param function_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#function_arn CloudfrontMultitenantDistribution#function_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df0046aae3c18929131317acc0e19d9d9d88a14f06231b2e01f99b35a36c408b)
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_type": event_type,
            "function_arn": function_arn,
        }

    @builtins.property
    def event_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#event_type CloudfrontMultitenantDistribution#event_type}.'''
        result = self._values.get("event_type")
        assert result is not None, "Required property 'event_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def function_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#function_arn CloudfrontMultitenantDistribution#function_arn}.'''
        result = self._values.get("function_arn")
        assert result is not None, "Required property 'function_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b56cde9427d1c4087d32356c6b5c4925c067891b2184b9bb8a5c993ce69b289)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa2788b78e058515ffb6e4ef9d7a608498aa339a8c90feca1eb868ea821036e1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbf8abc0a1443fe1abcff723bc9d3956446dbe9ddce580b79e22ffc1ae087c4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ddf26ede42ed989b19d4624864ebf217dd632432326827207d63f6f09b20416)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5b76a047300cc587916c9a693d3bc227c4e47f32a0396dda85e7101d6aaf01a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociation]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociation]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__494f0ebfe60a478ce9c9e64042c3afe754eadf2ebf69fb3f40a5f5e8fe4054a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a607e222c5bf9895f8e04dfbe459fb6e422187e3f31b300a52521e31195247f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b4e9be8df284b5262216f697264cffa518fb30f5acc64257ef92b1a6ed61449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionArn"))

    @function_arn.setter
    def function_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a130583f67ea31bd0f16673a4fb7ec8d63c7ee0698ae4ca4b3f88bb918615709)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociation]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociation]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociation]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7402a768f27246291f04a968f22e2e2e423862136e10528497a3d8bfb4c1622d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociation",
    jsii_struct_bases=[],
    name_mapping={
        "event_type": "eventType",
        "lambda_function_arn": "lambdaFunctionArn",
        "include_body": "includeBody",
    },
)
class CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociation:
    def __init__(
        self,
        *,
        event_type: builtins.str,
        lambda_function_arn: builtins.str,
        include_body: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param event_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#event_type CloudfrontMultitenantDistribution#event_type}.
        :param lambda_function_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#lambda_function_arn CloudfrontMultitenantDistribution#lambda_function_arn}.
        :param include_body: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#include_body CloudfrontMultitenantDistribution#include_body}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff02a4e7d00071a283316a4d2676a27c08b6843bc51ab2ca9d63c7185407a2d7)
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument lambda_function_arn", value=lambda_function_arn, expected_type=type_hints["lambda_function_arn"])
            check_type(argname="argument include_body", value=include_body, expected_type=type_hints["include_body"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_type": event_type,
            "lambda_function_arn": lambda_function_arn,
        }
        if include_body is not None:
            self._values["include_body"] = include_body

    @builtins.property
    def event_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#event_type CloudfrontMultitenantDistribution#event_type}.'''
        result = self._values.get("event_type")
        assert result is not None, "Required property 'event_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lambda_function_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#lambda_function_arn CloudfrontMultitenantDistribution#lambda_function_arn}.'''
        result = self._values.get("lambda_function_arn")
        assert result is not None, "Required property 'lambda_function_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include_body(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#include_body CloudfrontMultitenantDistribution#include_body}.'''
        result = self._values.get("include_body")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__426d9ae900cb5db04326fbe4cbf6881f77ecf28b0468c1c3d0eabab6d8950875)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__175b0502548413df42c29583d48fe1717155659ad4a08cb59f11912a58f23672)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0877c049fae20c2a603bfe602079a81f14c23f1115c2f556ec654e86454972c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2e234979b23c0c2bd0a8d30f32372d055bccec5dcb63b2954e1b57dc2b180a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ff83a3e85e2fc6b7850f251376673d8fad303115ac57f45ea8d6994da033ab9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociation]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociation]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd939dad28ce94ae7db2f03f22ddf307bf35c8f476dc72e8841e6fbb0ee5922d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca289b3f69489c587cb488bbdcdccb94476e1c51b7ed372575bf9abba40c7719)
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
    @jsii.member(jsii_name="lambdaFunctionArnInput")
    def lambda_function_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lambdaFunctionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="eventType")
    def event_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventType"))

    @event_type.setter
    def event_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71a89c91842ad360aecd874cc20cebb5df42c5931590b887709bc74e48c57791)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e81309837781cdc96470a12155a30bdc904230ea72b842aafd612e24a292c874)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionArn")
    def lambda_function_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lambdaFunctionArn"))

    @lambda_function_arn.setter
    def lambda_function_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ffadaaed8849d99dbbec6c647451af1b5f7abe7c76b509779408731e51284e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaFunctionArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociation]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociation]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociation]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d28707361224a103f7116184089457d1869ea908470a6c69689ca969b03b6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionDefaultCacheBehaviorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionDefaultCacheBehaviorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d307473570d593a7230ad73f6508f0bcf4c8acfb06235460538db8dca4549cbd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionDefaultCacheBehaviorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1db87a604a88355fca55acbb29ea42ca12a94e7c575c716bde5e338865e9f19)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionDefaultCacheBehaviorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff96ed9c13659f3c12d81e1a3cb5558dfe6dc0fb39207ea21a5e06457fac58a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__595e0faa5f3e0eafed594da6cef811392381a5b52d4dc6e078e398352f3da966)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4b2d54783ede3a214ab559e80b4f1a6adf2306c30a4b65a5fd9b5a291fb2577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehavior]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehavior]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehavior]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605f40acdd83e8c9103318d5caed93a754769fbcfdebf99566248d90c4c5ced3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionDefaultCacheBehaviorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionDefaultCacheBehaviorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__138fd1e56db28855120f6586f9e9ff604d2fffa1ac953d0c1203c9e7f355d672)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAllowedMethods")
    def put_allowed_methods(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethods, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__560cdf10a6d5f8894e95874841fa38882164af20a88e530e7f5b1cccd613619e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowedMethods", [value]))

    @jsii.member(jsii_name="putFunctionAssociation")
    def put_function_association(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9febd8b9641d16ad68d9a31b52829168bace858bb56548c9262674972dfe2bee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFunctionAssociation", [value]))

    @jsii.member(jsii_name="putLambdaFunctionAssociation")
    def put_lambda_function_association(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81fa16a9649801e657748477707bd527d5c5cf2854bd5f132a03d3c99480f9c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLambdaFunctionAssociation", [value]))

    @jsii.member(jsii_name="putTrustedKeyGroups")
    def put_trusted_key_groups(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroups", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d47fe957fd33aa053fa1e31a8ddd6cd8548ae406282b8fa00811d0659506d978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTrustedKeyGroups", [value]))

    @jsii.member(jsii_name="resetAllowedMethods")
    def reset_allowed_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedMethods", []))

    @jsii.member(jsii_name="resetCachePolicyId")
    def reset_cache_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCachePolicyId", []))

    @jsii.member(jsii_name="resetCompress")
    def reset_compress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompress", []))

    @jsii.member(jsii_name="resetFieldLevelEncryptionId")
    def reset_field_level_encryption_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldLevelEncryptionId", []))

    @jsii.member(jsii_name="resetFunctionAssociation")
    def reset_function_association(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunctionAssociation", []))

    @jsii.member(jsii_name="resetLambdaFunctionAssociation")
    def reset_lambda_function_association(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaFunctionAssociation", []))

    @jsii.member(jsii_name="resetOriginRequestPolicyId")
    def reset_origin_request_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginRequestPolicyId", []))

    @jsii.member(jsii_name="resetRealtimeLogConfigArn")
    def reset_realtime_log_config_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRealtimeLogConfigArn", []))

    @jsii.member(jsii_name="resetResponseHeadersPolicyId")
    def reset_response_headers_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseHeadersPolicyId", []))

    @jsii.member(jsii_name="resetTrustedKeyGroups")
    def reset_trusted_key_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedKeyGroups", []))

    @builtins.property
    @jsii.member(jsii_name="allowedMethods")
    def allowed_methods(
        self,
    ) -> CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethodsList:
        return typing.cast(CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethodsList, jsii.get(self, "allowedMethods"))

    @builtins.property
    @jsii.member(jsii_name="functionAssociation")
    def function_association(
        self,
    ) -> CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociationList:
        return typing.cast(CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociationList, jsii.get(self, "functionAssociation"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionAssociation")
    def lambda_function_association(
        self,
    ) -> CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociationList:
        return typing.cast(CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociationList, jsii.get(self, "lambdaFunctionAssociation"))

    @builtins.property
    @jsii.member(jsii_name="trustedKeyGroups")
    def trusted_key_groups(
        self,
    ) -> "CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroupsList":
        return typing.cast("CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroupsList", jsii.get(self, "trustedKeyGroups"))

    @builtins.property
    @jsii.member(jsii_name="allowedMethodsInput")
    def allowed_methods_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethods]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethods]]], jsii.get(self, "allowedMethodsInput"))

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
    @jsii.member(jsii_name="fieldLevelEncryptionIdInput")
    def field_level_encryption_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldLevelEncryptionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="functionAssociationInput")
    def function_association_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociation]]], jsii.get(self, "functionAssociationInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionAssociationInput")
    def lambda_function_association_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociation]]], jsii.get(self, "lambdaFunctionAssociationInput"))

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
    @jsii.member(jsii_name="targetOriginIdInput")
    def target_origin_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetOriginIdInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedKeyGroupsInput")
    def trusted_key_groups_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroups"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroups"]]], jsii.get(self, "trustedKeyGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="viewerProtocolPolicyInput")
    def viewer_protocol_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "viewerProtocolPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="cachePolicyId")
    def cache_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cachePolicyId"))

    @cache_policy_id.setter
    def cache_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88dce4e54c7389317649aa29f5bc2326f7525fa4c11cfe16214b207d3e4bc169)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4463fef4eefe7fd46c042fc847908a6bb1179a928ff0e017c4447c0397d69d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fieldLevelEncryptionId")
    def field_level_encryption_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldLevelEncryptionId"))

    @field_level_encryption_id.setter
    def field_level_encryption_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3991e17df2d764431112cd0c0fa3a9779ac4f3b8b9320544e8a06ecb1ad9f9ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldLevelEncryptionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originRequestPolicyId")
    def origin_request_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originRequestPolicyId"))

    @origin_request_policy_id.setter
    def origin_request_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b415718b7d66f08c4a728c478fed0b6d4420c5f589977f4d2856044e5a211707)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originRequestPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="realtimeLogConfigArn")
    def realtime_log_config_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "realtimeLogConfigArn"))

    @realtime_log_config_arn.setter
    def realtime_log_config_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f5daf1c81607fd2a01c3540763b219a6b88445860a787ae4bcb4b861292de1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "realtimeLogConfigArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseHeadersPolicyId")
    def response_headers_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseHeadersPolicyId"))

    @response_headers_policy_id.setter
    def response_headers_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c1867de29fa44f1c5f678e44b505cc047b9aa2397b4315beab94943c22017a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseHeadersPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetOriginId")
    def target_origin_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetOriginId"))

    @target_origin_id.setter
    def target_origin_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75feffbc724f1f1fc83eec3b416abe14d8c395a3161b010c5230f35ad2dff69a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetOriginId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="viewerProtocolPolicy")
    def viewer_protocol_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "viewerProtocolPolicy"))

    @viewer_protocol_policy.setter
    def viewer_protocol_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eca0b770100fde4c8294d95ccdb4928ecddce81e476cfd5f7e5cf1c641b3537e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "viewerProtocolPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionDefaultCacheBehavior]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionDefaultCacheBehavior]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionDefaultCacheBehavior]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e733a449a93bb929215c7560fdda29a89f027b54eb24f2b2725484e250d247ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroups",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "items": "items"},
)
class CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroups:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        items: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#enabled CloudfrontMultitenantDistribution#enabled}.
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#items CloudfrontMultitenantDistribution#items}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__108bdbfeb1082e65432d3153ace3194b1accb04a58dbabb24000803a39d8b2be)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if items is not None:
            self._values["items"] = items

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#enabled CloudfrontMultitenantDistribution#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def items(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#items CloudfrontMultitenantDistribution#items}.'''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ee3d8691ed19c1a14e3e078406741e4d33bcd67123e2b3f33bdd5f87e2c5d94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8505c7ca24428bba115d9ea6c69396edf216e96af74e232e4b08b1e1b1a870d2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a44f99697484e5ed98f6aa4faf97e1703c08c7b94990f516b98cb168b73de73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__082fde28f7d927db72197781a03c192d4aeae08c2f9e819a7c85875b36e0ea12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__348cabbb7daac5edc0619206625229e25cdbaf529c5a57dc566622bf3e9c8273)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroups]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroups]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d27090994e65471a7deeb86f8c087e219ab4111586ed143d03d6967711e2a44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__469fe398a5532a159213f9080d95dc89accd0796cd7fff6f2a40f798ae4c176e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetItems")
    def reset_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItems", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "itemsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ca967bb059ba8705d5b509ab65c7a70f477a07974b77c5a930368399e1ee60a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "items"))

    @items.setter
    def items(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a1f51692779c674e13ac8d1bda887b35977360215529688da12dc755c13846)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "items", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroups]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroups]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroups]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6461d071a83be4bbcf0cc25cd523227a7936b620782f218202988611fd4dfdd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOrigin",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "id": "id",
        "connection_attempts": "connectionAttempts",
        "connection_timeout": "connectionTimeout",
        "custom_header": "customHeader",
        "custom_origin_config": "customOriginConfig",
        "origin_access_control_id": "originAccessControlId",
        "origin_path": "originPath",
        "origin_shield": "originShield",
        "response_completion_timeout": "responseCompletionTimeout",
        "vpc_origin_config": "vpcOriginConfig",
    },
)
class CloudfrontMultitenantDistributionOrigin:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        id: builtins.str,
        connection_attempts: typing.Optional[jsii.Number] = None,
        connection_timeout: typing.Optional[jsii.Number] = None,
        custom_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionOriginCustomHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_origin_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionOriginCustomOriginConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        origin_access_control_id: typing.Optional[builtins.str] = None,
        origin_path: typing.Optional[builtins.str] = None,
        origin_shield: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionOriginOriginShield", typing.Dict[builtins.str, typing.Any]]]]] = None,
        response_completion_timeout: typing.Optional[jsii.Number] = None,
        vpc_origin_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionOriginVpcOriginConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#domain_name CloudfrontMultitenantDistribution#domain_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#id CloudfrontMultitenantDistribution#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection_attempts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#connection_attempts CloudfrontMultitenantDistribution#connection_attempts}.
        :param connection_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#connection_timeout CloudfrontMultitenantDistribution#connection_timeout}.
        :param custom_header: custom_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#custom_header CloudfrontMultitenantDistribution#custom_header}
        :param custom_origin_config: custom_origin_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#custom_origin_config CloudfrontMultitenantDistribution#custom_origin_config}
        :param origin_access_control_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_access_control_id CloudfrontMultitenantDistribution#origin_access_control_id}.
        :param origin_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_path CloudfrontMultitenantDistribution#origin_path}.
        :param origin_shield: origin_shield block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_shield CloudfrontMultitenantDistribution#origin_shield}
        :param response_completion_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#response_completion_timeout CloudfrontMultitenantDistribution#response_completion_timeout}.
        :param vpc_origin_config: vpc_origin_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#vpc_origin_config CloudfrontMultitenantDistribution#vpc_origin_config}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e591d622930693b75d6c15b65d2278fdd422c289d2d8389447260a38810caa59)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument connection_attempts", value=connection_attempts, expected_type=type_hints["connection_attempts"])
            check_type(argname="argument connection_timeout", value=connection_timeout, expected_type=type_hints["connection_timeout"])
            check_type(argname="argument custom_header", value=custom_header, expected_type=type_hints["custom_header"])
            check_type(argname="argument custom_origin_config", value=custom_origin_config, expected_type=type_hints["custom_origin_config"])
            check_type(argname="argument origin_access_control_id", value=origin_access_control_id, expected_type=type_hints["origin_access_control_id"])
            check_type(argname="argument origin_path", value=origin_path, expected_type=type_hints["origin_path"])
            check_type(argname="argument origin_shield", value=origin_shield, expected_type=type_hints["origin_shield"])
            check_type(argname="argument response_completion_timeout", value=response_completion_timeout, expected_type=type_hints["response_completion_timeout"])
            check_type(argname="argument vpc_origin_config", value=vpc_origin_config, expected_type=type_hints["vpc_origin_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
            "id": id,
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
        if vpc_origin_config is not None:
            self._values["vpc_origin_config"] = vpc_origin_config

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#domain_name CloudfrontMultitenantDistribution#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#id CloudfrontMultitenantDistribution#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connection_attempts(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#connection_attempts CloudfrontMultitenantDistribution#connection_attempts}.'''
        result = self._values.get("connection_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def connection_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#connection_timeout CloudfrontMultitenantDistribution#connection_timeout}.'''
        result = self._values.get("connection_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def custom_header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOriginCustomHeader"]]]:
        '''custom_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#custom_header CloudfrontMultitenantDistribution#custom_header}
        '''
        result = self._values.get("custom_header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOriginCustomHeader"]]], result)

    @builtins.property
    def custom_origin_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOriginCustomOriginConfig"]]]:
        '''custom_origin_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#custom_origin_config CloudfrontMultitenantDistribution#custom_origin_config}
        '''
        result = self._values.get("custom_origin_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOriginCustomOriginConfig"]]], result)

    @builtins.property
    def origin_access_control_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_access_control_id CloudfrontMultitenantDistribution#origin_access_control_id}.'''
        result = self._values.get("origin_access_control_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origin_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_path CloudfrontMultitenantDistribution#origin_path}.'''
        result = self._values.get("origin_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origin_shield(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOriginOriginShield"]]]:
        '''origin_shield block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_shield CloudfrontMultitenantDistribution#origin_shield}
        '''
        result = self._values.get("origin_shield")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOriginOriginShield"]]], result)

    @builtins.property
    def response_completion_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#response_completion_timeout CloudfrontMultitenantDistribution#response_completion_timeout}.'''
        result = self._values.get("response_completion_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc_origin_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOriginVpcOriginConfig"]]]:
        '''vpc_origin_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#vpc_origin_config CloudfrontMultitenantDistribution#vpc_origin_config}
        '''
        result = self._values.get("vpc_origin_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOriginVpcOriginConfig"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionOrigin(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginCustomHeader",
    jsii_struct_bases=[],
    name_mapping={"header_name": "headerName", "header_value": "headerValue"},
)
class CloudfrontMultitenantDistributionOriginCustomHeader:
    def __init__(
        self,
        *,
        header_name: builtins.str,
        header_value: builtins.str,
    ) -> None:
        '''
        :param header_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#header_name CloudfrontMultitenantDistribution#header_name}.
        :param header_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#header_value CloudfrontMultitenantDistribution#header_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d896c83e6297d7b6a2f4882d82250f50d479a950f1b9cce4f078b9967c7ca77c)
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
            check_type(argname="argument header_value", value=header_value, expected_type=type_hints["header_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header_name": header_name,
            "header_value": header_value,
        }

    @builtins.property
    def header_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#header_name CloudfrontMultitenantDistribution#header_name}.'''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def header_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#header_value CloudfrontMultitenantDistribution#header_value}.'''
        result = self._values.get("header_value")
        assert result is not None, "Required property 'header_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionOriginCustomHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionOriginCustomHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginCustomHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__925d4fcf29ee4e116c9614779c9f0dd0c3cbe77acbcb994f24a6519342b94e7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionOriginCustomHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9cfb0d71e510597b74f0e671e1df5a37a6476dc77aef01f89a882a75f1aaa86)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionOriginCustomHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bfbae4a1ee55b3f25faa16f48bb7583d1f81c6433776f4374f9cee3db618253)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9423c096861dc0215285b0c8de9e8d007679d894eef6ec5fbe7ed8fafd6df1f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__083d93f74907f0febf1d18a8d42c796c8936368392a3f3036e430422d89fcf66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginCustomHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginCustomHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginCustomHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7eb861899e67f991a97d9573a7029994b784026c4f0a86f6b5bafcc2046098a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionOriginCustomHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginCustomHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9542e2a8bc7d8259253893e8d732295743e419b95d780056e624dd9a86ae1c96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="headerNameInput")
    def header_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="headerValueInput")
    def header_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerValueInput"))

    @builtins.property
    @jsii.member(jsii_name="headerName")
    def header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerName"))

    @header_name.setter
    def header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5a4d054ceabbe47ca068ae918e07ceb296e687389388ea068ac93be77457ea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerValue")
    def header_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "headerValue"))

    @header_value.setter
    def header_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f77c0d04899dc8634e3d1014f9f6449a9c6483d3903512bb44e07db29ebc009)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginCustomHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginCustomHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginCustomHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b01352dbee700ab3efaea01be47169c071ee5eeda2b335c5b8d3b1c3be084cf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginCustomOriginConfig",
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
class CloudfrontMultitenantDistributionOriginCustomOriginConfig:
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
        :param http_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#http_port CloudfrontMultitenantDistribution#http_port}.
        :param https_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#https_port CloudfrontMultitenantDistribution#https_port}.
        :param origin_protocol_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_protocol_policy CloudfrontMultitenantDistribution#origin_protocol_policy}.
        :param origin_ssl_protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_ssl_protocols CloudfrontMultitenantDistribution#origin_ssl_protocols}.
        :param ip_address_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#ip_address_type CloudfrontMultitenantDistribution#ip_address_type}.
        :param origin_keepalive_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_keepalive_timeout CloudfrontMultitenantDistribution#origin_keepalive_timeout}.
        :param origin_read_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_read_timeout CloudfrontMultitenantDistribution#origin_read_timeout}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c981a1dfb6d4571febac01041b53571cbbd69f2abdab446e7c72853e964cf5a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#http_port CloudfrontMultitenantDistribution#http_port}.'''
        result = self._values.get("http_port")
        assert result is not None, "Required property 'http_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def https_port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#https_port CloudfrontMultitenantDistribution#https_port}.'''
        result = self._values.get("https_port")
        assert result is not None, "Required property 'https_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def origin_protocol_policy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_protocol_policy CloudfrontMultitenantDistribution#origin_protocol_policy}.'''
        result = self._values.get("origin_protocol_policy")
        assert result is not None, "Required property 'origin_protocol_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origin_ssl_protocols(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_ssl_protocols CloudfrontMultitenantDistribution#origin_ssl_protocols}.'''
        result = self._values.get("origin_ssl_protocols")
        assert result is not None, "Required property 'origin_ssl_protocols' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#ip_address_type CloudfrontMultitenantDistribution#ip_address_type}.'''
        result = self._values.get("ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origin_keepalive_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_keepalive_timeout CloudfrontMultitenantDistribution#origin_keepalive_timeout}.'''
        result = self._values.get("origin_keepalive_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def origin_read_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_read_timeout CloudfrontMultitenantDistribution#origin_read_timeout}.'''
        result = self._values.get("origin_read_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionOriginCustomOriginConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionOriginCustomOriginConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginCustomOriginConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1384fbcd2b24328726d5a8c9acd8e037e23357c8e84598034a10057d0152ef4a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionOriginCustomOriginConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e297bf71c669fbd5c07ca55a10579fefb67f3fd253894d19e2878a314e83b5c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionOriginCustomOriginConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d8557cbe80acfcf8e9e2791319db85d9a76f6e8c017bdaf5672d1c29a9b20f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f4af8a5f47a0b2c035374b3d238b9e1995ab4b776ffa2c3e40318fae41e1630)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0595e6a49a73b42cc03017749faed98c3d6c8b554c8c1be915696291199b6bd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginCustomOriginConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginCustomOriginConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginCustomOriginConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0799237a2e25c61869816259fb93a78065c32657a8a7cccf6011231ae767719b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionOriginCustomOriginConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginCustomOriginConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb6a5a8854b940eafaa6a6d7a0b04e5d0df431669a5597e337c569aea59612a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
            type_hints = typing.get_type_hints(_typecheckingstub__5e317e6ba87279005d8728ecb7d8881bd245f3fb8981cea742ab3098056ef66d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsPort")
    def https_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "httpsPort"))

    @https_port.setter
    def https_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a73db28fa6ed6b181d6839aeebfede07dbc6d506bdc7fffd26f44266b92b2e7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddressType")
    def ip_address_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddressType"))

    @ip_address_type.setter
    def ip_address_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6169db21cd1dce6c9df252cfd8b89be333dbf933c0efc6e39428ee4e5f9adf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddressType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originKeepaliveTimeout")
    def origin_keepalive_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "originKeepaliveTimeout"))

    @origin_keepalive_timeout.setter
    def origin_keepalive_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04f0d81b9fae5e33c8e9f278114e442f5ab979ed417dbd88f14c3c816a065834)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originKeepaliveTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originProtocolPolicy")
    def origin_protocol_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originProtocolPolicy"))

    @origin_protocol_policy.setter
    def origin_protocol_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4ed62f8817bad9a635cf2abb78605b1f37fa06176283f42a41fbe8c99fa2df7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originProtocolPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originReadTimeout")
    def origin_read_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "originReadTimeout"))

    @origin_read_timeout.setter
    def origin_read_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e238cfe3b6a92f8e0c9adf9778139d863d6d66e3b89300daf952fc16517f7e47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originReadTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originSslProtocols")
    def origin_ssl_protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "originSslProtocols"))

    @origin_ssl_protocols.setter
    def origin_ssl_protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb5a5bf1a5cc92b1440dd7015fd4731deb1cd60ce27ff50b9a3bdbc667bd0fe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originSslProtocols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginCustomOriginConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginCustomOriginConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginCustomOriginConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f51b20fb2f3f8478235472cba93615703b80fd70f94f6876452ad544c8654a2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginGroup",
    jsii_struct_bases=[],
    name_mapping={
        "origin_id": "originId",
        "failover_criteria": "failoverCriteria",
        "member": "member",
    },
)
class CloudfrontMultitenantDistributionOriginGroup:
    def __init__(
        self,
        *,
        origin_id: builtins.str,
        failover_criteria: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionOriginGroupFailoverCriteria", typing.Dict[builtins.str, typing.Any]]]]] = None,
        member: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionOriginGroupMember", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param origin_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_id CloudfrontMultitenantDistribution#origin_id}.
        :param failover_criteria: failover_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#failover_criteria CloudfrontMultitenantDistribution#failover_criteria}
        :param member: member block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#member CloudfrontMultitenantDistribution#member}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ba015ae8a46f2d7a01cf7fe644a4011a7691e04aa46332cf18c43e6589b4ea2)
            check_type(argname="argument origin_id", value=origin_id, expected_type=type_hints["origin_id"])
            check_type(argname="argument failover_criteria", value=failover_criteria, expected_type=type_hints["failover_criteria"])
            check_type(argname="argument member", value=member, expected_type=type_hints["member"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "origin_id": origin_id,
        }
        if failover_criteria is not None:
            self._values["failover_criteria"] = failover_criteria
        if member is not None:
            self._values["member"] = member

    @builtins.property
    def origin_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_id CloudfrontMultitenantDistribution#origin_id}.'''
        result = self._values.get("origin_id")
        assert result is not None, "Required property 'origin_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def failover_criteria(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOriginGroupFailoverCriteria"]]]:
        '''failover_criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#failover_criteria CloudfrontMultitenantDistribution#failover_criteria}
        '''
        result = self._values.get("failover_criteria")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOriginGroupFailoverCriteria"]]], result)

    @builtins.property
    def member(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOriginGroupMember"]]]:
        '''member block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#member CloudfrontMultitenantDistribution#member}
        '''
        result = self._values.get("member")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOriginGroupMember"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionOriginGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginGroupFailoverCriteria",
    jsii_struct_bases=[],
    name_mapping={"status_codes": "statusCodes"},
)
class CloudfrontMultitenantDistributionOriginGroupFailoverCriteria:
    def __init__(self, *, status_codes: typing.Sequence[jsii.Number]) -> None:
        '''
        :param status_codes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#status_codes CloudfrontMultitenantDistribution#status_codes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d1b48752e5b7fe4c9b611c083f7a73b3023a118f7aed6227e47c44530847faa)
            check_type(argname="argument status_codes", value=status_codes, expected_type=type_hints["status_codes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status_codes": status_codes,
        }

    @builtins.property
    def status_codes(self) -> typing.List[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#status_codes CloudfrontMultitenantDistribution#status_codes}.'''
        result = self._values.get("status_codes")
        assert result is not None, "Required property 'status_codes' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionOriginGroupFailoverCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionOriginGroupFailoverCriteriaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginGroupFailoverCriteriaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f5504853a07c9dd9252cf6158c48f01a458f4f19d5c0240469939ca22fcabce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionOriginGroupFailoverCriteriaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__931b031cf4e71298aaeb6b6dd3747f3e751f00ba7518b24ef39ab4850988bdce)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionOriginGroupFailoverCriteriaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e084c2c838d066f0eb087d003ec06a41ad3d903cdb01b217ef2a93c35f8e1cd5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6834381b62396266b08a359b280d4cf91c01b1e30baafd1b5128a185df60a65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27e8d312c3a598908e0c8ef606f06164ef60b6d7733a6379818d0075be98340d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginGroupFailoverCriteria]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginGroupFailoverCriteria]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginGroupFailoverCriteria]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df25c54f81e9ec79d096d641eb59e9799d8ec3998f3440c504c1aefc7ea9956b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionOriginGroupFailoverCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginGroupFailoverCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6d251ebf73d5009d214d2f9142f2aa75a80da25057872fdfe8e70c944d8a231)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
            type_hints = typing.get_type_hints(_typecheckingstub__a71f5d1b0316dfcdd92d67157d53b2d15b809be4663f60f272c702b43338ba35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginGroupFailoverCriteria]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginGroupFailoverCriteria]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginGroupFailoverCriteria]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e64efa2b0b0b4d28c7e07d81b0da3d01f81c976b2bbd16d44fbccc124c7f235b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionOriginGroupList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginGroupList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03718e7e88ad952c8074b931d823ebf0b3819f4c46ee3fb25395e09f4909d366)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionOriginGroupOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2912e52e4984e5be7ec5f1916ac17dab0e28648caee00ebe0358918475b4ce60)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionOriginGroupOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f60832681f52cf04889174e394ea16e92f060ecf58178daa3d8b78380b6166c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a608c5743c0469f3f60c17f0165ed21c9130153dc0273f0fb51a4d818fee0676)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ef54b9b1d970c1813d6a7c187655d16ce53e53aedeafa6b0726759123ca9dd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginGroup]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginGroup]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aadd53c1aafa57fc4af89e202778cd8b10f572911f1e7822c8d8d506715c3356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginGroupMember",
    jsii_struct_bases=[],
    name_mapping={"origin_id": "originId"},
)
class CloudfrontMultitenantDistributionOriginGroupMember:
    def __init__(self, *, origin_id: builtins.str) -> None:
        '''
        :param origin_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_id CloudfrontMultitenantDistribution#origin_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d6604906333885d0d4933e7b96d9dbb88ee73608a5703141ba9632c2be0a35f)
            check_type(argname="argument origin_id", value=origin_id, expected_type=type_hints["origin_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "origin_id": origin_id,
        }

    @builtins.property
    def origin_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_id CloudfrontMultitenantDistribution#origin_id}.'''
        result = self._values.get("origin_id")
        assert result is not None, "Required property 'origin_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionOriginGroupMember(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionOriginGroupMemberList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginGroupMemberList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9d52a7399c07c7dade02f7a27b97cd5d7a3292ebb4260a2d4fe7a9679428f74)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionOriginGroupMemberOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__380a1577281b30095cecd272ea29dbb3e7591706a92128d5625d49e51f95d98b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionOriginGroupMemberOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7796ef2cdd1b5498cd06a0b4d34127b84ce355f62224bf16cbe68a04a0d18e5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__acde513b660361c40f6f5f54effcc1773e90ad368a628ec56d52379f2324e6f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69cc08fe43e63435717da24332d215dee4586ed8ec3d5d2b0c5f9ec1cdb5c410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginGroupMember]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginGroupMember]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginGroupMember]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__306927c6c5e615817249b6bd2be272b6104b92eeb5332bbf4fd68f5e1c43896d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionOriginGroupMemberOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginGroupMemberOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d0ea096e617d37b03a97862309a291c3e1b2e6225592cf3de073c2eab5970a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c87454742819b9dd925932941bc7b33285da40dd2cfc1b66fe29a9a2df9cdfa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginGroupMember]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginGroupMember]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginGroupMember]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__480c865df71aa44443d17872ee7901147ddb2e5a606bf775d6581f67e61c8ca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionOriginGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9262f82638257a884615fda6275b2c1c18dc6e99c61d91d7a2c6b417c2e363af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFailoverCriteria")
    def put_failover_criteria(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOriginGroupFailoverCriteria, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b072ced6b848d1250c1ee6c730698c96a974c5a3cdbaa7da1dc87bf755c0779d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFailoverCriteria", [value]))

    @jsii.member(jsii_name="putMember")
    def put_member(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOriginGroupMember, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd5d5d71714e9d12073574e5ef90d0dddddf6f2d7e419b79628e17dac1011301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMember", [value]))

    @jsii.member(jsii_name="resetFailoverCriteria")
    def reset_failover_criteria(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailoverCriteria", []))

    @jsii.member(jsii_name="resetMember")
    def reset_member(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMember", []))

    @builtins.property
    @jsii.member(jsii_name="failoverCriteria")
    def failover_criteria(
        self,
    ) -> CloudfrontMultitenantDistributionOriginGroupFailoverCriteriaList:
        return typing.cast(CloudfrontMultitenantDistributionOriginGroupFailoverCriteriaList, jsii.get(self, "failoverCriteria"))

    @builtins.property
    @jsii.member(jsii_name="member")
    def member(self) -> CloudfrontMultitenantDistributionOriginGroupMemberList:
        return typing.cast(CloudfrontMultitenantDistributionOriginGroupMemberList, jsii.get(self, "member"))

    @builtins.property
    @jsii.member(jsii_name="failoverCriteriaInput")
    def failover_criteria_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginGroupFailoverCriteria]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginGroupFailoverCriteria]]], jsii.get(self, "failoverCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="memberInput")
    def member_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginGroupMember]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginGroupMember]]], jsii.get(self, "memberInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__804d304eb6c69f8d98df38ac91e39a61956573037907ec2765544e342e2d5aa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginGroup]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginGroup]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginGroup]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__712008b233aef39c5fd9c8405e3117d9215348a7edb8baf8af9ffb7daa4bedea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionOriginList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4a5e643f99b48584dea119505c1bff30cf8be69dc3b16c6c2f1f4ac91993331)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionOriginOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80da6a502d4ac5967534a6f126875c640f8f772e504323f576d4ca9c08b45449)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionOriginOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c01f7c2b8ca5f3b9c007db4db60982248a5d6b5378534c6cfbe63320c15befca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c60ef2dd42f0068da1a68b2731d2e00c7825740f80f52d92c11e5fa318312a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdcaca763915ccf901b7de856e49398dd9007928d4524b7b320819850b997ac5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOrigin]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOrigin]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOrigin]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba2acd3f40a8e8645d930dd41d57035ada5ccba361a3360a48f6b332b689d9a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginOriginShield",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "origin_shield_region": "originShieldRegion"},
)
class CloudfrontMultitenantDistributionOriginOriginShield:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        origin_shield_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#enabled CloudfrontMultitenantDistribution#enabled}.
        :param origin_shield_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_shield_region CloudfrontMultitenantDistribution#origin_shield_region}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89982a5a64dec50b8ba5c3aefd8573a1aa168b1d688981d35a14d435f790d477)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument origin_shield_region", value=origin_shield_region, expected_type=type_hints["origin_shield_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if origin_shield_region is not None:
            self._values["origin_shield_region"] = origin_shield_region

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#enabled CloudfrontMultitenantDistribution#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def origin_shield_region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_shield_region CloudfrontMultitenantDistribution#origin_shield_region}.'''
        result = self._values.get("origin_shield_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionOriginOriginShield(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionOriginOriginShieldList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginOriginShieldList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__505619c53510232071f20df04c665982e85290fa389e9200878836850bee6f5c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionOriginOriginShieldOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783e018bf49b1e77076ec160069edea1862a0107f24871d4b472f6739b3dce42)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionOriginOriginShieldOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38dce2c8e5b3b477e3570f309a26c2b05f6fef87d50972560ba5f88ae2d33413)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79257fe2899dccb77b7713c2d7ccc17ecb92f6feddad17bd039d7d21024d5792)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf6f4e05611b94a96a6c05b3faa04f7965a4a5f70c4b92415e40aff3bd5469af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginOriginShield]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginOriginShield]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginOriginShield]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b7fc0f4149d473617d628235f977af447875b004fedc14ca31ff375b29762bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionOriginOriginShieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginOriginShieldOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb39f96f2a0907527c5cc89e09dec9bc89cdd4baf29adf0cc0147dd83241c016)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
            type_hints = typing.get_type_hints(_typecheckingstub__0b78937c45d5a9b5f65f0a78fa684b65c8a66f526a70742bfd15d689b3df496b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originShieldRegion")
    def origin_shield_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originShieldRegion"))

    @origin_shield_region.setter
    def origin_shield_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e282b7cfd8f9b356e67d0883d325b8788d8b7d101ebdb95e330d17ae7f0011)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originShieldRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginOriginShield]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginOriginShield]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginOriginShield]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__374cabcffeca4e88709e9a426e88ba5ded015c660f0cdd6a30a1b8c8e4249413)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionOriginOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d3e261b0950b6c3a2d4b470c8020627600f35d2d64be502f0751d35543c72ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCustomHeader")
    def put_custom_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOriginCustomHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__546fc4349a12ac5fad76f3094eb983be9782fc90d39816bfdeecc2e2e7081dbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomHeader", [value]))

    @jsii.member(jsii_name="putCustomOriginConfig")
    def put_custom_origin_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOriginCustomOriginConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f662eef87e087fe3041dc7d2a549ddea7d258f3bea8a6f7bed2bd9892db8b3ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomOriginConfig", [value]))

    @jsii.member(jsii_name="putOriginShield")
    def put_origin_shield(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOriginOriginShield, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__352444e9ba583e6fe7f5a69afdcb6874b361ff5843d5ca5e84afe228722e1360)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOriginShield", [value]))

    @jsii.member(jsii_name="putVpcOriginConfig")
    def put_vpc_origin_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionOriginVpcOriginConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e83f4379801331ed128dc28b7435d7f445318fded02e110f008a24fa78f50dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
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

    @jsii.member(jsii_name="resetVpcOriginConfig")
    def reset_vpc_origin_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcOriginConfig", []))

    @builtins.property
    @jsii.member(jsii_name="customHeader")
    def custom_header(self) -> CloudfrontMultitenantDistributionOriginCustomHeaderList:
        return typing.cast(CloudfrontMultitenantDistributionOriginCustomHeaderList, jsii.get(self, "customHeader"))

    @builtins.property
    @jsii.member(jsii_name="customOriginConfig")
    def custom_origin_config(
        self,
    ) -> CloudfrontMultitenantDistributionOriginCustomOriginConfigList:
        return typing.cast(CloudfrontMultitenantDistributionOriginCustomOriginConfigList, jsii.get(self, "customOriginConfig"))

    @builtins.property
    @jsii.member(jsii_name="originShield")
    def origin_shield(self) -> CloudfrontMultitenantDistributionOriginOriginShieldList:
        return typing.cast(CloudfrontMultitenantDistributionOriginOriginShieldList, jsii.get(self, "originShield"))

    @builtins.property
    @jsii.member(jsii_name="vpcOriginConfig")
    def vpc_origin_config(
        self,
    ) -> "CloudfrontMultitenantDistributionOriginVpcOriginConfigList":
        return typing.cast("CloudfrontMultitenantDistributionOriginVpcOriginConfigList", jsii.get(self, "vpcOriginConfig"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginCustomHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginCustomHeader]]], jsii.get(self, "customHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="customOriginConfigInput")
    def custom_origin_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginCustomOriginConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginCustomOriginConfig]]], jsii.get(self, "customOriginConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="originAccessControlIdInput")
    def origin_access_control_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originAccessControlIdInput"))

    @builtins.property
    @jsii.member(jsii_name="originPathInput")
    def origin_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originPathInput"))

    @builtins.property
    @jsii.member(jsii_name="originShieldInput")
    def origin_shield_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginOriginShield]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginOriginShield]]], jsii.get(self, "originShieldInput"))

    @builtins.property
    @jsii.member(jsii_name="responseCompletionTimeoutInput")
    def response_completion_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "responseCompletionTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcOriginConfigInput")
    def vpc_origin_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOriginVpcOriginConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionOriginVpcOriginConfig"]]], jsii.get(self, "vpcOriginConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionAttempts")
    def connection_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "connectionAttempts"))

    @connection_attempts.setter
    def connection_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a468f472eb730537295addbc0872270be1e5372c19bcfbe192889bd0e177e5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectionTimeout")
    def connection_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "connectionTimeout"))

    @connection_timeout.setter
    def connection_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3530613fb1ba394b29d7d89703e8c64f506d2e4a0045a0a4fe10397ed7447aa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be09d521d7db57f856bdc14bf78116d4e1eb26a565852ca2872e3a7dfb15c9fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7720284cf367ce105b25d8381bd065e0c69eea60a7cf63261a05f7718d78482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originAccessControlId")
    def origin_access_control_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originAccessControlId"))

    @origin_access_control_id.setter
    def origin_access_control_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__473a88916137e3c945785a3b0259b51a3fa626b3576be503616bb8d7ba661227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originAccessControlId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originPath")
    def origin_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originPath"))

    @origin_path.setter
    def origin_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9531237b0e9f15a3e551aa98134a28296f4bd90babed13b623d421ccaf8ad03e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseCompletionTimeout")
    def response_completion_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "responseCompletionTimeout"))

    @response_completion_timeout.setter
    def response_completion_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f008f37fd9486416c1cf20b32198205675d6f85bf4082bf302b001f5a708be29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseCompletionTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOrigin]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOrigin]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOrigin]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c5d522d9e914eccd4f2bf86025f85ed5bae50b43bd4cdd2b02f34962034ed6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginVpcOriginConfig",
    jsii_struct_bases=[],
    name_mapping={
        "vpc_origin_id": "vpcOriginId",
        "origin_keepalive_timeout": "originKeepaliveTimeout",
        "origin_read_timeout": "originReadTimeout",
    },
)
class CloudfrontMultitenantDistributionOriginVpcOriginConfig:
    def __init__(
        self,
        *,
        vpc_origin_id: builtins.str,
        origin_keepalive_timeout: typing.Optional[jsii.Number] = None,
        origin_read_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param vpc_origin_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#vpc_origin_id CloudfrontMultitenantDistribution#vpc_origin_id}.
        :param origin_keepalive_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_keepalive_timeout CloudfrontMultitenantDistribution#origin_keepalive_timeout}.
        :param origin_read_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_read_timeout CloudfrontMultitenantDistribution#origin_read_timeout}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49ca1c2df8a4aa90786a71625e67a5ea2bbb6ad8189c4fd6b015b6f2cd11aa79)
            check_type(argname="argument vpc_origin_id", value=vpc_origin_id, expected_type=type_hints["vpc_origin_id"])
            check_type(argname="argument origin_keepalive_timeout", value=origin_keepalive_timeout, expected_type=type_hints["origin_keepalive_timeout"])
            check_type(argname="argument origin_read_timeout", value=origin_read_timeout, expected_type=type_hints["origin_read_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc_origin_id": vpc_origin_id,
        }
        if origin_keepalive_timeout is not None:
            self._values["origin_keepalive_timeout"] = origin_keepalive_timeout
        if origin_read_timeout is not None:
            self._values["origin_read_timeout"] = origin_read_timeout

    @builtins.property
    def vpc_origin_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#vpc_origin_id CloudfrontMultitenantDistribution#vpc_origin_id}.'''
        result = self._values.get("vpc_origin_id")
        assert result is not None, "Required property 'vpc_origin_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origin_keepalive_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_keepalive_timeout CloudfrontMultitenantDistribution#origin_keepalive_timeout}.'''
        result = self._values.get("origin_keepalive_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def origin_read_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#origin_read_timeout CloudfrontMultitenantDistribution#origin_read_timeout}.'''
        result = self._values.get("origin_read_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionOriginVpcOriginConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionOriginVpcOriginConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginVpcOriginConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__439fbbd634a659eb8656647485260205d13e250c7bf6044a3aa6da6768e58bc1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionOriginVpcOriginConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6c662aca5cf64f9266ab2bccb35057faa140611aa8ebd584e23da58bffffdcb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionOriginVpcOriginConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8a749f7a1219a448d8d0cb28b59a721a64e69650a4331a8f93eb7fad4be2b57)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b80e69ec8df5c8d0aea635e3ab8dfdf4431b9cc2f851289d30143155df8bd737)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb755d545e544985ac99f01955e8b85c331ca020b9afcda7da3b18bcbd9dc702)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginVpcOriginConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginVpcOriginConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginVpcOriginConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__550dbb1337707f3a4cdf281c63492eabd85564a310fb1561a39db09335efd50e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionOriginVpcOriginConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionOriginVpcOriginConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e96237ecd22ea3f6f3a08b9865eb6afc2955840e0ad267e40f978f84a2fcf038)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOriginKeepaliveTimeout")
    def reset_origin_keepalive_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginKeepaliveTimeout", []))

    @jsii.member(jsii_name="resetOriginReadTimeout")
    def reset_origin_read_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginReadTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="originKeepaliveTimeoutInput")
    def origin_keepalive_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "originKeepaliveTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="originReadTimeoutInput")
    def origin_read_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "originReadTimeoutInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__255d4cc1cba403b3f070760f1a2597649d0741833ddada0b474210442d3baf94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originKeepaliveTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originReadTimeout")
    def origin_read_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "originReadTimeout"))

    @origin_read_timeout.setter
    def origin_read_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5802aa2f45ac68ee35a5143ee062c9eba56948f6711e904c7b5600c85757e107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originReadTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcOriginId")
    def vpc_origin_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcOriginId"))

    @vpc_origin_id.setter
    def vpc_origin_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e78fc3db2f204ea5b6ceaa5369fb449aa62e49eaba8ff1c083478747ef9c6a1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcOriginId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginVpcOriginConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginVpcOriginConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginVpcOriginConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c2c1dd133cb61a45b94400f40e4adbf170cbef65ce645f99e7885301ac0a02b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionRestrictions",
    jsii_struct_bases=[],
    name_mapping={"geo_restriction": "geoRestriction"},
)
class CloudfrontMultitenantDistributionRestrictions:
    def __init__(
        self,
        *,
        geo_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionRestrictionsGeoRestriction", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param geo_restriction: geo_restriction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#geo_restriction CloudfrontMultitenantDistribution#geo_restriction}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73e805cf2123df54576db4e3a2865f7a48420eab0a694dd09bdd8f0772f78b3f)
            check_type(argname="argument geo_restriction", value=geo_restriction, expected_type=type_hints["geo_restriction"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if geo_restriction is not None:
            self._values["geo_restriction"] = geo_restriction

    @builtins.property
    def geo_restriction(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionRestrictionsGeoRestriction"]]]:
        '''geo_restriction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#geo_restriction CloudfrontMultitenantDistribution#geo_restriction}
        '''
        result = self._values.get("geo_restriction")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionRestrictionsGeoRestriction"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionRestrictions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionRestrictionsGeoRestriction",
    jsii_struct_bases=[],
    name_mapping={"restriction_type": "restrictionType", "items": "items"},
)
class CloudfrontMultitenantDistributionRestrictionsGeoRestriction:
    def __init__(
        self,
        *,
        restriction_type: builtins.str,
        items: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param restriction_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#restriction_type CloudfrontMultitenantDistribution#restriction_type}.
        :param items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#items CloudfrontMultitenantDistribution#items}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d67f10f2eed2a04aa33fbd2ff812699a400a40b2f0bb0fa8ad9e6e2680bb43f)
            check_type(argname="argument restriction_type", value=restriction_type, expected_type=type_hints["restriction_type"])
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "restriction_type": restriction_type,
        }
        if items is not None:
            self._values["items"] = items

    @builtins.property
    def restriction_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#restriction_type CloudfrontMultitenantDistribution#restriction_type}.'''
        result = self._values.get("restriction_type")
        assert result is not None, "Required property 'restriction_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def items(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#items CloudfrontMultitenantDistribution#items}.'''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionRestrictionsGeoRestriction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionRestrictionsGeoRestrictionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionRestrictionsGeoRestrictionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2652fa976f2d817f82376cc0f0ac83f70e28689c0630b4d7b36701061ca22bfb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionRestrictionsGeoRestrictionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51cf7ec6947107b85c08b7a61aea8b120e1928c425ab879e0e7f8e26906d3a76)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionRestrictionsGeoRestrictionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__456cb4ef0eeaba38c2d7b8a84b59a1980727febb3bcd9930b1d6d81b799b50b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f8326890ccdf4b3a6680f4e1a6cbb58c4d0ac154a6d642da97f462ead345eb6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__261139e892797d4e02e2f0d7ecded6633a98c7be86b24fc0d13a91f37be42169)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionRestrictionsGeoRestriction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionRestrictionsGeoRestriction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionRestrictionsGeoRestriction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0a6b0c0524f615bc7b52344bc8435926cf6ba80864c569cd875f011e8e59b96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionRestrictionsGeoRestrictionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionRestrictionsGeoRestrictionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__832e2b47cdf92ccee0542ba7bf69b2921b492bde38440dda225650de8568e730)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetItems")
    def reset_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItems", []))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictionTypeInput")
    def restriction_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "restrictionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "items"))

    @items.setter
    def items(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604ace424e90c0caf1cc35550f009366cb1ca86a71c53132a5b46a943cae273f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "items", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restrictionType")
    def restriction_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "restrictionType"))

    @restriction_type.setter
    def restriction_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caaac8a49385a1ac0529a9fb5ce703e7acae94a050a9b02d2108b03b296b6591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restrictionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionRestrictionsGeoRestriction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionRestrictionsGeoRestriction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionRestrictionsGeoRestriction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c6d9b88dbf4c85f9a373939ad0e16dd39a517df4e1d5c58a97f0bf33affd40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionRestrictionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionRestrictionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2e9b697b5c820c5c977b968b40182e85eee0ed9d394ee8b279a50744a44d57a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionRestrictionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__258f47c773986937ec30275fe745dfdb6c3ba4f7ff2c78b30f056862f7a6ef6b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionRestrictionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__871c8b93e8c54a55b8922392b74fdcb2617dd28dd229fc5241c88ed1d674258f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c109802f9259f8ab5aa07d7240649bb0ce90842ae05a927a239f098f8087c17)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6ac21aae8e7e6108e9d231139c02e49f2d521ae3994a5f1f8a5f10848c6cc21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionRestrictions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionRestrictions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionRestrictions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6858cc252ca50f428aee3262ef528c4e72f8c08be9dc233c8afeb93a4a9fc234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionRestrictionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionRestrictionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0d0315c7ea626bc86c9a30b3d15a8dedb9cb0dda9759a38a90d0d0580d6b9f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putGeoRestriction")
    def put_geo_restriction(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionRestrictionsGeoRestriction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d23ebc025ae9e21a7644a8ee26ea150df52b0c3f4fd15ed5fb541b0c93e1da1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGeoRestriction", [value]))

    @jsii.member(jsii_name="resetGeoRestriction")
    def reset_geo_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeoRestriction", []))

    @builtins.property
    @jsii.member(jsii_name="geoRestriction")
    def geo_restriction(
        self,
    ) -> CloudfrontMultitenantDistributionRestrictionsGeoRestrictionList:
        return typing.cast(CloudfrontMultitenantDistributionRestrictionsGeoRestrictionList, jsii.get(self, "geoRestriction"))

    @builtins.property
    @jsii.member(jsii_name="geoRestrictionInput")
    def geo_restriction_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionRestrictionsGeoRestriction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionRestrictionsGeoRestriction]]], jsii.get(self, "geoRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionRestrictions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionRestrictions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionRestrictions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3887420a8e60e9e4c989d5727ef5b1e28dadea1f6bab226cdfecd65b5b8e6e47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionTenantConfig",
    jsii_struct_bases=[],
    name_mapping={"parameter_definition": "parameterDefinition"},
)
class CloudfrontMultitenantDistributionTenantConfig:
    def __init__(
        self,
        *,
        parameter_definition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionTenantConfigParameterDefinition", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param parameter_definition: parameter_definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#parameter_definition CloudfrontMultitenantDistribution#parameter_definition}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8a0a05736b832322d0765252c08c2c31173bad7f93a780ae4580c8ff6609208)
            check_type(argname="argument parameter_definition", value=parameter_definition, expected_type=type_hints["parameter_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if parameter_definition is not None:
            self._values["parameter_definition"] = parameter_definition

    @builtins.property
    def parameter_definition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionTenantConfigParameterDefinition"]]]:
        '''parameter_definition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#parameter_definition CloudfrontMultitenantDistribution#parameter_definition}
        '''
        result = self._values.get("parameter_definition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionTenantConfigParameterDefinition"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionTenantConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionTenantConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionTenantConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__512527fba0ba4d34060f116a3f09b9fa375d8b9a8e10cc06d26de9dd4b20930f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionTenantConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c010d670111134ad977e15cedba25f77f1283bfaf16ab5908f9226535bb9903)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionTenantConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad2942f4d02ae5e04f2c9c9d013e200b3c4341e3e851c50ffe805f3819676433)
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
            type_hints = typing.get_type_hints(_typecheckingstub__520123ab16f573cad2c1598483cc28ff0a8807856d20ca04db36fadfc73ab40b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2352cd7a499ab1febbd3fc5b8fdf9d13706be2c76437019b27853434ecf9c7c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionTenantConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionTenantConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionTenantConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac801acf6ed24df6fc6a094ab0d06ac7616a30421e91538dfc7f053caf07ee33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionTenantConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionTenantConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5dc19f2dd64659f5ab53e42d1dc808ece1019c18672281250d05120f3950bf8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putParameterDefinition")
    def put_parameter_definition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionTenantConfigParameterDefinition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f25bbcd36fd43450c926b5bc345170ea6a3a9d3c88a042f76b99f4dbb8a63d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParameterDefinition", [value]))

    @jsii.member(jsii_name="resetParameterDefinition")
    def reset_parameter_definition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameterDefinition", []))

    @builtins.property
    @jsii.member(jsii_name="parameterDefinition")
    def parameter_definition(
        self,
    ) -> "CloudfrontMultitenantDistributionTenantConfigParameterDefinitionList":
        return typing.cast("CloudfrontMultitenantDistributionTenantConfigParameterDefinitionList", jsii.get(self, "parameterDefinition"))

    @builtins.property
    @jsii.member(jsii_name="parameterDefinitionInput")
    def parameter_definition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionTenantConfigParameterDefinition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionTenantConfigParameterDefinition"]]], jsii.get(self, "parameterDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionTenantConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionTenantConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionTenantConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ba94863fe5df4fc92ab261fbf337bfc21ad434e60762437d13b6ad29030b0ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionTenantConfigParameterDefinition",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "definition": "definition"},
)
class CloudfrontMultitenantDistributionTenantConfigParameterDefinition:
    def __init__(
        self,
        *,
        name: builtins.str,
        definition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinition", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#name CloudfrontMultitenantDistribution#name}.
        :param definition: definition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#definition CloudfrontMultitenantDistribution#definition}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d2a63ac8e26d4799c6c07c6ab0545a67ff5958151520af92381186f40c8434c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if definition is not None:
            self._values["definition"] = definition

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#name CloudfrontMultitenantDistribution#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def definition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinition"]]]:
        '''definition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#definition CloudfrontMultitenantDistribution#definition}
        '''
        result = self._values.get("definition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinition"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionTenantConfigParameterDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinition",
    jsii_struct_bases=[],
    name_mapping={"string_schema": "stringSchema"},
)
class CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinition:
    def __init__(
        self,
        *,
        string_schema: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchema", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param string_schema: string_schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#string_schema CloudfrontMultitenantDistribution#string_schema}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0580f07a9c8763e36d058abf1003c773ec8cbf96a3d558b91ef67bed0f8f51ce)
            check_type(argname="argument string_schema", value=string_schema, expected_type=type_hints["string_schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if string_schema is not None:
            self._values["string_schema"] = string_schema

    @builtins.property
    def string_schema(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchema"]]]:
        '''string_schema block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#string_schema CloudfrontMultitenantDistribution#string_schema}
        '''
        result = self._values.get("string_schema")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchema"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c3c79f8c356c189931c871cc8061b31ceb0a9f3602f354e78a378c812c78ae6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e275faf648462b11de25172a82e37b67127904f9769de91ba57ee633336e267a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8c45c7503820c7394ebd03dbdb745a07a9d170e36c9c0a92e862483d2efd1ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__590647864c12329c56d18f165386be51f8a8137555bfc80b15b3b000a7066fb3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a45a225986e5317b2670e492ce09cf7982ab24cad7a4be8da4e00869382a8bd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa03ce343c0e95636dfa916f7eda2e38ee5c4693cf0e260d993aae85f84b4d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef33ac96a85ff701fbf02590c1571bd30bbd66233f1791562bba0e1a6de20d3d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putStringSchema")
    def put_string_schema(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchema", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__190cd04c9fae75e5c38681a33ec11e7af4c7f99ad34ed1f3b8f98aac8e79f300)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStringSchema", [value]))

    @jsii.member(jsii_name="resetStringSchema")
    def reset_string_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringSchema", []))

    @builtins.property
    @jsii.member(jsii_name="stringSchema")
    def string_schema(
        self,
    ) -> "CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchemaList":
        return typing.cast("CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchemaList", jsii.get(self, "stringSchema"))

    @builtins.property
    @jsii.member(jsii_name="stringSchemaInput")
    def string_schema_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchema"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchema"]]], jsii.get(self, "stringSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80bf103f8ef5138020f99ebc95d1252927caeda31af51bab6be10ff5c8722844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchema",
    jsii_struct_bases=[],
    name_mapping={
        "required": "required",
        "comment": "comment",
        "default_value": "defaultValue",
    },
)
class CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchema:
    def __init__(
        self,
        *,
        required: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        comment: typing.Optional[builtins.str] = None,
        default_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param required: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#required CloudfrontMultitenantDistribution#required}.
        :param comment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#comment CloudfrontMultitenantDistribution#comment}.
        :param default_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#default_value CloudfrontMultitenantDistribution#default_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc09d6bde161e718c695579faf20054ad9c32be288ccc3f76226fee5a5dfca0b)
            check_type(argname="argument required", value=required, expected_type=type_hints["required"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "required": required,
        }
        if comment is not None:
            self._values["comment"] = comment
        if default_value is not None:
            self._values["default_value"] = default_value

    @builtins.property
    def required(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#required CloudfrontMultitenantDistribution#required}.'''
        result = self._values.get("required")
        assert result is not None, "Required property 'required' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#comment CloudfrontMultitenantDistribution#comment}.'''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#default_value CloudfrontMultitenantDistribution#default_value}.'''
        result = self._values.get("default_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchema(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchemaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchemaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98748f0ce75c4639a0638ae1ba19d75a537a5ed27a6ac9167bd778cd6bb87a21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchemaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dca52ec6b5810cab1926d9a6b73a96bf88f3ff1d50e40b25bce8f3cc8a3f752b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchemaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cde6c6fa3d895d3437ebf3c68f9463903ef037a2d5c5c30edd29cd8fad8a84c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2570b20a812134ef38b53cfe0478dff14f58bdb4d2dbca68a1a0ec8dacd24a9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fb789cb88ad5195447b3fb14a1ffe61d5f3b5f730b8eb192f56af6305bbb94f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchema]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchema]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchema]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec19030ded8dc083188f30885a8e2168f08ad8c987e2c922b7b55c9a44c87d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchemaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchemaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2ab4e5a9d6cd6641e4ad5ef8a4da835613fbcefe6e38ecc7cac534cfd0dae51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetDefaultValue")
    def reset_default_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultValue", []))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultValueInput")
    def default_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultValueInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredInput")
    def required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requiredInput"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a90a09a57d82232b9254ea4413e0d99d9ab8300e086d329d4d707030d80f643d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultValue")
    def default_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultValue"))

    @default_value.setter
    def default_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d671131f50f6e8b708c73505ea2d0e5557bf6583fa8aaa38a7d82809358e97ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="required")
    def required(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "required"))

    @required.setter
    def required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1cb45fb08f67e2ec3b13809d23603e40629ad8e4413c0cc9e7226be6f6b1111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchema]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchema]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchema]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3c1734a01d4e99a653996ae0a84fec650af29cf19664db20631746f0d563a3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionTenantConfigParameterDefinitionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionTenantConfigParameterDefinitionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1680172446144085f38d74ab4f61f37c2e5f30ca1723db662ff21ccac91eb4ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionTenantConfigParameterDefinitionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b69aeb832a67378cd821762c4ffff2394d946ee2bf5d6face7cceed035f61ec)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionTenantConfigParameterDefinitionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72204060773affeab624852a3fbb52bea5a7ecc11101b5c2a547b6f24981f6f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abfe5a9d3adba8f40ba240cd7fe1363b87ac08100f70ab1cac79440e9f34a04f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44638099c8b5fbacee71a9fbd0d91898012b7c707efa6634d5401480b3e2c02e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionTenantConfigParameterDefinition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionTenantConfigParameterDefinition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionTenantConfigParameterDefinition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c37da86b00575d3229db0034549c3bd6af91c265335273200fffbff4632d115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionTenantConfigParameterDefinitionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionTenantConfigParameterDefinitionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b49294573be2698256de40e262889eb1a49df5836186973fe07bbe72142c144)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDefinition")
    def put_definition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinition, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12f509dde9ec7fc82170d6724fc7fdc71ef38eec41b33e35600a731fbb4dfaa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDefinition", [value]))

    @jsii.member(jsii_name="resetDefinition")
    def reset_definition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefinition", []))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(
        self,
    ) -> CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionList:
        return typing.cast(CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionList, jsii.get(self, "definition"))

    @builtins.property
    @jsii.member(jsii_name="definitionInput")
    def definition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinition]]], jsii.get(self, "definitionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3b0e95ce82f3f18fb79c2edab58486be4f79497eb3ff6d86d6707e322e64d09c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionTenantConfigParameterDefinition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionTenantConfigParameterDefinition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionTenantConfigParameterDefinition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a77267d3f0ffca1a8c7071a5f6611eb1598b6d5612f969daf8e0468c8270e44e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CloudfrontMultitenantDistributionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#create CloudfrontMultitenantDistribution#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#delete CloudfrontMultitenantDistribution#delete}
        :param update: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#update CloudfrontMultitenantDistribution#update}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2ae6725fbb7625494d9f2d9087ae9c080add22255aa9e09cb9c7b76a0ea432f)
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
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#create CloudfrontMultitenantDistribution#create}
        '''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#delete CloudfrontMultitenantDistribution#delete}
        '''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#update CloudfrontMultitenantDistribution#update}
        '''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82fa67cf536010a57215e428c103c6b75385810e816dcd80c537dc770e2770ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5ea88188a74bac51638fbe330005eeee3ff5ec959212d440de14c0ac22670ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8743927b82db40cd69ad6a980bd4cde6cbb2edbcc2e7ed19620d493a35e629ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce6b14e810a711c9eedd01235978d47b30bbb68eeae43adf26c66e66657eb9f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a32ab14254f274d5767d21315057806db11e742d111f6fb570052c77f7067dc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionViewerCertificate",
    jsii_struct_bases=[],
    name_mapping={
        "acm_certificate_arn": "acmCertificateArn",
        "cloudfront_default_certificate": "cloudfrontDefaultCertificate",
        "minimum_protocol_version": "minimumProtocolVersion",
        "ssl_support_method": "sslSupportMethod",
    },
)
class CloudfrontMultitenantDistributionViewerCertificate:
    def __init__(
        self,
        *,
        acm_certificate_arn: typing.Optional[builtins.str] = None,
        cloudfront_default_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        minimum_protocol_version: typing.Optional[builtins.str] = None,
        ssl_support_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param acm_certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#acm_certificate_arn CloudfrontMultitenantDistribution#acm_certificate_arn}.
        :param cloudfront_default_certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#cloudfront_default_certificate CloudfrontMultitenantDistribution#cloudfront_default_certificate}.
        :param minimum_protocol_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#minimum_protocol_version CloudfrontMultitenantDistribution#minimum_protocol_version}.
        :param ssl_support_method: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#ssl_support_method CloudfrontMultitenantDistribution#ssl_support_method}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a927c9251a8a12b9a06f2960353118a897e8fd16d41d9d6144c9351d7b8bfb9)
            check_type(argname="argument acm_certificate_arn", value=acm_certificate_arn, expected_type=type_hints["acm_certificate_arn"])
            check_type(argname="argument cloudfront_default_certificate", value=cloudfront_default_certificate, expected_type=type_hints["cloudfront_default_certificate"])
            check_type(argname="argument minimum_protocol_version", value=minimum_protocol_version, expected_type=type_hints["minimum_protocol_version"])
            check_type(argname="argument ssl_support_method", value=ssl_support_method, expected_type=type_hints["ssl_support_method"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if acm_certificate_arn is not None:
            self._values["acm_certificate_arn"] = acm_certificate_arn
        if cloudfront_default_certificate is not None:
            self._values["cloudfront_default_certificate"] = cloudfront_default_certificate
        if minimum_protocol_version is not None:
            self._values["minimum_protocol_version"] = minimum_protocol_version
        if ssl_support_method is not None:
            self._values["ssl_support_method"] = ssl_support_method

    @builtins.property
    def acm_certificate_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#acm_certificate_arn CloudfrontMultitenantDistribution#acm_certificate_arn}.'''
        result = self._values.get("acm_certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudfront_default_certificate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#cloudfront_default_certificate CloudfrontMultitenantDistribution#cloudfront_default_certificate}.'''
        result = self._values.get("cloudfront_default_certificate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def minimum_protocol_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#minimum_protocol_version CloudfrontMultitenantDistribution#minimum_protocol_version}.'''
        result = self._values.get("minimum_protocol_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_support_method(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/cloudfront_multitenant_distribution#ssl_support_method CloudfrontMultitenantDistribution#ssl_support_method}.'''
        result = self._values.get("ssl_support_method")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontMultitenantDistributionViewerCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudfrontMultitenantDistributionViewerCertificateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionViewerCertificateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a97a6f434e7c0cd707e1dd8be16c0549f2e141f18f545af7e2aa89a412824a36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudfrontMultitenantDistributionViewerCertificateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332c5ea0193f50cec68bd1f39ce95d18c37db92425beddb4ddeddb55910447aa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudfrontMultitenantDistributionViewerCertificateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a4af56b596f165d046c6c5ad6828fb3734f0549abff281b3f2144ca70d642a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a81303d0d7f98ab9e1d99422c62ec73ade73929a20f150b55154d61ac3c9c40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aec6b61bc9d8177418878a4d9a3ab17dcdb7de9793dfcc2b8d03ea51fb3f2838)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionViewerCertificate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionViewerCertificate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionViewerCertificate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c09d26b01f2293567e91ca6c88e16ffbeed4b978a4f67648cab6c57133e6219)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudfrontMultitenantDistributionViewerCertificateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.cloudfrontMultitenantDistribution.CloudfrontMultitenantDistributionViewerCertificateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e864e6ce822dde0b8fa2235967aba0614332a7b89391dcdd75b17b169c0409c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAcmCertificateArn")
    def reset_acm_certificate_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcmCertificateArn", []))

    @jsii.member(jsii_name="resetCloudfrontDefaultCertificate")
    def reset_cloudfront_default_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudfrontDefaultCertificate", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b72e9fe4e838eaee553bd86a42bd740b65edcb498a9badefffdb49170e814df8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f67b382f538c348a448d614ec2d7563cedfc2ba04def5d69a472b800cb91808)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudfrontDefaultCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumProtocolVersion")
    def minimum_protocol_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumProtocolVersion"))

    @minimum_protocol_version.setter
    def minimum_protocol_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9da220deda426315410ed5f82d30d6ef4c8c029f36ed9b71cf817ef4542df01d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumProtocolVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sslSupportMethod")
    def ssl_support_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sslSupportMethod"))

    @ssl_support_method.setter
    def ssl_support_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d21e29c3ee216690149f8814ec171272fe0dfda54ce73fdf42419c7faa39bf2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sslSupportMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionViewerCertificate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionViewerCertificate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionViewerCertificate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52ee7c5b56f75e1cb20bc6443ec2246f384cc532e697669df15591be27e4525e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudfrontMultitenantDistribution",
    "CloudfrontMultitenantDistributionActiveTrustedKeyGroups",
    "CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItems",
    "CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItemsList",
    "CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItemsOutputReference",
    "CloudfrontMultitenantDistributionActiveTrustedKeyGroupsList",
    "CloudfrontMultitenantDistributionActiveTrustedKeyGroupsOutputReference",
    "CloudfrontMultitenantDistributionCacheBehavior",
    "CloudfrontMultitenantDistributionCacheBehaviorAllowedMethods",
    "CloudfrontMultitenantDistributionCacheBehaviorAllowedMethodsList",
    "CloudfrontMultitenantDistributionCacheBehaviorAllowedMethodsOutputReference",
    "CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociation",
    "CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociationList",
    "CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociationOutputReference",
    "CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociation",
    "CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociationList",
    "CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociationOutputReference",
    "CloudfrontMultitenantDistributionCacheBehaviorList",
    "CloudfrontMultitenantDistributionCacheBehaviorOutputReference",
    "CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroups",
    "CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroupsList",
    "CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroupsOutputReference",
    "CloudfrontMultitenantDistributionConfig",
    "CloudfrontMultitenantDistributionCustomErrorResponse",
    "CloudfrontMultitenantDistributionCustomErrorResponseList",
    "CloudfrontMultitenantDistributionCustomErrorResponseOutputReference",
    "CloudfrontMultitenantDistributionDefaultCacheBehavior",
    "CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethods",
    "CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethodsList",
    "CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethodsOutputReference",
    "CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociation",
    "CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociationList",
    "CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociationOutputReference",
    "CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociation",
    "CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociationList",
    "CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociationOutputReference",
    "CloudfrontMultitenantDistributionDefaultCacheBehaviorList",
    "CloudfrontMultitenantDistributionDefaultCacheBehaviorOutputReference",
    "CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroups",
    "CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroupsList",
    "CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroupsOutputReference",
    "CloudfrontMultitenantDistributionOrigin",
    "CloudfrontMultitenantDistributionOriginCustomHeader",
    "CloudfrontMultitenantDistributionOriginCustomHeaderList",
    "CloudfrontMultitenantDistributionOriginCustomHeaderOutputReference",
    "CloudfrontMultitenantDistributionOriginCustomOriginConfig",
    "CloudfrontMultitenantDistributionOriginCustomOriginConfigList",
    "CloudfrontMultitenantDistributionOriginCustomOriginConfigOutputReference",
    "CloudfrontMultitenantDistributionOriginGroup",
    "CloudfrontMultitenantDistributionOriginGroupFailoverCriteria",
    "CloudfrontMultitenantDistributionOriginGroupFailoverCriteriaList",
    "CloudfrontMultitenantDistributionOriginGroupFailoverCriteriaOutputReference",
    "CloudfrontMultitenantDistributionOriginGroupList",
    "CloudfrontMultitenantDistributionOriginGroupMember",
    "CloudfrontMultitenantDistributionOriginGroupMemberList",
    "CloudfrontMultitenantDistributionOriginGroupMemberOutputReference",
    "CloudfrontMultitenantDistributionOriginGroupOutputReference",
    "CloudfrontMultitenantDistributionOriginList",
    "CloudfrontMultitenantDistributionOriginOriginShield",
    "CloudfrontMultitenantDistributionOriginOriginShieldList",
    "CloudfrontMultitenantDistributionOriginOriginShieldOutputReference",
    "CloudfrontMultitenantDistributionOriginOutputReference",
    "CloudfrontMultitenantDistributionOriginVpcOriginConfig",
    "CloudfrontMultitenantDistributionOriginVpcOriginConfigList",
    "CloudfrontMultitenantDistributionOriginVpcOriginConfigOutputReference",
    "CloudfrontMultitenantDistributionRestrictions",
    "CloudfrontMultitenantDistributionRestrictionsGeoRestriction",
    "CloudfrontMultitenantDistributionRestrictionsGeoRestrictionList",
    "CloudfrontMultitenantDistributionRestrictionsGeoRestrictionOutputReference",
    "CloudfrontMultitenantDistributionRestrictionsList",
    "CloudfrontMultitenantDistributionRestrictionsOutputReference",
    "CloudfrontMultitenantDistributionTenantConfig",
    "CloudfrontMultitenantDistributionTenantConfigList",
    "CloudfrontMultitenantDistributionTenantConfigOutputReference",
    "CloudfrontMultitenantDistributionTenantConfigParameterDefinition",
    "CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinition",
    "CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionList",
    "CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionOutputReference",
    "CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchema",
    "CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchemaList",
    "CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchemaOutputReference",
    "CloudfrontMultitenantDistributionTenantConfigParameterDefinitionList",
    "CloudfrontMultitenantDistributionTenantConfigParameterDefinitionOutputReference",
    "CloudfrontMultitenantDistributionTimeouts",
    "CloudfrontMultitenantDistributionTimeoutsOutputReference",
    "CloudfrontMultitenantDistributionViewerCertificate",
    "CloudfrontMultitenantDistributionViewerCertificateList",
    "CloudfrontMultitenantDistributionViewerCertificateOutputReference",
]

publication.publish()

def _typecheckingstub__e30f44d9a1c3ca9305d2f7bc4fe4f1fe821b016da6055961394bd8c976d4a874(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    comment: builtins.str,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    active_trusted_key_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionActiveTrustedKeyGroups, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cache_behavior: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionCacheBehavior, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_error_response: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionCustomErrorResponse, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_cache_behavior: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionDefaultCacheBehavior, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_root_object: typing.Optional[builtins.str] = None,
    http_version: typing.Optional[builtins.str] = None,
    origin: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOrigin, typing.Dict[builtins.str, typing.Any]]]]] = None,
    origin_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOriginGroup, typing.Dict[builtins.str, typing.Any]]]]] = None,
    restrictions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionRestrictions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tenant_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionTenantConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[CloudfrontMultitenantDistributionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    viewer_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionViewerCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__ba7f52c2fa44ba35415e3002150235d92987d7e13d0f79348dfd707bb2c6009f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe7550b51fcdd3a11a85ec95dcff9d0da4e2094a33135aff9a64e46f836561e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionActiveTrustedKeyGroups, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b126bfb733d27affb0b6db427f12c5db1dfbeeadcab093e73c1334c6289850f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionCacheBehavior, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__272a450852cc1a6ff58be9324f36e7832bb594f6bfea754c123f91a6dd9ba5d6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionCustomErrorResponse, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4dd8467e20f12a93555c493d35743d9a71fd8672ad09b7cbcb1b454d9be5e83(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionDefaultCacheBehavior, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bb062dcfd361d30b2dd3714d1792483db233cd8f3518997efade2e720b844de(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOrigin, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83039afda0b67a8bbae9767872be82c48dac5debbd0b515e21ac89079e6fd81(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOriginGroup, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea68a4f694bd32e0f9ef27ebd0b19e98920d559da2098cbdde9b0c8e048bb563(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionRestrictions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3b7f3523b3be3ce452e701395e79c5919cee6acd783bef44e56e52c337f7ff(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionTenantConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab9e068882796f390d094cdb36f4a7c79de2d5196076ba46b5494d7c80f04e7e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionViewerCertificate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da9135aa3383970b0da397e2efcba31d6649361cdb5c937376655f31eb0123f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b4140340551e069a87011378d0a13153c8a3f406568ac92c36237a916d0f95b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b051485483656642bd375157d6267161695053e1bd529031312d16e4e02c8509(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddf8f590ab104ebb4e3d232401f5bd710d1a98640de714de8583d13808a0ea7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__994e046b35eebd71a9f10937a038d6a13ee1be5d83d77d25a5161292b68d5083(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4ebf20ca8e14b8c61dfdab033eef16db624d361c4ff8bdc51ea2c5280c4b93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__728c2b79de5f2f9b6829de921323891c77f01bbee0c69e13d900f6a0b2fdd695(
    *,
    items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItems, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a91704f59fb5d638b938b40eef7d61004f63870700b809ec52d235453b1ec8d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4763e54509de7e03b4c8f80e163074d3a7771b8e16bbca19dc2caf77cd5010e5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60bcc7435db18426e41d60a224745a0529ba80ddb90128b0425d3230b5db3134(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__647f9e6747adb7de8a60a48ed2165b9c221a04c74904e9c4b4e1de09aa47caac(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf5906f291ad8664ff4a2e73234f3a4df6c5add7ab0c4ed592908d3878191d54(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cc2d2f540107e202cc7cc433cf8660ecc717f7719a93a1b15d55bf84021c9f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItems]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d45fc232ab743326415b923bf7d0dc5cd90a6355faa31113fcfdb138ed74452(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5fc280cbb528e84935bd80e61a8cd92f91dc9dbc4035d1d959912570580ed2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItems]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffff850bab7634b5551d71877f8ccb2df95a0198e263368aa592cdc84f6ac582(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cde858e18dabc21ab1bb74222650f4252eef141196c1add756e097fcdad4619(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f15acf8eee261cc00bc15f7442548f2d8b0bf0f69dd6bc70376835a4291e4b8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08a7c32114134e856dbc714540d41fc7ec54d9956c383f44dc018a520536a1d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d8486910568046eb0557f34c15a709315e5d48d504953e858a03fa04b220333(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363100cbea47cd501cdc676cc16f7f4a17e6e170d6341ed517ad4c2667e907e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionActiveTrustedKeyGroups]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4674536802181acea0804e92b660a177168a7d6c2d1260609db124266f98c09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3052f741c77080b375795909e226f03e38490939794cb1f483d69cf073d24fe(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionActiveTrustedKeyGroupsItems, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54696b762951bfc50012fc3e6aed3d74403d8b967022bf355b683893275acdfd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionActiveTrustedKeyGroups]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c3e119136eabbf910f606f77021b4100f2b3d8f3e3885db392c5bae810ae666(
    *,
    path_pattern: builtins.str,
    target_origin_id: builtins.str,
    viewer_protocol_policy: builtins.str,
    allowed_methods: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionCacheBehaviorAllowedMethods, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cache_policy_id: typing.Optional[builtins.str] = None,
    compress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    field_level_encryption_id: typing.Optional[builtins.str] = None,
    function_association: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lambda_function_association: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]]] = None,
    origin_request_policy_id: typing.Optional[builtins.str] = None,
    realtime_log_config_arn: typing.Optional[builtins.str] = None,
    response_headers_policy_id: typing.Optional[builtins.str] = None,
    trusted_key_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroups, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b0fe6072cd84719d9477a506bc20f3792ed4ae0bed3d4a8acef0d2d8c34cefb(
    *,
    cached_methods: typing.Sequence[builtins.str],
    items: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__547bd74ce4036f6ce60250021a61cf04465e2d72e0f8d57b1644379b3c0057fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a28fcd77334f4c05bee8106679296f5bd8747a9a01c7cdc3799531b9251bb11(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77ff76c85a7bccb29acb00fc61bf33e05d98be8cf04d5eef854b3e12d802dda2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e44cc53d80a666daa54251eff41b7a42c8f42113af81365b57ce6280f671b108(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd1cc7f5390a3dbcd8114d5f59ede15151732345c9c5fc97289063831cf70dc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4337114cff48a718b0a7856d799b21ae99d7f328d2e305600edfb99f30c41c1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorAllowedMethods]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__950743de9ac27a94bdc3ae4410367f39d8e35a9a8a51cc37a6a862d2c4ee6b39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2face7a433e055cf80a11f261d62be7c58a8cb91fc3262b652206856bceffe6e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a9931041364ceab3fd211c02112818928fbd99a42787a52548ded26f57562ba(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32826f4dca97aaeb07de08f25973c2982adfe95723a1c6df34bb82203d19eba1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCacheBehaviorAllowedMethods]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aface80e582dde466ae9dbc74e7fc42be57e799af3ef5b38c68b6c1845f87097(
    *,
    event_type: builtins.str,
    function_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2864d4238a74bdea9388c14a7238b9a6a936aa4b2a65ad8114ec531d2b281beb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3d17287056b8054bc9f7e97e93f0e9d80ed5a23377243846813591f896810d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f49cc596dadf0c6134f9446fce6a46b7acacc4c9c501f375aaf983e6c18c92d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e16d9f6af7916e799c4884f82da4b41d87939fd6d0d6e140ed69e196933727(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39ac320b832efc604adfbd80369704c40a6e611ef9f6eb8f20bb88c31397f893(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e4a452104733a342a061ac08753cf94523a868e3074437d1de8f121ffb4d7f8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociation]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__959b031aefb3e884403f3017ccf4c63afcc58a3e60ec1b5338a2e5a16522d107(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__952582ffad209518d41d40acdd414bb90ffa399f7a1b058d75c33e69ab2438b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca8fe12b72e11a92f335b2d1a8dbaedeab82c93287d545b9847db7a47d99729c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f8c0e3377a2607c4a889b3ee6ee4f97213f0987e2316e81812b9c97d51e491(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociation]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da7c02fb8b1a53139bfef01ef010d384504814c88cb742db244c6f77fd4bee9(
    *,
    event_type: builtins.str,
    lambda_function_arn: builtins.str,
    include_body: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__236b01480ac7fb93e6fdf572cd2c20cf5d3b9c44a94c6c117ab44084ca6acc77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__672d7faf18b277621568845b29e094e92337466051c902c1bec5b973aa10c4cd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228512f25b7f4122afa2a0e290a94ffb2b9b35e0cd4acc3e94e42b00c725ff97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59bed4258dc09eb17b7b79341d19f2dc272e150a4d819d142eee74e8e3584b5d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9613ac74f574da6a1b199b4fff6e546e51d345160ded85815eeca3905c95c7b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d6b21b7e461a15e0bf5ebd1c9e25f15539b779ad944bab6b70fd6c70b4a1965(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociation]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e5764f4e41390d0820d2ebc67893a4d51903d9476f1adf7fd5691e5ec88e00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f745b1f762afc3331898ea12ff2000e9f3e36f6343d82dd4fb4c6e9e2a4e9fc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2844f81b463fc264ae789e0647127fc85dfc9716c8a87c2f52736a85774d071c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f842037517afaf3a35d345b95632a50b43269e34c0622c208d69add1c6370eb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daa88dd39ac1878a6ab915a07503eff8eb3be81e4240cec1ee652499a215c808(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociation]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__386476adae5132ce001294508312708af524ecfbceb81f83ca97d7750d9d3085(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6846cac31d025b3576bfaa159a5cd8e26a9674084688dacd5f6b788453c109b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__940a48eba6e90a4cb8ae81f0f31e13585194c24ee4a87198fe8debeb94ab6e56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c5d8ec311dcb2ec2be2e1736ceb1f8aaa315a58f9673fc479e06e8a37d13bf9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b904b6a45ff5f25e51c1e4d154c2f4132f91ffe31de3002376d006d684af67d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f04641138b2e2bb07cca8dc63cad1d0f1e241b010f47ff63ce84fd442a4e7c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehavior]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37a83464f32add2fca550cd47a6f0c8c1233811b46f80bb8c3c684efb72ad5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3596606a0c2aa17d7c4deb2efb17e76299035408ae11de1755ae8607730b83e5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionCacheBehaviorAllowedMethods, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc6c085f2b94e4211e9307fbc51cd71fc22b99c1f5e63715e3dc915501bf8f75(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionCacheBehaviorFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d41df34232135ecb98cb1201743797673c739fc574642ee828423e25644d58e0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionCacheBehaviorLambdaFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f46c7bbfcba8ccfceee964593051c4aed7957f96c3d201c6720e2c410b7b76fa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroups, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23cd0861886563d9ade5de9159aa8b5e2a833ee4d343ad75e99e4350e189c2a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796063907baa8e8da058ea441c9c814883417b78a4ce51a52d90f4fc9c59dc07(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d310000e673b115fdf57fb2053d6345f19b0872e01c9739020751105c4cff932(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f820bf2c33693fffbecce800c483a62c9812fb628103d3a009dde5a719a4a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41aa9230ad31eb03c210c28f5ab02311bbb5085bc08520f5a42a53afee20c89f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__055b5bb9a46ae8a21cd76c14921207ba48219997a24e750aa2851d055cc74118(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228b84319e0bc0daaf6021c4af52f5c99c2e2223d41e55a190700f90f2935dd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5482ab88102f2161093aca936fa6f13baecaf6798e1959e8922ca6e4a684dab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7471ed99ad0c0d79adae566c2b10ddc993f4e55f75a995253485b3740554ec5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda1e63e5230e0377e2de0c0c437cd5ea391801cb5fc82da1187f96b20d30db9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCacheBehavior]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f0bbe2830fd5bd374e3c169b9fe7e5a66a3d1bf184735f2e04dfa32b7249ca2(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    items: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6fc21f94e4b58228b5af80752baf724496cb8c6aa2b1444d2d601e7401a4809(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86efd4ab4abd40662db0397edf4d8e64bda4a8328fa79183ea12ece71ee0915d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ffc5b0b64b01b3822fd19aced15914e68beba6c6b8bbbff6a8eef1689f354a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c96b91546d5ecc2c44207083f334207be5a904a59ec710a6e779defa1c131c5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e07eb5a808c14c3d4baf440c30be08f0b2da11d898f680d9ae671ff95c5d7f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c277b83e291c678cbf0144486643b70eed55782c51c65d88a9b2973f689bf9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroups]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55364e5120691b19cb8dd855fc6031a7cced771cd1dee63e992512375cce35a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b036c2f5d85ff75f52c9a426a60ca35a42647f4cf64e15569a27233fb506c54e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5100058fe41287cf483656ee59ef79386921cf38bd9a6caf0a3291cea8ed20(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73038b9f71143777589ea4a06a551cbd5d5acbfcd6acc4a37a6cab0fd036ebc1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCacheBehaviorTrustedKeyGroups]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e1d893e03ab4358dc164b3862a31da88907930025a83954fcc1f6eef14b9ca1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    comment: builtins.str,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    active_trusted_key_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionActiveTrustedKeyGroups, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cache_behavior: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionCacheBehavior, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_error_response: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionCustomErrorResponse, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_cache_behavior: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionDefaultCacheBehavior, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_root_object: typing.Optional[builtins.str] = None,
    http_version: typing.Optional[builtins.str] = None,
    origin: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOrigin, typing.Dict[builtins.str, typing.Any]]]]] = None,
    origin_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOriginGroup, typing.Dict[builtins.str, typing.Any]]]]] = None,
    restrictions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionRestrictions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tenant_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionTenantConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[CloudfrontMultitenantDistributionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    viewer_certificate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionViewerCertificate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    web_acl_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed058b937bfc8904d89cbea7b96145544a62170d6f81b64f49d08d9d93611dc6(
    *,
    error_code: jsii.Number,
    error_caching_min_ttl: typing.Optional[jsii.Number] = None,
    response_code: typing.Optional[builtins.str] = None,
    response_page_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af480b1f274d8187b5b311e5a92c9df972bd37f7a5060ea9f458972aa3a0ff08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b140747faf0c03e52612a6d467531fd087f6e597212795dc788300eb6d4790c0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88d8b5de344d2780b71f94bb7b9c243be4d236bd53e46dc9dc378b1d4885a46f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a212b6fba81a118d52703cc7f33bd9ba6e97038df1257482bf25c81892322a49(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__399e5a141d5d381ca86baa1b941fb2c3b0545dba2704b08601a83e129a354313(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a518790f4cc689959628b04ca0f27db5f3d77b83ac64ede8496f5163d9706fe2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionCustomErrorResponse]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71bd16d398ca50893a1a028d1287283e3e648fbc9d12015d8e4d2896d1092f21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cebb4c070181b8516e3a9cca50974b051afd8e9aafe652378e4050663f56a2be(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83859c764f643f373218cdb21482e36f1574c5669424c8f12c09eb0884764ec2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa7df1b4ff69aaca26bf64b12a3f86bc30e8d723c7d375af80d657a176b4225(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef942bb7d241bc2be1cf7fefbc0c7d524f225b20704b91ce07ff12d81de445a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b921df196d33005ceaf8eedc9a1c2910aa882725e17ada0efe4ee92be629ff4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionCustomErrorResponse]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba80b017f01fe7862ca29009c7f9ae179ccdc59de36a6c4a5e8b79ed1dcc21b0(
    *,
    target_origin_id: builtins.str,
    viewer_protocol_policy: builtins.str,
    allowed_methods: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethods, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cache_policy_id: typing.Optional[builtins.str] = None,
    compress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    field_level_encryption_id: typing.Optional[builtins.str] = None,
    function_association: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lambda_function_association: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]]] = None,
    origin_request_policy_id: typing.Optional[builtins.str] = None,
    realtime_log_config_arn: typing.Optional[builtins.str] = None,
    response_headers_policy_id: typing.Optional[builtins.str] = None,
    trusted_key_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroups, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4262c433b52f5306c4c44a1b94067d971c17cb70763f0c09ecc1fdcf1512e038(
    *,
    cached_methods: typing.Sequence[builtins.str],
    items: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6908e3b368431a36e3e13f3eef7dae7f8ccaf5880bc3c16d901f73c03234d9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b669e30d15c2475cc873ae661903220ced5c273929911d4b40df347f0572e6a7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__658882202ac20dff6be7b31c00710b88b366cdf073073b502a30df511105f8fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b764fbe87b0fd17e7e643321bebfff83c022c4349f061524feea0d691c86b05(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd9c49482abb1233cf02511a1326e3ad0b3ea0d5462a22304320f9a4a22aebab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a46a45a87ea1fb4fc864ba99fe8a6b9f7cf8c33923b32cb226e55cc9f84f85d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethods]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3590ac8c0137098cbfb58a65757c070a2468a1463efa66e2cf7a6b804365f438(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae711513d90708e51a5f8f4c7f2b96c9d711253353da34d4735fde1764c2cd0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e3bf4e5e89d6197da66a4a27d851210cc273337efa8dd8461869058ea9736a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66fdf06f32a3e5d14478f2651aae7c151c50da70471ebf54d708389a68564c49(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethods]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df0046aae3c18929131317acc0e19d9d9d88a14f06231b2e01f99b35a36c408b(
    *,
    event_type: builtins.str,
    function_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b56cde9427d1c4087d32356c6b5c4925c067891b2184b9bb8a5c993ce69b289(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa2788b78e058515ffb6e4ef9d7a608498aa339a8c90feca1eb868ea821036e1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf8abc0a1443fe1abcff723bc9d3956446dbe9ddce580b79e22ffc1ae087c4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ddf26ede42ed989b19d4624864ebf217dd632432326827207d63f6f09b20416(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5b76a047300cc587916c9a693d3bc227c4e47f32a0396dda85e7101d6aaf01a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494f0ebfe60a478ce9c9e64042c3afe754eadf2ebf69fb3f40a5f5e8fe4054a3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociation]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a607e222c5bf9895f8e04dfbe459fb6e422187e3f31b300a52521e31195247f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4e9be8df284b5262216f697264cffa518fb30f5acc64257ef92b1a6ed61449(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a130583f67ea31bd0f16673a4fb7ec8d63c7ee0698ae4ca4b3f88bb918615709(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7402a768f27246291f04a968f22e2e2e423862136e10528497a3d8bfb4c1622d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociation]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff02a4e7d00071a283316a4d2676a27c08b6843bc51ab2ca9d63c7185407a2d7(
    *,
    event_type: builtins.str,
    lambda_function_arn: builtins.str,
    include_body: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__426d9ae900cb5db04326fbe4cbf6881f77ecf28b0468c1c3d0eabab6d8950875(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175b0502548413df42c29583d48fe1717155659ad4a08cb59f11912a58f23672(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0877c049fae20c2a603bfe602079a81f14c23f1115c2f556ec654e86454972c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e234979b23c0c2bd0a8d30f32372d055bccec5dcb63b2954e1b57dc2b180a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff83a3e85e2fc6b7850f251376673d8fad303115ac57f45ea8d6994da033ab9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd939dad28ce94ae7db2f03f22ddf307bf35c8f476dc72e8841e6fbb0ee5922d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociation]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca289b3f69489c587cb488bbdcdccb94476e1c51b7ed372575bf9abba40c7719(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a89c91842ad360aecd874cc20cebb5df42c5931590b887709bc74e48c57791(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e81309837781cdc96470a12155a30bdc904230ea72b842aafd612e24a292c874(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ffadaaed8849d99dbbec6c647451af1b5f7abe7c76b509779408731e51284e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d28707361224a103f7116184089457d1869ea908470a6c69689ca969b03b6a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociation]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d307473570d593a7230ad73f6508f0bcf4c8acfb06235460538db8dca4549cbd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1db87a604a88355fca55acbb29ea42ca12a94e7c575c716bde5e338865e9f19(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff96ed9c13659f3c12d81e1a3cb5558dfe6dc0fb39207ea21a5e06457fac58a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__595e0faa5f3e0eafed594da6cef811392381a5b52d4dc6e078e398352f3da966(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4b2d54783ede3a214ab559e80b4f1a6adf2306c30a4b65a5fd9b5a291fb2577(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605f40acdd83e8c9103318d5caed93a754769fbcfdebf99566248d90c4c5ced3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehavior]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138fd1e56db28855120f6586f9e9ff604d2fffa1ac953d0c1203c9e7f355d672(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560cdf10a6d5f8894e95874841fa38882164af20a88e530e7f5b1cccd613619e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionDefaultCacheBehaviorAllowedMethods, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9febd8b9641d16ad68d9a31b52829168bace858bb56548c9262674972dfe2bee(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionDefaultCacheBehaviorFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81fa16a9649801e657748477707bd527d5c5cf2854bd5f132a03d3c99480f9c7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionDefaultCacheBehaviorLambdaFunctionAssociation, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47fe957fd33aa053fa1e31a8ddd6cd8548ae406282b8fa00811d0659506d978(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroups, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88dce4e54c7389317649aa29f5bc2326f7525fa4c11cfe16214b207d3e4bc169(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4463fef4eefe7fd46c042fc847908a6bb1179a928ff0e017c4447c0397d69d9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3991e17df2d764431112cd0c0fa3a9779ac4f3b8b9320544e8a06ecb1ad9f9ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b415718b7d66f08c4a728c478fed0b6d4420c5f589977f4d2856044e5a211707(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f5daf1c81607fd2a01c3540763b219a6b88445860a787ae4bcb4b861292de1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1867de29fa44f1c5f678e44b505cc047b9aa2397b4315beab94943c22017a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75feffbc724f1f1fc83eec3b416abe14d8c395a3161b010c5230f35ad2dff69a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eca0b770100fde4c8294d95ccdb4928ecddce81e476cfd5f7e5cf1c641b3537e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e733a449a93bb929215c7560fdda29a89f027b54eb24f2b2725484e250d247ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionDefaultCacheBehavior]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__108bdbfeb1082e65432d3153ace3194b1accb04a58dbabb24000803a39d8b2be(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    items: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee3d8691ed19c1a14e3e078406741e4d33bcd67123e2b3f33bdd5f87e2c5d94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8505c7ca24428bba115d9ea6c69396edf216e96af74e232e4b08b1e1b1a870d2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a44f99697484e5ed98f6aa4faf97e1703c08c7b94990f516b98cb168b73de73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082fde28f7d927db72197781a03c192d4aeae08c2f9e819a7c85875b36e0ea12(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348cabbb7daac5edc0619206625229e25cdbaf529c5a57dc566622bf3e9c8273(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d27090994e65471a7deeb86f8c087e219ab4111586ed143d03d6967711e2a44(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroups]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__469fe398a5532a159213f9080d95dc89accd0796cd7fff6f2a40f798ae4c176e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca967bb059ba8705d5b509ab65c7a70f477a07974b77c5a930368399e1ee60a7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a1f51692779c674e13ac8d1bda887b35977360215529688da12dc755c13846(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6461d071a83be4bbcf0cc25cd523227a7936b620782f218202988611fd4dfdd1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionDefaultCacheBehaviorTrustedKeyGroups]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e591d622930693b75d6c15b65d2278fdd422c289d2d8389447260a38810caa59(
    *,
    domain_name: builtins.str,
    id: builtins.str,
    connection_attempts: typing.Optional[jsii.Number] = None,
    connection_timeout: typing.Optional[jsii.Number] = None,
    custom_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOriginCustomHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_origin_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOriginCustomOriginConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    origin_access_control_id: typing.Optional[builtins.str] = None,
    origin_path: typing.Optional[builtins.str] = None,
    origin_shield: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOriginOriginShield, typing.Dict[builtins.str, typing.Any]]]]] = None,
    response_completion_timeout: typing.Optional[jsii.Number] = None,
    vpc_origin_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOriginVpcOriginConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d896c83e6297d7b6a2f4882d82250f50d479a950f1b9cce4f078b9967c7ca77c(
    *,
    header_name: builtins.str,
    header_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__925d4fcf29ee4e116c9614779c9f0dd0c3cbe77acbcb994f24a6519342b94e7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9cfb0d71e510597b74f0e671e1df5a37a6476dc77aef01f89a882a75f1aaa86(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bfbae4a1ee55b3f25faa16f48bb7583d1f81c6433776f4374f9cee3db618253(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9423c096861dc0215285b0c8de9e8d007679d894eef6ec5fbe7ed8fafd6df1f1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083d93f74907f0febf1d18a8d42c796c8936368392a3f3036e430422d89fcf66(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7eb861899e67f991a97d9573a7029994b784026c4f0a86f6b5bafcc2046098a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginCustomHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9542e2a8bc7d8259253893e8d732295743e419b95d780056e624dd9a86ae1c96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5a4d054ceabbe47ca068ae918e07ceb296e687389388ea068ac93be77457ea8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f77c0d04899dc8634e3d1014f9f6449a9c6483d3903512bb44e07db29ebc009(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01352dbee700ab3efaea01be47169c071ee5eeda2b335c5b8d3b1c3be084cf7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginCustomHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c981a1dfb6d4571febac01041b53571cbbd69f2abdab446e7c72853e964cf5a(
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

def _typecheckingstub__1384fbcd2b24328726d5a8c9acd8e037e23357c8e84598034a10057d0152ef4a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e297bf71c669fbd5c07ca55a10579fefb67f3fd253894d19e2878a314e83b5c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d8557cbe80acfcf8e9e2791319db85d9a76f6e8c017bdaf5672d1c29a9b20f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f4af8a5f47a0b2c035374b3d238b9e1995ab4b776ffa2c3e40318fae41e1630(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0595e6a49a73b42cc03017749faed98c3d6c8b554c8c1be915696291199b6bd3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0799237a2e25c61869816259fb93a78065c32657a8a7cccf6011231ae767719b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginCustomOriginConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb6a5a8854b940eafaa6a6d7a0b04e5d0df431669a5597e337c569aea59612a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e317e6ba87279005d8728ecb7d8881bd245f3fb8981cea742ab3098056ef66d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73db28fa6ed6b181d6839aeebfede07dbc6d506bdc7fffd26f44266b92b2e7c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6169db21cd1dce6c9df252cfd8b89be333dbf933c0efc6e39428ee4e5f9adf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f0d81b9fae5e33c8e9f278114e442f5ab979ed417dbd88f14c3c816a065834(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4ed62f8817bad9a635cf2abb78605b1f37fa06176283f42a41fbe8c99fa2df7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e238cfe3b6a92f8e0c9adf9778139d863d6d66e3b89300daf952fc16517f7e47(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb5a5bf1a5cc92b1440dd7015fd4731deb1cd60ce27ff50b9a3bdbc667bd0fe1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f51b20fb2f3f8478235472cba93615703b80fd70f94f6876452ad544c8654a2a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginCustomOriginConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba015ae8a46f2d7a01cf7fe644a4011a7691e04aa46332cf18c43e6589b4ea2(
    *,
    origin_id: builtins.str,
    failover_criteria: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOriginGroupFailoverCriteria, typing.Dict[builtins.str, typing.Any]]]]] = None,
    member: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOriginGroupMember, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d1b48752e5b7fe4c9b611c083f7a73b3023a118f7aed6227e47c44530847faa(
    *,
    status_codes: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5504853a07c9dd9252cf6158c48f01a458f4f19d5c0240469939ca22fcabce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931b031cf4e71298aaeb6b6dd3747f3e751f00ba7518b24ef39ab4850988bdce(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e084c2c838d066f0eb087d003ec06a41ad3d903cdb01b217ef2a93c35f8e1cd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6834381b62396266b08a359b280d4cf91c01b1e30baafd1b5128a185df60a65(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e8d312c3a598908e0c8ef606f06164ef60b6d7733a6379818d0075be98340d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df25c54f81e9ec79d096d641eb59e9799d8ec3998f3440c504c1aefc7ea9956b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginGroupFailoverCriteria]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d251ebf73d5009d214d2f9142f2aa75a80da25057872fdfe8e70c944d8a231(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71f5d1b0316dfcdd92d67157d53b2d15b809be4663f60f272c702b43338ba35(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e64efa2b0b0b4d28c7e07d81b0da3d01f81c976b2bbd16d44fbccc124c7f235b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginGroupFailoverCriteria]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03718e7e88ad952c8074b931d823ebf0b3819f4c46ee3fb25395e09f4909d366(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2912e52e4984e5be7ec5f1916ac17dab0e28648caee00ebe0358918475b4ce60(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f60832681f52cf04889174e394ea16e92f060ecf58178daa3d8b78380b6166c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a608c5743c0469f3f60c17f0165ed21c9130153dc0273f0fb51a4d818fee0676(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef54b9b1d970c1813d6a7c187655d16ce53e53aedeafa6b0726759123ca9dd5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aadd53c1aafa57fc4af89e202778cd8b10f572911f1e7822c8d8d506715c3356(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginGroup]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d6604906333885d0d4933e7b96d9dbb88ee73608a5703141ba9632c2be0a35f(
    *,
    origin_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d52a7399c07c7dade02f7a27b97cd5d7a3292ebb4260a2d4fe7a9679428f74(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380a1577281b30095cecd272ea29dbb3e7591706a92128d5625d49e51f95d98b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7796ef2cdd1b5498cd06a0b4d34127b84ce355f62224bf16cbe68a04a0d18e5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acde513b660361c40f6f5f54effcc1773e90ad368a628ec56d52379f2324e6f2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69cc08fe43e63435717da24332d215dee4586ed8ec3d5d2b0c5f9ec1cdb5c410(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306927c6c5e615817249b6bd2be272b6104b92eeb5332bbf4fd68f5e1c43896d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginGroupMember]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0ea096e617d37b03a97862309a291c3e1b2e6225592cf3de073c2eab5970a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c87454742819b9dd925932941bc7b33285da40dd2cfc1b66fe29a9a2df9cdfa1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480c865df71aa44443d17872ee7901147ddb2e5a606bf775d6581f67e61c8ca8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginGroupMember]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9262f82638257a884615fda6275b2c1c18dc6e99c61d91d7a2c6b417c2e363af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b072ced6b848d1250c1ee6c730698c96a974c5a3cdbaa7da1dc87bf755c0779d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOriginGroupFailoverCriteria, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd5d5d71714e9d12073574e5ef90d0dddddf6f2d7e419b79628e17dac1011301(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOriginGroupMember, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__804d304eb6c69f8d98df38ac91e39a61956573037907ec2765544e342e2d5aa6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712008b233aef39c5fd9c8405e3117d9215348a7edb8baf8af9ffb7daa4bedea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginGroup]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a5e643f99b48584dea119505c1bff30cf8be69dc3b16c6c2f1f4ac91993331(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80da6a502d4ac5967534a6f126875c640f8f772e504323f576d4ca9c08b45449(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c01f7c2b8ca5f3b9c007db4db60982248a5d6b5378534c6cfbe63320c15befca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c60ef2dd42f0068da1a68b2731d2e00c7825740f80f52d92c11e5fa318312a9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdcaca763915ccf901b7de856e49398dd9007928d4524b7b320819850b997ac5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2acd3f40a8e8645d930dd41d57035ada5ccba361a3360a48f6b332b689d9a6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOrigin]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89982a5a64dec50b8ba5c3aefd8573a1aa168b1d688981d35a14d435f790d477(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    origin_shield_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__505619c53510232071f20df04c665982e85290fa389e9200878836850bee6f5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783e018bf49b1e77076ec160069edea1862a0107f24871d4b472f6739b3dce42(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38dce2c8e5b3b477e3570f309a26c2b05f6fef87d50972560ba5f88ae2d33413(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79257fe2899dccb77b7713c2d7ccc17ecb92f6feddad17bd039d7d21024d5792(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf6f4e05611b94a96a6c05b3faa04f7965a4a5f70c4b92415e40aff3bd5469af(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b7fc0f4149d473617d628235f977af447875b004fedc14ca31ff375b29762bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginOriginShield]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb39f96f2a0907527c5cc89e09dec9bc89cdd4baf29adf0cc0147dd83241c016(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b78937c45d5a9b5f65f0a78fa684b65c8a66f526a70742bfd15d689b3df496b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e282b7cfd8f9b356e67d0883d325b8788d8b7d101ebdb95e330d17ae7f0011(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374cabcffeca4e88709e9a426e88ba5ded015c660f0cdd6a30a1b8c8e4249413(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginOriginShield]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d3e261b0950b6c3a2d4b470c8020627600f35d2d64be502f0751d35543c72ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__546fc4349a12ac5fad76f3094eb983be9782fc90d39816bfdeecc2e2e7081dbb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOriginCustomHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f662eef87e087fe3041dc7d2a549ddea7d258f3bea8a6f7bed2bd9892db8b3ea(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOriginCustomOriginConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__352444e9ba583e6fe7f5a69afdcb6874b361ff5843d5ca5e84afe228722e1360(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOriginOriginShield, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e83f4379801331ed128dc28b7435d7f445318fded02e110f008a24fa78f50dc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionOriginVpcOriginConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a468f472eb730537295addbc0872270be1e5372c19bcfbe192889bd0e177e5a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3530613fb1ba394b29d7d89703e8c64f506d2e4a0045a0a4fe10397ed7447aa9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be09d521d7db57f856bdc14bf78116d4e1eb26a565852ca2872e3a7dfb15c9fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7720284cf367ce105b25d8381bd065e0c69eea60a7cf63261a05f7718d78482(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__473a88916137e3c945785a3b0259b51a3fa626b3576be503616bb8d7ba661227(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9531237b0e9f15a3e551aa98134a28296f4bd90babed13b623d421ccaf8ad03e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f008f37fd9486416c1cf20b32198205675d6f85bf4082bf302b001f5a708be29(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c5d522d9e914eccd4f2bf86025f85ed5bae50b43bd4cdd2b02f34962034ed6c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOrigin]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ca1c2df8a4aa90786a71625e67a5ea2bbb6ad8189c4fd6b015b6f2cd11aa79(
    *,
    vpc_origin_id: builtins.str,
    origin_keepalive_timeout: typing.Optional[jsii.Number] = None,
    origin_read_timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__439fbbd634a659eb8656647485260205d13e250c7bf6044a3aa6da6768e58bc1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6c662aca5cf64f9266ab2bccb35057faa140611aa8ebd584e23da58bffffdcb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a749f7a1219a448d8d0cb28b59a721a64e69650a4331a8f93eb7fad4be2b57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b80e69ec8df5c8d0aea635e3ab8dfdf4431b9cc2f851289d30143155df8bd737(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb755d545e544985ac99f01955e8b85c331ca020b9afcda7da3b18bcbd9dc702(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__550dbb1337707f3a4cdf281c63492eabd85564a310fb1561a39db09335efd50e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionOriginVpcOriginConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96237ecd22ea3f6f3a08b9865eb6afc2955840e0ad267e40f978f84a2fcf038(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__255d4cc1cba403b3f070760f1a2597649d0741833ddada0b474210442d3baf94(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5802aa2f45ac68ee35a5143ee062c9eba56948f6711e904c7b5600c85757e107(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e78fc3db2f204ea5b6ceaa5369fb449aa62e49eaba8ff1c083478747ef9c6a1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2c1dd133cb61a45b94400f40e4adbf170cbef65ce645f99e7885301ac0a02b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionOriginVpcOriginConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e805cf2123df54576db4e3a2865f7a48420eab0a694dd09bdd8f0772f78b3f(
    *,
    geo_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionRestrictionsGeoRestriction, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d67f10f2eed2a04aa33fbd2ff812699a400a40b2f0bb0fa8ad9e6e2680bb43f(
    *,
    restriction_type: builtins.str,
    items: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2652fa976f2d817f82376cc0f0ac83f70e28689c0630b4d7b36701061ca22bfb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51cf7ec6947107b85c08b7a61aea8b120e1928c425ab879e0e7f8e26906d3a76(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__456cb4ef0eeaba38c2d7b8a84b59a1980727febb3bcd9930b1d6d81b799b50b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8326890ccdf4b3a6680f4e1a6cbb58c4d0ac154a6d642da97f462ead345eb6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__261139e892797d4e02e2f0d7ecded6633a98c7be86b24fc0d13a91f37be42169(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0a6b0c0524f615bc7b52344bc8435926cf6ba80864c569cd875f011e8e59b96(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionRestrictionsGeoRestriction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832e2b47cdf92ccee0542ba7bf69b2921b492bde38440dda225650de8568e730(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604ace424e90c0caf1cc35550f009366cb1ca86a71c53132a5b46a943cae273f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caaac8a49385a1ac0529a9fb5ce703e7acae94a050a9b02d2108b03b296b6591(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c6d9b88dbf4c85f9a373939ad0e16dd39a517df4e1d5c58a97f0bf33affd40(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionRestrictionsGeoRestriction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e9b697b5c820c5c977b968b40182e85eee0ed9d394ee8b279a50744a44d57a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__258f47c773986937ec30275fe745dfdb6c3ba4f7ff2c78b30f056862f7a6ef6b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__871c8b93e8c54a55b8922392b74fdcb2617dd28dd229fc5241c88ed1d674258f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c109802f9259f8ab5aa07d7240649bb0ce90842ae05a927a239f098f8087c17(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ac21aae8e7e6108e9d231139c02e49f2d521ae3994a5f1f8a5f10848c6cc21(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6858cc252ca50f428aee3262ef528c4e72f8c08be9dc233c8afeb93a4a9fc234(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionRestrictions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d0315c7ea626bc86c9a30b3d15a8dedb9cb0dda9759a38a90d0d0580d6b9f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23ebc025ae9e21a7644a8ee26ea150df52b0c3f4fd15ed5fb541b0c93e1da1d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionRestrictionsGeoRestriction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3887420a8e60e9e4c989d5727ef5b1e28dadea1f6bab226cdfecd65b5b8e6e47(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionRestrictions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8a0a05736b832322d0765252c08c2c31173bad7f93a780ae4580c8ff6609208(
    *,
    parameter_definition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionTenantConfigParameterDefinition, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__512527fba0ba4d34060f116a3f09b9fa375d8b9a8e10cc06d26de9dd4b20930f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c010d670111134ad977e15cedba25f77f1283bfaf16ab5908f9226535bb9903(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad2942f4d02ae5e04f2c9c9d013e200b3c4341e3e851c50ffe805f3819676433(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520123ab16f573cad2c1598483cc28ff0a8807856d20ca04db36fadfc73ab40b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2352cd7a499ab1febbd3fc5b8fdf9d13706be2c76437019b27853434ecf9c7c1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac801acf6ed24df6fc6a094ab0d06ac7616a30421e91538dfc7f053caf07ee33(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionTenantConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5dc19f2dd64659f5ab53e42d1dc808ece1019c18672281250d05120f3950bf8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f25bbcd36fd43450c926b5bc345170ea6a3a9d3c88a042f76b99f4dbb8a63d9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionTenantConfigParameterDefinition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba94863fe5df4fc92ab261fbf337bfc21ad434e60762437d13b6ad29030b0ce(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionTenantConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d2a63ac8e26d4799c6c07c6ab0545a67ff5958151520af92381186f40c8434c(
    *,
    name: builtins.str,
    definition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinition, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0580f07a9c8763e36d058abf1003c773ec8cbf96a3d558b91ef67bed0f8f51ce(
    *,
    string_schema: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchema, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c3c79f8c356c189931c871cc8061b31ceb0a9f3602f354e78a378c812c78ae6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e275faf648462b11de25172a82e37b67127904f9769de91ba57ee633336e267a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c45c7503820c7394ebd03dbdb745a07a9d170e36c9c0a92e862483d2efd1ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__590647864c12329c56d18f165386be51f8a8137555bfc80b15b3b000a7066fb3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a45a225986e5317b2670e492ce09cf7982ab24cad7a4be8da4e00869382a8bd1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa03ce343c0e95636dfa916f7eda2e38ee5c4693cf0e260d993aae85f84b4d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef33ac96a85ff701fbf02590c1571bd30bbd66233f1791562bba0e1a6de20d3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__190cd04c9fae75e5c38681a33ec11e7af4c7f99ad34ed1f3b8f98aac8e79f300(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchema, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80bf103f8ef5138020f99ebc95d1252927caeda31af51bab6be10ff5c8722844(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc09d6bde161e718c695579faf20054ad9c32be288ccc3f76226fee5a5dfca0b(
    *,
    required: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    comment: typing.Optional[builtins.str] = None,
    default_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98748f0ce75c4639a0638ae1ba19d75a537a5ed27a6ac9167bd778cd6bb87a21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca52ec6b5810cab1926d9a6b73a96bf88f3ff1d50e40b25bce8f3cc8a3f752b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cde6c6fa3d895d3437ebf3c68f9463903ef037a2d5c5c30edd29cd8fad8a84c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2570b20a812134ef38b53cfe0478dff14f58bdb4d2dbca68a1a0ec8dacd24a9a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb789cb88ad5195447b3fb14a1ffe61d5f3b5f730b8eb192f56af6305bbb94f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec19030ded8dc083188f30885a8e2168f08ad8c987e2c922b7b55c9a44c87d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchema]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ab4e5a9d6cd6641e4ad5ef8a4da835613fbcefe6e38ecc7cac534cfd0dae51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90a09a57d82232b9254ea4413e0d99d9ab8300e086d329d4d707030d80f643d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d671131f50f6e8b708c73505ea2d0e5557bf6583fa8aaa38a7d82809358e97ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1cb45fb08f67e2ec3b13809d23603e40629ad8e4413c0cc9e7226be6f6b1111(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3c1734a01d4e99a653996ae0a84fec650af29cf19664db20631746f0d563a3c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinitionStringSchema]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1680172446144085f38d74ab4f61f37c2e5f30ca1723db662ff21ccac91eb4ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b69aeb832a67378cd821762c4ffff2394d946ee2bf5d6face7cceed035f61ec(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72204060773affeab624852a3fbb52bea5a7ecc11101b5c2a547b6f24981f6f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abfe5a9d3adba8f40ba240cd7fe1363b87ac08100f70ab1cac79440e9f34a04f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44638099c8b5fbacee71a9fbd0d91898012b7c707efa6634d5401480b3e2c02e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c37da86b00575d3229db0034549c3bd6af91c265335273200fffbff4632d115(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionTenantConfigParameterDefinition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b49294573be2698256de40e262889eb1a49df5836186973fe07bbe72142c144(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12f509dde9ec7fc82170d6724fc7fdc71ef38eec41b33e35600a731fbb4dfaa5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudfrontMultitenantDistributionTenantConfigParameterDefinitionDefinition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0e95ce82f3f18fb79c2edab58486be4f79497eb3ff6d86d6707e322e64d09c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a77267d3f0ffca1a8c7071a5f6611eb1598b6d5612f969daf8e0468c8270e44e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionTenantConfigParameterDefinition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ae6725fbb7625494d9f2d9087ae9c080add22255aa9e09cb9c7b76a0ea432f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82fa67cf536010a57215e428c103c6b75385810e816dcd80c537dc770e2770ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ea88188a74bac51638fbe330005eeee3ff5ec959212d440de14c0ac22670ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8743927b82db40cd69ad6a980bd4cde6cbb2edbcc2e7ed19620d493a35e629ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce6b14e810a711c9eedd01235978d47b30bbb68eeae43adf26c66e66657eb9f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32ab14254f274d5767d21315057806db11e742d111f6fb570052c77f7067dc7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a927c9251a8a12b9a06f2960353118a897e8fd16d41d9d6144c9351d7b8bfb9(
    *,
    acm_certificate_arn: typing.Optional[builtins.str] = None,
    cloudfront_default_certificate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    minimum_protocol_version: typing.Optional[builtins.str] = None,
    ssl_support_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a97a6f434e7c0cd707e1dd8be16c0549f2e141f18f545af7e2aa89a412824a36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332c5ea0193f50cec68bd1f39ce95d18c37db92425beddb4ddeddb55910447aa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a4af56b596f165d046c6c5ad6828fb3734f0549abff281b3f2144ca70d642a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a81303d0d7f98ab9e1d99422c62ec73ade73929a20f150b55154d61ac3c9c40(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec6b61bc9d8177418878a4d9a3ab17dcdb7de9793dfcc2b8d03ea51fb3f2838(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c09d26b01f2293567e91ca6c88e16ffbeed4b978a4f67648cab6c57133e6219(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudfrontMultitenantDistributionViewerCertificate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e864e6ce822dde0b8fa2235967aba0614332a7b89391dcdd75b17b169c0409c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b72e9fe4e838eaee553bd86a42bd740b65edcb498a9badefffdb49170e814df8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f67b382f538c348a448d614ec2d7563cedfc2ba04def5d69a472b800cb91808(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9da220deda426315410ed5f82d30d6ef4c8c029f36ed9b71cf817ef4542df01d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d21e29c3ee216690149f8814ec171272fe0dfda54ce73fdf42419c7faa39bf2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ee7c5b56f75e1cb20bc6443ec2246f384cc532e697669df15591be27e4525e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudfrontMultitenantDistributionViewerCertificate]],
) -> None:
    """Type checking stubs"""
    pass
