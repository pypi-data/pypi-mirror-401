r'''
# `aws_fsx_ontap_volume`

Refer to the Terraform Registry for docs: [`aws_fsx_ontap_volume`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume).
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


class FsxOntapVolume(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fsxOntapVolume.FsxOntapVolume",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume aws_fsx_ontap_volume}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        storage_virtual_machine_id: builtins.str,
        aggregate_configuration: typing.Optional[typing.Union["FsxOntapVolumeAggregateConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        bypass_snaplock_enterprise_retention: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        copy_tags_to_backups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        final_backup_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        junction_path: typing.Optional[builtins.str] = None,
        ontap_volume_type: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        security_style: typing.Optional[builtins.str] = None,
        size_in_bytes: typing.Optional[builtins.str] = None,
        size_in_megabytes: typing.Optional[jsii.Number] = None,
        skip_final_backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        snaplock_configuration: typing.Optional[typing.Union["FsxOntapVolumeSnaplockConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        snapshot_policy: typing.Optional[builtins.str] = None,
        storage_efficiency_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tiering_policy: typing.Optional[typing.Union["FsxOntapVolumeTieringPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["FsxOntapVolumeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_style: typing.Optional[builtins.str] = None,
        volume_type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume aws_fsx_ontap_volume} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#name FsxOntapVolume#name}.
        :param storage_virtual_machine_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#storage_virtual_machine_id FsxOntapVolume#storage_virtual_machine_id}.
        :param aggregate_configuration: aggregate_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#aggregate_configuration FsxOntapVolume#aggregate_configuration}
        :param bypass_snaplock_enterprise_retention: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#bypass_snaplock_enterprise_retention FsxOntapVolume#bypass_snaplock_enterprise_retention}.
        :param copy_tags_to_backups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#copy_tags_to_backups FsxOntapVolume#copy_tags_to_backups}.
        :param final_backup_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#final_backup_tags FsxOntapVolume#final_backup_tags}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#id FsxOntapVolume#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param junction_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#junction_path FsxOntapVolume#junction_path}.
        :param ontap_volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#ontap_volume_type FsxOntapVolume#ontap_volume_type}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#region FsxOntapVolume#region}
        :param security_style: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#security_style FsxOntapVolume#security_style}.
        :param size_in_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#size_in_bytes FsxOntapVolume#size_in_bytes}.
        :param size_in_megabytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#size_in_megabytes FsxOntapVolume#size_in_megabytes}.
        :param skip_final_backup: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#skip_final_backup FsxOntapVolume#skip_final_backup}.
        :param snaplock_configuration: snaplock_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#snaplock_configuration FsxOntapVolume#snaplock_configuration}
        :param snapshot_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#snapshot_policy FsxOntapVolume#snapshot_policy}.
        :param storage_efficiency_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#storage_efficiency_enabled FsxOntapVolume#storage_efficiency_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#tags FsxOntapVolume#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#tags_all FsxOntapVolume#tags_all}.
        :param tiering_policy: tiering_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#tiering_policy FsxOntapVolume#tiering_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#timeouts FsxOntapVolume#timeouts}
        :param volume_style: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#volume_style FsxOntapVolume#volume_style}.
        :param volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#volume_type FsxOntapVolume#volume_type}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a805007864cd3868bfa1ad56f0043baba0659b9e610d0916a71aecfbd14b6ad)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FsxOntapVolumeConfig(
            name=name,
            storage_virtual_machine_id=storage_virtual_machine_id,
            aggregate_configuration=aggregate_configuration,
            bypass_snaplock_enterprise_retention=bypass_snaplock_enterprise_retention,
            copy_tags_to_backups=copy_tags_to_backups,
            final_backup_tags=final_backup_tags,
            id=id,
            junction_path=junction_path,
            ontap_volume_type=ontap_volume_type,
            region=region,
            security_style=security_style,
            size_in_bytes=size_in_bytes,
            size_in_megabytes=size_in_megabytes,
            skip_final_backup=skip_final_backup,
            snaplock_configuration=snaplock_configuration,
            snapshot_policy=snapshot_policy,
            storage_efficiency_enabled=storage_efficiency_enabled,
            tags=tags,
            tags_all=tags_all,
            tiering_policy=tiering_policy,
            timeouts=timeouts,
            volume_style=volume_style,
            volume_type=volume_type,
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
        '''Generates CDKTF code for importing a FsxOntapVolume resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FsxOntapVolume to import.
        :param import_from_id: The id of the existing FsxOntapVolume that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FsxOntapVolume to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2410589cf366c53e6c91a6d5e32fb979ee421f3b23d6e27df9416da277a57cdd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAggregateConfiguration")
    def put_aggregate_configuration(
        self,
        *,
        aggregates: typing.Optional[typing.Sequence[builtins.str]] = None,
        constituents_per_aggregate: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aggregates: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#aggregates FsxOntapVolume#aggregates}.
        :param constituents_per_aggregate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#constituents_per_aggregate FsxOntapVolume#constituents_per_aggregate}.
        '''
        value = FsxOntapVolumeAggregateConfiguration(
            aggregates=aggregates,
            constituents_per_aggregate=constituents_per_aggregate,
        )

        return typing.cast(None, jsii.invoke(self, "putAggregateConfiguration", [value]))

    @jsii.member(jsii_name="putSnaplockConfiguration")
    def put_snaplock_configuration(
        self,
        *,
        snaplock_type: builtins.str,
        audit_log_volume: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        autocommit_period: typing.Optional[typing.Union["FsxOntapVolumeSnaplockConfigurationAutocommitPeriod", typing.Dict[builtins.str, typing.Any]]] = None,
        privileged_delete: typing.Optional[builtins.str] = None,
        retention_period: typing.Optional[typing.Union["FsxOntapVolumeSnaplockConfigurationRetentionPeriod", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_append_mode_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param snaplock_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#snaplock_type FsxOntapVolume#snaplock_type}.
        :param audit_log_volume: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#audit_log_volume FsxOntapVolume#audit_log_volume}.
        :param autocommit_period: autocommit_period block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#autocommit_period FsxOntapVolume#autocommit_period}
        :param privileged_delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#privileged_delete FsxOntapVolume#privileged_delete}.
        :param retention_period: retention_period block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#retention_period FsxOntapVolume#retention_period}
        :param volume_append_mode_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#volume_append_mode_enabled FsxOntapVolume#volume_append_mode_enabled}.
        '''
        value = FsxOntapVolumeSnaplockConfiguration(
            snaplock_type=snaplock_type,
            audit_log_volume=audit_log_volume,
            autocommit_period=autocommit_period,
            privileged_delete=privileged_delete,
            retention_period=retention_period,
            volume_append_mode_enabled=volume_append_mode_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putSnaplockConfiguration", [value]))

    @jsii.member(jsii_name="putTieringPolicy")
    def put_tiering_policy(
        self,
        *,
        cooling_period: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cooling_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#cooling_period FsxOntapVolume#cooling_period}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#name FsxOntapVolume#name}.
        '''
        value = FsxOntapVolumeTieringPolicy(cooling_period=cooling_period, name=name)

        return typing.cast(None, jsii.invoke(self, "putTieringPolicy", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#create FsxOntapVolume#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#delete FsxOntapVolume#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#update FsxOntapVolume#update}.
        '''
        value = FsxOntapVolumeTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAggregateConfiguration")
    def reset_aggregate_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregateConfiguration", []))

    @jsii.member(jsii_name="resetBypassSnaplockEnterpriseRetention")
    def reset_bypass_snaplock_enterprise_retention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBypassSnaplockEnterpriseRetention", []))

    @jsii.member(jsii_name="resetCopyTagsToBackups")
    def reset_copy_tags_to_backups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyTagsToBackups", []))

    @jsii.member(jsii_name="resetFinalBackupTags")
    def reset_final_backup_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFinalBackupTags", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetJunctionPath")
    def reset_junction_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJunctionPath", []))

    @jsii.member(jsii_name="resetOntapVolumeType")
    def reset_ontap_volume_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOntapVolumeType", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSecurityStyle")
    def reset_security_style(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityStyle", []))

    @jsii.member(jsii_name="resetSizeInBytes")
    def reset_size_in_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizeInBytes", []))

    @jsii.member(jsii_name="resetSizeInMegabytes")
    def reset_size_in_megabytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizeInMegabytes", []))

    @jsii.member(jsii_name="resetSkipFinalBackup")
    def reset_skip_final_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipFinalBackup", []))

    @jsii.member(jsii_name="resetSnaplockConfiguration")
    def reset_snaplock_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnaplockConfiguration", []))

    @jsii.member(jsii_name="resetSnapshotPolicy")
    def reset_snapshot_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshotPolicy", []))

    @jsii.member(jsii_name="resetStorageEfficiencyEnabled")
    def reset_storage_efficiency_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageEfficiencyEnabled", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTieringPolicy")
    def reset_tiering_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTieringPolicy", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVolumeStyle")
    def reset_volume_style(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeStyle", []))

    @jsii.member(jsii_name="resetVolumeType")
    def reset_volume_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeType", []))

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
    @jsii.member(jsii_name="aggregateConfiguration")
    def aggregate_configuration(
        self,
    ) -> "FsxOntapVolumeAggregateConfigurationOutputReference":
        return typing.cast("FsxOntapVolumeAggregateConfigurationOutputReference", jsii.get(self, "aggregateConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileSystemId"))

    @builtins.property
    @jsii.member(jsii_name="flexcacheEndpointType")
    def flexcache_endpoint_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flexcacheEndpointType"))

    @builtins.property
    @jsii.member(jsii_name="snaplockConfiguration")
    def snaplock_configuration(
        self,
    ) -> "FsxOntapVolumeSnaplockConfigurationOutputReference":
        return typing.cast("FsxOntapVolumeSnaplockConfigurationOutputReference", jsii.get(self, "snaplockConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="tieringPolicy")
    def tiering_policy(self) -> "FsxOntapVolumeTieringPolicyOutputReference":
        return typing.cast("FsxOntapVolumeTieringPolicyOutputReference", jsii.get(self, "tieringPolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "FsxOntapVolumeTimeoutsOutputReference":
        return typing.cast("FsxOntapVolumeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

    @builtins.property
    @jsii.member(jsii_name="aggregateConfigurationInput")
    def aggregate_configuration_input(
        self,
    ) -> typing.Optional["FsxOntapVolumeAggregateConfiguration"]:
        return typing.cast(typing.Optional["FsxOntapVolumeAggregateConfiguration"], jsii.get(self, "aggregateConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="bypassSnaplockEnterpriseRetentionInput")
    def bypass_snaplock_enterprise_retention_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bypassSnaplockEnterpriseRetentionInput"))

    @builtins.property
    @jsii.member(jsii_name="copyTagsToBackupsInput")
    def copy_tags_to_backups_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "copyTagsToBackupsInput"))

    @builtins.property
    @jsii.member(jsii_name="finalBackupTagsInput")
    def final_backup_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "finalBackupTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="junctionPathInput")
    def junction_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "junctionPathInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="ontapVolumeTypeInput")
    def ontap_volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ontapVolumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="securityStyleInput")
    def security_style_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityStyleInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInBytesInput")
    def size_in_bytes_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sizeInBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInMegabytesInput")
    def size_in_megabytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInMegabytesInput"))

    @builtins.property
    @jsii.member(jsii_name="skipFinalBackupInput")
    def skip_final_backup_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipFinalBackupInput"))

    @builtins.property
    @jsii.member(jsii_name="snaplockConfigurationInput")
    def snaplock_configuration_input(
        self,
    ) -> typing.Optional["FsxOntapVolumeSnaplockConfiguration"]:
        return typing.cast(typing.Optional["FsxOntapVolumeSnaplockConfiguration"], jsii.get(self, "snaplockConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotPolicyInput")
    def snapshot_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="storageEfficiencyEnabledInput")
    def storage_efficiency_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "storageEfficiencyEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="storageVirtualMachineIdInput")
    def storage_virtual_machine_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageVirtualMachineIdInput"))

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
    @jsii.member(jsii_name="tieringPolicyInput")
    def tiering_policy_input(self) -> typing.Optional["FsxOntapVolumeTieringPolicy"]:
        return typing.cast(typing.Optional["FsxOntapVolumeTieringPolicy"], jsii.get(self, "tieringPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FsxOntapVolumeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FsxOntapVolumeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeStyleInput")
    def volume_style_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeStyleInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeTypeInput")
    def volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="bypassSnaplockEnterpriseRetention")
    def bypass_snaplock_enterprise_retention(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bypassSnaplockEnterpriseRetention"))

    @bypass_snaplock_enterprise_retention.setter
    def bypass_snaplock_enterprise_retention(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd936f7ad6427df0dd8db6a8809fa9b626756f991fddb37e87b8f69592529a6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bypassSnaplockEnterpriseRetention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="copyTagsToBackups")
    def copy_tags_to_backups(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "copyTagsToBackups"))

    @copy_tags_to_backups.setter
    def copy_tags_to_backups(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a720083beb8ed160f761bc12cba78b71c96aa9e570838070b0ce4de1f29fd69b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyTagsToBackups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="finalBackupTags")
    def final_backup_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "finalBackupTags"))

    @final_backup_tags.setter
    def final_backup_tags(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d672b37a0dcbc4468c5e0374ab4a92a46722863ae01774d589a2dd109feb782d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "finalBackupTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7beb88ded730face2c2903fa17393d45524bce011550252eca001e02b5338586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="junctionPath")
    def junction_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "junctionPath"))

    @junction_path.setter
    def junction_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d628e2ad34bb90b7f735b210eeca055aa75fa5b8993a65b5f9a6f3a56ab56f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "junctionPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e441e214d5a274f897f70d9c1cf1e0fecb8b96fa9082c7e8a68f1e173b9f94b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ontapVolumeType")
    def ontap_volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ontapVolumeType"))

    @ontap_volume_type.setter
    def ontap_volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e572e6dd2a3d64677cca0b198c4a2f2824a02b8af58769fce5c441b1570dc868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ontapVolumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42c31d1a8759c3a7da4f990c7b07eaa71d7adf7ae4dc962222a5ba435c1a02dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityStyle")
    def security_style(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityStyle"))

    @security_style.setter
    def security_style(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afe87d7e3cabf132cf2e6e077261e7c7554fb8d555234e6ea283a5dbb9a8df44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityStyle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeInBytes")
    def size_in_bytes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sizeInBytes"))

    @size_in_bytes.setter
    def size_in_bytes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f27721d33823680322282133363b2a042cc5c6eb92fd24bc4081453d4e609fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeInBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeInMegabytes")
    def size_in_megabytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeInMegabytes"))

    @size_in_megabytes.setter
    def size_in_megabytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__703d61100a963653cf53fa8e15bddeffd0b7ffcbda71201595039d336c94dc5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeInMegabytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipFinalBackup")
    def skip_final_backup(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipFinalBackup"))

    @skip_final_backup.setter
    def skip_final_backup(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__919a296702c747bd366cb25896e99366168dcdcf8c9924de424faa8f94e1786f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipFinalBackup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotPolicy")
    def snapshot_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshotPolicy"))

    @snapshot_policy.setter
    def snapshot_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d7e2bc3faa9696a7d974541ab6f1f18d6dcfe6092d16e854a4d5d6cd687449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageEfficiencyEnabled")
    def storage_efficiency_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "storageEfficiencyEnabled"))

    @storage_efficiency_enabled.setter
    def storage_efficiency_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93e902074a38655015badf2c3ad99c7c2cd44bdd5bfb920927fc2c15cee73aa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageEfficiencyEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageVirtualMachineId")
    def storage_virtual_machine_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageVirtualMachineId"))

    @storage_virtual_machine_id.setter
    def storage_virtual_machine_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfffdacfca88f1fb7b96999aed6939bc609cdfc60fc09c41be65ce50f9c5d754)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageVirtualMachineId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f12bf0713704cb03d09885e065d77fe6226085c747f39784a9fc508ae324a928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67ccc8d77da37aaa2373073da9749bcce4bdc20651368df51fc628ea076cbe1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeStyle")
    def volume_style(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeStyle"))

    @volume_style.setter
    def volume_style(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d3e16e47d2538a7af0d76af419c6539edae2f89af5605bf619633a4dd5159cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeStyle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeType")
    def volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeType"))

    @volume_type.setter
    def volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40e9f9c76f6b5b5a38ee4225aa0ab2a95e833db3d733aad43451a4614c039c1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fsxOntapVolume.FsxOntapVolumeAggregateConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "aggregates": "aggregates",
        "constituents_per_aggregate": "constituentsPerAggregate",
    },
)
class FsxOntapVolumeAggregateConfiguration:
    def __init__(
        self,
        *,
        aggregates: typing.Optional[typing.Sequence[builtins.str]] = None,
        constituents_per_aggregate: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aggregates: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#aggregates FsxOntapVolume#aggregates}.
        :param constituents_per_aggregate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#constituents_per_aggregate FsxOntapVolume#constituents_per_aggregate}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e4eaa305fc5fd125fed5c17939b86eadcec416546a0f2acfa3f278896e3dc84)
            check_type(argname="argument aggregates", value=aggregates, expected_type=type_hints["aggregates"])
            check_type(argname="argument constituents_per_aggregate", value=constituents_per_aggregate, expected_type=type_hints["constituents_per_aggregate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aggregates is not None:
            self._values["aggregates"] = aggregates
        if constituents_per_aggregate is not None:
            self._values["constituents_per_aggregate"] = constituents_per_aggregate

    @builtins.property
    def aggregates(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#aggregates FsxOntapVolume#aggregates}.'''
        result = self._values.get("aggregates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def constituents_per_aggregate(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#constituents_per_aggregate FsxOntapVolume#constituents_per_aggregate}.'''
        result = self._values.get("constituents_per_aggregate")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FsxOntapVolumeAggregateConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FsxOntapVolumeAggregateConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fsxOntapVolume.FsxOntapVolumeAggregateConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8410bc24bdddcd0de16c597bd7700ceb7cbc3cf9f5dfc690178206e105513ccb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAggregates")
    def reset_aggregates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregates", []))

    @jsii.member(jsii_name="resetConstituentsPerAggregate")
    def reset_constituents_per_aggregate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConstituentsPerAggregate", []))

    @builtins.property
    @jsii.member(jsii_name="totalConstituents")
    def total_constituents(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalConstituents"))

    @builtins.property
    @jsii.member(jsii_name="aggregatesInput")
    def aggregates_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "aggregatesInput"))

    @builtins.property
    @jsii.member(jsii_name="constituentsPerAggregateInput")
    def constituents_per_aggregate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "constituentsPerAggregateInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregates")
    def aggregates(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "aggregates"))

    @aggregates.setter
    def aggregates(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d51c2ec2574af814676ae41deae402c4e316f280020ab536c9da12ab9a78cd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregates", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="constituentsPerAggregate")
    def constituents_per_aggregate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "constituentsPerAggregate"))

    @constituents_per_aggregate.setter
    def constituents_per_aggregate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bbf3f36a9805562d091b4120c66d348ad64cbde27f7f4417c1e370193a3a7a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "constituentsPerAggregate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FsxOntapVolumeAggregateConfiguration]:
        return typing.cast(typing.Optional[FsxOntapVolumeAggregateConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FsxOntapVolumeAggregateConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0e5736089a7ec90f734ef73acf7565d2521e417d27e29b2eef18c58617d921a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fsxOntapVolume.FsxOntapVolumeConfig",
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
        "storage_virtual_machine_id": "storageVirtualMachineId",
        "aggregate_configuration": "aggregateConfiguration",
        "bypass_snaplock_enterprise_retention": "bypassSnaplockEnterpriseRetention",
        "copy_tags_to_backups": "copyTagsToBackups",
        "final_backup_tags": "finalBackupTags",
        "id": "id",
        "junction_path": "junctionPath",
        "ontap_volume_type": "ontapVolumeType",
        "region": "region",
        "security_style": "securityStyle",
        "size_in_bytes": "sizeInBytes",
        "size_in_megabytes": "sizeInMegabytes",
        "skip_final_backup": "skipFinalBackup",
        "snaplock_configuration": "snaplockConfiguration",
        "snapshot_policy": "snapshotPolicy",
        "storage_efficiency_enabled": "storageEfficiencyEnabled",
        "tags": "tags",
        "tags_all": "tagsAll",
        "tiering_policy": "tieringPolicy",
        "timeouts": "timeouts",
        "volume_style": "volumeStyle",
        "volume_type": "volumeType",
    },
)
class FsxOntapVolumeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        storage_virtual_machine_id: builtins.str,
        aggregate_configuration: typing.Optional[typing.Union[FsxOntapVolumeAggregateConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        bypass_snaplock_enterprise_retention: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        copy_tags_to_backups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        final_backup_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        junction_path: typing.Optional[builtins.str] = None,
        ontap_volume_type: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        security_style: typing.Optional[builtins.str] = None,
        size_in_bytes: typing.Optional[builtins.str] = None,
        size_in_megabytes: typing.Optional[jsii.Number] = None,
        skip_final_backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        snaplock_configuration: typing.Optional[typing.Union["FsxOntapVolumeSnaplockConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        snapshot_policy: typing.Optional[builtins.str] = None,
        storage_efficiency_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tiering_policy: typing.Optional[typing.Union["FsxOntapVolumeTieringPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["FsxOntapVolumeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_style: typing.Optional[builtins.str] = None,
        volume_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#name FsxOntapVolume#name}.
        :param storage_virtual_machine_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#storage_virtual_machine_id FsxOntapVolume#storage_virtual_machine_id}.
        :param aggregate_configuration: aggregate_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#aggregate_configuration FsxOntapVolume#aggregate_configuration}
        :param bypass_snaplock_enterprise_retention: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#bypass_snaplock_enterprise_retention FsxOntapVolume#bypass_snaplock_enterprise_retention}.
        :param copy_tags_to_backups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#copy_tags_to_backups FsxOntapVolume#copy_tags_to_backups}.
        :param final_backup_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#final_backup_tags FsxOntapVolume#final_backup_tags}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#id FsxOntapVolume#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param junction_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#junction_path FsxOntapVolume#junction_path}.
        :param ontap_volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#ontap_volume_type FsxOntapVolume#ontap_volume_type}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#region FsxOntapVolume#region}
        :param security_style: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#security_style FsxOntapVolume#security_style}.
        :param size_in_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#size_in_bytes FsxOntapVolume#size_in_bytes}.
        :param size_in_megabytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#size_in_megabytes FsxOntapVolume#size_in_megabytes}.
        :param skip_final_backup: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#skip_final_backup FsxOntapVolume#skip_final_backup}.
        :param snaplock_configuration: snaplock_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#snaplock_configuration FsxOntapVolume#snaplock_configuration}
        :param snapshot_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#snapshot_policy FsxOntapVolume#snapshot_policy}.
        :param storage_efficiency_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#storage_efficiency_enabled FsxOntapVolume#storage_efficiency_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#tags FsxOntapVolume#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#tags_all FsxOntapVolume#tags_all}.
        :param tiering_policy: tiering_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#tiering_policy FsxOntapVolume#tiering_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#timeouts FsxOntapVolume#timeouts}
        :param volume_style: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#volume_style FsxOntapVolume#volume_style}.
        :param volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#volume_type FsxOntapVolume#volume_type}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(aggregate_configuration, dict):
            aggregate_configuration = FsxOntapVolumeAggregateConfiguration(**aggregate_configuration)
        if isinstance(snaplock_configuration, dict):
            snaplock_configuration = FsxOntapVolumeSnaplockConfiguration(**snaplock_configuration)
        if isinstance(tiering_policy, dict):
            tiering_policy = FsxOntapVolumeTieringPolicy(**tiering_policy)
        if isinstance(timeouts, dict):
            timeouts = FsxOntapVolumeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d37faa495e1e5e716a06fb89bcfd992756f080e35cecb77dbd06162d2fddb0bf)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument storage_virtual_machine_id", value=storage_virtual_machine_id, expected_type=type_hints["storage_virtual_machine_id"])
            check_type(argname="argument aggregate_configuration", value=aggregate_configuration, expected_type=type_hints["aggregate_configuration"])
            check_type(argname="argument bypass_snaplock_enterprise_retention", value=bypass_snaplock_enterprise_retention, expected_type=type_hints["bypass_snaplock_enterprise_retention"])
            check_type(argname="argument copy_tags_to_backups", value=copy_tags_to_backups, expected_type=type_hints["copy_tags_to_backups"])
            check_type(argname="argument final_backup_tags", value=final_backup_tags, expected_type=type_hints["final_backup_tags"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument junction_path", value=junction_path, expected_type=type_hints["junction_path"])
            check_type(argname="argument ontap_volume_type", value=ontap_volume_type, expected_type=type_hints["ontap_volume_type"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument security_style", value=security_style, expected_type=type_hints["security_style"])
            check_type(argname="argument size_in_bytes", value=size_in_bytes, expected_type=type_hints["size_in_bytes"])
            check_type(argname="argument size_in_megabytes", value=size_in_megabytes, expected_type=type_hints["size_in_megabytes"])
            check_type(argname="argument skip_final_backup", value=skip_final_backup, expected_type=type_hints["skip_final_backup"])
            check_type(argname="argument snaplock_configuration", value=snaplock_configuration, expected_type=type_hints["snaplock_configuration"])
            check_type(argname="argument snapshot_policy", value=snapshot_policy, expected_type=type_hints["snapshot_policy"])
            check_type(argname="argument storage_efficiency_enabled", value=storage_efficiency_enabled, expected_type=type_hints["storage_efficiency_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument tiering_policy", value=tiering_policy, expected_type=type_hints["tiering_policy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument volume_style", value=volume_style, expected_type=type_hints["volume_style"])
            check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "storage_virtual_machine_id": storage_virtual_machine_id,
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
        if aggregate_configuration is not None:
            self._values["aggregate_configuration"] = aggregate_configuration
        if bypass_snaplock_enterprise_retention is not None:
            self._values["bypass_snaplock_enterprise_retention"] = bypass_snaplock_enterprise_retention
        if copy_tags_to_backups is not None:
            self._values["copy_tags_to_backups"] = copy_tags_to_backups
        if final_backup_tags is not None:
            self._values["final_backup_tags"] = final_backup_tags
        if id is not None:
            self._values["id"] = id
        if junction_path is not None:
            self._values["junction_path"] = junction_path
        if ontap_volume_type is not None:
            self._values["ontap_volume_type"] = ontap_volume_type
        if region is not None:
            self._values["region"] = region
        if security_style is not None:
            self._values["security_style"] = security_style
        if size_in_bytes is not None:
            self._values["size_in_bytes"] = size_in_bytes
        if size_in_megabytes is not None:
            self._values["size_in_megabytes"] = size_in_megabytes
        if skip_final_backup is not None:
            self._values["skip_final_backup"] = skip_final_backup
        if snaplock_configuration is not None:
            self._values["snaplock_configuration"] = snaplock_configuration
        if snapshot_policy is not None:
            self._values["snapshot_policy"] = snapshot_policy
        if storage_efficiency_enabled is not None:
            self._values["storage_efficiency_enabled"] = storage_efficiency_enabled
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if tiering_policy is not None:
            self._values["tiering_policy"] = tiering_policy
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if volume_style is not None:
            self._values["volume_style"] = volume_style
        if volume_type is not None:
            self._values["volume_type"] = volume_type

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#name FsxOntapVolume#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_virtual_machine_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#storage_virtual_machine_id FsxOntapVolume#storage_virtual_machine_id}.'''
        result = self._values.get("storage_virtual_machine_id")
        assert result is not None, "Required property 'storage_virtual_machine_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aggregate_configuration(
        self,
    ) -> typing.Optional[FsxOntapVolumeAggregateConfiguration]:
        '''aggregate_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#aggregate_configuration FsxOntapVolume#aggregate_configuration}
        '''
        result = self._values.get("aggregate_configuration")
        return typing.cast(typing.Optional[FsxOntapVolumeAggregateConfiguration], result)

    @builtins.property
    def bypass_snaplock_enterprise_retention(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#bypass_snaplock_enterprise_retention FsxOntapVolume#bypass_snaplock_enterprise_retention}.'''
        result = self._values.get("bypass_snaplock_enterprise_retention")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def copy_tags_to_backups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#copy_tags_to_backups FsxOntapVolume#copy_tags_to_backups}.'''
        result = self._values.get("copy_tags_to_backups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def final_backup_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#final_backup_tags FsxOntapVolume#final_backup_tags}.'''
        result = self._values.get("final_backup_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#id FsxOntapVolume#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def junction_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#junction_path FsxOntapVolume#junction_path}.'''
        result = self._values.get("junction_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ontap_volume_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#ontap_volume_type FsxOntapVolume#ontap_volume_type}.'''
        result = self._values.get("ontap_volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#region FsxOntapVolume#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_style(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#security_style FsxOntapVolume#security_style}.'''
        result = self._values.get("security_style")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_in_bytes(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#size_in_bytes FsxOntapVolume#size_in_bytes}.'''
        result = self._values.get("size_in_bytes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_in_megabytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#size_in_megabytes FsxOntapVolume#size_in_megabytes}.'''
        result = self._values.get("size_in_megabytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def skip_final_backup(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#skip_final_backup FsxOntapVolume#skip_final_backup}.'''
        result = self._values.get("skip_final_backup")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def snaplock_configuration(
        self,
    ) -> typing.Optional["FsxOntapVolumeSnaplockConfiguration"]:
        '''snaplock_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#snaplock_configuration FsxOntapVolume#snaplock_configuration}
        '''
        result = self._values.get("snaplock_configuration")
        return typing.cast(typing.Optional["FsxOntapVolumeSnaplockConfiguration"], result)

    @builtins.property
    def snapshot_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#snapshot_policy FsxOntapVolume#snapshot_policy}.'''
        result = self._values.get("snapshot_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_efficiency_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#storage_efficiency_enabled FsxOntapVolume#storage_efficiency_enabled}.'''
        result = self._values.get("storage_efficiency_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#tags FsxOntapVolume#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#tags_all FsxOntapVolume#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tiering_policy(self) -> typing.Optional["FsxOntapVolumeTieringPolicy"]:
        '''tiering_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#tiering_policy FsxOntapVolume#tiering_policy}
        '''
        result = self._values.get("tiering_policy")
        return typing.cast(typing.Optional["FsxOntapVolumeTieringPolicy"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["FsxOntapVolumeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#timeouts FsxOntapVolume#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["FsxOntapVolumeTimeouts"], result)

    @builtins.property
    def volume_style(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#volume_style FsxOntapVolume#volume_style}.'''
        result = self._values.get("volume_style")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#volume_type FsxOntapVolume#volume_type}.'''
        result = self._values.get("volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FsxOntapVolumeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fsxOntapVolume.FsxOntapVolumeSnaplockConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "snaplock_type": "snaplockType",
        "audit_log_volume": "auditLogVolume",
        "autocommit_period": "autocommitPeriod",
        "privileged_delete": "privilegedDelete",
        "retention_period": "retentionPeriod",
        "volume_append_mode_enabled": "volumeAppendModeEnabled",
    },
)
class FsxOntapVolumeSnaplockConfiguration:
    def __init__(
        self,
        *,
        snaplock_type: builtins.str,
        audit_log_volume: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        autocommit_period: typing.Optional[typing.Union["FsxOntapVolumeSnaplockConfigurationAutocommitPeriod", typing.Dict[builtins.str, typing.Any]]] = None,
        privileged_delete: typing.Optional[builtins.str] = None,
        retention_period: typing.Optional[typing.Union["FsxOntapVolumeSnaplockConfigurationRetentionPeriod", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_append_mode_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param snaplock_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#snaplock_type FsxOntapVolume#snaplock_type}.
        :param audit_log_volume: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#audit_log_volume FsxOntapVolume#audit_log_volume}.
        :param autocommit_period: autocommit_period block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#autocommit_period FsxOntapVolume#autocommit_period}
        :param privileged_delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#privileged_delete FsxOntapVolume#privileged_delete}.
        :param retention_period: retention_period block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#retention_period FsxOntapVolume#retention_period}
        :param volume_append_mode_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#volume_append_mode_enabled FsxOntapVolume#volume_append_mode_enabled}.
        '''
        if isinstance(autocommit_period, dict):
            autocommit_period = FsxOntapVolumeSnaplockConfigurationAutocommitPeriod(**autocommit_period)
        if isinstance(retention_period, dict):
            retention_period = FsxOntapVolumeSnaplockConfigurationRetentionPeriod(**retention_period)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b70024be950e757d19f914249fc38354860c49c2bd88ecbdb5e8dd77ca4a3590)
            check_type(argname="argument snaplock_type", value=snaplock_type, expected_type=type_hints["snaplock_type"])
            check_type(argname="argument audit_log_volume", value=audit_log_volume, expected_type=type_hints["audit_log_volume"])
            check_type(argname="argument autocommit_period", value=autocommit_period, expected_type=type_hints["autocommit_period"])
            check_type(argname="argument privileged_delete", value=privileged_delete, expected_type=type_hints["privileged_delete"])
            check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
            check_type(argname="argument volume_append_mode_enabled", value=volume_append_mode_enabled, expected_type=type_hints["volume_append_mode_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "snaplock_type": snaplock_type,
        }
        if audit_log_volume is not None:
            self._values["audit_log_volume"] = audit_log_volume
        if autocommit_period is not None:
            self._values["autocommit_period"] = autocommit_period
        if privileged_delete is not None:
            self._values["privileged_delete"] = privileged_delete
        if retention_period is not None:
            self._values["retention_period"] = retention_period
        if volume_append_mode_enabled is not None:
            self._values["volume_append_mode_enabled"] = volume_append_mode_enabled

    @builtins.property
    def snaplock_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#snaplock_type FsxOntapVolume#snaplock_type}.'''
        result = self._values.get("snaplock_type")
        assert result is not None, "Required property 'snaplock_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def audit_log_volume(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#audit_log_volume FsxOntapVolume#audit_log_volume}.'''
        result = self._values.get("audit_log_volume")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def autocommit_period(
        self,
    ) -> typing.Optional["FsxOntapVolumeSnaplockConfigurationAutocommitPeriod"]:
        '''autocommit_period block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#autocommit_period FsxOntapVolume#autocommit_period}
        '''
        result = self._values.get("autocommit_period")
        return typing.cast(typing.Optional["FsxOntapVolumeSnaplockConfigurationAutocommitPeriod"], result)

    @builtins.property
    def privileged_delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#privileged_delete FsxOntapVolume#privileged_delete}.'''
        result = self._values.get("privileged_delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_period(
        self,
    ) -> typing.Optional["FsxOntapVolumeSnaplockConfigurationRetentionPeriod"]:
        '''retention_period block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#retention_period FsxOntapVolume#retention_period}
        '''
        result = self._values.get("retention_period")
        return typing.cast(typing.Optional["FsxOntapVolumeSnaplockConfigurationRetentionPeriod"], result)

    @builtins.property
    def volume_append_mode_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#volume_append_mode_enabled FsxOntapVolume#volume_append_mode_enabled}.'''
        result = self._values.get("volume_append_mode_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FsxOntapVolumeSnaplockConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fsxOntapVolume.FsxOntapVolumeSnaplockConfigurationAutocommitPeriod",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class FsxOntapVolumeSnaplockConfigurationAutocommitPeriod:
    def __init__(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#type FsxOntapVolume#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#value FsxOntapVolume#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16cb0b279dc644cf807dc492b5e449016bed9d9e0fe048228d3d0b0f5552b6c6)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#type FsxOntapVolume#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#value FsxOntapVolume#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FsxOntapVolumeSnaplockConfigurationAutocommitPeriod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FsxOntapVolumeSnaplockConfigurationAutocommitPeriodOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fsxOntapVolume.FsxOntapVolumeSnaplockConfigurationAutocommitPeriodOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0200f131553398095670fa277b5ebd0cbc4132a3200d16a0995c5b28b2ec5b5d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf635a2b8e7db97773999a2312f1373bcbed62d4b673e4f4b366342d10e49d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9db95db985a47174f8d909edb357048bf2e17e247c6f441c7a0fe0204ab66bb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FsxOntapVolumeSnaplockConfigurationAutocommitPeriod]:
        return typing.cast(typing.Optional[FsxOntapVolumeSnaplockConfigurationAutocommitPeriod], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FsxOntapVolumeSnaplockConfigurationAutocommitPeriod],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b2780c725438724a95eef96a31189ab0cbb2f174e32d09c6d189dba1b45574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FsxOntapVolumeSnaplockConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fsxOntapVolume.FsxOntapVolumeSnaplockConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfce4ae7aac19f5fc9f97eef205517ff076785a403ea7f2b08c9a784b3188d52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutocommitPeriod")
    def put_autocommit_period(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#type FsxOntapVolume#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#value FsxOntapVolume#value}.
        '''
        value_ = FsxOntapVolumeSnaplockConfigurationAutocommitPeriod(
            type=type, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putAutocommitPeriod", [value_]))

    @jsii.member(jsii_name="putRetentionPeriod")
    def put_retention_period(
        self,
        *,
        default_retention: typing.Optional[typing.Union["FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetention", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_retention: typing.Optional[typing.Union["FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetention", typing.Dict[builtins.str, typing.Any]]] = None,
        minimum_retention: typing.Optional[typing.Union["FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetention", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param default_retention: default_retention block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#default_retention FsxOntapVolume#default_retention}
        :param maximum_retention: maximum_retention block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#maximum_retention FsxOntapVolume#maximum_retention}
        :param minimum_retention: minimum_retention block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#minimum_retention FsxOntapVolume#minimum_retention}
        '''
        value = FsxOntapVolumeSnaplockConfigurationRetentionPeriod(
            default_retention=default_retention,
            maximum_retention=maximum_retention,
            minimum_retention=minimum_retention,
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionPeriod", [value]))

    @jsii.member(jsii_name="resetAuditLogVolume")
    def reset_audit_log_volume(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuditLogVolume", []))

    @jsii.member(jsii_name="resetAutocommitPeriod")
    def reset_autocommit_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutocommitPeriod", []))

    @jsii.member(jsii_name="resetPrivilegedDelete")
    def reset_privileged_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivilegedDelete", []))

    @jsii.member(jsii_name="resetRetentionPeriod")
    def reset_retention_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPeriod", []))

    @jsii.member(jsii_name="resetVolumeAppendModeEnabled")
    def reset_volume_append_mode_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeAppendModeEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="autocommitPeriod")
    def autocommit_period(
        self,
    ) -> FsxOntapVolumeSnaplockConfigurationAutocommitPeriodOutputReference:
        return typing.cast(FsxOntapVolumeSnaplockConfigurationAutocommitPeriodOutputReference, jsii.get(self, "autocommitPeriod"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriod")
    def retention_period(
        self,
    ) -> "FsxOntapVolumeSnaplockConfigurationRetentionPeriodOutputReference":
        return typing.cast("FsxOntapVolumeSnaplockConfigurationRetentionPeriodOutputReference", jsii.get(self, "retentionPeriod"))

    @builtins.property
    @jsii.member(jsii_name="auditLogVolumeInput")
    def audit_log_volume_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "auditLogVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="autocommitPeriodInput")
    def autocommit_period_input(
        self,
    ) -> typing.Optional[FsxOntapVolumeSnaplockConfigurationAutocommitPeriod]:
        return typing.cast(typing.Optional[FsxOntapVolumeSnaplockConfigurationAutocommitPeriod], jsii.get(self, "autocommitPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="privilegedDeleteInput")
    def privileged_delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privilegedDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodInput")
    def retention_period_input(
        self,
    ) -> typing.Optional["FsxOntapVolumeSnaplockConfigurationRetentionPeriod"]:
        return typing.cast(typing.Optional["FsxOntapVolumeSnaplockConfigurationRetentionPeriod"], jsii.get(self, "retentionPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="snaplockTypeInput")
    def snaplock_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snaplockTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeAppendModeEnabledInput")
    def volume_append_mode_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "volumeAppendModeEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="auditLogVolume")
    def audit_log_volume(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "auditLogVolume"))

    @audit_log_volume.setter
    def audit_log_volume(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1f08e655fec017b72c20a38ee33c13eda79ed29ec5bfb00562d171f5f8c4756)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auditLogVolume", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privilegedDelete")
    def privileged_delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privilegedDelete"))

    @privileged_delete.setter
    def privileged_delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a15e920377d781d715e1472504f2f879f42335446d9e70e8e271c7c10db207b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privilegedDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snaplockType")
    def snaplock_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snaplockType"))

    @snaplock_type.setter
    def snaplock_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5092affa0e83daeb9ec6fa52e9045f779032e437547441e2fb0d39dcd35fca80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snaplockType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeAppendModeEnabled")
    def volume_append_mode_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "volumeAppendModeEnabled"))

    @volume_append_mode_enabled.setter
    def volume_append_mode_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b437b9a71dc22ffa53db7cb3e2b3cd810c8f90ac3283ef5615dcc5b2be6970bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeAppendModeEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FsxOntapVolumeSnaplockConfiguration]:
        return typing.cast(typing.Optional[FsxOntapVolumeSnaplockConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FsxOntapVolumeSnaplockConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfbd5639fe618b2ddca2874a02eb29e729b4bb950a35f16dc89c846bcfd143f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fsxOntapVolume.FsxOntapVolumeSnaplockConfigurationRetentionPeriod",
    jsii_struct_bases=[],
    name_mapping={
        "default_retention": "defaultRetention",
        "maximum_retention": "maximumRetention",
        "minimum_retention": "minimumRetention",
    },
)
class FsxOntapVolumeSnaplockConfigurationRetentionPeriod:
    def __init__(
        self,
        *,
        default_retention: typing.Optional[typing.Union["FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetention", typing.Dict[builtins.str, typing.Any]]] = None,
        maximum_retention: typing.Optional[typing.Union["FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetention", typing.Dict[builtins.str, typing.Any]]] = None,
        minimum_retention: typing.Optional[typing.Union["FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetention", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param default_retention: default_retention block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#default_retention FsxOntapVolume#default_retention}
        :param maximum_retention: maximum_retention block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#maximum_retention FsxOntapVolume#maximum_retention}
        :param minimum_retention: minimum_retention block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#minimum_retention FsxOntapVolume#minimum_retention}
        '''
        if isinstance(default_retention, dict):
            default_retention = FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetention(**default_retention)
        if isinstance(maximum_retention, dict):
            maximum_retention = FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetention(**maximum_retention)
        if isinstance(minimum_retention, dict):
            minimum_retention = FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetention(**minimum_retention)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb8828113ae3534f97005f71b93c09fd5de4224f5664ddee6884fcc0d551725)
            check_type(argname="argument default_retention", value=default_retention, expected_type=type_hints["default_retention"])
            check_type(argname="argument maximum_retention", value=maximum_retention, expected_type=type_hints["maximum_retention"])
            check_type(argname="argument minimum_retention", value=minimum_retention, expected_type=type_hints["minimum_retention"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_retention is not None:
            self._values["default_retention"] = default_retention
        if maximum_retention is not None:
            self._values["maximum_retention"] = maximum_retention
        if minimum_retention is not None:
            self._values["minimum_retention"] = minimum_retention

    @builtins.property
    def default_retention(
        self,
    ) -> typing.Optional["FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetention"]:
        '''default_retention block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#default_retention FsxOntapVolume#default_retention}
        '''
        result = self._values.get("default_retention")
        return typing.cast(typing.Optional["FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetention"], result)

    @builtins.property
    def maximum_retention(
        self,
    ) -> typing.Optional["FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetention"]:
        '''maximum_retention block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#maximum_retention FsxOntapVolume#maximum_retention}
        '''
        result = self._values.get("maximum_retention")
        return typing.cast(typing.Optional["FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetention"], result)

    @builtins.property
    def minimum_retention(
        self,
    ) -> typing.Optional["FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetention"]:
        '''minimum_retention block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#minimum_retention FsxOntapVolume#minimum_retention}
        '''
        result = self._values.get("minimum_retention")
        return typing.cast(typing.Optional["FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetention"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FsxOntapVolumeSnaplockConfigurationRetentionPeriod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fsxOntapVolume.FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetention",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetention:
    def __init__(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#type FsxOntapVolume#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#value FsxOntapVolume#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f0b1edeadb1ddeaba7747488638354a3708da3c2de19bf54e1b2d5eb97db66a)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#type FsxOntapVolume#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#value FsxOntapVolume#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetention(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetentionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fsxOntapVolume.FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetentionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9a068f377d696c44b67d833816469faade34f1a72b9d47c5f65518f10d9d15c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba5fb102ec16cfa6e6fbd7c8bc6d1af0e530f1ad4d3b1326af6cd59465fb5509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eda26caf7f47d8b96c48468a80e8acd0d7be3d6f9cda05554f0843fe8f804afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetention]:
        return typing.cast(typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetention], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetention],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c7f50fc19683f57357cc67129a260de88be70db5f52ae0b8d02f15ed5e75f66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fsxOntapVolume.FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetention",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetention:
    def __init__(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#type FsxOntapVolume#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#value FsxOntapVolume#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1563c248722e02393180a52c74b91ca48dd495fa1f16ffdca5bb838136b9da1a)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#type FsxOntapVolume#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#value FsxOntapVolume#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetention(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetentionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fsxOntapVolume.FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetentionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5794c7b237e24700f25d4b50d94ab93a454529f0c293dc90ec237e0103ad6ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75db6afc0288393907073d374acfff06c01141d1d4e92f673bc56e18e33ba1bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1130dde5bab2f459d33717dd4d03fa3b35c811d6af641d22a2c170ce27e94208)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetention]:
        return typing.cast(typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetention], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetention],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a2b9fce399c1b5cae86046e3455fe1abb22e9a47cff6c3704542c17bec8b067)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fsxOntapVolume.FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetention",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetention:
    def __init__(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#type FsxOntapVolume#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#value FsxOntapVolume#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__748f76b9ea72ac9cac0efab9bb4732c0e528fe938d236d889bfed073fef5edb0)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#type FsxOntapVolume#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#value FsxOntapVolume#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetention(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetentionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fsxOntapVolume.FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetentionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79536d4ac5942596413e529155d5a5ce002ec970ca4d809b652a462e02a2c78f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1bbfc03ebf29974ed14432a7cd194bf868818917cf00753a07fa86c4e44e047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7979fdb6168a4164de677c25e54817eec34680af00508ad56c401d578ed19b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetention]:
        return typing.cast(typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetention], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetention],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae291ebf92b0b382cd4cfeccbf2e9a7c36770e07da654cce5181a66c14bcbdbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FsxOntapVolumeSnaplockConfigurationRetentionPeriodOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fsxOntapVolume.FsxOntapVolumeSnaplockConfigurationRetentionPeriodOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f88d907a37d21250f1d2e3bf14cf4c9032bfcb2eb4e0f349e63035825a8fb89d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDefaultRetention")
    def put_default_retention(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#type FsxOntapVolume#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#value FsxOntapVolume#value}.
        '''
        value_ = FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetention(
            type=type, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultRetention", [value_]))

    @jsii.member(jsii_name="putMaximumRetention")
    def put_maximum_retention(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#type FsxOntapVolume#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#value FsxOntapVolume#value}.
        '''
        value_ = FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetention(
            type=type, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putMaximumRetention", [value_]))

    @jsii.member(jsii_name="putMinimumRetention")
    def put_minimum_retention(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#type FsxOntapVolume#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#value FsxOntapVolume#value}.
        '''
        value_ = FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetention(
            type=type, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putMinimumRetention", [value_]))

    @jsii.member(jsii_name="resetDefaultRetention")
    def reset_default_retention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultRetention", []))

    @jsii.member(jsii_name="resetMaximumRetention")
    def reset_maximum_retention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumRetention", []))

    @jsii.member(jsii_name="resetMinimumRetention")
    def reset_minimum_retention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumRetention", []))

    @builtins.property
    @jsii.member(jsii_name="defaultRetention")
    def default_retention(
        self,
    ) -> FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetentionOutputReference:
        return typing.cast(FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetentionOutputReference, jsii.get(self, "defaultRetention"))

    @builtins.property
    @jsii.member(jsii_name="maximumRetention")
    def maximum_retention(
        self,
    ) -> FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetentionOutputReference:
        return typing.cast(FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetentionOutputReference, jsii.get(self, "maximumRetention"))

    @builtins.property
    @jsii.member(jsii_name="minimumRetention")
    def minimum_retention(
        self,
    ) -> FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetentionOutputReference:
        return typing.cast(FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetentionOutputReference, jsii.get(self, "minimumRetention"))

    @builtins.property
    @jsii.member(jsii_name="defaultRetentionInput")
    def default_retention_input(
        self,
    ) -> typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetention]:
        return typing.cast(typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetention], jsii.get(self, "defaultRetentionInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumRetentionInput")
    def maximum_retention_input(
        self,
    ) -> typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetention]:
        return typing.cast(typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetention], jsii.get(self, "maximumRetentionInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumRetentionInput")
    def minimum_retention_input(
        self,
    ) -> typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetention]:
        return typing.cast(typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetention], jsii.get(self, "minimumRetentionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriod]:
        return typing.cast(typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriod], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriod],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__914e4348a0d8891ea1eb24b79d38b9426e77720481c30edc599fec85302c1b59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fsxOntapVolume.FsxOntapVolumeTieringPolicy",
    jsii_struct_bases=[],
    name_mapping={"cooling_period": "coolingPeriod", "name": "name"},
)
class FsxOntapVolumeTieringPolicy:
    def __init__(
        self,
        *,
        cooling_period: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cooling_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#cooling_period FsxOntapVolume#cooling_period}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#name FsxOntapVolume#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc1d2ba7ac512f367f01894da5361bed6560a793a8f353a0a34a6c68741aa817)
            check_type(argname="argument cooling_period", value=cooling_period, expected_type=type_hints["cooling_period"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cooling_period is not None:
            self._values["cooling_period"] = cooling_period
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def cooling_period(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#cooling_period FsxOntapVolume#cooling_period}.'''
        result = self._values.get("cooling_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#name FsxOntapVolume#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FsxOntapVolumeTieringPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FsxOntapVolumeTieringPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fsxOntapVolume.FsxOntapVolumeTieringPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da790d9f1cc7ffa666361820615877326ba8fbc26ebfbb0de9e156bcdc4256c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCoolingPeriod")
    def reset_cooling_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoolingPeriod", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="coolingPeriodInput")
    def cooling_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coolingPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="coolingPeriod")
    def cooling_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "coolingPeriod"))

    @cooling_period.setter
    def cooling_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67c6b42792bdd0a0f5fcc9a98e83c369ed7d2b8e252b4359416facec73913e3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coolingPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bf5da0a8388765ef3ed29da8ab3532630ab43246b95780186a7dfc37f765eb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FsxOntapVolumeTieringPolicy]:
        return typing.cast(typing.Optional[FsxOntapVolumeTieringPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FsxOntapVolumeTieringPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb3e0bd9064ac03cc32a3f3e18e3acc7c541915f4615c98fb1cd3bdcba08528)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.fsxOntapVolume.FsxOntapVolumeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class FsxOntapVolumeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#create FsxOntapVolume#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#delete FsxOntapVolume#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#update FsxOntapVolume#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96203840f30ef221b4d548c18ad85a3dfbcd2d315c57d6de7873ab3358fbde7)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#create FsxOntapVolume#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#delete FsxOntapVolume#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/fsx_ontap_volume#update FsxOntapVolume#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FsxOntapVolumeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FsxOntapVolumeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.fsxOntapVolume.FsxOntapVolumeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c911a510dd1a35257400797e6c5beb949602a6e3535f9383c488e358be20a42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c14c0755e1616224fdd4d732c62a40273b1d266ae4c4b5c6986111d446a008e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83f15da449456346e1dd87322f1840969e95676c8ad87e9a7916259fd5da69d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f9481255ccc66e048979c6d75d9f2c75d66a74506d261f442429782b36c7bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FsxOntapVolumeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FsxOntapVolumeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FsxOntapVolumeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f052018b6c61534e3cf6d98afe19fb0d75da1272a595660da34a9844e9d3963)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FsxOntapVolume",
    "FsxOntapVolumeAggregateConfiguration",
    "FsxOntapVolumeAggregateConfigurationOutputReference",
    "FsxOntapVolumeConfig",
    "FsxOntapVolumeSnaplockConfiguration",
    "FsxOntapVolumeSnaplockConfigurationAutocommitPeriod",
    "FsxOntapVolumeSnaplockConfigurationAutocommitPeriodOutputReference",
    "FsxOntapVolumeSnaplockConfigurationOutputReference",
    "FsxOntapVolumeSnaplockConfigurationRetentionPeriod",
    "FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetention",
    "FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetentionOutputReference",
    "FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetention",
    "FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetentionOutputReference",
    "FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetention",
    "FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetentionOutputReference",
    "FsxOntapVolumeSnaplockConfigurationRetentionPeriodOutputReference",
    "FsxOntapVolumeTieringPolicy",
    "FsxOntapVolumeTieringPolicyOutputReference",
    "FsxOntapVolumeTimeouts",
    "FsxOntapVolumeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__5a805007864cd3868bfa1ad56f0043baba0659b9e610d0916a71aecfbd14b6ad(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    storage_virtual_machine_id: builtins.str,
    aggregate_configuration: typing.Optional[typing.Union[FsxOntapVolumeAggregateConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    bypass_snaplock_enterprise_retention: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    copy_tags_to_backups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    final_backup_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    junction_path: typing.Optional[builtins.str] = None,
    ontap_volume_type: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    security_style: typing.Optional[builtins.str] = None,
    size_in_bytes: typing.Optional[builtins.str] = None,
    size_in_megabytes: typing.Optional[jsii.Number] = None,
    skip_final_backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    snaplock_configuration: typing.Optional[typing.Union[FsxOntapVolumeSnaplockConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    snapshot_policy: typing.Optional[builtins.str] = None,
    storage_efficiency_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tiering_policy: typing.Optional[typing.Union[FsxOntapVolumeTieringPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[FsxOntapVolumeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    volume_style: typing.Optional[builtins.str] = None,
    volume_type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__2410589cf366c53e6c91a6d5e32fb979ee421f3b23d6e27df9416da277a57cdd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd936f7ad6427df0dd8db6a8809fa9b626756f991fddb37e87b8f69592529a6b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a720083beb8ed160f761bc12cba78b71c96aa9e570838070b0ce4de1f29fd69b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d672b37a0dcbc4468c5e0374ab4a92a46722863ae01774d589a2dd109feb782d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7beb88ded730face2c2903fa17393d45524bce011550252eca001e02b5338586(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d628e2ad34bb90b7f735b210eeca055aa75fa5b8993a65b5f9a6f3a56ab56f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e441e214d5a274f897f70d9c1cf1e0fecb8b96fa9082c7e8a68f1e173b9f94b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e572e6dd2a3d64677cca0b198c4a2f2824a02b8af58769fce5c441b1570dc868(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42c31d1a8759c3a7da4f990c7b07eaa71d7adf7ae4dc962222a5ba435c1a02dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe87d7e3cabf132cf2e6e077261e7c7554fb8d555234e6ea283a5dbb9a8df44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f27721d33823680322282133363b2a042cc5c6eb92fd24bc4081453d4e609fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703d61100a963653cf53fa8e15bddeffd0b7ffcbda71201595039d336c94dc5b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__919a296702c747bd366cb25896e99366168dcdcf8c9924de424faa8f94e1786f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d7e2bc3faa9696a7d974541ab6f1f18d6dcfe6092d16e854a4d5d6cd687449(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e902074a38655015badf2c3ad99c7c2cd44bdd5bfb920927fc2c15cee73aa8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfffdacfca88f1fb7b96999aed6939bc609cdfc60fc09c41be65ce50f9c5d754(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f12bf0713704cb03d09885e065d77fe6226085c747f39784a9fc508ae324a928(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ccc8d77da37aaa2373073da9749bcce4bdc20651368df51fc628ea076cbe1f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3e16e47d2538a7af0d76af419c6539edae2f89af5605bf619633a4dd5159cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e9f9c76f6b5b5a38ee4225aa0ab2a95e833db3d733aad43451a4614c039c1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4eaa305fc5fd125fed5c17939b86eadcec416546a0f2acfa3f278896e3dc84(
    *,
    aggregates: typing.Optional[typing.Sequence[builtins.str]] = None,
    constituents_per_aggregate: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8410bc24bdddcd0de16c597bd7700ceb7cbc3cf9f5dfc690178206e105513ccb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d51c2ec2574af814676ae41deae402c4e316f280020ab536c9da12ab9a78cd8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bbf3f36a9805562d091b4120c66d348ad64cbde27f7f4417c1e370193a3a7a4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0e5736089a7ec90f734ef73acf7565d2521e417d27e29b2eef18c58617d921a(
    value: typing.Optional[FsxOntapVolumeAggregateConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d37faa495e1e5e716a06fb89bcfd992756f080e35cecb77dbd06162d2fddb0bf(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    storage_virtual_machine_id: builtins.str,
    aggregate_configuration: typing.Optional[typing.Union[FsxOntapVolumeAggregateConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    bypass_snaplock_enterprise_retention: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    copy_tags_to_backups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    final_backup_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    junction_path: typing.Optional[builtins.str] = None,
    ontap_volume_type: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    security_style: typing.Optional[builtins.str] = None,
    size_in_bytes: typing.Optional[builtins.str] = None,
    size_in_megabytes: typing.Optional[jsii.Number] = None,
    skip_final_backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    snaplock_configuration: typing.Optional[typing.Union[FsxOntapVolumeSnaplockConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    snapshot_policy: typing.Optional[builtins.str] = None,
    storage_efficiency_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tiering_policy: typing.Optional[typing.Union[FsxOntapVolumeTieringPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[FsxOntapVolumeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    volume_style: typing.Optional[builtins.str] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b70024be950e757d19f914249fc38354860c49c2bd88ecbdb5e8dd77ca4a3590(
    *,
    snaplock_type: builtins.str,
    audit_log_volume: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    autocommit_period: typing.Optional[typing.Union[FsxOntapVolumeSnaplockConfigurationAutocommitPeriod, typing.Dict[builtins.str, typing.Any]]] = None,
    privileged_delete: typing.Optional[builtins.str] = None,
    retention_period: typing.Optional[typing.Union[FsxOntapVolumeSnaplockConfigurationRetentionPeriod, typing.Dict[builtins.str, typing.Any]]] = None,
    volume_append_mode_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16cb0b279dc644cf807dc492b5e449016bed9d9e0fe048228d3d0b0f5552b6c6(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0200f131553398095670fa277b5ebd0cbc4132a3200d16a0995c5b28b2ec5b5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf635a2b8e7db97773999a2312f1373bcbed62d4b673e4f4b366342d10e49d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db95db985a47174f8d909edb357048bf2e17e247c6f441c7a0fe0204ab66bb6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b2780c725438724a95eef96a31189ab0cbb2f174e32d09c6d189dba1b45574(
    value: typing.Optional[FsxOntapVolumeSnaplockConfigurationAutocommitPeriod],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfce4ae7aac19f5fc9f97eef205517ff076785a403ea7f2b08c9a784b3188d52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1f08e655fec017b72c20a38ee33c13eda79ed29ec5bfb00562d171f5f8c4756(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a15e920377d781d715e1472504f2f879f42335446d9e70e8e271c7c10db207b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5092affa0e83daeb9ec6fa52e9045f779032e437547441e2fb0d39dcd35fca80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b437b9a71dc22ffa53db7cb3e2b3cd810c8f90ac3283ef5615dcc5b2be6970bb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfbd5639fe618b2ddca2874a02eb29e729b4bb950a35f16dc89c846bcfd143f5(
    value: typing.Optional[FsxOntapVolumeSnaplockConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb8828113ae3534f97005f71b93c09fd5de4224f5664ddee6884fcc0d551725(
    *,
    default_retention: typing.Optional[typing.Union[FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetention, typing.Dict[builtins.str, typing.Any]]] = None,
    maximum_retention: typing.Optional[typing.Union[FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetention, typing.Dict[builtins.str, typing.Any]]] = None,
    minimum_retention: typing.Optional[typing.Union[FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetention, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f0b1edeadb1ddeaba7747488638354a3708da3c2de19bf54e1b2d5eb97db66a(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a068f377d696c44b67d833816469faade34f1a72b9d47c5f65518f10d9d15c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba5fb102ec16cfa6e6fbd7c8bc6d1af0e530f1ad4d3b1326af6cd59465fb5509(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda26caf7f47d8b96c48468a80e8acd0d7be3d6f9cda05554f0843fe8f804afa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c7f50fc19683f57357cc67129a260de88be70db5f52ae0b8d02f15ed5e75f66(
    value: typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriodDefaultRetention],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1563c248722e02393180a52c74b91ca48dd495fa1f16ffdca5bb838136b9da1a(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5794c7b237e24700f25d4b50d94ab93a454529f0c293dc90ec237e0103ad6ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75db6afc0288393907073d374acfff06c01141d1d4e92f673bc56e18e33ba1bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1130dde5bab2f459d33717dd4d03fa3b35c811d6af641d22a2c170ce27e94208(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a2b9fce399c1b5cae86046e3455fe1abb22e9a47cff6c3704542c17bec8b067(
    value: typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriodMaximumRetention],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__748f76b9ea72ac9cac0efab9bb4732c0e528fe938d236d889bfed073fef5edb0(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79536d4ac5942596413e529155d5a5ce002ec970ca4d809b652a462e02a2c78f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1bbfc03ebf29974ed14432a7cd194bf868818917cf00753a07fa86c4e44e047(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7979fdb6168a4164de677c25e54817eec34680af00508ad56c401d578ed19b3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae291ebf92b0b382cd4cfeccbf2e9a7c36770e07da654cce5181a66c14bcbdbf(
    value: typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriodMinimumRetention],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f88d907a37d21250f1d2e3bf14cf4c9032bfcb2eb4e0f349e63035825a8fb89d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__914e4348a0d8891ea1eb24b79d38b9426e77720481c30edc599fec85302c1b59(
    value: typing.Optional[FsxOntapVolumeSnaplockConfigurationRetentionPeriod],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1d2ba7ac512f367f01894da5361bed6560a793a8f353a0a34a6c68741aa817(
    *,
    cooling_period: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da790d9f1cc7ffa666361820615877326ba8fbc26ebfbb0de9e156bcdc4256c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c6b42792bdd0a0f5fcc9a98e83c369ed7d2b8e252b4359416facec73913e3d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf5da0a8388765ef3ed29da8ab3532630ab43246b95780186a7dfc37f765eb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb3e0bd9064ac03cc32a3f3e18e3acc7c541915f4615c98fb1cd3bdcba08528(
    value: typing.Optional[FsxOntapVolumeTieringPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96203840f30ef221b4d548c18ad85a3dfbcd2d315c57d6de7873ab3358fbde7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c911a510dd1a35257400797e6c5beb949602a6e3535f9383c488e358be20a42(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c14c0755e1616224fdd4d732c62a40273b1d266ae4c4b5c6986111d446a008e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83f15da449456346e1dd87322f1840969e95676c8ad87e9a7916259fd5da69d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f9481255ccc66e048979c6d75d9f2c75d66a74506d261f442429782b36c7bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f052018b6c61534e3cf6d98afe19fb0d75da1272a595660da34a9844e9d3963(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FsxOntapVolumeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
