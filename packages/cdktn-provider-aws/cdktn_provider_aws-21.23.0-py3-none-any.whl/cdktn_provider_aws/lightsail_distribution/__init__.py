r'''
# `aws_lightsail_distribution`

Refer to the Terraform Registry for docs: [`aws_lightsail_distribution`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution).
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


class LightsailDistribution(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistribution",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution aws_lightsail_distribution}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bundle_id: builtins.str,
        default_cache_behavior: typing.Union["LightsailDistributionDefaultCacheBehavior", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        origin: typing.Union["LightsailDistributionOrigin", typing.Dict[builtins.str, typing.Any]],
        cache_behavior: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LightsailDistributionCacheBehavior", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cache_behavior_settings: typing.Optional[typing.Union["LightsailDistributionCacheBehaviorSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        certificate_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address_type: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["LightsailDistributionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution aws_lightsail_distribution} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bundle_id: The bundle ID to use for the distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#bundle_id LightsailDistribution#bundle_id}
        :param default_cache_behavior: default_cache_behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#default_cache_behavior LightsailDistribution#default_cache_behavior}
        :param name: The name of the distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#name LightsailDistribution#name}
        :param origin: origin block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#origin LightsailDistribution#origin}
        :param cache_behavior: cache_behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#cache_behavior LightsailDistribution#cache_behavior}
        :param cache_behavior_settings: cache_behavior_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#cache_behavior_settings LightsailDistribution#cache_behavior_settings}
        :param certificate_name: The name of the SSL/TLS certificate attached to the distribution, if any. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#certificate_name LightsailDistribution#certificate_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#id LightsailDistribution#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address_type: The IP address type of the distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#ip_address_type LightsailDistribution#ip_address_type}
        :param is_enabled: Indicates whether the distribution is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#is_enabled LightsailDistribution#is_enabled}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#region LightsailDistribution#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#tags LightsailDistribution#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#tags_all LightsailDistribution#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#timeouts LightsailDistribution#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8844245546592794ddc93477787b57d5a9a888d9ca1ef3b52d0bfb1bd2b1f25a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LightsailDistributionConfig(
            bundle_id=bundle_id,
            default_cache_behavior=default_cache_behavior,
            name=name,
            origin=origin,
            cache_behavior=cache_behavior,
            cache_behavior_settings=cache_behavior_settings,
            certificate_name=certificate_name,
            id=id,
            ip_address_type=ip_address_type,
            is_enabled=is_enabled,
            region=region,
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
        '''Generates CDKTF code for importing a LightsailDistribution resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LightsailDistribution to import.
        :param import_from_id: The id of the existing LightsailDistribution that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LightsailDistribution to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__408de95cf5fc5935117a7c8184113c9daf7e507c545c1493f98f49f3536e024e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCacheBehavior")
    def put_cache_behavior(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LightsailDistributionCacheBehavior", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e7ff6ca8e50be34c5963aec544bc176e8df4363920493c0d964f7b4fbdbf0c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCacheBehavior", [value]))

    @jsii.member(jsii_name="putCacheBehaviorSettings")
    def put_cache_behavior_settings(
        self,
        *,
        allowed_http_methods: typing.Optional[builtins.str] = None,
        cached_http_methods: typing.Optional[builtins.str] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        forwarded_cookies: typing.Optional[typing.Union["LightsailDistributionCacheBehaviorSettingsForwardedCookies", typing.Dict[builtins.str, typing.Any]]] = None,
        forwarded_headers: typing.Optional[typing.Union["LightsailDistributionCacheBehaviorSettingsForwardedHeaders", typing.Dict[builtins.str, typing.Any]]] = None,
        forwarded_query_strings: typing.Optional[typing.Union["LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_ttl: typing.Optional[jsii.Number] = None,
        minimum_ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allowed_http_methods: The HTTP methods that are processed and forwarded to the distribution's origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#allowed_http_methods LightsailDistribution#allowed_http_methods}
        :param cached_http_methods: The HTTP method responses that are cached by your distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#cached_http_methods LightsailDistribution#cached_http_methods}
        :param default_ttl: The default amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the content has been updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#default_ttl LightsailDistribution#default_ttl}
        :param forwarded_cookies: forwarded_cookies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#forwarded_cookies LightsailDistribution#forwarded_cookies}
        :param forwarded_headers: forwarded_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#forwarded_headers LightsailDistribution#forwarded_headers}
        :param forwarded_query_strings: forwarded_query_strings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#forwarded_query_strings LightsailDistribution#forwarded_query_strings}
        :param maximum_ttl: The maximum amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the object has been updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#maximum_ttl LightsailDistribution#maximum_ttl}
        :param minimum_ttl: The minimum amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the object has been updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#minimum_ttl LightsailDistribution#minimum_ttl}
        '''
        value = LightsailDistributionCacheBehaviorSettings(
            allowed_http_methods=allowed_http_methods,
            cached_http_methods=cached_http_methods,
            default_ttl=default_ttl,
            forwarded_cookies=forwarded_cookies,
            forwarded_headers=forwarded_headers,
            forwarded_query_strings=forwarded_query_strings,
            maximum_ttl=maximum_ttl,
            minimum_ttl=minimum_ttl,
        )

        return typing.cast(None, jsii.invoke(self, "putCacheBehaviorSettings", [value]))

    @jsii.member(jsii_name="putDefaultCacheBehavior")
    def put_default_cache_behavior(self, *, behavior: builtins.str) -> None:
        '''
        :param behavior: The cache behavior of the distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#behavior LightsailDistribution#behavior}
        '''
        value = LightsailDistributionDefaultCacheBehavior(behavior=behavior)

        return typing.cast(None, jsii.invoke(self, "putDefaultCacheBehavior", [value]))

    @jsii.member(jsii_name="putOrigin")
    def put_origin(
        self,
        *,
        name: builtins.str,
        region_name: builtins.str,
        protocol_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the origin resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#name LightsailDistribution#name}
        :param region_name: The AWS Region name of the origin resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#region_name LightsailDistribution#region_name}
        :param protocol_policy: The protocol that your Amazon Lightsail distribution uses when establishing a connection with your origin to pull content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#protocol_policy LightsailDistribution#protocol_policy}
        '''
        value = LightsailDistributionOrigin(
            name=name, region_name=region_name, protocol_policy=protocol_policy
        )

        return typing.cast(None, jsii.invoke(self, "putOrigin", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#create LightsailDistribution#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#delete LightsailDistribution#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#update LightsailDistribution#update}.
        '''
        value = LightsailDistributionTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCacheBehavior")
    def reset_cache_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheBehavior", []))

    @jsii.member(jsii_name="resetCacheBehaviorSettings")
    def reset_cache_behavior_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheBehaviorSettings", []))

    @jsii.member(jsii_name="resetCertificateName")
    def reset_certificate_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpAddressType")
    def reset_ip_address_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddressType", []))

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="alternativeDomainNames")
    def alternative_domain_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "alternativeDomainNames"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="cacheBehavior")
    def cache_behavior(self) -> "LightsailDistributionCacheBehaviorList":
        return typing.cast("LightsailDistributionCacheBehaviorList", jsii.get(self, "cacheBehavior"))

    @builtins.property
    @jsii.member(jsii_name="cacheBehaviorSettings")
    def cache_behavior_settings(
        self,
    ) -> "LightsailDistributionCacheBehaviorSettingsOutputReference":
        return typing.cast("LightsailDistributionCacheBehaviorSettingsOutputReference", jsii.get(self, "cacheBehaviorSettings"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="defaultCacheBehavior")
    def default_cache_behavior(
        self,
    ) -> "LightsailDistributionDefaultCacheBehaviorOutputReference":
        return typing.cast("LightsailDistributionDefaultCacheBehaviorOutputReference", jsii.get(self, "defaultCacheBehavior"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> "LightsailDistributionLocationList":
        return typing.cast("LightsailDistributionLocationList", jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="origin")
    def origin(self) -> "LightsailDistributionOriginOutputReference":
        return typing.cast("LightsailDistributionOriginOutputReference", jsii.get(self, "origin"))

    @builtins.property
    @jsii.member(jsii_name="originPublicDns")
    def origin_public_dns(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originPublicDns"))

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="supportCode")
    def support_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportCode"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "LightsailDistributionTimeoutsOutputReference":
        return typing.cast("LightsailDistributionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="bundleIdInput")
    def bundle_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bundleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheBehaviorInput")
    def cache_behavior_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LightsailDistributionCacheBehavior"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LightsailDistributionCacheBehavior"]]], jsii.get(self, "cacheBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheBehaviorSettingsInput")
    def cache_behavior_settings_input(
        self,
    ) -> typing.Optional["LightsailDistributionCacheBehaviorSettings"]:
        return typing.cast(typing.Optional["LightsailDistributionCacheBehaviorSettings"], jsii.get(self, "cacheBehaviorSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateNameInput")
    def certificate_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateNameInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultCacheBehaviorInput")
    def default_cache_behavior_input(
        self,
    ) -> typing.Optional["LightsailDistributionDefaultCacheBehavior"]:
        return typing.cast(typing.Optional["LightsailDistributionDefaultCacheBehavior"], jsii.get(self, "defaultCacheBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressTypeInput")
    def ip_address_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="originInput")
    def origin_input(self) -> typing.Optional["LightsailDistributionOrigin"]:
        return typing.cast(typing.Optional["LightsailDistributionOrigin"], jsii.get(self, "originInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LightsailDistributionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LightsailDistributionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="bundleId")
    def bundle_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bundleId"))

    @bundle_id.setter
    def bundle_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2cc1c1228778c23a699ec0a0ced53b5279c6fcae202936bcde54f84e586eaef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bundleId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificateName")
    def certificate_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateName"))

    @certificate_name.setter
    def certificate_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54d5d92ebbcb0b2bf24bf1749a93f2c1a5892f0d76031b507224dd7f597119cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8440ad39bdc07870d79db6dee64c5c1fca06b6cda810d52d03d28c139a693e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddressType")
    def ip_address_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddressType"))

    @ip_address_type.setter
    def ip_address_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a283fd3d00b7f282ba79cfabd36ccb7da82ef36996e895419c8ffd757c7368f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddressType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cf0490180fc35f7625a3828384c190922be99ca060160c9558d7c3a6af9a914)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb9e4f1a056867988da0d5f75fddc2fc400c0d8e265dae90c277442026b1fe15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cde7fbefec1fc9e9ba337086242b535899e9401b0196851b0820fc171797a36b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c105bbc7b5555640cbc5ad166d5a70bbb065d8d083b2069adb8f708cb1691133)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f23b926523b34f1b0ee97d44601ca1282ad5b405cccefc8f68a6fcbbfc5c4c86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionCacheBehavior",
    jsii_struct_bases=[],
    name_mapping={"behavior": "behavior", "path": "path"},
)
class LightsailDistributionCacheBehavior:
    def __init__(self, *, behavior: builtins.str, path: builtins.str) -> None:
        '''
        :param behavior: The cache behavior for the specified path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#behavior LightsailDistribution#behavior}
        :param path: The path to a directory or file to cached, or not cache. Use an asterisk symbol to specify wildcard directories (path/to/assets/*), and file types (*.html, *jpg, *js). Directories and file paths are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#path LightsailDistribution#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43d695805cdcc83d017fbb4b415183abc26fa8c56ff3d5f35da2d5c7e0cf7dbe)
            check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "behavior": behavior,
            "path": path,
        }

    @builtins.property
    def behavior(self) -> builtins.str:
        '''The cache behavior for the specified path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#behavior LightsailDistribution#behavior}
        '''
        result = self._values.get("behavior")
        assert result is not None, "Required property 'behavior' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The path to a directory or file to cached, or not cache.

        Use an asterisk symbol to specify wildcard directories (path/to/assets/*), and file types (*.html, *jpg, *js). Directories and file paths are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#path LightsailDistribution#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LightsailDistributionCacheBehavior(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LightsailDistributionCacheBehaviorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionCacheBehaviorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b556fb87d5a34cdfc368365b71448238841cc26e29c432e0f44d2e27d212275f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LightsailDistributionCacheBehaviorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__034b44d833aa1954b243c2341531e20c40158ec23bb8637415e2fae0feb4f79f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LightsailDistributionCacheBehaviorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85caf7e6a9f4ab36aba1ea1d1a091b87e5e2984936f28cdbf92cd362f09185fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5f616bcc1f2140b2854929b767a70abf9850843566a2b23d9b2fd892a22b44a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9c31c2fe0465c956a4d44dda8923ed19a6e1e16a0e0be4f8b8a7fa3b691bc9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LightsailDistributionCacheBehavior]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LightsailDistributionCacheBehavior]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LightsailDistributionCacheBehavior]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5826a120aeecb0564de000a951936129d3aa4855bb964910a5fe170e81fa3501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LightsailDistributionCacheBehaviorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionCacheBehaviorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f03856a7426316da9057753b4723886200bd20080fac35b02ee1ccb92031199)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="behaviorInput")
    def behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "behaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="behavior")
    def behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "behavior"))

    @behavior.setter
    def behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c942c43341925fd9bdb381a1d29a5b306ac710f49292e97945fd27ba22b697e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "behavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20d8e4edf0943694178b3c62c14d731d8c15ba6d80d8e95f82dbdf1f94ad80b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LightsailDistributionCacheBehavior]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LightsailDistributionCacheBehavior]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LightsailDistributionCacheBehavior]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d8d9c933c2034b2fe852f968736b68ad10336b18fa5d731be4446b5727cf1a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionCacheBehaviorSettings",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_http_methods": "allowedHttpMethods",
        "cached_http_methods": "cachedHttpMethods",
        "default_ttl": "defaultTtl",
        "forwarded_cookies": "forwardedCookies",
        "forwarded_headers": "forwardedHeaders",
        "forwarded_query_strings": "forwardedQueryStrings",
        "maximum_ttl": "maximumTtl",
        "minimum_ttl": "minimumTtl",
    },
)
class LightsailDistributionCacheBehaviorSettings:
    def __init__(
        self,
        *,
        allowed_http_methods: typing.Optional[builtins.str] = None,
        cached_http_methods: typing.Optional[builtins.str] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        forwarded_cookies: typing.Optional[typing.Union["LightsailDistributionCacheBehaviorSettingsForwardedCookies", typing.Dict[builtins.str, typing.Any]]] = None,
        forwarded_headers: typing.Optional[typing.Union["LightsailDistributionCacheBehaviorSettingsForwardedHeaders", typing.Dict[builtins.str, typing.Any]]] = None,
        forwarded_query_strings: typing.Optional[typing.Union["LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_ttl: typing.Optional[jsii.Number] = None,
        minimum_ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param allowed_http_methods: The HTTP methods that are processed and forwarded to the distribution's origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#allowed_http_methods LightsailDistribution#allowed_http_methods}
        :param cached_http_methods: The HTTP method responses that are cached by your distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#cached_http_methods LightsailDistribution#cached_http_methods}
        :param default_ttl: The default amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the content has been updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#default_ttl LightsailDistribution#default_ttl}
        :param forwarded_cookies: forwarded_cookies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#forwarded_cookies LightsailDistribution#forwarded_cookies}
        :param forwarded_headers: forwarded_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#forwarded_headers LightsailDistribution#forwarded_headers}
        :param forwarded_query_strings: forwarded_query_strings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#forwarded_query_strings LightsailDistribution#forwarded_query_strings}
        :param maximum_ttl: The maximum amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the object has been updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#maximum_ttl LightsailDistribution#maximum_ttl}
        :param minimum_ttl: The minimum amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the object has been updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#minimum_ttl LightsailDistribution#minimum_ttl}
        '''
        if isinstance(forwarded_cookies, dict):
            forwarded_cookies = LightsailDistributionCacheBehaviorSettingsForwardedCookies(**forwarded_cookies)
        if isinstance(forwarded_headers, dict):
            forwarded_headers = LightsailDistributionCacheBehaviorSettingsForwardedHeaders(**forwarded_headers)
        if isinstance(forwarded_query_strings, dict):
            forwarded_query_strings = LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings(**forwarded_query_strings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__853b7ceb68e075211cd3c83e94db75028f64181703c41ea5ccf54388c89b2300)
            check_type(argname="argument allowed_http_methods", value=allowed_http_methods, expected_type=type_hints["allowed_http_methods"])
            check_type(argname="argument cached_http_methods", value=cached_http_methods, expected_type=type_hints["cached_http_methods"])
            check_type(argname="argument default_ttl", value=default_ttl, expected_type=type_hints["default_ttl"])
            check_type(argname="argument forwarded_cookies", value=forwarded_cookies, expected_type=type_hints["forwarded_cookies"])
            check_type(argname="argument forwarded_headers", value=forwarded_headers, expected_type=type_hints["forwarded_headers"])
            check_type(argname="argument forwarded_query_strings", value=forwarded_query_strings, expected_type=type_hints["forwarded_query_strings"])
            check_type(argname="argument maximum_ttl", value=maximum_ttl, expected_type=type_hints["maximum_ttl"])
            check_type(argname="argument minimum_ttl", value=minimum_ttl, expected_type=type_hints["minimum_ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_http_methods is not None:
            self._values["allowed_http_methods"] = allowed_http_methods
        if cached_http_methods is not None:
            self._values["cached_http_methods"] = cached_http_methods
        if default_ttl is not None:
            self._values["default_ttl"] = default_ttl
        if forwarded_cookies is not None:
            self._values["forwarded_cookies"] = forwarded_cookies
        if forwarded_headers is not None:
            self._values["forwarded_headers"] = forwarded_headers
        if forwarded_query_strings is not None:
            self._values["forwarded_query_strings"] = forwarded_query_strings
        if maximum_ttl is not None:
            self._values["maximum_ttl"] = maximum_ttl
        if minimum_ttl is not None:
            self._values["minimum_ttl"] = minimum_ttl

    @builtins.property
    def allowed_http_methods(self) -> typing.Optional[builtins.str]:
        '''The HTTP methods that are processed and forwarded to the distribution's origin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#allowed_http_methods LightsailDistribution#allowed_http_methods}
        '''
        result = self._values.get("allowed_http_methods")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cached_http_methods(self) -> typing.Optional[builtins.str]:
        '''The HTTP method responses that are cached by your distribution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#cached_http_methods LightsailDistribution#cached_http_methods}
        '''
        result = self._values.get("cached_http_methods")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_ttl(self) -> typing.Optional[jsii.Number]:
        '''The default amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the content has been updated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#default_ttl LightsailDistribution#default_ttl}
        '''
        result = self._values.get("default_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def forwarded_cookies(
        self,
    ) -> typing.Optional["LightsailDistributionCacheBehaviorSettingsForwardedCookies"]:
        '''forwarded_cookies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#forwarded_cookies LightsailDistribution#forwarded_cookies}
        '''
        result = self._values.get("forwarded_cookies")
        return typing.cast(typing.Optional["LightsailDistributionCacheBehaviorSettingsForwardedCookies"], result)

    @builtins.property
    def forwarded_headers(
        self,
    ) -> typing.Optional["LightsailDistributionCacheBehaviorSettingsForwardedHeaders"]:
        '''forwarded_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#forwarded_headers LightsailDistribution#forwarded_headers}
        '''
        result = self._values.get("forwarded_headers")
        return typing.cast(typing.Optional["LightsailDistributionCacheBehaviorSettingsForwardedHeaders"], result)

    @builtins.property
    def forwarded_query_strings(
        self,
    ) -> typing.Optional["LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings"]:
        '''forwarded_query_strings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#forwarded_query_strings LightsailDistribution#forwarded_query_strings}
        '''
        result = self._values.get("forwarded_query_strings")
        return typing.cast(typing.Optional["LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings"], result)

    @builtins.property
    def maximum_ttl(self) -> typing.Optional[jsii.Number]:
        '''The maximum amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the object has been updated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#maximum_ttl LightsailDistribution#maximum_ttl}
        '''
        result = self._values.get("maximum_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum_ttl(self) -> typing.Optional[jsii.Number]:
        '''The minimum amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the object has been updated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#minimum_ttl LightsailDistribution#minimum_ttl}
        '''
        result = self._values.get("minimum_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LightsailDistributionCacheBehaviorSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionCacheBehaviorSettingsForwardedCookies",
    jsii_struct_bases=[],
    name_mapping={"cookies_allow_list": "cookiesAllowList", "option": "option"},
)
class LightsailDistributionCacheBehaviorSettingsForwardedCookies:
    def __init__(
        self,
        *,
        cookies_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        option: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cookies_allow_list: The specific cookies to forward to your distribution's origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#cookies_allow_list LightsailDistribution#cookies_allow_list}
        :param option: Specifies which cookies to forward to the distribution's origin for a cache behavior: all, none, or allow-list to forward only the cookies specified in the cookiesAllowList parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#option LightsailDistribution#option}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be7e7557ead35b552d5b914339d8d74fe01e99ebd9d4a90ea9a2aedb4dfd6c29)
            check_type(argname="argument cookies_allow_list", value=cookies_allow_list, expected_type=type_hints["cookies_allow_list"])
            check_type(argname="argument option", value=option, expected_type=type_hints["option"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cookies_allow_list is not None:
            self._values["cookies_allow_list"] = cookies_allow_list
        if option is not None:
            self._values["option"] = option

    @builtins.property
    def cookies_allow_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The specific cookies to forward to your distribution's origin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#cookies_allow_list LightsailDistribution#cookies_allow_list}
        '''
        result = self._values.get("cookies_allow_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def option(self) -> typing.Optional[builtins.str]:
        '''Specifies which cookies to forward to the distribution's origin for a cache behavior: all, none, or allow-list to forward only the cookies specified in the cookiesAllowList parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#option LightsailDistribution#option}
        '''
        result = self._values.get("option")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LightsailDistributionCacheBehaviorSettingsForwardedCookies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LightsailDistributionCacheBehaviorSettingsForwardedCookiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionCacheBehaviorSettingsForwardedCookiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ae0a2b8b9845156922d36b603283c1fdae841a0df907358eba77e0a3f8f86ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCookiesAllowList")
    def reset_cookies_allow_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCookiesAllowList", []))

    @jsii.member(jsii_name="resetOption")
    def reset_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOption", []))

    @builtins.property
    @jsii.member(jsii_name="cookiesAllowListInput")
    def cookies_allow_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cookiesAllowListInput"))

    @builtins.property
    @jsii.member(jsii_name="optionInput")
    def option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "optionInput"))

    @builtins.property
    @jsii.member(jsii_name="cookiesAllowList")
    def cookies_allow_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cookiesAllowList"))

    @cookies_allow_list.setter
    def cookies_allow_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e04b2d2a9ad6bfccf594836c1805741a7a0e13eb849926d875e4c57d1c901fbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cookiesAllowList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="option")
    def option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "option"))

    @option.setter
    def option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8b389677fca924ebc44ac6aa05561f058ef67b8b180bbd8f7f5183274cc9f01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "option", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedCookies]:
        return typing.cast(typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedCookies], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedCookies],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab09da520d5db7ad67721d60445c245f5374354a8001c8d3771344f3ea742b0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionCacheBehaviorSettingsForwardedHeaders",
    jsii_struct_bases=[],
    name_mapping={"headers_allow_list": "headersAllowList", "option": "option"},
)
class LightsailDistributionCacheBehaviorSettingsForwardedHeaders:
    def __init__(
        self,
        *,
        headers_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        option: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param headers_allow_list: The specific headers to forward to your distribution's origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#headers_allow_list LightsailDistribution#headers_allow_list}
        :param option: The headers that you want your distribution to forward to your origin and base caching on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#option LightsailDistribution#option}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28fc52b1b9e10afe6116273afca41cf47e1c98d4f0be4d4773f84aa5cca68297)
            check_type(argname="argument headers_allow_list", value=headers_allow_list, expected_type=type_hints["headers_allow_list"])
            check_type(argname="argument option", value=option, expected_type=type_hints["option"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if headers_allow_list is not None:
            self._values["headers_allow_list"] = headers_allow_list
        if option is not None:
            self._values["option"] = option

    @builtins.property
    def headers_allow_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The specific headers to forward to your distribution's origin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#headers_allow_list LightsailDistribution#headers_allow_list}
        '''
        result = self._values.get("headers_allow_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def option(self) -> typing.Optional[builtins.str]:
        '''The headers that you want your distribution to forward to your origin and base caching on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#option LightsailDistribution#option}
        '''
        result = self._values.get("option")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LightsailDistributionCacheBehaviorSettingsForwardedHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LightsailDistributionCacheBehaviorSettingsForwardedHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionCacheBehaviorSettingsForwardedHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43ec08db1ff140e6ba71fe0c2fb8547143cf4b1792697ee330fa7e7dd99fede2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHeadersAllowList")
    def reset_headers_allow_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeadersAllowList", []))

    @jsii.member(jsii_name="resetOption")
    def reset_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOption", []))

    @builtins.property
    @jsii.member(jsii_name="headersAllowListInput")
    def headers_allow_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "headersAllowListInput"))

    @builtins.property
    @jsii.member(jsii_name="optionInput")
    def option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "optionInput"))

    @builtins.property
    @jsii.member(jsii_name="headersAllowList")
    def headers_allow_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "headersAllowList"))

    @headers_allow_list.setter
    def headers_allow_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7af6fc3ff489a6ae05d8aaab52af2e18455a1fa18c3067c9a209ac1bd63f6671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headersAllowList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="option")
    def option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "option"))

    @option.setter
    def option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d68a075fcbb126bef8b589ee40ede3836b81aa187c3592a5af735a5ffe0ab17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "option", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedHeaders]:
        return typing.cast(typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedHeaders], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedHeaders],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41259f73b6da034aeb5206c706fbd2918bb4ebaa181bf7680bbdb4d58f3e7b37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings",
    jsii_struct_bases=[],
    name_mapping={
        "option": "option",
        "query_strings_allowed_list": "queryStringsAllowedList",
    },
)
class LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings:
    def __init__(
        self,
        *,
        option: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_strings_allowed_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param option: Indicates whether the distribution forwards and caches based on query strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#option LightsailDistribution#option}
        :param query_strings_allowed_list: The specific query strings that the distribution forwards to the origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#query_strings_allowed_list LightsailDistribution#query_strings_allowed_list}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26d60ad731cafb9597f1b28f4472b8b52a01fd3ec1d48c5052133e392345993c)
            check_type(argname="argument option", value=option, expected_type=type_hints["option"])
            check_type(argname="argument query_strings_allowed_list", value=query_strings_allowed_list, expected_type=type_hints["query_strings_allowed_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if option is not None:
            self._values["option"] = option
        if query_strings_allowed_list is not None:
            self._values["query_strings_allowed_list"] = query_strings_allowed_list

    @builtins.property
    def option(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether the distribution forwards and caches based on query strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#option LightsailDistribution#option}
        '''
        result = self._values.get("option")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def query_strings_allowed_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The specific query strings that the distribution forwards to the origin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#query_strings_allowed_list LightsailDistribution#query_strings_allowed_list}
        '''
        result = self._values.get("query_strings_allowed_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LightsailDistributionCacheBehaviorSettingsForwardedQueryStringsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionCacheBehaviorSettingsForwardedQueryStringsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bcd3c3ed872daa29775e3b881f94ba996c059fe0e7f28875f120fe4e9f6a3d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOption")
    def reset_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOption", []))

    @jsii.member(jsii_name="resetQueryStringsAllowedList")
    def reset_query_strings_allowed_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryStringsAllowedList", []))

    @builtins.property
    @jsii.member(jsii_name="optionInput")
    def option_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "optionInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringsAllowedListInput")
    def query_strings_allowed_list_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queryStringsAllowedListInput"))

    @builtins.property
    @jsii.member(jsii_name="option")
    def option(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "option"))

    @option.setter
    def option(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbded2d80f57bea352ab279e306e7d6c6c08154f90a1ca0e77ce6d988366b10e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "option", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryStringsAllowedList")
    def query_strings_allowed_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queryStringsAllowedList"))

    @query_strings_allowed_list.setter
    def query_strings_allowed_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f46bd9510952b08e7cfe5bac1a3aa1604949748e62db17edeb07101a671026d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringsAllowedList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings]:
        return typing.cast(typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abcbcc67f2aedb3f195a62c3aabf941138bfdcb029a6a3ce9178cbf287c98ea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LightsailDistributionCacheBehaviorSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionCacheBehaviorSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ca9163716809ea7975bf474fbdbc57c09b9ebe4c10c03f43b75cc0532b82563)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putForwardedCookies")
    def put_forwarded_cookies(
        self,
        *,
        cookies_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        option: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cookies_allow_list: The specific cookies to forward to your distribution's origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#cookies_allow_list LightsailDistribution#cookies_allow_list}
        :param option: Specifies which cookies to forward to the distribution's origin for a cache behavior: all, none, or allow-list to forward only the cookies specified in the cookiesAllowList parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#option LightsailDistribution#option}
        '''
        value = LightsailDistributionCacheBehaviorSettingsForwardedCookies(
            cookies_allow_list=cookies_allow_list, option=option
        )

        return typing.cast(None, jsii.invoke(self, "putForwardedCookies", [value]))

    @jsii.member(jsii_name="putForwardedHeaders")
    def put_forwarded_headers(
        self,
        *,
        headers_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        option: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param headers_allow_list: The specific headers to forward to your distribution's origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#headers_allow_list LightsailDistribution#headers_allow_list}
        :param option: The headers that you want your distribution to forward to your origin and base caching on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#option LightsailDistribution#option}
        '''
        value = LightsailDistributionCacheBehaviorSettingsForwardedHeaders(
            headers_allow_list=headers_allow_list, option=option
        )

        return typing.cast(None, jsii.invoke(self, "putForwardedHeaders", [value]))

    @jsii.member(jsii_name="putForwardedQueryStrings")
    def put_forwarded_query_strings(
        self,
        *,
        option: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_strings_allowed_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param option: Indicates whether the distribution forwards and caches based on query strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#option LightsailDistribution#option}
        :param query_strings_allowed_list: The specific query strings that the distribution forwards to the origin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#query_strings_allowed_list LightsailDistribution#query_strings_allowed_list}
        '''
        value = LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings(
            option=option, query_strings_allowed_list=query_strings_allowed_list
        )

        return typing.cast(None, jsii.invoke(self, "putForwardedQueryStrings", [value]))

    @jsii.member(jsii_name="resetAllowedHttpMethods")
    def reset_allowed_http_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedHttpMethods", []))

    @jsii.member(jsii_name="resetCachedHttpMethods")
    def reset_cached_http_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCachedHttpMethods", []))

    @jsii.member(jsii_name="resetDefaultTtl")
    def reset_default_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTtl", []))

    @jsii.member(jsii_name="resetForwardedCookies")
    def reset_forwarded_cookies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardedCookies", []))

    @jsii.member(jsii_name="resetForwardedHeaders")
    def reset_forwarded_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardedHeaders", []))

    @jsii.member(jsii_name="resetForwardedQueryStrings")
    def reset_forwarded_query_strings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardedQueryStrings", []))

    @jsii.member(jsii_name="resetMaximumTtl")
    def reset_maximum_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumTtl", []))

    @jsii.member(jsii_name="resetMinimumTtl")
    def reset_minimum_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumTtl", []))

    @builtins.property
    @jsii.member(jsii_name="forwardedCookies")
    def forwarded_cookies(
        self,
    ) -> LightsailDistributionCacheBehaviorSettingsForwardedCookiesOutputReference:
        return typing.cast(LightsailDistributionCacheBehaviorSettingsForwardedCookiesOutputReference, jsii.get(self, "forwardedCookies"))

    @builtins.property
    @jsii.member(jsii_name="forwardedHeaders")
    def forwarded_headers(
        self,
    ) -> LightsailDistributionCacheBehaviorSettingsForwardedHeadersOutputReference:
        return typing.cast(LightsailDistributionCacheBehaviorSettingsForwardedHeadersOutputReference, jsii.get(self, "forwardedHeaders"))

    @builtins.property
    @jsii.member(jsii_name="forwardedQueryStrings")
    def forwarded_query_strings(
        self,
    ) -> LightsailDistributionCacheBehaviorSettingsForwardedQueryStringsOutputReference:
        return typing.cast(LightsailDistributionCacheBehaviorSettingsForwardedQueryStringsOutputReference, jsii.get(self, "forwardedQueryStrings"))

    @builtins.property
    @jsii.member(jsii_name="allowedHttpMethodsInput")
    def allowed_http_methods_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allowedHttpMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="cachedHttpMethodsInput")
    def cached_http_methods_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cachedHttpMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTtlInput")
    def default_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardedCookiesInput")
    def forwarded_cookies_input(
        self,
    ) -> typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedCookies]:
        return typing.cast(typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedCookies], jsii.get(self, "forwardedCookiesInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardedHeadersInput")
    def forwarded_headers_input(
        self,
    ) -> typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedHeaders]:
        return typing.cast(typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedHeaders], jsii.get(self, "forwardedHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardedQueryStringsInput")
    def forwarded_query_strings_input(
        self,
    ) -> typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings]:
        return typing.cast(typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings], jsii.get(self, "forwardedQueryStringsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumTtlInput")
    def maximum_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumTtlInput")
    def minimum_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedHttpMethods")
    def allowed_http_methods(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allowedHttpMethods"))

    @allowed_http_methods.setter
    def allowed_http_methods(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf1082ee6764db7d515ccbe870c16e2868b805d67a1277953e666e167c950e9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedHttpMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cachedHttpMethods")
    def cached_http_methods(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cachedHttpMethods"))

    @cached_http_methods.setter
    def cached_http_methods(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e03b9c539baac10b91f7ea523950d16ed0199f9ca320dd5b966ee19aabf1f6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cachedHttpMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTtl")
    def default_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultTtl"))

    @default_ttl.setter
    def default_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__273a9986beeeadd05275618bda6734158b3926b1f903f8bc234557f29387e8a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumTtl")
    def maximum_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumTtl"))

    @maximum_ttl.setter
    def maximum_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8cedbc66d0cf19dd1ae748f7f0a58527635b06e4f36113efe8d1538079336d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumTtl")
    def minimum_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumTtl"))

    @minimum_ttl.setter
    def minimum_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34595ef6b06d284a48e6c9aa9e7b51a53a7f646db9aeed613fbbd93e872eec04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LightsailDistributionCacheBehaviorSettings]:
        return typing.cast(typing.Optional[LightsailDistributionCacheBehaviorSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LightsailDistributionCacheBehaviorSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a342793e87f0663a9a75da8cb7e5fa91d4b7ccb4114dac93686c4051366ce93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bundle_id": "bundleId",
        "default_cache_behavior": "defaultCacheBehavior",
        "name": "name",
        "origin": "origin",
        "cache_behavior": "cacheBehavior",
        "cache_behavior_settings": "cacheBehaviorSettings",
        "certificate_name": "certificateName",
        "id": "id",
        "ip_address_type": "ipAddressType",
        "is_enabled": "isEnabled",
        "region": "region",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
    },
)
class LightsailDistributionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bundle_id: builtins.str,
        default_cache_behavior: typing.Union["LightsailDistributionDefaultCacheBehavior", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        origin: typing.Union["LightsailDistributionOrigin", typing.Dict[builtins.str, typing.Any]],
        cache_behavior: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LightsailDistributionCacheBehavior, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cache_behavior_settings: typing.Optional[typing.Union[LightsailDistributionCacheBehaviorSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        certificate_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address_type: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["LightsailDistributionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bundle_id: The bundle ID to use for the distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#bundle_id LightsailDistribution#bundle_id}
        :param default_cache_behavior: default_cache_behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#default_cache_behavior LightsailDistribution#default_cache_behavior}
        :param name: The name of the distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#name LightsailDistribution#name}
        :param origin: origin block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#origin LightsailDistribution#origin}
        :param cache_behavior: cache_behavior block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#cache_behavior LightsailDistribution#cache_behavior}
        :param cache_behavior_settings: cache_behavior_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#cache_behavior_settings LightsailDistribution#cache_behavior_settings}
        :param certificate_name: The name of the SSL/TLS certificate attached to the distribution, if any. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#certificate_name LightsailDistribution#certificate_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#id LightsailDistribution#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address_type: The IP address type of the distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#ip_address_type LightsailDistribution#ip_address_type}
        :param is_enabled: Indicates whether the distribution is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#is_enabled LightsailDistribution#is_enabled}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#region LightsailDistribution#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#tags LightsailDistribution#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#tags_all LightsailDistribution#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#timeouts LightsailDistribution#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(default_cache_behavior, dict):
            default_cache_behavior = LightsailDistributionDefaultCacheBehavior(**default_cache_behavior)
        if isinstance(origin, dict):
            origin = LightsailDistributionOrigin(**origin)
        if isinstance(cache_behavior_settings, dict):
            cache_behavior_settings = LightsailDistributionCacheBehaviorSettings(**cache_behavior_settings)
        if isinstance(timeouts, dict):
            timeouts = LightsailDistributionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e026525a56fed82ab68a5fae7e494d7ad3fb9472765f1659a248a2b181dba1d7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument default_cache_behavior", value=default_cache_behavior, expected_type=type_hints["default_cache_behavior"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
            check_type(argname="argument cache_behavior", value=cache_behavior, expected_type=type_hints["cache_behavior"])
            check_type(argname="argument cache_behavior_settings", value=cache_behavior_settings, expected_type=type_hints["cache_behavior_settings"])
            check_type(argname="argument certificate_name", value=certificate_name, expected_type=type_hints["certificate_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bundle_id": bundle_id,
            "default_cache_behavior": default_cache_behavior,
            "name": name,
            "origin": origin,
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
        if cache_behavior is not None:
            self._values["cache_behavior"] = cache_behavior
        if cache_behavior_settings is not None:
            self._values["cache_behavior_settings"] = cache_behavior_settings
        if certificate_name is not None:
            self._values["certificate_name"] = certificate_name
        if id is not None:
            self._values["id"] = id
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if region is not None:
            self._values["region"] = region
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
    def bundle_id(self) -> builtins.str:
        '''The bundle ID to use for the distribution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#bundle_id LightsailDistribution#bundle_id}
        '''
        result = self._values.get("bundle_id")
        assert result is not None, "Required property 'bundle_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_cache_behavior(self) -> "LightsailDistributionDefaultCacheBehavior":
        '''default_cache_behavior block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#default_cache_behavior LightsailDistribution#default_cache_behavior}
        '''
        result = self._values.get("default_cache_behavior")
        assert result is not None, "Required property 'default_cache_behavior' is missing"
        return typing.cast("LightsailDistributionDefaultCacheBehavior", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the distribution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#name LightsailDistribution#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origin(self) -> "LightsailDistributionOrigin":
        '''origin block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#origin LightsailDistribution#origin}
        '''
        result = self._values.get("origin")
        assert result is not None, "Required property 'origin' is missing"
        return typing.cast("LightsailDistributionOrigin", result)

    @builtins.property
    def cache_behavior(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LightsailDistributionCacheBehavior]]]:
        '''cache_behavior block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#cache_behavior LightsailDistribution#cache_behavior}
        '''
        result = self._values.get("cache_behavior")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LightsailDistributionCacheBehavior]]], result)

    @builtins.property
    def cache_behavior_settings(
        self,
    ) -> typing.Optional[LightsailDistributionCacheBehaviorSettings]:
        '''cache_behavior_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#cache_behavior_settings LightsailDistribution#cache_behavior_settings}
        '''
        result = self._values.get("cache_behavior_settings")
        return typing.cast(typing.Optional[LightsailDistributionCacheBehaviorSettings], result)

    @builtins.property
    def certificate_name(self) -> typing.Optional[builtins.str]:
        '''The name of the SSL/TLS certificate attached to the distribution, if any.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#certificate_name LightsailDistribution#certificate_name}
        '''
        result = self._values.get("certificate_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#id LightsailDistribution#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        '''The IP address type of the distribution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#ip_address_type LightsailDistribution#ip_address_type}
        '''
        result = self._values.get("ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether the distribution is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#is_enabled LightsailDistribution#is_enabled}
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#region LightsailDistribution#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#tags LightsailDistribution#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#tags_all LightsailDistribution#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["LightsailDistributionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#timeouts LightsailDistribution#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["LightsailDistributionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LightsailDistributionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionDefaultCacheBehavior",
    jsii_struct_bases=[],
    name_mapping={"behavior": "behavior"},
)
class LightsailDistributionDefaultCacheBehavior:
    def __init__(self, *, behavior: builtins.str) -> None:
        '''
        :param behavior: The cache behavior of the distribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#behavior LightsailDistribution#behavior}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0b8215c3f551820e53c1b34e94780ff662c1b62ef1846565d592ea6dba5ba61)
            check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "behavior": behavior,
        }

    @builtins.property
    def behavior(self) -> builtins.str:
        '''The cache behavior of the distribution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#behavior LightsailDistribution#behavior}
        '''
        result = self._values.get("behavior")
        assert result is not None, "Required property 'behavior' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LightsailDistributionDefaultCacheBehavior(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LightsailDistributionDefaultCacheBehaviorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionDefaultCacheBehaviorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b99858035ff94c261ea3b25607debf108819be588829e0452a0989c1452d2eb2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="behaviorInput")
    def behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "behaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="behavior")
    def behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "behavior"))

    @behavior.setter
    def behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d74da7ba8b479f3a77d3975d437b8268115d05e751eb2a205c0aaa566d824b58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "behavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LightsailDistributionDefaultCacheBehavior]:
        return typing.cast(typing.Optional[LightsailDistributionDefaultCacheBehavior], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LightsailDistributionDefaultCacheBehavior],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28a96919e0b363a3a5ccba4e51c8c245971c936e4a1d9e96b91982e9a595201a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionLocation",
    jsii_struct_bases=[],
    name_mapping={},
)
class LightsailDistributionLocation:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LightsailDistributionLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LightsailDistributionLocationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionLocationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9de6aeb01612839a206255914953d9a957de2125c5d3663073146b9386f2e73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LightsailDistributionLocationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a95952dfe9416435b32d4f2f7181da6d11fa1dab3bad74466f7e11cf372cebbd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LightsailDistributionLocationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7847bb4705957bcdb0f07b329b198a08791d126e57f27baddafa6d7500a5304)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6325e4c9b7b4fc4449131d2d4eae36167aa9fcd8bf130ca8dd65824593dbec16)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89ef3bd48b5cd0baf82b37dd0ba6b4305b2a2cef3cf6d22bba4a90201718dfa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LightsailDistributionLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f7b7d29690af1dc478dd79b48532c10a7f84b977a91c59ca53186c53f4a3d09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @builtins.property
    @jsii.member(jsii_name="regionName")
    def region_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionName"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LightsailDistributionLocation]:
        return typing.cast(typing.Optional[LightsailDistributionLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LightsailDistributionLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__622bd16cc87e522a4a5dafa69b9daeeb2b6c64b4ba588f3148fc5237fa1e2e60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionOrigin",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "region_name": "regionName",
        "protocol_policy": "protocolPolicy",
    },
)
class LightsailDistributionOrigin:
    def __init__(
        self,
        *,
        name: builtins.str,
        region_name: builtins.str,
        protocol_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the origin resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#name LightsailDistribution#name}
        :param region_name: The AWS Region name of the origin resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#region_name LightsailDistribution#region_name}
        :param protocol_policy: The protocol that your Amazon Lightsail distribution uses when establishing a connection with your origin to pull content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#protocol_policy LightsailDistribution#protocol_policy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cab4a4ec7e5879c14881bd11a7d5857d8afc1b2783af5f678b273eaad62c3c6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region_name", value=region_name, expected_type=type_hints["region_name"])
            check_type(argname="argument protocol_policy", value=protocol_policy, expected_type=type_hints["protocol_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "region_name": region_name,
        }
        if protocol_policy is not None:
            self._values["protocol_policy"] = protocol_policy

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the origin resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#name LightsailDistribution#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region_name(self) -> builtins.str:
        '''The AWS Region name of the origin resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#region_name LightsailDistribution#region_name}
        '''
        result = self._values.get("region_name")
        assert result is not None, "Required property 'region_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol_policy(self) -> typing.Optional[builtins.str]:
        '''The protocol that your Amazon Lightsail distribution uses when establishing a connection with your origin to pull content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#protocol_policy LightsailDistribution#protocol_policy}
        '''
        result = self._values.get("protocol_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LightsailDistributionOrigin(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LightsailDistributionOriginOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionOriginOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5809e40975c407b738d65d24bcc09d0dc7e62ae3cb9bf2e07cc3c57d8e44e77e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProtocolPolicy")
    def reset_protocol_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocolPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolPolicyInput")
    def protocol_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="regionNameInput")
    def region_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be7b3c4495d69b98a70038f19360cf5d988fecade26377bef7b07be408fc59f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocolPolicy")
    def protocol_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocolPolicy"))

    @protocol_policy.setter
    def protocol_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a64c7db49f642a66dfced45e8ec82644142e418faa357509acfcbc0bc71b9774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionName")
    def region_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionName"))

    @region_name.setter
    def region_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d4fd5c284497dab2b4a883a27eb59ecdd5f49bf39eda7b498a49300fd1e7f9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LightsailDistributionOrigin]:
        return typing.cast(typing.Optional[LightsailDistributionOrigin], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LightsailDistributionOrigin],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79c5e8b7afa23dc98b40aa380fa463e08bdb7bb03541232955909b15cdc6f7c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class LightsailDistributionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#create LightsailDistribution#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#delete LightsailDistribution#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#update LightsailDistribution#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f89c2447ca170ff9be6c3458dd43f204d6954baafbc5cee0cc1c873d42e928c3)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#create LightsailDistribution#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#delete LightsailDistribution#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/lightsail_distribution#update LightsailDistribution#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LightsailDistributionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LightsailDistributionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.lightsailDistribution.LightsailDistributionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a3a9ae1a0195c4879338de6a758a8c681d2dbbee70540b4ea2a1bddd59d0ba9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c7b2dfd9aca52629de1290649007efec6ec99dc5b04fe02b1a3651a5f4f87a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d243a13061517cb0ed83fa3ea0404c597a6c8e59274ec600b2f0fe4e540a472d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1ec73d8e582a07502706f2fccfccd5d5b5e4ee114668e445813eaf9d1bf6681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LightsailDistributionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LightsailDistributionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LightsailDistributionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44de2f743e8dd05933dacaf6bb74a31d6fa183280c8ecda36b46d9e87bb32684)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LightsailDistribution",
    "LightsailDistributionCacheBehavior",
    "LightsailDistributionCacheBehaviorList",
    "LightsailDistributionCacheBehaviorOutputReference",
    "LightsailDistributionCacheBehaviorSettings",
    "LightsailDistributionCacheBehaviorSettingsForwardedCookies",
    "LightsailDistributionCacheBehaviorSettingsForwardedCookiesOutputReference",
    "LightsailDistributionCacheBehaviorSettingsForwardedHeaders",
    "LightsailDistributionCacheBehaviorSettingsForwardedHeadersOutputReference",
    "LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings",
    "LightsailDistributionCacheBehaviorSettingsForwardedQueryStringsOutputReference",
    "LightsailDistributionCacheBehaviorSettingsOutputReference",
    "LightsailDistributionConfig",
    "LightsailDistributionDefaultCacheBehavior",
    "LightsailDistributionDefaultCacheBehaviorOutputReference",
    "LightsailDistributionLocation",
    "LightsailDistributionLocationList",
    "LightsailDistributionLocationOutputReference",
    "LightsailDistributionOrigin",
    "LightsailDistributionOriginOutputReference",
    "LightsailDistributionTimeouts",
    "LightsailDistributionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__8844245546592794ddc93477787b57d5a9a888d9ca1ef3b52d0bfb1bd2b1f25a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bundle_id: builtins.str,
    default_cache_behavior: typing.Union[LightsailDistributionDefaultCacheBehavior, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    origin: typing.Union[LightsailDistributionOrigin, typing.Dict[builtins.str, typing.Any]],
    cache_behavior: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LightsailDistributionCacheBehavior, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cache_behavior_settings: typing.Optional[typing.Union[LightsailDistributionCacheBehaviorSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address_type: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[LightsailDistributionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__408de95cf5fc5935117a7c8184113c9daf7e507c545c1493f98f49f3536e024e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e7ff6ca8e50be34c5963aec544bc176e8df4363920493c0d964f7b4fbdbf0c2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LightsailDistributionCacheBehavior, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2cc1c1228778c23a699ec0a0ced53b5279c6fcae202936bcde54f84e586eaef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d5d92ebbcb0b2bf24bf1749a93f2c1a5892f0d76031b507224dd7f597119cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8440ad39bdc07870d79db6dee64c5c1fca06b6cda810d52d03d28c139a693e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a283fd3d00b7f282ba79cfabd36ccb7da82ef36996e895419c8ffd757c7368f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf0490180fc35f7625a3828384c190922be99ca060160c9558d7c3a6af9a914(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb9e4f1a056867988da0d5f75fddc2fc400c0d8e265dae90c277442026b1fe15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde7fbefec1fc9e9ba337086242b535899e9401b0196851b0820fc171797a36b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c105bbc7b5555640cbc5ad166d5a70bbb065d8d083b2069adb8f708cb1691133(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f23b926523b34f1b0ee97d44601ca1282ad5b405cccefc8f68a6fcbbfc5c4c86(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d695805cdcc83d017fbb4b415183abc26fa8c56ff3d5f35da2d5c7e0cf7dbe(
    *,
    behavior: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b556fb87d5a34cdfc368365b71448238841cc26e29c432e0f44d2e27d212275f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__034b44d833aa1954b243c2341531e20c40158ec23bb8637415e2fae0feb4f79f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85caf7e6a9f4ab36aba1ea1d1a091b87e5e2984936f28cdbf92cd362f09185fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f616bcc1f2140b2854929b767a70abf9850843566a2b23d9b2fd892a22b44a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c31c2fe0465c956a4d44dda8923ed19a6e1e16a0e0be4f8b8a7fa3b691bc9f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5826a120aeecb0564de000a951936129d3aa4855bb964910a5fe170e81fa3501(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LightsailDistributionCacheBehavior]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f03856a7426316da9057753b4723886200bd20080fac35b02ee1ccb92031199(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c942c43341925fd9bdb381a1d29a5b306ac710f49292e97945fd27ba22b697e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20d8e4edf0943694178b3c62c14d731d8c15ba6d80d8e95f82dbdf1f94ad80b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8d9c933c2034b2fe852f968736b68ad10336b18fa5d731be4446b5727cf1a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LightsailDistributionCacheBehavior]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853b7ceb68e075211cd3c83e94db75028f64181703c41ea5ccf54388c89b2300(
    *,
    allowed_http_methods: typing.Optional[builtins.str] = None,
    cached_http_methods: typing.Optional[builtins.str] = None,
    default_ttl: typing.Optional[jsii.Number] = None,
    forwarded_cookies: typing.Optional[typing.Union[LightsailDistributionCacheBehaviorSettingsForwardedCookies, typing.Dict[builtins.str, typing.Any]]] = None,
    forwarded_headers: typing.Optional[typing.Union[LightsailDistributionCacheBehaviorSettingsForwardedHeaders, typing.Dict[builtins.str, typing.Any]]] = None,
    forwarded_query_strings: typing.Optional[typing.Union[LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_ttl: typing.Optional[jsii.Number] = None,
    minimum_ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be7e7557ead35b552d5b914339d8d74fe01e99ebd9d4a90ea9a2aedb4dfd6c29(
    *,
    cookies_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    option: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae0a2b8b9845156922d36b603283c1fdae841a0df907358eba77e0a3f8f86ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04b2d2a9ad6bfccf594836c1805741a7a0e13eb849926d875e4c57d1c901fbf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b389677fca924ebc44ac6aa05561f058ef67b8b180bbd8f7f5183274cc9f01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab09da520d5db7ad67721d60445c245f5374354a8001c8d3771344f3ea742b0f(
    value: typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedCookies],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28fc52b1b9e10afe6116273afca41cf47e1c98d4f0be4d4773f84aa5cca68297(
    *,
    headers_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    option: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43ec08db1ff140e6ba71fe0c2fb8547143cf4b1792697ee330fa7e7dd99fede2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af6fc3ff489a6ae05d8aaab52af2e18455a1fa18c3067c9a209ac1bd63f6671(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d68a075fcbb126bef8b589ee40ede3836b81aa187c3592a5af735a5ffe0ab17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41259f73b6da034aeb5206c706fbd2918bb4ebaa181bf7680bbdb4d58f3e7b37(
    value: typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedHeaders],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d60ad731cafb9597f1b28f4472b8b52a01fd3ec1d48c5052133e392345993c(
    *,
    option: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query_strings_allowed_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bcd3c3ed872daa29775e3b881f94ba996c059fe0e7f28875f120fe4e9f6a3d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbded2d80f57bea352ab279e306e7d6c6c08154f90a1ca0e77ce6d988366b10e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f46bd9510952b08e7cfe5bac1a3aa1604949748e62db17edeb07101a671026d0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abcbcc67f2aedb3f195a62c3aabf941138bfdcb029a6a3ce9178cbf287c98ea8(
    value: typing.Optional[LightsailDistributionCacheBehaviorSettingsForwardedQueryStrings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca9163716809ea7975bf474fbdbc57c09b9ebe4c10c03f43b75cc0532b82563(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf1082ee6764db7d515ccbe870c16e2868b805d67a1277953e666e167c950e9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e03b9c539baac10b91f7ea523950d16ed0199f9ca320dd5b966ee19aabf1f6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__273a9986beeeadd05275618bda6734158b3926b1f903f8bc234557f29387e8a1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8cedbc66d0cf19dd1ae748f7f0a58527635b06e4f36113efe8d1538079336d6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34595ef6b06d284a48e6c9aa9e7b51a53a7f646db9aeed613fbbd93e872eec04(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a342793e87f0663a9a75da8cb7e5fa91d4b7ccb4114dac93686c4051366ce93(
    value: typing.Optional[LightsailDistributionCacheBehaviorSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e026525a56fed82ab68a5fae7e494d7ad3fb9472765f1659a248a2b181dba1d7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bundle_id: builtins.str,
    default_cache_behavior: typing.Union[LightsailDistributionDefaultCacheBehavior, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    origin: typing.Union[LightsailDistributionOrigin, typing.Dict[builtins.str, typing.Any]],
    cache_behavior: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LightsailDistributionCacheBehavior, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cache_behavior_settings: typing.Optional[typing.Union[LightsailDistributionCacheBehaviorSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address_type: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[LightsailDistributionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b8215c3f551820e53c1b34e94780ff662c1b62ef1846565d592ea6dba5ba61(
    *,
    behavior: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b99858035ff94c261ea3b25607debf108819be588829e0452a0989c1452d2eb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d74da7ba8b479f3a77d3975d437b8268115d05e751eb2a205c0aaa566d824b58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a96919e0b363a3a5ccba4e51c8c245971c936e4a1d9e96b91982e9a595201a(
    value: typing.Optional[LightsailDistributionDefaultCacheBehavior],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9de6aeb01612839a206255914953d9a957de2125c5d3663073146b9386f2e73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a95952dfe9416435b32d4f2f7181da6d11fa1dab3bad74466f7e11cf372cebbd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7847bb4705957bcdb0f07b329b198a08791d126e57f27baddafa6d7500a5304(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6325e4c9b7b4fc4449131d2d4eae36167aa9fcd8bf130ca8dd65824593dbec16(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ef3bd48b5cd0baf82b37dd0ba6b4305b2a2cef3cf6d22bba4a90201718dfa4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f7b7d29690af1dc478dd79b48532c10a7f84b977a91c59ca53186c53f4a3d09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622bd16cc87e522a4a5dafa69b9daeeb2b6c64b4ba588f3148fc5237fa1e2e60(
    value: typing.Optional[LightsailDistributionLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cab4a4ec7e5879c14881bd11a7d5857d8afc1b2783af5f678b273eaad62c3c6(
    *,
    name: builtins.str,
    region_name: builtins.str,
    protocol_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5809e40975c407b738d65d24bcc09d0dc7e62ae3cb9bf2e07cc3c57d8e44e77e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be7b3c4495d69b98a70038f19360cf5d988fecade26377bef7b07be408fc59f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64c7db49f642a66dfced45e8ec82644142e418faa357509acfcbc0bc71b9774(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d4fd5c284497dab2b4a883a27eb59ecdd5f49bf39eda7b498a49300fd1e7f9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79c5e8b7afa23dc98b40aa380fa463e08bdb7bb03541232955909b15cdc6f7c6(
    value: typing.Optional[LightsailDistributionOrigin],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f89c2447ca170ff9be6c3458dd43f204d6954baafbc5cee0cc1c873d42e928c3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3a9ae1a0195c4879338de6a758a8c681d2dbbee70540b4ea2a1bddd59d0ba9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c7b2dfd9aca52629de1290649007efec6ec99dc5b04fe02b1a3651a5f4f87a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d243a13061517cb0ed83fa3ea0404c597a6c8e59274ec600b2f0fe4e540a472d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ec73d8e582a07502706f2fccfccd5d5b5e4ee114668e445813eaf9d1bf6681(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44de2f743e8dd05933dacaf6bb74a31d6fa183280c8ecda36b46d9e87bb32684(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LightsailDistributionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
