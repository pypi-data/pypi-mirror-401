r'''
# `aws_elasticsearch_domain`

Refer to the Terraform Registry for docs: [`aws_elasticsearch_domain`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain).
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


class ElasticsearchDomain(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomain",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain aws_elasticsearch_domain}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        domain_name: builtins.str,
        access_policies: typing.Optional[builtins.str] = None,
        advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        advanced_security_options: typing.Optional[typing.Union["ElasticsearchDomainAdvancedSecurityOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_tune_options: typing.Optional[typing.Union["ElasticsearchDomainAutoTuneOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_config: typing.Optional[typing.Union["ElasticsearchDomainClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        cognito_options: typing.Optional[typing.Union["ElasticsearchDomainCognitoOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        domain_endpoint_options: typing.Optional[typing.Union["ElasticsearchDomainDomainEndpointOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        ebs_options: typing.Optional[typing.Union["ElasticsearchDomainEbsOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        elasticsearch_version: typing.Optional[builtins.str] = None,
        encrypt_at_rest: typing.Optional[typing.Union["ElasticsearchDomainEncryptAtRest", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        log_publishing_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElasticsearchDomainLogPublishingOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        node_to_node_encryption: typing.Optional[typing.Union["ElasticsearchDomainNodeToNodeEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        snapshot_options: typing.Optional[typing.Union["ElasticsearchDomainSnapshotOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ElasticsearchDomainTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_options: typing.Optional[typing.Union["ElasticsearchDomainVpcOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain aws_elasticsearch_domain} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#domain_name ElasticsearchDomain#domain_name}.
        :param access_policies: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#access_policies ElasticsearchDomain#access_policies}.
        :param advanced_options: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#advanced_options ElasticsearchDomain#advanced_options}.
        :param advanced_security_options: advanced_security_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#advanced_security_options ElasticsearchDomain#advanced_security_options}
        :param auto_tune_options: auto_tune_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#auto_tune_options ElasticsearchDomain#auto_tune_options}
        :param cluster_config: cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#cluster_config ElasticsearchDomain#cluster_config}
        :param cognito_options: cognito_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#cognito_options ElasticsearchDomain#cognito_options}
        :param domain_endpoint_options: domain_endpoint_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#domain_endpoint_options ElasticsearchDomain#domain_endpoint_options}
        :param ebs_options: ebs_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#ebs_options ElasticsearchDomain#ebs_options}
        :param elasticsearch_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#elasticsearch_version ElasticsearchDomain#elasticsearch_version}.
        :param encrypt_at_rest: encrypt_at_rest block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#encrypt_at_rest ElasticsearchDomain#encrypt_at_rest}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#id ElasticsearchDomain#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_publishing_options: log_publishing_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#log_publishing_options ElasticsearchDomain#log_publishing_options}
        :param node_to_node_encryption: node_to_node_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#node_to_node_encryption ElasticsearchDomain#node_to_node_encryption}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#region ElasticsearchDomain#region}
        :param snapshot_options: snapshot_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#snapshot_options ElasticsearchDomain#snapshot_options}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#tags ElasticsearchDomain#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#tags_all ElasticsearchDomain#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#timeouts ElasticsearchDomain#timeouts}
        :param vpc_options: vpc_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#vpc_options ElasticsearchDomain#vpc_options}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc69a2ad64da28603e272dacdc005fd8de20f89953480ee2660a53613d5fc11e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ElasticsearchDomainConfig(
            domain_name=domain_name,
            access_policies=access_policies,
            advanced_options=advanced_options,
            advanced_security_options=advanced_security_options,
            auto_tune_options=auto_tune_options,
            cluster_config=cluster_config,
            cognito_options=cognito_options,
            domain_endpoint_options=domain_endpoint_options,
            ebs_options=ebs_options,
            elasticsearch_version=elasticsearch_version,
            encrypt_at_rest=encrypt_at_rest,
            id=id,
            log_publishing_options=log_publishing_options,
            node_to_node_encryption=node_to_node_encryption,
            region=region,
            snapshot_options=snapshot_options,
            tags=tags,
            tags_all=tags_all,
            timeouts=timeouts,
            vpc_options=vpc_options,
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
        '''Generates CDKTF code for importing a ElasticsearchDomain resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ElasticsearchDomain to import.
        :param import_from_id: The id of the existing ElasticsearchDomain that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ElasticsearchDomain to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__808f7d9bf8f04be77300504f9472b95b76581a93bb1cb02f9652cab01e64a444)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdvancedSecurityOptions")
    def put_advanced_security_options(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        internal_user_database_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        master_user_options: typing.Optional[typing.Union["ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#enabled ElasticsearchDomain#enabled}.
        :param internal_user_database_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#internal_user_database_enabled ElasticsearchDomain#internal_user_database_enabled}.
        :param master_user_options: master_user_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#master_user_options ElasticsearchDomain#master_user_options}
        '''
        value = ElasticsearchDomainAdvancedSecurityOptions(
            enabled=enabled,
            internal_user_database_enabled=internal_user_database_enabled,
            master_user_options=master_user_options,
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedSecurityOptions", [value]))

    @jsii.member(jsii_name="putAutoTuneOptions")
    def put_auto_tune_options(
        self,
        *,
        desired_state: builtins.str,
        maintenance_schedule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rollback_on_disable: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param desired_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#desired_state ElasticsearchDomain#desired_state}.
        :param maintenance_schedule: maintenance_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#maintenance_schedule ElasticsearchDomain#maintenance_schedule}
        :param rollback_on_disable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#rollback_on_disable ElasticsearchDomain#rollback_on_disable}.
        '''
        value = ElasticsearchDomainAutoTuneOptions(
            desired_state=desired_state,
            maintenance_schedule=maintenance_schedule,
            rollback_on_disable=rollback_on_disable,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoTuneOptions", [value]))

    @jsii.member(jsii_name="putClusterConfig")
    def put_cluster_config(
        self,
        *,
        cold_storage_options: typing.Optional[typing.Union["ElasticsearchDomainClusterConfigColdStorageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        dedicated_master_count: typing.Optional[jsii.Number] = None,
        dedicated_master_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dedicated_master_type: typing.Optional[builtins.str] = None,
        instance_count: typing.Optional[jsii.Number] = None,
        instance_type: typing.Optional[builtins.str] = None,
        warm_count: typing.Optional[jsii.Number] = None,
        warm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        warm_type: typing.Optional[builtins.str] = None,
        zone_awareness_config: typing.Optional[typing.Union["ElasticsearchDomainClusterConfigZoneAwarenessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        zone_awareness_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cold_storage_options: cold_storage_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#cold_storage_options ElasticsearchDomain#cold_storage_options}
        :param dedicated_master_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#dedicated_master_count ElasticsearchDomain#dedicated_master_count}.
        :param dedicated_master_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#dedicated_master_enabled ElasticsearchDomain#dedicated_master_enabled}.
        :param dedicated_master_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#dedicated_master_type ElasticsearchDomain#dedicated_master_type}.
        :param instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#instance_count ElasticsearchDomain#instance_count}.
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#instance_type ElasticsearchDomain#instance_type}.
        :param warm_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#warm_count ElasticsearchDomain#warm_count}.
        :param warm_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#warm_enabled ElasticsearchDomain#warm_enabled}.
        :param warm_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#warm_type ElasticsearchDomain#warm_type}.
        :param zone_awareness_config: zone_awareness_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#zone_awareness_config ElasticsearchDomain#zone_awareness_config}
        :param zone_awareness_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#zone_awareness_enabled ElasticsearchDomain#zone_awareness_enabled}.
        '''
        value = ElasticsearchDomainClusterConfig(
            cold_storage_options=cold_storage_options,
            dedicated_master_count=dedicated_master_count,
            dedicated_master_enabled=dedicated_master_enabled,
            dedicated_master_type=dedicated_master_type,
            instance_count=instance_count,
            instance_type=instance_type,
            warm_count=warm_count,
            warm_enabled=warm_enabled,
            warm_type=warm_type,
            zone_awareness_config=zone_awareness_config,
            zone_awareness_enabled=zone_awareness_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putClusterConfig", [value]))

    @jsii.member(jsii_name="putCognitoOptions")
    def put_cognito_options(
        self,
        *,
        identity_pool_id: builtins.str,
        role_arn: builtins.str,
        user_pool_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param identity_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#identity_pool_id ElasticsearchDomain#identity_pool_id}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#role_arn ElasticsearchDomain#role_arn}.
        :param user_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#user_pool_id ElasticsearchDomain#user_pool_id}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#enabled ElasticsearchDomain#enabled}.
        '''
        value = ElasticsearchDomainCognitoOptions(
            identity_pool_id=identity_pool_id,
            role_arn=role_arn,
            user_pool_id=user_pool_id,
            enabled=enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putCognitoOptions", [value]))

    @jsii.member(jsii_name="putDomainEndpointOptions")
    def put_domain_endpoint_options(
        self,
        *,
        custom_endpoint: typing.Optional[builtins.str] = None,
        custom_endpoint_certificate_arn: typing.Optional[builtins.str] = None,
        custom_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enforce_https: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_security_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#custom_endpoint ElasticsearchDomain#custom_endpoint}.
        :param custom_endpoint_certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#custom_endpoint_certificate_arn ElasticsearchDomain#custom_endpoint_certificate_arn}.
        :param custom_endpoint_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#custom_endpoint_enabled ElasticsearchDomain#custom_endpoint_enabled}.
        :param enforce_https: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#enforce_https ElasticsearchDomain#enforce_https}.
        :param tls_security_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#tls_security_policy ElasticsearchDomain#tls_security_policy}.
        '''
        value = ElasticsearchDomainDomainEndpointOptions(
            custom_endpoint=custom_endpoint,
            custom_endpoint_certificate_arn=custom_endpoint_certificate_arn,
            custom_endpoint_enabled=custom_endpoint_enabled,
            enforce_https=enforce_https,
            tls_security_policy=tls_security_policy,
        )

        return typing.cast(None, jsii.invoke(self, "putDomainEndpointOptions", [value]))

    @jsii.member(jsii_name="putEbsOptions")
    def put_ebs_options(
        self,
        *,
        ebs_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        iops: typing.Optional[jsii.Number] = None,
        throughput: typing.Optional[jsii.Number] = None,
        volume_size: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ebs_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#ebs_enabled ElasticsearchDomain#ebs_enabled}.
        :param iops: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#iops ElasticsearchDomain#iops}.
        :param throughput: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#throughput ElasticsearchDomain#throughput}.
        :param volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#volume_size ElasticsearchDomain#volume_size}.
        :param volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#volume_type ElasticsearchDomain#volume_type}.
        '''
        value = ElasticsearchDomainEbsOptions(
            ebs_enabled=ebs_enabled,
            iops=iops,
            throughput=throughput,
            volume_size=volume_size,
            volume_type=volume_type,
        )

        return typing.cast(None, jsii.invoke(self, "putEbsOptions", [value]))

    @jsii.member(jsii_name="putEncryptAtRest")
    def put_encrypt_at_rest(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#enabled ElasticsearchDomain#enabled}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#kms_key_id ElasticsearchDomain#kms_key_id}.
        '''
        value = ElasticsearchDomainEncryptAtRest(
            enabled=enabled, kms_key_id=kms_key_id
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptAtRest", [value]))

    @jsii.member(jsii_name="putLogPublishingOptions")
    def put_log_publishing_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElasticsearchDomainLogPublishingOptions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5e9e114a8e26de5063607b04c325ff85274230c953b404e9d7ef0dbb8f63e4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLogPublishingOptions", [value]))

    @jsii.member(jsii_name="putNodeToNodeEncryption")
    def put_node_to_node_encryption(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#enabled ElasticsearchDomain#enabled}.
        '''
        value = ElasticsearchDomainNodeToNodeEncryption(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putNodeToNodeEncryption", [value]))

    @jsii.member(jsii_name="putSnapshotOptions")
    def put_snapshot_options(
        self,
        *,
        automated_snapshot_start_hour: jsii.Number,
    ) -> None:
        '''
        :param automated_snapshot_start_hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#automated_snapshot_start_hour ElasticsearchDomain#automated_snapshot_start_hour}.
        '''
        value = ElasticsearchDomainSnapshotOptions(
            automated_snapshot_start_hour=automated_snapshot_start_hour
        )

        return typing.cast(None, jsii.invoke(self, "putSnapshotOptions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#create ElasticsearchDomain#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#delete ElasticsearchDomain#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#update ElasticsearchDomain#update}.
        '''
        value = ElasticsearchDomainTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVpcOptions")
    def put_vpc_options(
        self,
        *,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#security_group_ids ElasticsearchDomain#security_group_ids}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#subnet_ids ElasticsearchDomain#subnet_ids}.
        '''
        value = ElasticsearchDomainVpcOptions(
            security_group_ids=security_group_ids, subnet_ids=subnet_ids
        )

        return typing.cast(None, jsii.invoke(self, "putVpcOptions", [value]))

    @jsii.member(jsii_name="resetAccessPolicies")
    def reset_access_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessPolicies", []))

    @jsii.member(jsii_name="resetAdvancedOptions")
    def reset_advanced_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedOptions", []))

    @jsii.member(jsii_name="resetAdvancedSecurityOptions")
    def reset_advanced_security_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedSecurityOptions", []))

    @jsii.member(jsii_name="resetAutoTuneOptions")
    def reset_auto_tune_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoTuneOptions", []))

    @jsii.member(jsii_name="resetClusterConfig")
    def reset_cluster_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterConfig", []))

    @jsii.member(jsii_name="resetCognitoOptions")
    def reset_cognito_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCognitoOptions", []))

    @jsii.member(jsii_name="resetDomainEndpointOptions")
    def reset_domain_endpoint_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainEndpointOptions", []))

    @jsii.member(jsii_name="resetEbsOptions")
    def reset_ebs_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEbsOptions", []))

    @jsii.member(jsii_name="resetElasticsearchVersion")
    def reset_elasticsearch_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchVersion", []))

    @jsii.member(jsii_name="resetEncryptAtRest")
    def reset_encrypt_at_rest(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptAtRest", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogPublishingOptions")
    def reset_log_publishing_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogPublishingOptions", []))

    @jsii.member(jsii_name="resetNodeToNodeEncryption")
    def reset_node_to_node_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeToNodeEncryption", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSnapshotOptions")
    def reset_snapshot_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshotOptions", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVpcOptions")
    def reset_vpc_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcOptions", []))

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
    @jsii.member(jsii_name="advancedSecurityOptions")
    def advanced_security_options(
        self,
    ) -> "ElasticsearchDomainAdvancedSecurityOptionsOutputReference":
        return typing.cast("ElasticsearchDomainAdvancedSecurityOptionsOutputReference", jsii.get(self, "advancedSecurityOptions"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="autoTuneOptions")
    def auto_tune_options(self) -> "ElasticsearchDomainAutoTuneOptionsOutputReference":
        return typing.cast("ElasticsearchDomainAutoTuneOptionsOutputReference", jsii.get(self, "autoTuneOptions"))

    @builtins.property
    @jsii.member(jsii_name="clusterConfig")
    def cluster_config(self) -> "ElasticsearchDomainClusterConfigOutputReference":
        return typing.cast("ElasticsearchDomainClusterConfigOutputReference", jsii.get(self, "clusterConfig"))

    @builtins.property
    @jsii.member(jsii_name="cognitoOptions")
    def cognito_options(self) -> "ElasticsearchDomainCognitoOptionsOutputReference":
        return typing.cast("ElasticsearchDomainCognitoOptionsOutputReference", jsii.get(self, "cognitoOptions"))

    @builtins.property
    @jsii.member(jsii_name="domainEndpointOptions")
    def domain_endpoint_options(
        self,
    ) -> "ElasticsearchDomainDomainEndpointOptionsOutputReference":
        return typing.cast("ElasticsearchDomainDomainEndpointOptionsOutputReference", jsii.get(self, "domainEndpointOptions"))

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainId"))

    @builtins.property
    @jsii.member(jsii_name="ebsOptions")
    def ebs_options(self) -> "ElasticsearchDomainEbsOptionsOutputReference":
        return typing.cast("ElasticsearchDomainEbsOptionsOutputReference", jsii.get(self, "ebsOptions"))

    @builtins.property
    @jsii.member(jsii_name="encryptAtRest")
    def encrypt_at_rest(self) -> "ElasticsearchDomainEncryptAtRestOutputReference":
        return typing.cast("ElasticsearchDomainEncryptAtRestOutputReference", jsii.get(self, "encryptAtRest"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="kibanaEndpoint")
    def kibana_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kibanaEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="logPublishingOptions")
    def log_publishing_options(self) -> "ElasticsearchDomainLogPublishingOptionsList":
        return typing.cast("ElasticsearchDomainLogPublishingOptionsList", jsii.get(self, "logPublishingOptions"))

    @builtins.property
    @jsii.member(jsii_name="nodeToNodeEncryption")
    def node_to_node_encryption(
        self,
    ) -> "ElasticsearchDomainNodeToNodeEncryptionOutputReference":
        return typing.cast("ElasticsearchDomainNodeToNodeEncryptionOutputReference", jsii.get(self, "nodeToNodeEncryption"))

    @builtins.property
    @jsii.member(jsii_name="snapshotOptions")
    def snapshot_options(self) -> "ElasticsearchDomainSnapshotOptionsOutputReference":
        return typing.cast("ElasticsearchDomainSnapshotOptionsOutputReference", jsii.get(self, "snapshotOptions"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ElasticsearchDomainTimeoutsOutputReference":
        return typing.cast("ElasticsearchDomainTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vpcOptions")
    def vpc_options(self) -> "ElasticsearchDomainVpcOptionsOutputReference":
        return typing.cast("ElasticsearchDomainVpcOptionsOutputReference", jsii.get(self, "vpcOptions"))

    @builtins.property
    @jsii.member(jsii_name="accessPoliciesInput")
    def access_policies_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="advancedOptionsInput")
    def advanced_options_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "advancedOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="advancedSecurityOptionsInput")
    def advanced_security_options_input(
        self,
    ) -> typing.Optional["ElasticsearchDomainAdvancedSecurityOptions"]:
        return typing.cast(typing.Optional["ElasticsearchDomainAdvancedSecurityOptions"], jsii.get(self, "advancedSecurityOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoTuneOptionsInput")
    def auto_tune_options_input(
        self,
    ) -> typing.Optional["ElasticsearchDomainAutoTuneOptions"]:
        return typing.cast(typing.Optional["ElasticsearchDomainAutoTuneOptions"], jsii.get(self, "autoTuneOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterConfigInput")
    def cluster_config_input(
        self,
    ) -> typing.Optional["ElasticsearchDomainClusterConfig"]:
        return typing.cast(typing.Optional["ElasticsearchDomainClusterConfig"], jsii.get(self, "clusterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="cognitoOptionsInput")
    def cognito_options_input(
        self,
    ) -> typing.Optional["ElasticsearchDomainCognitoOptions"]:
        return typing.cast(typing.Optional["ElasticsearchDomainCognitoOptions"], jsii.get(self, "cognitoOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="domainEndpointOptionsInput")
    def domain_endpoint_options_input(
        self,
    ) -> typing.Optional["ElasticsearchDomainDomainEndpointOptions"]:
        return typing.cast(typing.Optional["ElasticsearchDomainDomainEndpointOptions"], jsii.get(self, "domainEndpointOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="ebsOptionsInput")
    def ebs_options_input(self) -> typing.Optional["ElasticsearchDomainEbsOptions"]:
        return typing.cast(typing.Optional["ElasticsearchDomainEbsOptions"], jsii.get(self, "ebsOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchVersionInput")
    def elasticsearch_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elasticsearchVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptAtRestInput")
    def encrypt_at_rest_input(
        self,
    ) -> typing.Optional["ElasticsearchDomainEncryptAtRest"]:
        return typing.cast(typing.Optional["ElasticsearchDomainEncryptAtRest"], jsii.get(self, "encryptAtRestInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logPublishingOptionsInput")
    def log_publishing_options_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElasticsearchDomainLogPublishingOptions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElasticsearchDomainLogPublishingOptions"]]], jsii.get(self, "logPublishingOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeToNodeEncryptionInput")
    def node_to_node_encryption_input(
        self,
    ) -> typing.Optional["ElasticsearchDomainNodeToNodeEncryption"]:
        return typing.cast(typing.Optional["ElasticsearchDomainNodeToNodeEncryption"], jsii.get(self, "nodeToNodeEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotOptionsInput")
    def snapshot_options_input(
        self,
    ) -> typing.Optional["ElasticsearchDomainSnapshotOptions"]:
        return typing.cast(typing.Optional["ElasticsearchDomainSnapshotOptions"], jsii.get(self, "snapshotOptionsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ElasticsearchDomainTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ElasticsearchDomainTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcOptionsInput")
    def vpc_options_input(self) -> typing.Optional["ElasticsearchDomainVpcOptions"]:
        return typing.cast(typing.Optional["ElasticsearchDomainVpcOptions"], jsii.get(self, "vpcOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="accessPolicies")
    def access_policies(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessPolicies"))

    @access_policies.setter
    def access_policies(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__166cd9f2a9394f225368b33647c1c9714bdbfee1c1a877c7a1cc899a31862e63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessPolicies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="advancedOptions")
    def advanced_options(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "advancedOptions"))

    @advanced_options.setter
    def advanced_options(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__317d8a20e75a27f59ff38b12bd28c9d9967efd53ef63f4254743694050105f24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advancedOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fb2996da1bc9e2a7f815170b630ac17c3aeaf1eae2659b6431e2cb0a758b220)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="elasticsearchVersion")
    def elasticsearch_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "elasticsearchVersion"))

    @elasticsearch_version.setter
    def elasticsearch_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96dd3814b2791f9796bcd4241d05f224d1b417cf3f6715a618567ce8972ffb88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__854f65072a2eaaaf4d7050e8a235e28acba7b0f75c0d2f294597bee504c79646)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bb82ea8166d51dd062426b0a5737721343efdbb6949dc2b1ef60fe037d11892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bc2352a22bde00615bc167b9872db93be27c00d76f3acb9ca079df1ca5da2b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21f42f50656dc13bd017ace3c99d2a2e3e1f4c22db241cbaef74cd8bf6b2f150)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainAdvancedSecurityOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "internal_user_database_enabled": "internalUserDatabaseEnabled",
        "master_user_options": "masterUserOptions",
    },
)
class ElasticsearchDomainAdvancedSecurityOptions:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        internal_user_database_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        master_user_options: typing.Optional[typing.Union["ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#enabled ElasticsearchDomain#enabled}.
        :param internal_user_database_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#internal_user_database_enabled ElasticsearchDomain#internal_user_database_enabled}.
        :param master_user_options: master_user_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#master_user_options ElasticsearchDomain#master_user_options}
        '''
        if isinstance(master_user_options, dict):
            master_user_options = ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptions(**master_user_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a96a7b0205b18423dc88a2562a62e582678caf4534b38faebac7a83e2d3287f5)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument internal_user_database_enabled", value=internal_user_database_enabled, expected_type=type_hints["internal_user_database_enabled"])
            check_type(argname="argument master_user_options", value=master_user_options, expected_type=type_hints["master_user_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if internal_user_database_enabled is not None:
            self._values["internal_user_database_enabled"] = internal_user_database_enabled
        if master_user_options is not None:
            self._values["master_user_options"] = master_user_options

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#enabled ElasticsearchDomain#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def internal_user_database_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#internal_user_database_enabled ElasticsearchDomain#internal_user_database_enabled}.'''
        result = self._values.get("internal_user_database_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def master_user_options(
        self,
    ) -> typing.Optional["ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptions"]:
        '''master_user_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#master_user_options ElasticsearchDomain#master_user_options}
        '''
        result = self._values.get("master_user_options")
        return typing.cast(typing.Optional["ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticsearchDomainAdvancedSecurityOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptions",
    jsii_struct_bases=[],
    name_mapping={
        "master_user_arn": "masterUserArn",
        "master_user_name": "masterUserName",
        "master_user_password": "masterUserPassword",
    },
)
class ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptions:
    def __init__(
        self,
        *,
        master_user_arn: typing.Optional[builtins.str] = None,
        master_user_name: typing.Optional[builtins.str] = None,
        master_user_password: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param master_user_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#master_user_arn ElasticsearchDomain#master_user_arn}.
        :param master_user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#master_user_name ElasticsearchDomain#master_user_name}.
        :param master_user_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#master_user_password ElasticsearchDomain#master_user_password}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b8df72959be87e5018598b56642899ef12575025dc17207646004086f779b8)
            check_type(argname="argument master_user_arn", value=master_user_arn, expected_type=type_hints["master_user_arn"])
            check_type(argname="argument master_user_name", value=master_user_name, expected_type=type_hints["master_user_name"])
            check_type(argname="argument master_user_password", value=master_user_password, expected_type=type_hints["master_user_password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if master_user_arn is not None:
            self._values["master_user_arn"] = master_user_arn
        if master_user_name is not None:
            self._values["master_user_name"] = master_user_name
        if master_user_password is not None:
            self._values["master_user_password"] = master_user_password

    @builtins.property
    def master_user_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#master_user_arn ElasticsearchDomain#master_user_arn}.'''
        result = self._values.get("master_user_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_user_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#master_user_name ElasticsearchDomain#master_user_name}.'''
        result = self._values.get("master_user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_user_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#master_user_password ElasticsearchDomain#master_user_password}.'''
        result = self._values.get("master_user_password")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__441bfef9b15fcf12e50a195439d4d5e0f467c83724d0ac6c7771894fe5c58e5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMasterUserArn")
    def reset_master_user_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterUserArn", []))

    @jsii.member(jsii_name="resetMasterUserName")
    def reset_master_user_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterUserName", []))

    @jsii.member(jsii_name="resetMasterUserPassword")
    def reset_master_user_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterUserPassword", []))

    @builtins.property
    @jsii.member(jsii_name="masterUserArnInput")
    def master_user_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "masterUserArnInput"))

    @builtins.property
    @jsii.member(jsii_name="masterUserNameInput")
    def master_user_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "masterUserNameInput"))

    @builtins.property
    @jsii.member(jsii_name="masterUserPasswordInput")
    def master_user_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "masterUserPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="masterUserArn")
    def master_user_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "masterUserArn"))

    @master_user_arn.setter
    def master_user_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__606e353cd046a1ebc3963f25bd06165099d29da6d969485e8f53d04532a2685f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterUserArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="masterUserName")
    def master_user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "masterUserName"))

    @master_user_name.setter
    def master_user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1392a204ef6fba06f99dfef80e0b5e3461514f0e723c47574175e81f2db62691)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterUserName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="masterUserPassword")
    def master_user_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "masterUserPassword"))

    @master_user_password.setter
    def master_user_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef6e0f9808b61c77b0e49bcf6eb0519f14a59dc9c553a157fd969484c0fbfb29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterUserPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptions]:
        return typing.cast(typing.Optional[ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf8a341e9606ea1c21db690606151574b3149c8189ce0bffab3ddae2e38ce8d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ElasticsearchDomainAdvancedSecurityOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainAdvancedSecurityOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__403d6d51eba6fd14f15acf99033665f55a5d13068f67e4cbf69336544505fc97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMasterUserOptions")
    def put_master_user_options(
        self,
        *,
        master_user_arn: typing.Optional[builtins.str] = None,
        master_user_name: typing.Optional[builtins.str] = None,
        master_user_password: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param master_user_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#master_user_arn ElasticsearchDomain#master_user_arn}.
        :param master_user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#master_user_name ElasticsearchDomain#master_user_name}.
        :param master_user_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#master_user_password ElasticsearchDomain#master_user_password}.
        '''
        value = ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptions(
            master_user_arn=master_user_arn,
            master_user_name=master_user_name,
            master_user_password=master_user_password,
        )

        return typing.cast(None, jsii.invoke(self, "putMasterUserOptions", [value]))

    @jsii.member(jsii_name="resetInternalUserDatabaseEnabled")
    def reset_internal_user_database_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalUserDatabaseEnabled", []))

    @jsii.member(jsii_name="resetMasterUserOptions")
    def reset_master_user_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMasterUserOptions", []))

    @builtins.property
    @jsii.member(jsii_name="masterUserOptions")
    def master_user_options(
        self,
    ) -> ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptionsOutputReference:
        return typing.cast(ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptionsOutputReference, jsii.get(self, "masterUserOptions"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="internalUserDatabaseEnabledInput")
    def internal_user_database_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalUserDatabaseEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="masterUserOptionsInput")
    def master_user_options_input(
        self,
    ) -> typing.Optional[ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptions]:
        return typing.cast(typing.Optional[ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptions], jsii.get(self, "masterUserOptionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f9ddcc95da4fe832be547d0ae6e94cb9c5aeb92e50e0a522b01fa8e586cbbde6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalUserDatabaseEnabled")
    def internal_user_database_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "internalUserDatabaseEnabled"))

    @internal_user_database_enabled.setter
    def internal_user_database_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d754812618d08ffe5dce58eeb5ffcacdc73a3aeab3b592639fe3b219bbaa490a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalUserDatabaseEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ElasticsearchDomainAdvancedSecurityOptions]:
        return typing.cast(typing.Optional[ElasticsearchDomainAdvancedSecurityOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElasticsearchDomainAdvancedSecurityOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba12c9548015d557feadb9bc996dce6584a9483fec1d8d902ea948f2c0040f88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainAutoTuneOptions",
    jsii_struct_bases=[],
    name_mapping={
        "desired_state": "desiredState",
        "maintenance_schedule": "maintenanceSchedule",
        "rollback_on_disable": "rollbackOnDisable",
    },
)
class ElasticsearchDomainAutoTuneOptions:
    def __init__(
        self,
        *,
        desired_state: builtins.str,
        maintenance_schedule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rollback_on_disable: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param desired_state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#desired_state ElasticsearchDomain#desired_state}.
        :param maintenance_schedule: maintenance_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#maintenance_schedule ElasticsearchDomain#maintenance_schedule}
        :param rollback_on_disable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#rollback_on_disable ElasticsearchDomain#rollback_on_disable}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bc4f50eaa5e90e946456bc263f9b7e27428f9a9da2cbbef7e65a9f4d20f6ba0)
            check_type(argname="argument desired_state", value=desired_state, expected_type=type_hints["desired_state"])
            check_type(argname="argument maintenance_schedule", value=maintenance_schedule, expected_type=type_hints["maintenance_schedule"])
            check_type(argname="argument rollback_on_disable", value=rollback_on_disable, expected_type=type_hints["rollback_on_disable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "desired_state": desired_state,
        }
        if maintenance_schedule is not None:
            self._values["maintenance_schedule"] = maintenance_schedule
        if rollback_on_disable is not None:
            self._values["rollback_on_disable"] = rollback_on_disable

    @builtins.property
    def desired_state(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#desired_state ElasticsearchDomain#desired_state}.'''
        result = self._values.get("desired_state")
        assert result is not None, "Required property 'desired_state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def maintenance_schedule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule"]]]:
        '''maintenance_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#maintenance_schedule ElasticsearchDomain#maintenance_schedule}
        '''
        result = self._values.get("maintenance_schedule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule"]]], result)

    @builtins.property
    def rollback_on_disable(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#rollback_on_disable ElasticsearchDomain#rollback_on_disable}.'''
        result = self._values.get("rollback_on_disable")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticsearchDomainAutoTuneOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "cron_expression_for_recurrence": "cronExpressionForRecurrence",
        "duration": "duration",
        "start_at": "startAt",
    },
)
class ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule:
    def __init__(
        self,
        *,
        cron_expression_for_recurrence: builtins.str,
        duration: typing.Union["ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDuration", typing.Dict[builtins.str, typing.Any]],
        start_at: builtins.str,
    ) -> None:
        '''
        :param cron_expression_for_recurrence: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#cron_expression_for_recurrence ElasticsearchDomain#cron_expression_for_recurrence}.
        :param duration: duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#duration ElasticsearchDomain#duration}
        :param start_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#start_at ElasticsearchDomain#start_at}.
        '''
        if isinstance(duration, dict):
            duration = ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDuration(**duration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ea602c5e0ba3980823878481b0701cb6245b3cb2dde5649d002984eb2dfea9c)
            check_type(argname="argument cron_expression_for_recurrence", value=cron_expression_for_recurrence, expected_type=type_hints["cron_expression_for_recurrence"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument start_at", value=start_at, expected_type=type_hints["start_at"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cron_expression_for_recurrence": cron_expression_for_recurrence,
            "duration": duration,
            "start_at": start_at,
        }

    @builtins.property
    def cron_expression_for_recurrence(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#cron_expression_for_recurrence ElasticsearchDomain#cron_expression_for_recurrence}.'''
        result = self._values.get("cron_expression_for_recurrence")
        assert result is not None, "Required property 'cron_expression_for_recurrence' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def duration(
        self,
    ) -> "ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDuration":
        '''duration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#duration ElasticsearchDomain#duration}
        '''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast("ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDuration", result)

    @builtins.property
    def start_at(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#start_at ElasticsearchDomain#start_at}.'''
        result = self._values.get("start_at")
        assert result is not None, "Required property 'start_at' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDuration",
    jsii_struct_bases=[],
    name_mapping={"unit": "unit", "value": "value"},
)
class ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDuration:
    def __init__(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#unit ElasticsearchDomain#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#value ElasticsearchDomain#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b97c831136582188b783e6af4f67792cc8209d86551fbe5b271d8f981c6bb45)
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "unit": unit,
            "value": value,
        }

    @builtins.property
    def unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#unit ElasticsearchDomain#unit}.'''
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#value ElasticsearchDomain#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5128b2255d16a58754f94c55bbf498d5cf379850c1ca60adcba3ae9632c33f72)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="unitInput")
    def unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unitInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="unit")
    def unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unit"))

    @unit.setter
    def unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6beb815a635771cd3a4d2cd81b8c5487b8b9b9a442f11766886c3fa4a9ea3877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8325d4e837538a4bb2a20c6335766caf3a8760af77d35a1130029884043dc06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDuration]:
        return typing.cast(typing.Optional[ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__538fbe5b74af2c682ea3b99f00a9e2f029afb747ac5781874c132b2d3556eeec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3b77f99214208f619ce7cc672508da981585ccc6e0613368e375350f2f1db43)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69519ae84cfbee21b6e01a272858f10e20edb0d260253361b86e9c4ab81ca65c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe41328d914678a9b9882ba5ba4c327299211f2f18e34cf8608f0e12d9738cc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc0e1fb834e5b67919cde551427de8eb7d22c71a38ac7741749b6f863d1aaddc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3178c4cd22ebd774beaceb670aea70f46db4c010fdb639698b6fbbef5787ea19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baf0a9da7c833845db1da2c1ac890aa8a4a4c5c4e32ad6d4a39c35f135571e1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e6b2fbcb4a08f9fbd34974094aa19d060e6c75dcfccf26b20c9adeeeac2ffd0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDuration")
    def put_duration(self, *, unit: builtins.str, value: jsii.Number) -> None:
        '''
        :param unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#unit ElasticsearchDomain#unit}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#value ElasticsearchDomain#value}.
        '''
        value_ = ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDuration(
            unit=unit, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putDuration", [value_]))

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(
        self,
    ) -> ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDurationOutputReference:
        return typing.cast(ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDurationOutputReference, jsii.get(self, "duration"))

    @builtins.property
    @jsii.member(jsii_name="cronExpressionForRecurrenceInput")
    def cron_expression_for_recurrence_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cronExpressionForRecurrenceInput"))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(
        self,
    ) -> typing.Optional[ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDuration]:
        return typing.cast(typing.Optional[ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDuration], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="startAtInput")
    def start_at_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startAtInput"))

    @builtins.property
    @jsii.member(jsii_name="cronExpressionForRecurrence")
    def cron_expression_for_recurrence(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cronExpressionForRecurrence"))

    @cron_expression_for_recurrence.setter
    def cron_expression_for_recurrence(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79cfb2f730c2c516a316196f4c8a4228173299e126205782945bfb86b403b3ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cronExpressionForRecurrence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startAt")
    def start_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startAt"))

    @start_at.setter
    def start_at(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__278f14ec2c24e86949722bc0556f3b1fb7e31f266bb3f1e42a889f5001553b92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b262b7ce23fa932e1e6a985a4d9a4baf069ac97560cc1906601956e25e51f346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ElasticsearchDomainAutoTuneOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainAutoTuneOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29c57b6bdd8e754de86c490fbabc8a863c2a45ee7f1a942e69da4f8ebc59ebb6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMaintenanceSchedule")
    def put_maintenance_schedule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee692940ca50044dab87f163c5a70f4ba1ecab19667fa4194def9c0f25c00416)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMaintenanceSchedule", [value]))

    @jsii.member(jsii_name="resetMaintenanceSchedule")
    def reset_maintenance_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceSchedule", []))

    @jsii.member(jsii_name="resetRollbackOnDisable")
    def reset_rollback_on_disable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRollbackOnDisable", []))

    @builtins.property
    @jsii.member(jsii_name="maintenanceSchedule")
    def maintenance_schedule(
        self,
    ) -> ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleList:
        return typing.cast(ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleList, jsii.get(self, "maintenanceSchedule"))

    @builtins.property
    @jsii.member(jsii_name="desiredStateInput")
    def desired_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "desiredStateInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceScheduleInput")
    def maintenance_schedule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule]]], jsii.get(self, "maintenanceScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="rollbackOnDisableInput")
    def rollback_on_disable_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rollbackOnDisableInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredState")
    def desired_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desiredState"))

    @desired_state.setter
    def desired_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4453335e6ae91f24c0fe5bae3b4f9a3e92d659100877ad56397915d5cda3d2e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desiredState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rollbackOnDisable")
    def rollback_on_disable(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rollbackOnDisable"))

    @rollback_on_disable.setter
    def rollback_on_disable(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e563f48de821d27c036aa67f41930876d2b9fab53286fdca1c12938363a4df4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rollbackOnDisable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ElasticsearchDomainAutoTuneOptions]:
        return typing.cast(typing.Optional[ElasticsearchDomainAutoTuneOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElasticsearchDomainAutoTuneOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bfed56fc1c66150791c92dba3d7e0078fa1c4e91e06071a9d1de9954a1557a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cold_storage_options": "coldStorageOptions",
        "dedicated_master_count": "dedicatedMasterCount",
        "dedicated_master_enabled": "dedicatedMasterEnabled",
        "dedicated_master_type": "dedicatedMasterType",
        "instance_count": "instanceCount",
        "instance_type": "instanceType",
        "warm_count": "warmCount",
        "warm_enabled": "warmEnabled",
        "warm_type": "warmType",
        "zone_awareness_config": "zoneAwarenessConfig",
        "zone_awareness_enabled": "zoneAwarenessEnabled",
    },
)
class ElasticsearchDomainClusterConfig:
    def __init__(
        self,
        *,
        cold_storage_options: typing.Optional[typing.Union["ElasticsearchDomainClusterConfigColdStorageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        dedicated_master_count: typing.Optional[jsii.Number] = None,
        dedicated_master_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dedicated_master_type: typing.Optional[builtins.str] = None,
        instance_count: typing.Optional[jsii.Number] = None,
        instance_type: typing.Optional[builtins.str] = None,
        warm_count: typing.Optional[jsii.Number] = None,
        warm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        warm_type: typing.Optional[builtins.str] = None,
        zone_awareness_config: typing.Optional[typing.Union["ElasticsearchDomainClusterConfigZoneAwarenessConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        zone_awareness_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cold_storage_options: cold_storage_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#cold_storage_options ElasticsearchDomain#cold_storage_options}
        :param dedicated_master_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#dedicated_master_count ElasticsearchDomain#dedicated_master_count}.
        :param dedicated_master_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#dedicated_master_enabled ElasticsearchDomain#dedicated_master_enabled}.
        :param dedicated_master_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#dedicated_master_type ElasticsearchDomain#dedicated_master_type}.
        :param instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#instance_count ElasticsearchDomain#instance_count}.
        :param instance_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#instance_type ElasticsearchDomain#instance_type}.
        :param warm_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#warm_count ElasticsearchDomain#warm_count}.
        :param warm_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#warm_enabled ElasticsearchDomain#warm_enabled}.
        :param warm_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#warm_type ElasticsearchDomain#warm_type}.
        :param zone_awareness_config: zone_awareness_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#zone_awareness_config ElasticsearchDomain#zone_awareness_config}
        :param zone_awareness_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#zone_awareness_enabled ElasticsearchDomain#zone_awareness_enabled}.
        '''
        if isinstance(cold_storage_options, dict):
            cold_storage_options = ElasticsearchDomainClusterConfigColdStorageOptions(**cold_storage_options)
        if isinstance(zone_awareness_config, dict):
            zone_awareness_config = ElasticsearchDomainClusterConfigZoneAwarenessConfig(**zone_awareness_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1214cfcffe1730ba09b21e6e40685c1512a6d383eb2d56ab535c04456cf411e9)
            check_type(argname="argument cold_storage_options", value=cold_storage_options, expected_type=type_hints["cold_storage_options"])
            check_type(argname="argument dedicated_master_count", value=dedicated_master_count, expected_type=type_hints["dedicated_master_count"])
            check_type(argname="argument dedicated_master_enabled", value=dedicated_master_enabled, expected_type=type_hints["dedicated_master_enabled"])
            check_type(argname="argument dedicated_master_type", value=dedicated_master_type, expected_type=type_hints["dedicated_master_type"])
            check_type(argname="argument instance_count", value=instance_count, expected_type=type_hints["instance_count"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument warm_count", value=warm_count, expected_type=type_hints["warm_count"])
            check_type(argname="argument warm_enabled", value=warm_enabled, expected_type=type_hints["warm_enabled"])
            check_type(argname="argument warm_type", value=warm_type, expected_type=type_hints["warm_type"])
            check_type(argname="argument zone_awareness_config", value=zone_awareness_config, expected_type=type_hints["zone_awareness_config"])
            check_type(argname="argument zone_awareness_enabled", value=zone_awareness_enabled, expected_type=type_hints["zone_awareness_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cold_storage_options is not None:
            self._values["cold_storage_options"] = cold_storage_options
        if dedicated_master_count is not None:
            self._values["dedicated_master_count"] = dedicated_master_count
        if dedicated_master_enabled is not None:
            self._values["dedicated_master_enabled"] = dedicated_master_enabled
        if dedicated_master_type is not None:
            self._values["dedicated_master_type"] = dedicated_master_type
        if instance_count is not None:
            self._values["instance_count"] = instance_count
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if warm_count is not None:
            self._values["warm_count"] = warm_count
        if warm_enabled is not None:
            self._values["warm_enabled"] = warm_enabled
        if warm_type is not None:
            self._values["warm_type"] = warm_type
        if zone_awareness_config is not None:
            self._values["zone_awareness_config"] = zone_awareness_config
        if zone_awareness_enabled is not None:
            self._values["zone_awareness_enabled"] = zone_awareness_enabled

    @builtins.property
    def cold_storage_options(
        self,
    ) -> typing.Optional["ElasticsearchDomainClusterConfigColdStorageOptions"]:
        '''cold_storage_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#cold_storage_options ElasticsearchDomain#cold_storage_options}
        '''
        result = self._values.get("cold_storage_options")
        return typing.cast(typing.Optional["ElasticsearchDomainClusterConfigColdStorageOptions"], result)

    @builtins.property
    def dedicated_master_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#dedicated_master_count ElasticsearchDomain#dedicated_master_count}.'''
        result = self._values.get("dedicated_master_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dedicated_master_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#dedicated_master_enabled ElasticsearchDomain#dedicated_master_enabled}.'''
        result = self._values.get("dedicated_master_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dedicated_master_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#dedicated_master_type ElasticsearchDomain#dedicated_master_type}.'''
        result = self._values.get("dedicated_master_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#instance_count ElasticsearchDomain#instance_count}.'''
        result = self._values.get("instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#instance_type ElasticsearchDomain#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def warm_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#warm_count ElasticsearchDomain#warm_count}.'''
        result = self._values.get("warm_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def warm_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#warm_enabled ElasticsearchDomain#warm_enabled}.'''
        result = self._values.get("warm_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def warm_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#warm_type ElasticsearchDomain#warm_type}.'''
        result = self._values.get("warm_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone_awareness_config(
        self,
    ) -> typing.Optional["ElasticsearchDomainClusterConfigZoneAwarenessConfig"]:
        '''zone_awareness_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#zone_awareness_config ElasticsearchDomain#zone_awareness_config}
        '''
        result = self._values.get("zone_awareness_config")
        return typing.cast(typing.Optional["ElasticsearchDomainClusterConfigZoneAwarenessConfig"], result)

    @builtins.property
    def zone_awareness_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#zone_awareness_enabled ElasticsearchDomain#zone_awareness_enabled}.'''
        result = self._values.get("zone_awareness_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticsearchDomainClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainClusterConfigColdStorageOptions",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class ElasticsearchDomainClusterConfigColdStorageOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#enabled ElasticsearchDomain#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0b4d24bee8776d655f77fbc343cb98ed3278038226a971e23588c7695b1772b)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#enabled ElasticsearchDomain#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticsearchDomainClusterConfigColdStorageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElasticsearchDomainClusterConfigColdStorageOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainClusterConfigColdStorageOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35cec65f11daee298ad4491f8567a4d77ed416285daf5c38aa23d8ad5f215e53)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1979602716c47c46893e50520c38d6281cfa9ca5f48543c2c97130145bb513e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ElasticsearchDomainClusterConfigColdStorageOptions]:
        return typing.cast(typing.Optional[ElasticsearchDomainClusterConfigColdStorageOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElasticsearchDomainClusterConfigColdStorageOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c512f8d1bebf2b2d9d76b45597500c75dd85f849146406c946b91f00dee8c14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ElasticsearchDomainClusterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainClusterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a97001b372843c2afe805559fb6d51c0cadeba34d9f19cbafdc58de5a0211096)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putColdStorageOptions")
    def put_cold_storage_options(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#enabled ElasticsearchDomain#enabled}.
        '''
        value = ElasticsearchDomainClusterConfigColdStorageOptions(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putColdStorageOptions", [value]))

    @jsii.member(jsii_name="putZoneAwarenessConfig")
    def put_zone_awareness_config(
        self,
        *,
        availability_zone_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param availability_zone_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#availability_zone_count ElasticsearchDomain#availability_zone_count}.
        '''
        value = ElasticsearchDomainClusterConfigZoneAwarenessConfig(
            availability_zone_count=availability_zone_count
        )

        return typing.cast(None, jsii.invoke(self, "putZoneAwarenessConfig", [value]))

    @jsii.member(jsii_name="resetColdStorageOptions")
    def reset_cold_storage_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColdStorageOptions", []))

    @jsii.member(jsii_name="resetDedicatedMasterCount")
    def reset_dedicated_master_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDedicatedMasterCount", []))

    @jsii.member(jsii_name="resetDedicatedMasterEnabled")
    def reset_dedicated_master_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDedicatedMasterEnabled", []))

    @jsii.member(jsii_name="resetDedicatedMasterType")
    def reset_dedicated_master_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDedicatedMasterType", []))

    @jsii.member(jsii_name="resetInstanceCount")
    def reset_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceCount", []))

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetWarmCount")
    def reset_warm_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarmCount", []))

    @jsii.member(jsii_name="resetWarmEnabled")
    def reset_warm_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarmEnabled", []))

    @jsii.member(jsii_name="resetWarmType")
    def reset_warm_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarmType", []))

    @jsii.member(jsii_name="resetZoneAwarenessConfig")
    def reset_zone_awareness_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneAwarenessConfig", []))

    @jsii.member(jsii_name="resetZoneAwarenessEnabled")
    def reset_zone_awareness_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneAwarenessEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="coldStorageOptions")
    def cold_storage_options(
        self,
    ) -> ElasticsearchDomainClusterConfigColdStorageOptionsOutputReference:
        return typing.cast(ElasticsearchDomainClusterConfigColdStorageOptionsOutputReference, jsii.get(self, "coldStorageOptions"))

    @builtins.property
    @jsii.member(jsii_name="zoneAwarenessConfig")
    def zone_awareness_config(
        self,
    ) -> "ElasticsearchDomainClusterConfigZoneAwarenessConfigOutputReference":
        return typing.cast("ElasticsearchDomainClusterConfigZoneAwarenessConfigOutputReference", jsii.get(self, "zoneAwarenessConfig"))

    @builtins.property
    @jsii.member(jsii_name="coldStorageOptionsInput")
    def cold_storage_options_input(
        self,
    ) -> typing.Optional[ElasticsearchDomainClusterConfigColdStorageOptions]:
        return typing.cast(typing.Optional[ElasticsearchDomainClusterConfigColdStorageOptions], jsii.get(self, "coldStorageOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedMasterCountInput")
    def dedicated_master_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dedicatedMasterCountInput"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedMasterEnabledInput")
    def dedicated_master_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dedicatedMasterEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedMasterTypeInput")
    def dedicated_master_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dedicatedMasterTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceCountInput")
    def instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "instanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="warmCountInput")
    def warm_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "warmCountInput"))

    @builtins.property
    @jsii.member(jsii_name="warmEnabledInput")
    def warm_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "warmEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="warmTypeInput")
    def warm_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "warmTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneAwarenessConfigInput")
    def zone_awareness_config_input(
        self,
    ) -> typing.Optional["ElasticsearchDomainClusterConfigZoneAwarenessConfig"]:
        return typing.cast(typing.Optional["ElasticsearchDomainClusterConfigZoneAwarenessConfig"], jsii.get(self, "zoneAwarenessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneAwarenessEnabledInput")
    def zone_awareness_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "zoneAwarenessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedMasterCount")
    def dedicated_master_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dedicatedMasterCount"))

    @dedicated_master_count.setter
    def dedicated_master_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4e0675ba84f05df4425db2dea4a5452b5630a89193965fddc74be1192347e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dedicatedMasterCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dedicatedMasterEnabled")
    def dedicated_master_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dedicatedMasterEnabled"))

    @dedicated_master_enabled.setter
    def dedicated_master_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67fa70279248d69dbbd9f2c3940f62584f3142ea76f8e610b2ef65cea7098eac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dedicatedMasterEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dedicatedMasterType")
    def dedicated_master_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dedicatedMasterType"))

    @dedicated_master_type.setter
    def dedicated_master_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f605ddb9437dd658259cb80e15e6ab139cf8f221d429fab1d2a5678a9a0a4b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dedicatedMasterType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceCount")
    def instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instanceCount"))

    @instance_count.setter
    def instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36362a2adc61f455726180718e500423ffcc01d2d101f3ce0bb1f0d90f3a581c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ff4e4737cacc883bb1dad1e0b667c057d4228d7c83306c87d6ac57747db01db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warmCount")
    def warm_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "warmCount"))

    @warm_count.setter
    def warm_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c161484c580455f1a397933cda6305470ddb8ea91b841ea643c8dd4177de98f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warmCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warmEnabled")
    def warm_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "warmEnabled"))

    @warm_enabled.setter
    def warm_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1cab310d1a8688f6c6ae95901f9e49de2ccf9ff1dbb0c36b28ed88bf34b2117)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warmEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warmType")
    def warm_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warmType"))

    @warm_type.setter
    def warm_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4af88a75a7623ea48c9a7a099c88f1ae4166058cab75ddc7794c6421d5a95f69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warmType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zoneAwarenessEnabled")
    def zone_awareness_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "zoneAwarenessEnabled"))

    @zone_awareness_enabled.setter
    def zone_awareness_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49c988d434d78a27a88a08ff52038a5fe00e923cd80003fbd8a5434b28f4d2a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneAwarenessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ElasticsearchDomainClusterConfig]:
        return typing.cast(typing.Optional[ElasticsearchDomainClusterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElasticsearchDomainClusterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dacce7ed52593f0e3fa94dfedb66d95537c7a498c78d221023ab439f692c407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainClusterConfigZoneAwarenessConfig",
    jsii_struct_bases=[],
    name_mapping={"availability_zone_count": "availabilityZoneCount"},
)
class ElasticsearchDomainClusterConfigZoneAwarenessConfig:
    def __init__(
        self,
        *,
        availability_zone_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param availability_zone_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#availability_zone_count ElasticsearchDomain#availability_zone_count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2acbc49788baf7f7c922f5a0ac55cba1d5e913418282fe4c2caffec3d6af4ea7)
            check_type(argname="argument availability_zone_count", value=availability_zone_count, expected_type=type_hints["availability_zone_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zone_count is not None:
            self._values["availability_zone_count"] = availability_zone_count

    @builtins.property
    def availability_zone_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#availability_zone_count ElasticsearchDomain#availability_zone_count}.'''
        result = self._values.get("availability_zone_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticsearchDomainClusterConfigZoneAwarenessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElasticsearchDomainClusterConfigZoneAwarenessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainClusterConfigZoneAwarenessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af1425119dc0c4ef219ac59943dbee34e6dd47b01a7e6d9da7007ddf9fbbd0f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailabilityZoneCount")
    def reset_availability_zone_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityZoneCount", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneCountInput")
    def availability_zone_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "availabilityZoneCountInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneCount")
    def availability_zone_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "availabilityZoneCount"))

    @availability_zone_count.setter
    def availability_zone_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ae54f98bfc939dd0b3ccb347684106ce3a5a29f62454648cb7a8874016321d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZoneCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ElasticsearchDomainClusterConfigZoneAwarenessConfig]:
        return typing.cast(typing.Optional[ElasticsearchDomainClusterConfigZoneAwarenessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElasticsearchDomainClusterConfigZoneAwarenessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__100a1795ec967390268f80ae82a3bd83addadcc38dca96722aa7c2723939ddcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainCognitoOptions",
    jsii_struct_bases=[],
    name_mapping={
        "identity_pool_id": "identityPoolId",
        "role_arn": "roleArn",
        "user_pool_id": "userPoolId",
        "enabled": "enabled",
    },
)
class ElasticsearchDomainCognitoOptions:
    def __init__(
        self,
        *,
        identity_pool_id: builtins.str,
        role_arn: builtins.str,
        user_pool_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param identity_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#identity_pool_id ElasticsearchDomain#identity_pool_id}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#role_arn ElasticsearchDomain#role_arn}.
        :param user_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#user_pool_id ElasticsearchDomain#user_pool_id}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#enabled ElasticsearchDomain#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__178dad721ef0b8b2d58ac829c8a6674d5eb2497a81c82da5606eb663efe1126b)
            check_type(argname="argument identity_pool_id", value=identity_pool_id, expected_type=type_hints["identity_pool_id"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "identity_pool_id": identity_pool_id,
            "role_arn": role_arn,
            "user_pool_id": user_pool_id,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def identity_pool_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#identity_pool_id ElasticsearchDomain#identity_pool_id}.'''
        result = self._values.get("identity_pool_id")
        assert result is not None, "Required property 'identity_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#role_arn ElasticsearchDomain#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_pool_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#user_pool_id ElasticsearchDomain#user_pool_id}.'''
        result = self._values.get("user_pool_id")
        assert result is not None, "Required property 'user_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#enabled ElasticsearchDomain#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticsearchDomainCognitoOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElasticsearchDomainCognitoOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainCognitoOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05045a3da1daf1e4c4febc7a147d2af1bcac1104c06e115e567d26f1f490a8e4)
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
    @jsii.member(jsii_name="identityPoolIdInput")
    def identity_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="userPoolIdInput")
    def user_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPoolIdInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__dca21830eb6e0f85dfadc36492f39e06fb95ca3f74b6d48b8c3eb5bb519c2c28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityPoolId")
    def identity_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityPoolId"))

    @identity_pool_id.setter
    def identity_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__331e3cc26df5ed3f6edb25d5c06b85cdb5335de39bd8237b6f96675f8f4d633e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityPoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b35b384ccd882e3653937ea58942134ddfd3cdfa6f392797b802a13b567b2e78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPoolId")
    def user_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPoolId"))

    @user_pool_id.setter
    def user_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1de51d3f3b86d420274724c1935fdfbdd966442f14dcbb55f2dfa3b7b9b893c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ElasticsearchDomainCognitoOptions]:
        return typing.cast(typing.Optional[ElasticsearchDomainCognitoOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElasticsearchDomainCognitoOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bd2d765c1c118058fe1bf25bf39e1ada69b3992b1f36dd1a0546ec180fb0c4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "domain_name": "domainName",
        "access_policies": "accessPolicies",
        "advanced_options": "advancedOptions",
        "advanced_security_options": "advancedSecurityOptions",
        "auto_tune_options": "autoTuneOptions",
        "cluster_config": "clusterConfig",
        "cognito_options": "cognitoOptions",
        "domain_endpoint_options": "domainEndpointOptions",
        "ebs_options": "ebsOptions",
        "elasticsearch_version": "elasticsearchVersion",
        "encrypt_at_rest": "encryptAtRest",
        "id": "id",
        "log_publishing_options": "logPublishingOptions",
        "node_to_node_encryption": "nodeToNodeEncryption",
        "region": "region",
        "snapshot_options": "snapshotOptions",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
        "vpc_options": "vpcOptions",
    },
)
class ElasticsearchDomainConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        domain_name: builtins.str,
        access_policies: typing.Optional[builtins.str] = None,
        advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        advanced_security_options: typing.Optional[typing.Union[ElasticsearchDomainAdvancedSecurityOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_tune_options: typing.Optional[typing.Union[ElasticsearchDomainAutoTuneOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_config: typing.Optional[typing.Union[ElasticsearchDomainClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        cognito_options: typing.Optional[typing.Union[ElasticsearchDomainCognitoOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        domain_endpoint_options: typing.Optional[typing.Union["ElasticsearchDomainDomainEndpointOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        ebs_options: typing.Optional[typing.Union["ElasticsearchDomainEbsOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        elasticsearch_version: typing.Optional[builtins.str] = None,
        encrypt_at_rest: typing.Optional[typing.Union["ElasticsearchDomainEncryptAtRest", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        log_publishing_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ElasticsearchDomainLogPublishingOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        node_to_node_encryption: typing.Optional[typing.Union["ElasticsearchDomainNodeToNodeEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        snapshot_options: typing.Optional[typing.Union["ElasticsearchDomainSnapshotOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ElasticsearchDomainTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_options: typing.Optional[typing.Union["ElasticsearchDomainVpcOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#domain_name ElasticsearchDomain#domain_name}.
        :param access_policies: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#access_policies ElasticsearchDomain#access_policies}.
        :param advanced_options: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#advanced_options ElasticsearchDomain#advanced_options}.
        :param advanced_security_options: advanced_security_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#advanced_security_options ElasticsearchDomain#advanced_security_options}
        :param auto_tune_options: auto_tune_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#auto_tune_options ElasticsearchDomain#auto_tune_options}
        :param cluster_config: cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#cluster_config ElasticsearchDomain#cluster_config}
        :param cognito_options: cognito_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#cognito_options ElasticsearchDomain#cognito_options}
        :param domain_endpoint_options: domain_endpoint_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#domain_endpoint_options ElasticsearchDomain#domain_endpoint_options}
        :param ebs_options: ebs_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#ebs_options ElasticsearchDomain#ebs_options}
        :param elasticsearch_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#elasticsearch_version ElasticsearchDomain#elasticsearch_version}.
        :param encrypt_at_rest: encrypt_at_rest block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#encrypt_at_rest ElasticsearchDomain#encrypt_at_rest}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#id ElasticsearchDomain#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_publishing_options: log_publishing_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#log_publishing_options ElasticsearchDomain#log_publishing_options}
        :param node_to_node_encryption: node_to_node_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#node_to_node_encryption ElasticsearchDomain#node_to_node_encryption}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#region ElasticsearchDomain#region}
        :param snapshot_options: snapshot_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#snapshot_options ElasticsearchDomain#snapshot_options}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#tags ElasticsearchDomain#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#tags_all ElasticsearchDomain#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#timeouts ElasticsearchDomain#timeouts}
        :param vpc_options: vpc_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#vpc_options ElasticsearchDomain#vpc_options}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(advanced_security_options, dict):
            advanced_security_options = ElasticsearchDomainAdvancedSecurityOptions(**advanced_security_options)
        if isinstance(auto_tune_options, dict):
            auto_tune_options = ElasticsearchDomainAutoTuneOptions(**auto_tune_options)
        if isinstance(cluster_config, dict):
            cluster_config = ElasticsearchDomainClusterConfig(**cluster_config)
        if isinstance(cognito_options, dict):
            cognito_options = ElasticsearchDomainCognitoOptions(**cognito_options)
        if isinstance(domain_endpoint_options, dict):
            domain_endpoint_options = ElasticsearchDomainDomainEndpointOptions(**domain_endpoint_options)
        if isinstance(ebs_options, dict):
            ebs_options = ElasticsearchDomainEbsOptions(**ebs_options)
        if isinstance(encrypt_at_rest, dict):
            encrypt_at_rest = ElasticsearchDomainEncryptAtRest(**encrypt_at_rest)
        if isinstance(node_to_node_encryption, dict):
            node_to_node_encryption = ElasticsearchDomainNodeToNodeEncryption(**node_to_node_encryption)
        if isinstance(snapshot_options, dict):
            snapshot_options = ElasticsearchDomainSnapshotOptions(**snapshot_options)
        if isinstance(timeouts, dict):
            timeouts = ElasticsearchDomainTimeouts(**timeouts)
        if isinstance(vpc_options, dict):
            vpc_options = ElasticsearchDomainVpcOptions(**vpc_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__881cbe09c1e51db5121c0db093e29c090508a2475f8be47c13d2c1e6423e648f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument access_policies", value=access_policies, expected_type=type_hints["access_policies"])
            check_type(argname="argument advanced_options", value=advanced_options, expected_type=type_hints["advanced_options"])
            check_type(argname="argument advanced_security_options", value=advanced_security_options, expected_type=type_hints["advanced_security_options"])
            check_type(argname="argument auto_tune_options", value=auto_tune_options, expected_type=type_hints["auto_tune_options"])
            check_type(argname="argument cluster_config", value=cluster_config, expected_type=type_hints["cluster_config"])
            check_type(argname="argument cognito_options", value=cognito_options, expected_type=type_hints["cognito_options"])
            check_type(argname="argument domain_endpoint_options", value=domain_endpoint_options, expected_type=type_hints["domain_endpoint_options"])
            check_type(argname="argument ebs_options", value=ebs_options, expected_type=type_hints["ebs_options"])
            check_type(argname="argument elasticsearch_version", value=elasticsearch_version, expected_type=type_hints["elasticsearch_version"])
            check_type(argname="argument encrypt_at_rest", value=encrypt_at_rest, expected_type=type_hints["encrypt_at_rest"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_publishing_options", value=log_publishing_options, expected_type=type_hints["log_publishing_options"])
            check_type(argname="argument node_to_node_encryption", value=node_to_node_encryption, expected_type=type_hints["node_to_node_encryption"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument snapshot_options", value=snapshot_options, expected_type=type_hints["snapshot_options"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument vpc_options", value=vpc_options, expected_type=type_hints["vpc_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
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
        if access_policies is not None:
            self._values["access_policies"] = access_policies
        if advanced_options is not None:
            self._values["advanced_options"] = advanced_options
        if advanced_security_options is not None:
            self._values["advanced_security_options"] = advanced_security_options
        if auto_tune_options is not None:
            self._values["auto_tune_options"] = auto_tune_options
        if cluster_config is not None:
            self._values["cluster_config"] = cluster_config
        if cognito_options is not None:
            self._values["cognito_options"] = cognito_options
        if domain_endpoint_options is not None:
            self._values["domain_endpoint_options"] = domain_endpoint_options
        if ebs_options is not None:
            self._values["ebs_options"] = ebs_options
        if elasticsearch_version is not None:
            self._values["elasticsearch_version"] = elasticsearch_version
        if encrypt_at_rest is not None:
            self._values["encrypt_at_rest"] = encrypt_at_rest
        if id is not None:
            self._values["id"] = id
        if log_publishing_options is not None:
            self._values["log_publishing_options"] = log_publishing_options
        if node_to_node_encryption is not None:
            self._values["node_to_node_encryption"] = node_to_node_encryption
        if region is not None:
            self._values["region"] = region
        if snapshot_options is not None:
            self._values["snapshot_options"] = snapshot_options
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if vpc_options is not None:
            self._values["vpc_options"] = vpc_options

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
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#domain_name ElasticsearchDomain#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_policies(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#access_policies ElasticsearchDomain#access_policies}.'''
        result = self._values.get("access_policies")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def advanced_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#advanced_options ElasticsearchDomain#advanced_options}.'''
        result = self._values.get("advanced_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def advanced_security_options(
        self,
    ) -> typing.Optional[ElasticsearchDomainAdvancedSecurityOptions]:
        '''advanced_security_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#advanced_security_options ElasticsearchDomain#advanced_security_options}
        '''
        result = self._values.get("advanced_security_options")
        return typing.cast(typing.Optional[ElasticsearchDomainAdvancedSecurityOptions], result)

    @builtins.property
    def auto_tune_options(self) -> typing.Optional[ElasticsearchDomainAutoTuneOptions]:
        '''auto_tune_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#auto_tune_options ElasticsearchDomain#auto_tune_options}
        '''
        result = self._values.get("auto_tune_options")
        return typing.cast(typing.Optional[ElasticsearchDomainAutoTuneOptions], result)

    @builtins.property
    def cluster_config(self) -> typing.Optional[ElasticsearchDomainClusterConfig]:
        '''cluster_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#cluster_config ElasticsearchDomain#cluster_config}
        '''
        result = self._values.get("cluster_config")
        return typing.cast(typing.Optional[ElasticsearchDomainClusterConfig], result)

    @builtins.property
    def cognito_options(self) -> typing.Optional[ElasticsearchDomainCognitoOptions]:
        '''cognito_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#cognito_options ElasticsearchDomain#cognito_options}
        '''
        result = self._values.get("cognito_options")
        return typing.cast(typing.Optional[ElasticsearchDomainCognitoOptions], result)

    @builtins.property
    def domain_endpoint_options(
        self,
    ) -> typing.Optional["ElasticsearchDomainDomainEndpointOptions"]:
        '''domain_endpoint_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#domain_endpoint_options ElasticsearchDomain#domain_endpoint_options}
        '''
        result = self._values.get("domain_endpoint_options")
        return typing.cast(typing.Optional["ElasticsearchDomainDomainEndpointOptions"], result)

    @builtins.property
    def ebs_options(self) -> typing.Optional["ElasticsearchDomainEbsOptions"]:
        '''ebs_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#ebs_options ElasticsearchDomain#ebs_options}
        '''
        result = self._values.get("ebs_options")
        return typing.cast(typing.Optional["ElasticsearchDomainEbsOptions"], result)

    @builtins.property
    def elasticsearch_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#elasticsearch_version ElasticsearchDomain#elasticsearch_version}.'''
        result = self._values.get("elasticsearch_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encrypt_at_rest(self) -> typing.Optional["ElasticsearchDomainEncryptAtRest"]:
        '''encrypt_at_rest block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#encrypt_at_rest ElasticsearchDomain#encrypt_at_rest}
        '''
        result = self._values.get("encrypt_at_rest")
        return typing.cast(typing.Optional["ElasticsearchDomainEncryptAtRest"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#id ElasticsearchDomain#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_publishing_options(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElasticsearchDomainLogPublishingOptions"]]]:
        '''log_publishing_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#log_publishing_options ElasticsearchDomain#log_publishing_options}
        '''
        result = self._values.get("log_publishing_options")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ElasticsearchDomainLogPublishingOptions"]]], result)

    @builtins.property
    def node_to_node_encryption(
        self,
    ) -> typing.Optional["ElasticsearchDomainNodeToNodeEncryption"]:
        '''node_to_node_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#node_to_node_encryption ElasticsearchDomain#node_to_node_encryption}
        '''
        result = self._values.get("node_to_node_encryption")
        return typing.cast(typing.Optional["ElasticsearchDomainNodeToNodeEncryption"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#region ElasticsearchDomain#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_options(self) -> typing.Optional["ElasticsearchDomainSnapshotOptions"]:
        '''snapshot_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#snapshot_options ElasticsearchDomain#snapshot_options}
        '''
        result = self._values.get("snapshot_options")
        return typing.cast(typing.Optional["ElasticsearchDomainSnapshotOptions"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#tags ElasticsearchDomain#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#tags_all ElasticsearchDomain#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ElasticsearchDomainTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#timeouts ElasticsearchDomain#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ElasticsearchDomainTimeouts"], result)

    @builtins.property
    def vpc_options(self) -> typing.Optional["ElasticsearchDomainVpcOptions"]:
        '''vpc_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#vpc_options ElasticsearchDomain#vpc_options}
        '''
        result = self._values.get("vpc_options")
        return typing.cast(typing.Optional["ElasticsearchDomainVpcOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticsearchDomainConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainDomainEndpointOptions",
    jsii_struct_bases=[],
    name_mapping={
        "custom_endpoint": "customEndpoint",
        "custom_endpoint_certificate_arn": "customEndpointCertificateArn",
        "custom_endpoint_enabled": "customEndpointEnabled",
        "enforce_https": "enforceHttps",
        "tls_security_policy": "tlsSecurityPolicy",
    },
)
class ElasticsearchDomainDomainEndpointOptions:
    def __init__(
        self,
        *,
        custom_endpoint: typing.Optional[builtins.str] = None,
        custom_endpoint_certificate_arn: typing.Optional[builtins.str] = None,
        custom_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enforce_https: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_security_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#custom_endpoint ElasticsearchDomain#custom_endpoint}.
        :param custom_endpoint_certificate_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#custom_endpoint_certificate_arn ElasticsearchDomain#custom_endpoint_certificate_arn}.
        :param custom_endpoint_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#custom_endpoint_enabled ElasticsearchDomain#custom_endpoint_enabled}.
        :param enforce_https: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#enforce_https ElasticsearchDomain#enforce_https}.
        :param tls_security_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#tls_security_policy ElasticsearchDomain#tls_security_policy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37dca1417b3003b915f1c076adf2a63d36fbc525a44965d41723961a7fd5ccda)
            check_type(argname="argument custom_endpoint", value=custom_endpoint, expected_type=type_hints["custom_endpoint"])
            check_type(argname="argument custom_endpoint_certificate_arn", value=custom_endpoint_certificate_arn, expected_type=type_hints["custom_endpoint_certificate_arn"])
            check_type(argname="argument custom_endpoint_enabled", value=custom_endpoint_enabled, expected_type=type_hints["custom_endpoint_enabled"])
            check_type(argname="argument enforce_https", value=enforce_https, expected_type=type_hints["enforce_https"])
            check_type(argname="argument tls_security_policy", value=tls_security_policy, expected_type=type_hints["tls_security_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_endpoint is not None:
            self._values["custom_endpoint"] = custom_endpoint
        if custom_endpoint_certificate_arn is not None:
            self._values["custom_endpoint_certificate_arn"] = custom_endpoint_certificate_arn
        if custom_endpoint_enabled is not None:
            self._values["custom_endpoint_enabled"] = custom_endpoint_enabled
        if enforce_https is not None:
            self._values["enforce_https"] = enforce_https
        if tls_security_policy is not None:
            self._values["tls_security_policy"] = tls_security_policy

    @builtins.property
    def custom_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#custom_endpoint ElasticsearchDomain#custom_endpoint}.'''
        result = self._values.get("custom_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_endpoint_certificate_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#custom_endpoint_certificate_arn ElasticsearchDomain#custom_endpoint_certificate_arn}.'''
        result = self._values.get("custom_endpoint_certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_endpoint_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#custom_endpoint_enabled ElasticsearchDomain#custom_endpoint_enabled}.'''
        result = self._values.get("custom_endpoint_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enforce_https(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#enforce_https ElasticsearchDomain#enforce_https}.'''
        result = self._values.get("enforce_https")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tls_security_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#tls_security_policy ElasticsearchDomain#tls_security_policy}.'''
        result = self._values.get("tls_security_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticsearchDomainDomainEndpointOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElasticsearchDomainDomainEndpointOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainDomainEndpointOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7a5644813e69d43967d7ef784c14c06e829ad6b0bece49985410a5c668e3294)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCustomEndpoint")
    def reset_custom_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomEndpoint", []))

    @jsii.member(jsii_name="resetCustomEndpointCertificateArn")
    def reset_custom_endpoint_certificate_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomEndpointCertificateArn", []))

    @jsii.member(jsii_name="resetCustomEndpointEnabled")
    def reset_custom_endpoint_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomEndpointEnabled", []))

    @jsii.member(jsii_name="resetEnforceHttps")
    def reset_enforce_https(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceHttps", []))

    @jsii.member(jsii_name="resetTlsSecurityPolicy")
    def reset_tls_security_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsSecurityPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="customEndpointCertificateArnInput")
    def custom_endpoint_certificate_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customEndpointCertificateArnInput"))

    @builtins.property
    @jsii.member(jsii_name="customEndpointEnabledInput")
    def custom_endpoint_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "customEndpointEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="customEndpointInput")
    def custom_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceHttpsInput")
    def enforce_https_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforceHttpsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsSecurityPolicyInput")
    def tls_security_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsSecurityPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="customEndpoint")
    def custom_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customEndpoint"))

    @custom_endpoint.setter
    def custom_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85247a598aac8c7c3ebe75b64352e9afeda5108f9112cc90e99e75ae0310efac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customEndpointCertificateArn")
    def custom_endpoint_certificate_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customEndpointCertificateArn"))

    @custom_endpoint_certificate_arn.setter
    def custom_endpoint_certificate_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c9ed1fcf5e015c8be4ee1e22d963390d5820a0ab28b15dd3e253284f2c596a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customEndpointCertificateArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customEndpointEnabled")
    def custom_endpoint_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "customEndpointEnabled"))

    @custom_endpoint_enabled.setter
    def custom_endpoint_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fac8dfd5fadc3b8e7201468d5e384502f96016eb524f5adeaf4b78837c985e57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customEndpointEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceHttps")
    def enforce_https(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforceHttps"))

    @enforce_https.setter
    def enforce_https(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c6e860b08d56473a58ec006a290bfe43176cdd9845f101746fefa56ee7b670d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceHttps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsSecurityPolicy")
    def tls_security_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsSecurityPolicy"))

    @tls_security_policy.setter
    def tls_security_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d852f4476e7567ebf341f805981a3d4c52cb9fb7204d52414de9a87f12a9243f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsSecurityPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ElasticsearchDomainDomainEndpointOptions]:
        return typing.cast(typing.Optional[ElasticsearchDomainDomainEndpointOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElasticsearchDomainDomainEndpointOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d54645d1718cf2928c61c7b70aedf6885829d3394208d46666e421687059b2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainEbsOptions",
    jsii_struct_bases=[],
    name_mapping={
        "ebs_enabled": "ebsEnabled",
        "iops": "iops",
        "throughput": "throughput",
        "volume_size": "volumeSize",
        "volume_type": "volumeType",
    },
)
class ElasticsearchDomainEbsOptions:
    def __init__(
        self,
        *,
        ebs_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        iops: typing.Optional[jsii.Number] = None,
        throughput: typing.Optional[jsii.Number] = None,
        volume_size: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ebs_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#ebs_enabled ElasticsearchDomain#ebs_enabled}.
        :param iops: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#iops ElasticsearchDomain#iops}.
        :param throughput: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#throughput ElasticsearchDomain#throughput}.
        :param volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#volume_size ElasticsearchDomain#volume_size}.
        :param volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#volume_type ElasticsearchDomain#volume_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39263d432faa103f708e1a9dc8487b5f68db1e403dcd952889d01070f1bb54f8)
            check_type(argname="argument ebs_enabled", value=ebs_enabled, expected_type=type_hints["ebs_enabled"])
            check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
            check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
            check_type(argname="argument volume_size", value=volume_size, expected_type=type_hints["volume_size"])
            check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ebs_enabled": ebs_enabled,
        }
        if iops is not None:
            self._values["iops"] = iops
        if throughput is not None:
            self._values["throughput"] = throughput
        if volume_size is not None:
            self._values["volume_size"] = volume_size
        if volume_type is not None:
            self._values["volume_type"] = volume_type

    @builtins.property
    def ebs_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#ebs_enabled ElasticsearchDomain#ebs_enabled}.'''
        result = self._values.get("ebs_enabled")
        assert result is not None, "Required property 'ebs_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#iops ElasticsearchDomain#iops}.'''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throughput(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#throughput ElasticsearchDomain#throughput}.'''
        result = self._values.get("throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#volume_size ElasticsearchDomain#volume_size}.'''
        result = self._values.get("volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#volume_type ElasticsearchDomain#volume_type}.'''
        result = self._values.get("volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticsearchDomainEbsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElasticsearchDomainEbsOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainEbsOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6591b84809ce07f9d83acf519cea72ee842bb14d3d1e1bbce254661820b7ff7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIops")
    def reset_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIops", []))

    @jsii.member(jsii_name="resetThroughput")
    def reset_throughput(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThroughput", []))

    @jsii.member(jsii_name="resetVolumeSize")
    def reset_volume_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeSize", []))

    @jsii.member(jsii_name="resetVolumeType")
    def reset_volume_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeType", []))

    @builtins.property
    @jsii.member(jsii_name="ebsEnabledInput")
    def ebs_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ebsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="iopsInput")
    def iops_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "iopsInput"))

    @builtins.property
    @jsii.member(jsii_name="throughputInput")
    def throughput_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throughputInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeSizeInput")
    def volume_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "volumeSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeTypeInput")
    def volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="ebsEnabled")
    def ebs_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ebsEnabled"))

    @ebs_enabled.setter
    def ebs_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__062409b1c41f8f9af464a917cdc17db350c0d09a92b3a179aa71e0e3874c600f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iops")
    def iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "iops"))

    @iops.setter
    def iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef11070d1694f140a9742e7d74d6810d8b02dffa21aef5548784d9d7ff29e234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="throughput")
    def throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throughput"))

    @throughput.setter
    def throughput(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e227db24c423a08fa89fe970ea4cd0606abb58ea81cf0b241ad089f62257135)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throughput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeSize")
    def volume_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "volumeSize"))

    @volume_size.setter
    def volume_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ef5d34b4c13e7832ec2a7c0da7aefcfe40a31f3058849a89b2f8f2d44c172a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeType")
    def volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeType"))

    @volume_type.setter
    def volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a8025f9ed54e1bdab09fb8007bd96aa8f0086f4845e7823f47b6c418c3045a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ElasticsearchDomainEbsOptions]:
        return typing.cast(typing.Optional[ElasticsearchDomainEbsOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElasticsearchDomainEbsOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c34324c993285672ddc88d659f2784d51610b46a62f83b38c4ec4424cb2272c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainEncryptAtRest",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "kms_key_id": "kmsKeyId"},
)
class ElasticsearchDomainEncryptAtRest:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        kms_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#enabled ElasticsearchDomain#enabled}.
        :param kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#kms_key_id ElasticsearchDomain#kms_key_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa1436d6e79412ee7314a9ff37d3225670adee70f346c6e3e32f06eaf0758b9)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#enabled ElasticsearchDomain#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#kms_key_id ElasticsearchDomain#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticsearchDomainEncryptAtRest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElasticsearchDomainEncryptAtRestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainEncryptAtRestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90f699e2c06abcdd0b4b83782c18a17d689da73df1fa816e3944815a9c897909)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__46e8cc6a6571847205a39b8cabe776beb60419e159bf7a18731e5c84562d6096)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__859e3f823ffd1c31b79c11e85820c769c6f834c74ef362d1a0a74622e72b2382)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ElasticsearchDomainEncryptAtRest]:
        return typing.cast(typing.Optional[ElasticsearchDomainEncryptAtRest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElasticsearchDomainEncryptAtRest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c451ec397783a3e4b7ea1b4abefdcc4490259a411931e39a95e7baff295e3b5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainLogPublishingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "cloudwatch_log_group_arn": "cloudwatchLogGroupArn",
        "log_type": "logType",
        "enabled": "enabled",
    },
)
class ElasticsearchDomainLogPublishingOptions:
    def __init__(
        self,
        *,
        cloudwatch_log_group_arn: builtins.str,
        log_type: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cloudwatch_log_group_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#cloudwatch_log_group_arn ElasticsearchDomain#cloudwatch_log_group_arn}.
        :param log_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#log_type ElasticsearchDomain#log_type}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#enabled ElasticsearchDomain#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8f40321b9de7d044754d293b9be24ef3afa3a7777a48d6f5e4af8119264b34)
            check_type(argname="argument cloudwatch_log_group_arn", value=cloudwatch_log_group_arn, expected_type=type_hints["cloudwatch_log_group_arn"])
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloudwatch_log_group_arn": cloudwatch_log_group_arn,
            "log_type": log_type,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def cloudwatch_log_group_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#cloudwatch_log_group_arn ElasticsearchDomain#cloudwatch_log_group_arn}.'''
        result = self._values.get("cloudwatch_log_group_arn")
        assert result is not None, "Required property 'cloudwatch_log_group_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#log_type ElasticsearchDomain#log_type}.'''
        result = self._values.get("log_type")
        assert result is not None, "Required property 'log_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#enabled ElasticsearchDomain#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticsearchDomainLogPublishingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElasticsearchDomainLogPublishingOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainLogPublishingOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0dcf9ace61b5a327f6ce2c29f36f4aa616a052426e0dd4a873ee34e0375cc82d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ElasticsearchDomainLogPublishingOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e1a6ecaccb6c7f04e98168607192d5cc2aeabf9d9d39c21ca8600d1fbcca8c7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ElasticsearchDomainLogPublishingOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4c018b96ddda634bbf70cbce838767f3906310b6b24c897c5fb5c9dcf8d65a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd1c61d0c72f437d145c9d872975fce143e61e97868df3da4d927b8daa7d17f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d166f05ae42be79101daa461bece693fb15488eab82c8bb788e39b173fc91ed5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElasticsearchDomainLogPublishingOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElasticsearchDomainLogPublishingOptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElasticsearchDomainLogPublishingOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__037842c6656635e9cc4c0239a8f49587b4d2ce5adae8fb3d8eabccbf6be78d8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ElasticsearchDomainLogPublishingOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainLogPublishingOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c5e034784956a938fa76482e352fca974f9be07957dde7b728d0de5b3aec336)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogGroupArnInput")
    def cloudwatch_log_group_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudwatchLogGroupArnInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="logTypeInput")
    def log_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchLogGroupArn")
    def cloudwatch_log_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudwatchLogGroupArn"))

    @cloudwatch_log_group_arn.setter
    def cloudwatch_log_group_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2da917e786feb1965c3e14378869b0b39619f8885800d1da8a7358789b2d1b92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudwatchLogGroupArn", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__fc3b71b26e4413108aa877454e51073969a8e26f72856cab17bde6240d50b496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logType")
    def log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))

    @log_type.setter
    def log_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__206ad54e7da2a116f441a67b6eef7c35c497945d46ec610c339aceda59fd3f62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElasticsearchDomainLogPublishingOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElasticsearchDomainLogPublishingOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElasticsearchDomainLogPublishingOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8efb788f8c630634269eb0a9afdf6281c688140d20696fda7be40d3c768ca1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainNodeToNodeEncryption",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class ElasticsearchDomainNodeToNodeEncryption:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#enabled ElasticsearchDomain#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc6de068ba0b35e53e8f830655624137fe1ebd391b0632e655e186df10752ac)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#enabled ElasticsearchDomain#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticsearchDomainNodeToNodeEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElasticsearchDomainNodeToNodeEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainNodeToNodeEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8dcaefe180dbe9fc13008475a65aac855c080c0ace61bb312bebc51525432a71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__f4c646d4413b674ddf2b8303a2c4de9e7f64eec49f3555cc5f2848782cf5f561)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ElasticsearchDomainNodeToNodeEncryption]:
        return typing.cast(typing.Optional[ElasticsearchDomainNodeToNodeEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElasticsearchDomainNodeToNodeEncryption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e48c0447da9ed35f9d32776ee2421ceeba2c9c4efb6ef3b0afac6206ac996670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainSnapshotOptions",
    jsii_struct_bases=[],
    name_mapping={"automated_snapshot_start_hour": "automatedSnapshotStartHour"},
)
class ElasticsearchDomainSnapshotOptions:
    def __init__(self, *, automated_snapshot_start_hour: jsii.Number) -> None:
        '''
        :param automated_snapshot_start_hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#automated_snapshot_start_hour ElasticsearchDomain#automated_snapshot_start_hour}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2557f1764f8e08c5400453f3ec59ef55e474bee8afa0a987159d907c10a2a4a8)
            check_type(argname="argument automated_snapshot_start_hour", value=automated_snapshot_start_hour, expected_type=type_hints["automated_snapshot_start_hour"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "automated_snapshot_start_hour": automated_snapshot_start_hour,
        }

    @builtins.property
    def automated_snapshot_start_hour(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#automated_snapshot_start_hour ElasticsearchDomain#automated_snapshot_start_hour}.'''
        result = self._values.get("automated_snapshot_start_hour")
        assert result is not None, "Required property 'automated_snapshot_start_hour' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticsearchDomainSnapshotOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElasticsearchDomainSnapshotOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainSnapshotOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a21e379b9c1144ad0cee5843d0b63269b02856ed136cbc251dc86e0a7d669f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="automatedSnapshotStartHourInput")
    def automated_snapshot_start_hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "automatedSnapshotStartHourInput"))

    @builtins.property
    @jsii.member(jsii_name="automatedSnapshotStartHour")
    def automated_snapshot_start_hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "automatedSnapshotStartHour"))

    @automated_snapshot_start_hour.setter
    def automated_snapshot_start_hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77c183c8790934afc1118d3fcec84e7dac1dcc1c42dc2b9f0665bc8d82ae4d5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automatedSnapshotStartHour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ElasticsearchDomainSnapshotOptions]:
        return typing.cast(typing.Optional[ElasticsearchDomainSnapshotOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElasticsearchDomainSnapshotOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0600f4998b8a418d29a8483217415360aac21f4242dec4d0c7e62f7db77cf96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ElasticsearchDomainTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#create ElasticsearchDomain#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#delete ElasticsearchDomain#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#update ElasticsearchDomain#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14048652cab0006aea76000be1f57df7d56a8c1c6032f1012b9b99d2280e4c43)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#create ElasticsearchDomain#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#delete ElasticsearchDomain#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#update ElasticsearchDomain#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticsearchDomainTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElasticsearchDomainTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9eee703999d59e97b5d9fded333563ebabf737ba7040e745ea4bd84b66f4db8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0dffadb8efce83f7ea387f4449a0eb262ad6c910cd0e93a4f264ed61a98c335)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d70a67933b9c1a5d3c07effcd9161dc5f53dab1ad11ac2f90c110c5dd20852f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f60901dcc0d776feb08b25f4115430d5d2843de79d665d2a123c06fd8db7900b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElasticsearchDomainTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElasticsearchDomainTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElasticsearchDomainTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47039c85f0fc81bc73ca8f0a0660412c3647cf3e7178d0d289a4ab80f85f4ecc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainVpcOptions",
    jsii_struct_bases=[],
    name_mapping={"security_group_ids": "securityGroupIds", "subnet_ids": "subnetIds"},
)
class ElasticsearchDomainVpcOptions:
    def __init__(
        self,
        *,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param security_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#security_group_ids ElasticsearchDomain#security_group_ids}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#subnet_ids ElasticsearchDomain#subnet_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39233374228cf00de6e7f7609530436034dab95d31138ce976c32fe7f103fdb)
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#security_group_ids ElasticsearchDomain#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/elasticsearch_domain#subnet_ids ElasticsearchDomain#subnet_ids}.'''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticsearchDomainVpcOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElasticsearchDomainVpcOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.elasticsearchDomain.ElasticsearchDomainVpcOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e15acbf628d9af2a9e38122ee3a2b611f6c5f02a2dddd7d156c2dbba15aebbee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSecurityGroupIds")
    def reset_security_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupIds", []))

    @jsii.member(jsii_name="resetSubnetIds")
    def reset_subnet_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetIds", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZones"))

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdsInput")
    def subnet_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2005e9d0194d58c9271d69a4c8e43778824dee55e363b6f2ad89bea3dc78e2c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb1192f600399af0e3bc208a4ec12ecaa2541c5389ce7ec1eef5b77229b1ce91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ElasticsearchDomainVpcOptions]:
        return typing.cast(typing.Optional[ElasticsearchDomainVpcOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ElasticsearchDomainVpcOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca15aefff0611ee1bed67ca43c8d7827450c43ed7ef5d2696dfaad2f603efc78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ElasticsearchDomain",
    "ElasticsearchDomainAdvancedSecurityOptions",
    "ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptions",
    "ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptionsOutputReference",
    "ElasticsearchDomainAdvancedSecurityOptionsOutputReference",
    "ElasticsearchDomainAutoTuneOptions",
    "ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule",
    "ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDuration",
    "ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDurationOutputReference",
    "ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleList",
    "ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleOutputReference",
    "ElasticsearchDomainAutoTuneOptionsOutputReference",
    "ElasticsearchDomainClusterConfig",
    "ElasticsearchDomainClusterConfigColdStorageOptions",
    "ElasticsearchDomainClusterConfigColdStorageOptionsOutputReference",
    "ElasticsearchDomainClusterConfigOutputReference",
    "ElasticsearchDomainClusterConfigZoneAwarenessConfig",
    "ElasticsearchDomainClusterConfigZoneAwarenessConfigOutputReference",
    "ElasticsearchDomainCognitoOptions",
    "ElasticsearchDomainCognitoOptionsOutputReference",
    "ElasticsearchDomainConfig",
    "ElasticsearchDomainDomainEndpointOptions",
    "ElasticsearchDomainDomainEndpointOptionsOutputReference",
    "ElasticsearchDomainEbsOptions",
    "ElasticsearchDomainEbsOptionsOutputReference",
    "ElasticsearchDomainEncryptAtRest",
    "ElasticsearchDomainEncryptAtRestOutputReference",
    "ElasticsearchDomainLogPublishingOptions",
    "ElasticsearchDomainLogPublishingOptionsList",
    "ElasticsearchDomainLogPublishingOptionsOutputReference",
    "ElasticsearchDomainNodeToNodeEncryption",
    "ElasticsearchDomainNodeToNodeEncryptionOutputReference",
    "ElasticsearchDomainSnapshotOptions",
    "ElasticsearchDomainSnapshotOptionsOutputReference",
    "ElasticsearchDomainTimeouts",
    "ElasticsearchDomainTimeoutsOutputReference",
    "ElasticsearchDomainVpcOptions",
    "ElasticsearchDomainVpcOptionsOutputReference",
]

publication.publish()

def _typecheckingstub__dc69a2ad64da28603e272dacdc005fd8de20f89953480ee2660a53613d5fc11e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    domain_name: builtins.str,
    access_policies: typing.Optional[builtins.str] = None,
    advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    advanced_security_options: typing.Optional[typing.Union[ElasticsearchDomainAdvancedSecurityOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_tune_options: typing.Optional[typing.Union[ElasticsearchDomainAutoTuneOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_config: typing.Optional[typing.Union[ElasticsearchDomainClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cognito_options: typing.Optional[typing.Union[ElasticsearchDomainCognitoOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    domain_endpoint_options: typing.Optional[typing.Union[ElasticsearchDomainDomainEndpointOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ebs_options: typing.Optional[typing.Union[ElasticsearchDomainEbsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    elasticsearch_version: typing.Optional[builtins.str] = None,
    encrypt_at_rest: typing.Optional[typing.Union[ElasticsearchDomainEncryptAtRest, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    log_publishing_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElasticsearchDomainLogPublishingOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    node_to_node_encryption: typing.Optional[typing.Union[ElasticsearchDomainNodeToNodeEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    snapshot_options: typing.Optional[typing.Union[ElasticsearchDomainSnapshotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ElasticsearchDomainTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_options: typing.Optional[typing.Union[ElasticsearchDomainVpcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__808f7d9bf8f04be77300504f9472b95b76581a93bb1cb02f9652cab01e64a444(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5e9e114a8e26de5063607b04c325ff85274230c953b404e9d7ef0dbb8f63e4a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElasticsearchDomainLogPublishingOptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__166cd9f2a9394f225368b33647c1c9714bdbfee1c1a877c7a1cc899a31862e63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__317d8a20e75a27f59ff38b12bd28c9d9967efd53ef63f4254743694050105f24(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb2996da1bc9e2a7f815170b630ac17c3aeaf1eae2659b6431e2cb0a758b220(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96dd3814b2791f9796bcd4241d05f224d1b417cf3f6715a618567ce8972ffb88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__854f65072a2eaaaf4d7050e8a235e28acba7b0f75c0d2f294597bee504c79646(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb82ea8166d51dd062426b0a5737721343efdbb6949dc2b1ef60fe037d11892(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc2352a22bde00615bc167b9872db93be27c00d76f3acb9ca079df1ca5da2b1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f42f50656dc13bd017ace3c99d2a2e3e1f4c22db241cbaef74cd8bf6b2f150(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96a7b0205b18423dc88a2562a62e582678caf4534b38faebac7a83e2d3287f5(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    internal_user_database_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    master_user_options: typing.Optional[typing.Union[ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b8df72959be87e5018598b56642899ef12575025dc17207646004086f779b8(
    *,
    master_user_arn: typing.Optional[builtins.str] = None,
    master_user_name: typing.Optional[builtins.str] = None,
    master_user_password: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441bfef9b15fcf12e50a195439d4d5e0f467c83724d0ac6c7771894fe5c58e5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__606e353cd046a1ebc3963f25bd06165099d29da6d969485e8f53d04532a2685f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1392a204ef6fba06f99dfef80e0b5e3461514f0e723c47574175e81f2db62691(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6e0f9808b61c77b0e49bcf6eb0519f14a59dc9c553a157fd969484c0fbfb29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf8a341e9606ea1c21db690606151574b3149c8189ce0bffab3ddae2e38ce8d1(
    value: typing.Optional[ElasticsearchDomainAdvancedSecurityOptionsMasterUserOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__403d6d51eba6fd14f15acf99033665f55a5d13068f67e4cbf69336544505fc97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ddcc95da4fe832be547d0ae6e94cb9c5aeb92e50e0a522b01fa8e586cbbde6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d754812618d08ffe5dce58eeb5ffcacdc73a3aeab3b592639fe3b219bbaa490a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba12c9548015d557feadb9bc996dce6584a9483fec1d8d902ea948f2c0040f88(
    value: typing.Optional[ElasticsearchDomainAdvancedSecurityOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bc4f50eaa5e90e946456bc263f9b7e27428f9a9da2cbbef7e65a9f4d20f6ba0(
    *,
    desired_state: builtins.str,
    maintenance_schedule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rollback_on_disable: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ea602c5e0ba3980823878481b0701cb6245b3cb2dde5649d002984eb2dfea9c(
    *,
    cron_expression_for_recurrence: builtins.str,
    duration: typing.Union[ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDuration, typing.Dict[builtins.str, typing.Any]],
    start_at: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b97c831136582188b783e6af4f67792cc8209d86551fbe5b271d8f981c6bb45(
    *,
    unit: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5128b2255d16a58754f94c55bbf498d5cf379850c1ca60adcba3ae9632c33f72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6beb815a635771cd3a4d2cd81b8c5487b8b9b9a442f11766886c3fa4a9ea3877(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8325d4e837538a4bb2a20c6335766caf3a8760af77d35a1130029884043dc06(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538fbe5b74af2c682ea3b99f00a9e2f029afb747ac5781874c132b2d3556eeec(
    value: typing.Optional[ElasticsearchDomainAutoTuneOptionsMaintenanceScheduleDuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b77f99214208f619ce7cc672508da981585ccc6e0613368e375350f2f1db43(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69519ae84cfbee21b6e01a272858f10e20edb0d260253361b86e9c4ab81ca65c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe41328d914678a9b9882ba5ba4c327299211f2f18e34cf8608f0e12d9738cc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc0e1fb834e5b67919cde551427de8eb7d22c71a38ac7741749b6f863d1aaddc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3178c4cd22ebd774beaceb670aea70f46db4c010fdb639698b6fbbef5787ea19(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf0a9da7c833845db1da2c1ac890aa8a4a4c5c4e32ad6d4a39c35f135571e1c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6b2fbcb4a08f9fbd34974094aa19d060e6c75dcfccf26b20c9adeeeac2ffd0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79cfb2f730c2c516a316196f4c8a4228173299e126205782945bfb86b403b3ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__278f14ec2c24e86949722bc0556f3b1fb7e31f266bb3f1e42a889f5001553b92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b262b7ce23fa932e1e6a985a4d9a4baf069ac97560cc1906601956e25e51f346(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c57b6bdd8e754de86c490fbabc8a863c2a45ee7f1a942e69da4f8ebc59ebb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee692940ca50044dab87f163c5a70f4ba1ecab19667fa4194def9c0f25c00416(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElasticsearchDomainAutoTuneOptionsMaintenanceSchedule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4453335e6ae91f24c0fe5bae3b4f9a3e92d659100877ad56397915d5cda3d2e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e563f48de821d27c036aa67f41930876d2b9fab53286fdca1c12938363a4df4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bfed56fc1c66150791c92dba3d7e0078fa1c4e91e06071a9d1de9954a1557a2(
    value: typing.Optional[ElasticsearchDomainAutoTuneOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1214cfcffe1730ba09b21e6e40685c1512a6d383eb2d56ab535c04456cf411e9(
    *,
    cold_storage_options: typing.Optional[typing.Union[ElasticsearchDomainClusterConfigColdStorageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    dedicated_master_count: typing.Optional[jsii.Number] = None,
    dedicated_master_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dedicated_master_type: typing.Optional[builtins.str] = None,
    instance_count: typing.Optional[jsii.Number] = None,
    instance_type: typing.Optional[builtins.str] = None,
    warm_count: typing.Optional[jsii.Number] = None,
    warm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    warm_type: typing.Optional[builtins.str] = None,
    zone_awareness_config: typing.Optional[typing.Union[ElasticsearchDomainClusterConfigZoneAwarenessConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    zone_awareness_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b4d24bee8776d655f77fbc343cb98ed3278038226a971e23588c7695b1772b(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35cec65f11daee298ad4491f8567a4d77ed416285daf5c38aa23d8ad5f215e53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1979602716c47c46893e50520c38d6281cfa9ca5f48543c2c97130145bb513e4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c512f8d1bebf2b2d9d76b45597500c75dd85f849146406c946b91f00dee8c14(
    value: typing.Optional[ElasticsearchDomainClusterConfigColdStorageOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a97001b372843c2afe805559fb6d51c0cadeba34d9f19cbafdc58de5a0211096(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e0675ba84f05df4425db2dea4a5452b5630a89193965fddc74be1192347e95(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67fa70279248d69dbbd9f2c3940f62584f3142ea76f8e610b2ef65cea7098eac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f605ddb9437dd658259cb80e15e6ab139cf8f221d429fab1d2a5678a9a0a4b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36362a2adc61f455726180718e500423ffcc01d2d101f3ce0bb1f0d90f3a581c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff4e4737cacc883bb1dad1e0b667c057d4228d7c83306c87d6ac57747db01db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c161484c580455f1a397933cda6305470ddb8ea91b841ea643c8dd4177de98f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1cab310d1a8688f6c6ae95901f9e49de2ccf9ff1dbb0c36b28ed88bf34b2117(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af88a75a7623ea48c9a7a099c88f1ae4166058cab75ddc7794c6421d5a95f69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49c988d434d78a27a88a08ff52038a5fe00e923cd80003fbd8a5434b28f4d2a3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dacce7ed52593f0e3fa94dfedb66d95537c7a498c78d221023ab439f692c407(
    value: typing.Optional[ElasticsearchDomainClusterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2acbc49788baf7f7c922f5a0ac55cba1d5e913418282fe4c2caffec3d6af4ea7(
    *,
    availability_zone_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af1425119dc0c4ef219ac59943dbee34e6dd47b01a7e6d9da7007ddf9fbbd0f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae54f98bfc939dd0b3ccb347684106ce3a5a29f62454648cb7a8874016321d2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__100a1795ec967390268f80ae82a3bd83addadcc38dca96722aa7c2723939ddcc(
    value: typing.Optional[ElasticsearchDomainClusterConfigZoneAwarenessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__178dad721ef0b8b2d58ac829c8a6674d5eb2497a81c82da5606eb663efe1126b(
    *,
    identity_pool_id: builtins.str,
    role_arn: builtins.str,
    user_pool_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05045a3da1daf1e4c4febc7a147d2af1bcac1104c06e115e567d26f1f490a8e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca21830eb6e0f85dfadc36492f39e06fb95ca3f74b6d48b8c3eb5bb519c2c28(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331e3cc26df5ed3f6edb25d5c06b85cdb5335de39bd8237b6f96675f8f4d633e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b35b384ccd882e3653937ea58942134ddfd3cdfa6f392797b802a13b567b2e78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1de51d3f3b86d420274724c1935fdfbdd966442f14dcbb55f2dfa3b7b9b893c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd2d765c1c118058fe1bf25bf39e1ada69b3992b1f36dd1a0546ec180fb0c4b(
    value: typing.Optional[ElasticsearchDomainCognitoOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__881cbe09c1e51db5121c0db093e29c090508a2475f8be47c13d2c1e6423e648f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    domain_name: builtins.str,
    access_policies: typing.Optional[builtins.str] = None,
    advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    advanced_security_options: typing.Optional[typing.Union[ElasticsearchDomainAdvancedSecurityOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_tune_options: typing.Optional[typing.Union[ElasticsearchDomainAutoTuneOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_config: typing.Optional[typing.Union[ElasticsearchDomainClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cognito_options: typing.Optional[typing.Union[ElasticsearchDomainCognitoOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    domain_endpoint_options: typing.Optional[typing.Union[ElasticsearchDomainDomainEndpointOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ebs_options: typing.Optional[typing.Union[ElasticsearchDomainEbsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    elasticsearch_version: typing.Optional[builtins.str] = None,
    encrypt_at_rest: typing.Optional[typing.Union[ElasticsearchDomainEncryptAtRest, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    log_publishing_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ElasticsearchDomainLogPublishingOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    node_to_node_encryption: typing.Optional[typing.Union[ElasticsearchDomainNodeToNodeEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    snapshot_options: typing.Optional[typing.Union[ElasticsearchDomainSnapshotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ElasticsearchDomainTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_options: typing.Optional[typing.Union[ElasticsearchDomainVpcOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37dca1417b3003b915f1c076adf2a63d36fbc525a44965d41723961a7fd5ccda(
    *,
    custom_endpoint: typing.Optional[builtins.str] = None,
    custom_endpoint_certificate_arn: typing.Optional[builtins.str] = None,
    custom_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enforce_https: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tls_security_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a5644813e69d43967d7ef784c14c06e829ad6b0bece49985410a5c668e3294(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85247a598aac8c7c3ebe75b64352e9afeda5108f9112cc90e99e75ae0310efac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c9ed1fcf5e015c8be4ee1e22d963390d5820a0ab28b15dd3e253284f2c596a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac8dfd5fadc3b8e7201468d5e384502f96016eb524f5adeaf4b78837c985e57(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c6e860b08d56473a58ec006a290bfe43176cdd9845f101746fefa56ee7b670d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d852f4476e7567ebf341f805981a3d4c52cb9fb7204d52414de9a87f12a9243f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d54645d1718cf2928c61c7b70aedf6885829d3394208d46666e421687059b2d(
    value: typing.Optional[ElasticsearchDomainDomainEndpointOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39263d432faa103f708e1a9dc8487b5f68db1e403dcd952889d01070f1bb54f8(
    *,
    ebs_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    iops: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_size: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6591b84809ce07f9d83acf519cea72ee842bb14d3d1e1bbce254661820b7ff7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__062409b1c41f8f9af464a917cdc17db350c0d09a92b3a179aa71e0e3874c600f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef11070d1694f140a9742e7d74d6810d8b02dffa21aef5548784d9d7ff29e234(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e227db24c423a08fa89fe970ea4cd0606abb58ea81cf0b241ad089f62257135(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef5d34b4c13e7832ec2a7c0da7aefcfe40a31f3058849a89b2f8f2d44c172a9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a8025f9ed54e1bdab09fb8007bd96aa8f0086f4845e7823f47b6c418c3045a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c34324c993285672ddc88d659f2784d51610b46a62f83b38c4ec4424cb2272c(
    value: typing.Optional[ElasticsearchDomainEbsOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa1436d6e79412ee7314a9ff37d3225670adee70f346c6e3e32f06eaf0758b9(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f699e2c06abcdd0b4b83782c18a17d689da73df1fa816e3944815a9c897909(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e8cc6a6571847205a39b8cabe776beb60419e159bf7a18731e5c84562d6096(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__859e3f823ffd1c31b79c11e85820c769c6f834c74ef362d1a0a74622e72b2382(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c451ec397783a3e4b7ea1b4abefdcc4490259a411931e39a95e7baff295e3b5c(
    value: typing.Optional[ElasticsearchDomainEncryptAtRest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8f40321b9de7d044754d293b9be24ef3afa3a7777a48d6f5e4af8119264b34(
    *,
    cloudwatch_log_group_arn: builtins.str,
    log_type: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dcf9ace61b5a327f6ce2c29f36f4aa616a052426e0dd4a873ee34e0375cc82d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1a6ecaccb6c7f04e98168607192d5cc2aeabf9d9d39c21ca8600d1fbcca8c7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c018b96ddda634bbf70cbce838767f3906310b6b24c897c5fb5c9dcf8d65a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd1c61d0c72f437d145c9d872975fce143e61e97868df3da4d927b8daa7d17f3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d166f05ae42be79101daa461bece693fb15488eab82c8bb788e39b173fc91ed5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037842c6656635e9cc4c0239a8f49587b4d2ce5adae8fb3d8eabccbf6be78d8b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ElasticsearchDomainLogPublishingOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5e034784956a938fa76482e352fca974f9be07957dde7b728d0de5b3aec336(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2da917e786feb1965c3e14378869b0b39619f8885800d1da8a7358789b2d1b92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3b71b26e4413108aa877454e51073969a8e26f72856cab17bde6240d50b496(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__206ad54e7da2a116f441a67b6eef7c35c497945d46ec610c339aceda59fd3f62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8efb788f8c630634269eb0a9afdf6281c688140d20696fda7be40d3c768ca1b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElasticsearchDomainLogPublishingOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc6de068ba0b35e53e8f830655624137fe1ebd391b0632e655e186df10752ac(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dcaefe180dbe9fc13008475a65aac855c080c0ace61bb312bebc51525432a71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c646d4413b674ddf2b8303a2c4de9e7f64eec49f3555cc5f2848782cf5f561(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48c0447da9ed35f9d32776ee2421ceeba2c9c4efb6ef3b0afac6206ac996670(
    value: typing.Optional[ElasticsearchDomainNodeToNodeEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2557f1764f8e08c5400453f3ec59ef55e474bee8afa0a987159d907c10a2a4a8(
    *,
    automated_snapshot_start_hour: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a21e379b9c1144ad0cee5843d0b63269b02856ed136cbc251dc86e0a7d669f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c183c8790934afc1118d3fcec84e7dac1dcc1c42dc2b9f0665bc8d82ae4d5d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0600f4998b8a418d29a8483217415360aac21f4242dec4d0c7e62f7db77cf96(
    value: typing.Optional[ElasticsearchDomainSnapshotOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14048652cab0006aea76000be1f57df7d56a8c1c6032f1012b9b99d2280e4c43(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9eee703999d59e97b5d9fded333563ebabf737ba7040e745ea4bd84b66f4db8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0dffadb8efce83f7ea387f4449a0eb262ad6c910cd0e93a4f264ed61a98c335(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d70a67933b9c1a5d3c07effcd9161dc5f53dab1ad11ac2f90c110c5dd20852f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60901dcc0d776feb08b25f4115430d5d2843de79d665d2a123c06fd8db7900b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47039c85f0fc81bc73ca8f0a0660412c3647cf3e7178d0d289a4ab80f85f4ecc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ElasticsearchDomainTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39233374228cf00de6e7f7609530436034dab95d31138ce976c32fe7f103fdb(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15acbf628d9af2a9e38122ee3a2b611f6c5f02a2dddd7d156c2dbba15aebbee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2005e9d0194d58c9271d69a4c8e43778824dee55e363b6f2ad89bea3dc78e2c5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb1192f600399af0e3bc208a4ec12ecaa2541c5389ce7ec1eef5b77229b1ce91(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca15aefff0611ee1bed67ca43c8d7827450c43ed7ef5d2696dfaad2f603efc78(
    value: typing.Optional[ElasticsearchDomainVpcOptions],
) -> None:
    """Type checking stubs"""
    pass
