r'''
# `aws_odb_cloud_vm_cluster`

Refer to the Terraform Registry for docs: [`aws_odb_cloud_vm_cluster`](https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster).
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


class OdbCloudVmCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.odbCloudVmCluster.OdbCloudVmCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster aws_odb_cloud_vm_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cpu_core_count: jsii.Number,
        data_storage_size_in_tbs: jsii.Number,
        db_servers: typing.Sequence[builtins.str],
        display_name: builtins.str,
        gi_version: builtins.str,
        hostname_prefix: builtins.str,
        ssh_public_keys: typing.Sequence[builtins.str],
        cloud_exadata_infrastructure_arn: typing.Optional[builtins.str] = None,
        cloud_exadata_infrastructure_id: typing.Optional[builtins.str] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        data_collection_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OdbCloudVmClusterDataCollectionOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        db_node_storage_size_in_gbs: typing.Optional[jsii.Number] = None,
        is_local_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_sparse_diskgroup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        license_model: typing.Optional[builtins.str] = None,
        memory_size_in_gbs: typing.Optional[jsii.Number] = None,
        odb_network_arn: typing.Optional[builtins.str] = None,
        odb_network_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        scan_listener_port_tcp: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["OdbCloudVmClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timezone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster aws_odb_cloud_vm_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cpu_core_count: The number of CPU cores to enable on the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#cpu_core_count OdbCloudVmCluster#cpu_core_count}
        :param data_storage_size_in_tbs: The size of the data disk group, in terabytes (TBs), to allocate for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#data_storage_size_in_tbs OdbCloudVmCluster#data_storage_size_in_tbs}
        :param db_servers: The list of database servers for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#db_servers OdbCloudVmCluster#db_servers}
        :param display_name: A user-friendly name for the VM cluster. This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#display_name OdbCloudVmCluster#display_name}
        :param gi_version: A valid software version of Oracle Grid Infrastructure (GI). To get the list of valid values, use the ListGiVersions operation and specify the shape of the Exadata infrastructure. Example: 19.0.0.0 This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#gi_version OdbCloudVmCluster#gi_version}
        :param hostname_prefix: The host name prefix for the VM cluster. Constraints: - Can't be "localhost" or "hostname". - Can't contain "-version". - The maximum length of the combined hostname and domain is 63 characters. - The hostname must be unique within the subnet. This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#hostname_prefix OdbCloudVmCluster#hostname_prefix}
        :param ssh_public_keys: The public key portion of one or more key pairs used for SSH access to the VM cluster. This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#ssh_public_keys OdbCloudVmCluster#ssh_public_keys}
        :param cloud_exadata_infrastructure_arn: The unique identifier of the Exadata infrastructure for this VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#cloud_exadata_infrastructure_arn OdbCloudVmCluster#cloud_exadata_infrastructure_arn}
        :param cloud_exadata_infrastructure_id: The unique identifier of the Exadata infrastructure for this VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#cloud_exadata_infrastructure_id OdbCloudVmCluster#cloud_exadata_infrastructure_id}
        :param cluster_name: The name of the Grid Infrastructure (GI) cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#cluster_name OdbCloudVmCluster#cluster_name}
        :param data_collection_options: data_collection_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#data_collection_options OdbCloudVmCluster#data_collection_options}
        :param db_node_storage_size_in_gbs: The amount of local node storage, in gigabytes (GBs), to allocate for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#db_node_storage_size_in_gbs OdbCloudVmCluster#db_node_storage_size_in_gbs}
        :param is_local_backup_enabled: Specifies whether to enable database backups to local Exadata storage for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#is_local_backup_enabled OdbCloudVmCluster#is_local_backup_enabled}
        :param is_sparse_diskgroup_enabled: Specifies whether to create a sparse disk group for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#is_sparse_diskgroup_enabled OdbCloudVmCluster#is_sparse_diskgroup_enabled}
        :param license_model: The Oracle license model to apply to the VM cluster. Default: LICENSE_INCLUDED. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#license_model OdbCloudVmCluster#license_model}
        :param memory_size_in_gbs: The amount of memory, in gigabytes (GBs), to allocate for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#memory_size_in_gbs OdbCloudVmCluster#memory_size_in_gbs}
        :param odb_network_arn: The unique identifier of the ODB network for the VM cluster. This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#odb_network_arn OdbCloudVmCluster#odb_network_arn}
        :param odb_network_id: The unique identifier of the ODB network for the VM cluster. This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#odb_network_id OdbCloudVmCluster#odb_network_id}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#region OdbCloudVmCluster#region}
        :param scan_listener_port_tcp: The port number for TCP connections to the single client access name (SCAN) listener. Valid values: 1024–8999 with the following exceptions: 2484 , 6100 , 6200 , 7060, 7070 , 7085 , and 7879Default: 1521. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#scan_listener_port_tcp OdbCloudVmCluster#scan_listener_port_tcp}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#tags OdbCloudVmCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#timeouts OdbCloudVmCluster#timeouts}
        :param timezone: The configured time zone of the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#timezone OdbCloudVmCluster#timezone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__001dc733a1fa4ae4d53916f2774a4007b8c1c9d6773e10857e163a226e1b3374)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = OdbCloudVmClusterConfig(
            cpu_core_count=cpu_core_count,
            data_storage_size_in_tbs=data_storage_size_in_tbs,
            db_servers=db_servers,
            display_name=display_name,
            gi_version=gi_version,
            hostname_prefix=hostname_prefix,
            ssh_public_keys=ssh_public_keys,
            cloud_exadata_infrastructure_arn=cloud_exadata_infrastructure_arn,
            cloud_exadata_infrastructure_id=cloud_exadata_infrastructure_id,
            cluster_name=cluster_name,
            data_collection_options=data_collection_options,
            db_node_storage_size_in_gbs=db_node_storage_size_in_gbs,
            is_local_backup_enabled=is_local_backup_enabled,
            is_sparse_diskgroup_enabled=is_sparse_diskgroup_enabled,
            license_model=license_model,
            memory_size_in_gbs=memory_size_in_gbs,
            odb_network_arn=odb_network_arn,
            odb_network_id=odb_network_id,
            region=region,
            scan_listener_port_tcp=scan_listener_port_tcp,
            tags=tags,
            timeouts=timeouts,
            timezone=timezone,
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
        '''Generates CDKTF code for importing a OdbCloudVmCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OdbCloudVmCluster to import.
        :param import_from_id: The id of the existing OdbCloudVmCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OdbCloudVmCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b97420e9120267b7bcb123a084073ec9aa223f3c92509147be4cd83d0444ab)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDataCollectionOptions")
    def put_data_collection_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OdbCloudVmClusterDataCollectionOptions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccd2bdd4cf4451b9a1ede1109ba3305cd65fd094a70c62d0397d90ae8aba57e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataCollectionOptions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#create OdbCloudVmCluster#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#delete OdbCloudVmCluster#delete}
        :param update: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#update OdbCloudVmCluster#update}
        '''
        value = OdbCloudVmClusterTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCloudExadataInfrastructureArn")
    def reset_cloud_exadata_infrastructure_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudExadataInfrastructureArn", []))

    @jsii.member(jsii_name="resetCloudExadataInfrastructureId")
    def reset_cloud_exadata_infrastructure_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudExadataInfrastructureId", []))

    @jsii.member(jsii_name="resetClusterName")
    def reset_cluster_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterName", []))

    @jsii.member(jsii_name="resetDataCollectionOptions")
    def reset_data_collection_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataCollectionOptions", []))

    @jsii.member(jsii_name="resetDbNodeStorageSizeInGbs")
    def reset_db_node_storage_size_in_gbs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbNodeStorageSizeInGbs", []))

    @jsii.member(jsii_name="resetIsLocalBackupEnabled")
    def reset_is_local_backup_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsLocalBackupEnabled", []))

    @jsii.member(jsii_name="resetIsSparseDiskgroupEnabled")
    def reset_is_sparse_diskgroup_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSparseDiskgroupEnabled", []))

    @jsii.member(jsii_name="resetLicenseModel")
    def reset_license_model(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicenseModel", []))

    @jsii.member(jsii_name="resetMemorySizeInGbs")
    def reset_memory_size_in_gbs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemorySizeInGbs", []))

    @jsii.member(jsii_name="resetOdbNetworkArn")
    def reset_odb_network_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOdbNetworkArn", []))

    @jsii.member(jsii_name="resetOdbNetworkId")
    def reset_odb_network_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOdbNetworkId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetScanListenerPortTcp")
    def reset_scan_listener_port_tcp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScanListenerPortTcp", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTimezone")
    def reset_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimezone", []))

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
    @jsii.member(jsii_name="computeModel")
    def compute_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computeModel"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="dataCollectionOptions")
    def data_collection_options(self) -> "OdbCloudVmClusterDataCollectionOptionsList":
        return typing.cast("OdbCloudVmClusterDataCollectionOptionsList", jsii.get(self, "dataCollectionOptions"))

    @builtins.property
    @jsii.member(jsii_name="diskRedundancy")
    def disk_redundancy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskRedundancy"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @builtins.property
    @jsii.member(jsii_name="giVersionComputed")
    def gi_version_computed(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "giVersionComputed"))

    @builtins.property
    @jsii.member(jsii_name="hostnamePrefixComputed")
    def hostname_prefix_computed(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostnamePrefixComputed"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="iormConfigCache")
    def iorm_config_cache(self) -> "OdbCloudVmClusterIormConfigCacheList":
        return typing.cast("OdbCloudVmClusterIormConfigCacheList", jsii.get(self, "iormConfigCache"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdateHistoryEntryId")
    def last_update_history_entry_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdateHistoryEntryId"))

    @builtins.property
    @jsii.member(jsii_name="listenerPort")
    def listener_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "listenerPort"))

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @builtins.property
    @jsii.member(jsii_name="ocid")
    def ocid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ocid"))

    @builtins.property
    @jsii.member(jsii_name="ociResourceAnchorName")
    def oci_resource_anchor_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociResourceAnchorName"))

    @builtins.property
    @jsii.member(jsii_name="ociUrl")
    def oci_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociUrl"))

    @builtins.property
    @jsii.member(jsii_name="percentProgress")
    def percent_progress(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentProgress"))

    @builtins.property
    @jsii.member(jsii_name="scanDnsName")
    def scan_dns_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scanDnsName"))

    @builtins.property
    @jsii.member(jsii_name="scanDnsRecordId")
    def scan_dns_record_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scanDnsRecordId"))

    @builtins.property
    @jsii.member(jsii_name="scanIpIds")
    def scan_ip_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scanIpIds"))

    @builtins.property
    @jsii.member(jsii_name="shape")
    def shape(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shape"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="statusReason")
    def status_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statusReason"))

    @builtins.property
    @jsii.member(jsii_name="storageSizeInGbs")
    def storage_size_in_gbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageSizeInGbs"))

    @builtins.property
    @jsii.member(jsii_name="systemVersion")
    def system_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemVersion"))

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tagsAll"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "OdbCloudVmClusterTimeoutsOutputReference":
        return typing.cast("OdbCloudVmClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vipIds")
    def vip_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vipIds"))

    @builtins.property
    @jsii.member(jsii_name="cloudExadataInfrastructureArnInput")
    def cloud_exadata_infrastructure_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudExadataInfrastructureArnInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudExadataInfrastructureIdInput")
    def cloud_exadata_infrastructure_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudExadataInfrastructureIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterNameInput")
    def cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuCoreCountInput")
    def cpu_core_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuCoreCountInput"))

    @builtins.property
    @jsii.member(jsii_name="dataCollectionOptionsInput")
    def data_collection_options_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OdbCloudVmClusterDataCollectionOptions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OdbCloudVmClusterDataCollectionOptions"]]], jsii.get(self, "dataCollectionOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeInTbsInput")
    def data_storage_size_in_tbs_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataStorageSizeInTbsInput"))

    @builtins.property
    @jsii.member(jsii_name="dbNodeStorageSizeInGbsInput")
    def db_node_storage_size_in_gbs_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dbNodeStorageSizeInGbsInput"))

    @builtins.property
    @jsii.member(jsii_name="dbServersInput")
    def db_servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dbServersInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="giVersionInput")
    def gi_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "giVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnamePrefixInput")
    def hostname_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnamePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="isLocalBackupEnabledInput")
    def is_local_backup_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isLocalBackupEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isSparseDiskgroupEnabledInput")
    def is_sparse_diskgroup_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isSparseDiskgroupEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseModelInput")
    def license_model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseModelInput"))

    @builtins.property
    @jsii.member(jsii_name="memorySizeInGbsInput")
    def memory_size_in_gbs_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memorySizeInGbsInput"))

    @builtins.property
    @jsii.member(jsii_name="odbNetworkArnInput")
    def odb_network_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "odbNetworkArnInput"))

    @builtins.property
    @jsii.member(jsii_name="odbNetworkIdInput")
    def odb_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "odbNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="scanListenerPortTcpInput")
    def scan_listener_port_tcp_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scanListenerPortTcpInput"))

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeysInput")
    def ssh_public_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sshPublicKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OdbCloudVmClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OdbCloudVmClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timezoneInput")
    def timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudExadataInfrastructureArn")
    def cloud_exadata_infrastructure_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudExadataInfrastructureArn"))

    @cloud_exadata_infrastructure_arn.setter
    def cloud_exadata_infrastructure_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95a6af93116a71031cc10ee1fb4957667d5adb35cbf5d854d83ccac062fc7e3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudExadataInfrastructureArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cloudExadataInfrastructureId")
    def cloud_exadata_infrastructure_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudExadataInfrastructureId"))

    @cloud_exadata_infrastructure_id.setter
    def cloud_exadata_infrastructure_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd9783dc11297a9d1a28ae3fa449064778f976cd17e1e80329b8d1213997189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudExadataInfrastructureId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c05e14111e238a5da8df49a19d155205647c036b9da31f8d365b6dfcd57a66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuCoreCount")
    def cpu_core_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuCoreCount"))

    @cpu_core_count.setter
    def cpu_core_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e075499e48cbca2d0a483f8cc31b0d39f1a6845110e6cd0cdfbbaf9be7d41dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCoreCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeInTbs")
    def data_storage_size_in_tbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataStorageSizeInTbs"))

    @data_storage_size_in_tbs.setter
    def data_storage_size_in_tbs(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b9203865c0b3b39517bda9179d98f908804e35e951f377300f213f50d2af565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStorageSizeInTbs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbNodeStorageSizeInGbs")
    def db_node_storage_size_in_gbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dbNodeStorageSizeInGbs"))

    @db_node_storage_size_in_gbs.setter
    def db_node_storage_size_in_gbs(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeaee6273b57f877789e0e7639a8beab405aaa25ff112235727eb19c52b0882b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbNodeStorageSizeInGbs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbServers")
    def db_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dbServers"))

    @db_servers.setter
    def db_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfc8579573b95eee3dba016646e57f16044ca5a278a3720c1e0cb15d5dfb9c91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__793b1afe8f55ce28919fadcd1402fe4c4223f8a7fbd09daef24624abc343bea9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="giVersion")
    def gi_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "giVersion"))

    @gi_version.setter
    def gi_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bb82411165eace2dbf06cf68a42b6787db6df7c63970af530bc5654a26b713f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "giVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostnamePrefix")
    def hostname_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostnamePrefix"))

    @hostname_prefix.setter
    def hostname_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaf887f212e3fd05095ae716503f68c3831a5e167fa206111d874d66856765c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostnamePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isLocalBackupEnabled")
    def is_local_backup_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isLocalBackupEnabled"))

    @is_local_backup_enabled.setter
    def is_local_backup_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d792d012ac46bffdac948815335d875c015cb237cf3ce56aa4017e0266f3499)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isLocalBackupEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isSparseDiskgroupEnabled")
    def is_sparse_diskgroup_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isSparseDiskgroupEnabled"))

    @is_sparse_diskgroup_enabled.setter
    def is_sparse_diskgroup_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e6af43d7d4fa013001c907fa05368669569f4dc16671ba0a8836f296c57c60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSparseDiskgroupEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="licenseModel")
    def license_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "licenseModel"))

    @license_model.setter
    def license_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca1887b97ce7192b4b814e613bcc264212e788cc3b0c268213454ea179455422)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memorySizeInGbs")
    def memory_size_in_gbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySizeInGbs"))

    @memory_size_in_gbs.setter
    def memory_size_in_gbs(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b039f72f5d977fb616b375b7f6cdcda849c87d53f2f5b27922eb6f5cf89261b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memorySizeInGbs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="odbNetworkArn")
    def odb_network_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "odbNetworkArn"))

    @odb_network_arn.setter
    def odb_network_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42e658e79b7cb14a75a70120c1ed1349fbd2066495933d8a0d12281e98a85642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "odbNetworkArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="odbNetworkId")
    def odb_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "odbNetworkId"))

    @odb_network_id.setter
    def odb_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bbc264a323451f682da1476bfee043c0bbc6a063ae80c705cd14aada920775d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "odbNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b35bdc192ff63bb2bf0409305f1fe961adc350e56ee4ea9e821a414dcc8cf830)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scanListenerPortTcp")
    def scan_listener_port_tcp(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scanListenerPortTcp"))

    @scan_listener_port_tcp.setter
    def scan_listener_port_tcp(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26aa7401e1a658885a1f9d2beea26422c540dd563550b5f17a322042d7fb023b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scanListenerPortTcp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeys")
    def ssh_public_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshPublicKeys"))

    @ssh_public_keys.setter
    def ssh_public_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bb157c5165acd79110bf70ba0f661703af17311043cc1532d04bd9c06384856)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPublicKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26635f215a4323da4715fcf6fcfb705855e282962951a33b10c6d1c9a1e6029e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d4b02d19da9cbee2067d357fd510e259d1591320915b4a3c476c716e58eaca6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.odbCloudVmCluster.OdbCloudVmClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cpu_core_count": "cpuCoreCount",
        "data_storage_size_in_tbs": "dataStorageSizeInTbs",
        "db_servers": "dbServers",
        "display_name": "displayName",
        "gi_version": "giVersion",
        "hostname_prefix": "hostnamePrefix",
        "ssh_public_keys": "sshPublicKeys",
        "cloud_exadata_infrastructure_arn": "cloudExadataInfrastructureArn",
        "cloud_exadata_infrastructure_id": "cloudExadataInfrastructureId",
        "cluster_name": "clusterName",
        "data_collection_options": "dataCollectionOptions",
        "db_node_storage_size_in_gbs": "dbNodeStorageSizeInGbs",
        "is_local_backup_enabled": "isLocalBackupEnabled",
        "is_sparse_diskgroup_enabled": "isSparseDiskgroupEnabled",
        "license_model": "licenseModel",
        "memory_size_in_gbs": "memorySizeInGbs",
        "odb_network_arn": "odbNetworkArn",
        "odb_network_id": "odbNetworkId",
        "region": "region",
        "scan_listener_port_tcp": "scanListenerPortTcp",
        "tags": "tags",
        "timeouts": "timeouts",
        "timezone": "timezone",
    },
)
class OdbCloudVmClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cpu_core_count: jsii.Number,
        data_storage_size_in_tbs: jsii.Number,
        db_servers: typing.Sequence[builtins.str],
        display_name: builtins.str,
        gi_version: builtins.str,
        hostname_prefix: builtins.str,
        ssh_public_keys: typing.Sequence[builtins.str],
        cloud_exadata_infrastructure_arn: typing.Optional[builtins.str] = None,
        cloud_exadata_infrastructure_id: typing.Optional[builtins.str] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        data_collection_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OdbCloudVmClusterDataCollectionOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        db_node_storage_size_in_gbs: typing.Optional[jsii.Number] = None,
        is_local_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_sparse_diskgroup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        license_model: typing.Optional[builtins.str] = None,
        memory_size_in_gbs: typing.Optional[jsii.Number] = None,
        odb_network_arn: typing.Optional[builtins.str] = None,
        odb_network_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        scan_listener_port_tcp: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["OdbCloudVmClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timezone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cpu_core_count: The number of CPU cores to enable on the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#cpu_core_count OdbCloudVmCluster#cpu_core_count}
        :param data_storage_size_in_tbs: The size of the data disk group, in terabytes (TBs), to allocate for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#data_storage_size_in_tbs OdbCloudVmCluster#data_storage_size_in_tbs}
        :param db_servers: The list of database servers for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#db_servers OdbCloudVmCluster#db_servers}
        :param display_name: A user-friendly name for the VM cluster. This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#display_name OdbCloudVmCluster#display_name}
        :param gi_version: A valid software version of Oracle Grid Infrastructure (GI). To get the list of valid values, use the ListGiVersions operation and specify the shape of the Exadata infrastructure. Example: 19.0.0.0 This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#gi_version OdbCloudVmCluster#gi_version}
        :param hostname_prefix: The host name prefix for the VM cluster. Constraints: - Can't be "localhost" or "hostname". - Can't contain "-version". - The maximum length of the combined hostname and domain is 63 characters. - The hostname must be unique within the subnet. This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#hostname_prefix OdbCloudVmCluster#hostname_prefix}
        :param ssh_public_keys: The public key portion of one or more key pairs used for SSH access to the VM cluster. This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#ssh_public_keys OdbCloudVmCluster#ssh_public_keys}
        :param cloud_exadata_infrastructure_arn: The unique identifier of the Exadata infrastructure for this VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#cloud_exadata_infrastructure_arn OdbCloudVmCluster#cloud_exadata_infrastructure_arn}
        :param cloud_exadata_infrastructure_id: The unique identifier of the Exadata infrastructure for this VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#cloud_exadata_infrastructure_id OdbCloudVmCluster#cloud_exadata_infrastructure_id}
        :param cluster_name: The name of the Grid Infrastructure (GI) cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#cluster_name OdbCloudVmCluster#cluster_name}
        :param data_collection_options: data_collection_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#data_collection_options OdbCloudVmCluster#data_collection_options}
        :param db_node_storage_size_in_gbs: The amount of local node storage, in gigabytes (GBs), to allocate for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#db_node_storage_size_in_gbs OdbCloudVmCluster#db_node_storage_size_in_gbs}
        :param is_local_backup_enabled: Specifies whether to enable database backups to local Exadata storage for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#is_local_backup_enabled OdbCloudVmCluster#is_local_backup_enabled}
        :param is_sparse_diskgroup_enabled: Specifies whether to create a sparse disk group for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#is_sparse_diskgroup_enabled OdbCloudVmCluster#is_sparse_diskgroup_enabled}
        :param license_model: The Oracle license model to apply to the VM cluster. Default: LICENSE_INCLUDED. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#license_model OdbCloudVmCluster#license_model}
        :param memory_size_in_gbs: The amount of memory, in gigabytes (GBs), to allocate for the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#memory_size_in_gbs OdbCloudVmCluster#memory_size_in_gbs}
        :param odb_network_arn: The unique identifier of the ODB network for the VM cluster. This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#odb_network_arn OdbCloudVmCluster#odb_network_arn}
        :param odb_network_id: The unique identifier of the ODB network for the VM cluster. This member is required. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#odb_network_id OdbCloudVmCluster#odb_network_id}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#region OdbCloudVmCluster#region}
        :param scan_listener_port_tcp: The port number for TCP connections to the single client access name (SCAN) listener. Valid values: 1024–8999 with the following exceptions: 2484 , 6100 , 6200 , 7060, 7070 , 7085 , and 7879Default: 1521. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#scan_listener_port_tcp OdbCloudVmCluster#scan_listener_port_tcp}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#tags OdbCloudVmCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#timeouts OdbCloudVmCluster#timeouts}
        :param timezone: The configured time zone of the VM cluster. Changing this will create a new resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#timezone OdbCloudVmCluster#timezone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = OdbCloudVmClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3de766057cee7ffad1d0269d4046666f3e9752815795dd8303dd09b2e69bbf63)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cpu_core_count", value=cpu_core_count, expected_type=type_hints["cpu_core_count"])
            check_type(argname="argument data_storage_size_in_tbs", value=data_storage_size_in_tbs, expected_type=type_hints["data_storage_size_in_tbs"])
            check_type(argname="argument db_servers", value=db_servers, expected_type=type_hints["db_servers"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument gi_version", value=gi_version, expected_type=type_hints["gi_version"])
            check_type(argname="argument hostname_prefix", value=hostname_prefix, expected_type=type_hints["hostname_prefix"])
            check_type(argname="argument ssh_public_keys", value=ssh_public_keys, expected_type=type_hints["ssh_public_keys"])
            check_type(argname="argument cloud_exadata_infrastructure_arn", value=cloud_exadata_infrastructure_arn, expected_type=type_hints["cloud_exadata_infrastructure_arn"])
            check_type(argname="argument cloud_exadata_infrastructure_id", value=cloud_exadata_infrastructure_id, expected_type=type_hints["cloud_exadata_infrastructure_id"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument data_collection_options", value=data_collection_options, expected_type=type_hints["data_collection_options"])
            check_type(argname="argument db_node_storage_size_in_gbs", value=db_node_storage_size_in_gbs, expected_type=type_hints["db_node_storage_size_in_gbs"])
            check_type(argname="argument is_local_backup_enabled", value=is_local_backup_enabled, expected_type=type_hints["is_local_backup_enabled"])
            check_type(argname="argument is_sparse_diskgroup_enabled", value=is_sparse_diskgroup_enabled, expected_type=type_hints["is_sparse_diskgroup_enabled"])
            check_type(argname="argument license_model", value=license_model, expected_type=type_hints["license_model"])
            check_type(argname="argument memory_size_in_gbs", value=memory_size_in_gbs, expected_type=type_hints["memory_size_in_gbs"])
            check_type(argname="argument odb_network_arn", value=odb_network_arn, expected_type=type_hints["odb_network_arn"])
            check_type(argname="argument odb_network_id", value=odb_network_id, expected_type=type_hints["odb_network_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument scan_listener_port_tcp", value=scan_listener_port_tcp, expected_type=type_hints["scan_listener_port_tcp"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cpu_core_count": cpu_core_count,
            "data_storage_size_in_tbs": data_storage_size_in_tbs,
            "db_servers": db_servers,
            "display_name": display_name,
            "gi_version": gi_version,
            "hostname_prefix": hostname_prefix,
            "ssh_public_keys": ssh_public_keys,
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
        if cloud_exadata_infrastructure_arn is not None:
            self._values["cloud_exadata_infrastructure_arn"] = cloud_exadata_infrastructure_arn
        if cloud_exadata_infrastructure_id is not None:
            self._values["cloud_exadata_infrastructure_id"] = cloud_exadata_infrastructure_id
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if data_collection_options is not None:
            self._values["data_collection_options"] = data_collection_options
        if db_node_storage_size_in_gbs is not None:
            self._values["db_node_storage_size_in_gbs"] = db_node_storage_size_in_gbs
        if is_local_backup_enabled is not None:
            self._values["is_local_backup_enabled"] = is_local_backup_enabled
        if is_sparse_diskgroup_enabled is not None:
            self._values["is_sparse_diskgroup_enabled"] = is_sparse_diskgroup_enabled
        if license_model is not None:
            self._values["license_model"] = license_model
        if memory_size_in_gbs is not None:
            self._values["memory_size_in_gbs"] = memory_size_in_gbs
        if odb_network_arn is not None:
            self._values["odb_network_arn"] = odb_network_arn
        if odb_network_id is not None:
            self._values["odb_network_id"] = odb_network_id
        if region is not None:
            self._values["region"] = region
        if scan_listener_port_tcp is not None:
            self._values["scan_listener_port_tcp"] = scan_listener_port_tcp
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if timezone is not None:
            self._values["timezone"] = timezone

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
    def cpu_core_count(self) -> jsii.Number:
        '''The number of CPU cores to enable on the VM cluster. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#cpu_core_count OdbCloudVmCluster#cpu_core_count}
        '''
        result = self._values.get("cpu_core_count")
        assert result is not None, "Required property 'cpu_core_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def data_storage_size_in_tbs(self) -> jsii.Number:
        '''The size of the data disk group, in terabytes (TBs), to allocate for the VM cluster.

        Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#data_storage_size_in_tbs OdbCloudVmCluster#data_storage_size_in_tbs}
        '''
        result = self._values.get("data_storage_size_in_tbs")
        assert result is not None, "Required property 'data_storage_size_in_tbs' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def db_servers(self) -> typing.List[builtins.str]:
        '''The list of database servers for the VM cluster. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#db_servers OdbCloudVmCluster#db_servers}
        '''
        result = self._values.get("db_servers")
        assert result is not None, "Required property 'db_servers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''A user-friendly name for the VM cluster. This member is required. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#display_name OdbCloudVmCluster#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gi_version(self) -> builtins.str:
        '''A valid software version of Oracle Grid Infrastructure (GI).

        To get the list of valid values, use the ListGiVersions operation and specify the shape of the Exadata infrastructure. Example: 19.0.0.0 This member is required. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#gi_version OdbCloudVmCluster#gi_version}
        '''
        result = self._values.get("gi_version")
        assert result is not None, "Required property 'gi_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hostname_prefix(self) -> builtins.str:
        '''The host name prefix for the VM cluster.

        Constraints: - Can't be "localhost" or "hostname". - Can't contain "-version". - The maximum length of the combined hostname and domain is 63 characters. - The hostname must be unique within the subnet. This member is required. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#hostname_prefix OdbCloudVmCluster#hostname_prefix}
        '''
        result = self._values.get("hostname_prefix")
        assert result is not None, "Required property 'hostname_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssh_public_keys(self) -> typing.List[builtins.str]:
        '''The public key portion of one or more key pairs used for SSH access to the VM cluster.

        This member is required. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#ssh_public_keys OdbCloudVmCluster#ssh_public_keys}
        '''
        result = self._values.get("ssh_public_keys")
        assert result is not None, "Required property 'ssh_public_keys' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cloud_exadata_infrastructure_arn(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the Exadata infrastructure for this VM cluster. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#cloud_exadata_infrastructure_arn OdbCloudVmCluster#cloud_exadata_infrastructure_arn}
        '''
        result = self._values.get("cloud_exadata_infrastructure_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_exadata_infrastructure_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the Exadata infrastructure for this VM cluster. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#cloud_exadata_infrastructure_id OdbCloudVmCluster#cloud_exadata_infrastructure_id}
        '''
        result = self._values.get("cloud_exadata_infrastructure_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Grid Infrastructure (GI) cluster. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#cluster_name OdbCloudVmCluster#cluster_name}
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_collection_options(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OdbCloudVmClusterDataCollectionOptions"]]]:
        '''data_collection_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#data_collection_options OdbCloudVmCluster#data_collection_options}
        '''
        result = self._values.get("data_collection_options")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OdbCloudVmClusterDataCollectionOptions"]]], result)

    @builtins.property
    def db_node_storage_size_in_gbs(self) -> typing.Optional[jsii.Number]:
        '''The amount of local node storage, in gigabytes (GBs), to allocate for the VM cluster.

        Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#db_node_storage_size_in_gbs OdbCloudVmCluster#db_node_storage_size_in_gbs}
        '''
        result = self._values.get("db_node_storage_size_in_gbs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def is_local_backup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to enable database backups to local Exadata storage for the VM cluster.

        Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#is_local_backup_enabled OdbCloudVmCluster#is_local_backup_enabled}
        '''
        result = self._values.get("is_local_backup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_sparse_diskgroup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to create a sparse disk group for the VM cluster. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#is_sparse_diskgroup_enabled OdbCloudVmCluster#is_sparse_diskgroup_enabled}
        '''
        result = self._values.get("is_sparse_diskgroup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def license_model(self) -> typing.Optional[builtins.str]:
        '''The Oracle license model to apply to the VM cluster. Default: LICENSE_INCLUDED. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#license_model OdbCloudVmCluster#license_model}
        '''
        result = self._values.get("license_model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory_size_in_gbs(self) -> typing.Optional[jsii.Number]:
        '''The amount of memory, in gigabytes (GBs), to allocate for the VM cluster.

        Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#memory_size_in_gbs OdbCloudVmCluster#memory_size_in_gbs}
        '''
        result = self._values.get("memory_size_in_gbs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def odb_network_arn(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the ODB network for the VM cluster.

        This member is required. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#odb_network_arn OdbCloudVmCluster#odb_network_arn}
        '''
        result = self._values.get("odb_network_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def odb_network_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the ODB network for the VM cluster.

        This member is required. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#odb_network_id OdbCloudVmCluster#odb_network_id}
        '''
        result = self._values.get("odb_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#region OdbCloudVmCluster#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scan_listener_port_tcp(self) -> typing.Optional[jsii.Number]:
        '''The port number for TCP connections to the single client access name (SCAN) listener.

        Valid values: 1024–8999 with the following exceptions: 2484 , 6100 , 6200 , 7060, 7070 , 7085 , and 7879Default: 1521. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#scan_listener_port_tcp OdbCloudVmCluster#scan_listener_port_tcp}
        '''
        result = self._values.get("scan_listener_port_tcp")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#tags OdbCloudVmCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["OdbCloudVmClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#timeouts OdbCloudVmCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["OdbCloudVmClusterTimeouts"], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''The configured time zone of the VM cluster. Changing this will create a new resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#timezone OdbCloudVmCluster#timezone}
        '''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbCloudVmClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.odbCloudVmCluster.OdbCloudVmClusterDataCollectionOptions",
    jsii_struct_bases=[],
    name_mapping={
        "is_diagnostics_events_enabled": "isDiagnosticsEventsEnabled",
        "is_health_monitoring_enabled": "isHealthMonitoringEnabled",
        "is_incident_logs_enabled": "isIncidentLogsEnabled",
    },
)
class OdbCloudVmClusterDataCollectionOptions:
    def __init__(
        self,
        *,
        is_diagnostics_events_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        is_health_monitoring_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        is_incident_logs_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param is_diagnostics_events_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#is_diagnostics_events_enabled OdbCloudVmCluster#is_diagnostics_events_enabled}.
        :param is_health_monitoring_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#is_health_monitoring_enabled OdbCloudVmCluster#is_health_monitoring_enabled}.
        :param is_incident_logs_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#is_incident_logs_enabled OdbCloudVmCluster#is_incident_logs_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__966737cdd23e722288a98bb5c9168f5676390f374f0df7a0b4ac62f2a2b4d41a)
            check_type(argname="argument is_diagnostics_events_enabled", value=is_diagnostics_events_enabled, expected_type=type_hints["is_diagnostics_events_enabled"])
            check_type(argname="argument is_health_monitoring_enabled", value=is_health_monitoring_enabled, expected_type=type_hints["is_health_monitoring_enabled"])
            check_type(argname="argument is_incident_logs_enabled", value=is_incident_logs_enabled, expected_type=type_hints["is_incident_logs_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "is_diagnostics_events_enabled": is_diagnostics_events_enabled,
            "is_health_monitoring_enabled": is_health_monitoring_enabled,
            "is_incident_logs_enabled": is_incident_logs_enabled,
        }

    @builtins.property
    def is_diagnostics_events_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#is_diagnostics_events_enabled OdbCloudVmCluster#is_diagnostics_events_enabled}.'''
        result = self._values.get("is_diagnostics_events_enabled")
        assert result is not None, "Required property 'is_diagnostics_events_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def is_health_monitoring_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#is_health_monitoring_enabled OdbCloudVmCluster#is_health_monitoring_enabled}.'''
        result = self._values.get("is_health_monitoring_enabled")
        assert result is not None, "Required property 'is_health_monitoring_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def is_incident_logs_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#is_incident_logs_enabled OdbCloudVmCluster#is_incident_logs_enabled}.'''
        result = self._values.get("is_incident_logs_enabled")
        assert result is not None, "Required property 'is_incident_logs_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbCloudVmClusterDataCollectionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OdbCloudVmClusterDataCollectionOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.odbCloudVmCluster.OdbCloudVmClusterDataCollectionOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7d7f70ada3389ab15d3b787f3e82d417a1151fbffe3ab22dac2f2c6bc323190)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OdbCloudVmClusterDataCollectionOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec372c1cc92f66d1cfc7bcc0f6f47600d879a662d1f230bec98c533a1431f900)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OdbCloudVmClusterDataCollectionOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a2e1980e5eaca97994d70c8e84700b2556071ed0db59d3a823609014b18eae4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fb9fd9a41a56964f69e139d98ef2b33bb273e2e02d8f420d901c04dbfe1ae00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b941e2ea7f85d6807912cade850a05654df06cfea3f0294d78fca8645b620fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudVmClusterDataCollectionOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudVmClusterDataCollectionOptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudVmClusterDataCollectionOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__266fb1083c8272da272551da337bcd80a0505a656d48acd9b6549b58d7fe16cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OdbCloudVmClusterDataCollectionOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.odbCloudVmCluster.OdbCloudVmClusterDataCollectionOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96ebebf8658375aef5f6281843521ab6fdd6e9e0d35d274e1ee017a4083069be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="isDiagnosticsEventsEnabledInput")
    def is_diagnostics_events_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isDiagnosticsEventsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isHealthMonitoringEnabledInput")
    def is_health_monitoring_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isHealthMonitoringEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isIncidentLogsEnabledInput")
    def is_incident_logs_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isIncidentLogsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isDiagnosticsEventsEnabled")
    def is_diagnostics_events_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isDiagnosticsEventsEnabled"))

    @is_diagnostics_events_enabled.setter
    def is_diagnostics_events_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37206e272776f3395f56cf475db44744c13f552f2186eea3adb3da895acbaa56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isDiagnosticsEventsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isHealthMonitoringEnabled")
    def is_health_monitoring_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isHealthMonitoringEnabled"))

    @is_health_monitoring_enabled.setter
    def is_health_monitoring_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__518cb7649255efa4066995955a4deffcbcfe62c881f756d09f2d660e9de20c3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isHealthMonitoringEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isIncidentLogsEnabled")
    def is_incident_logs_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isIncidentLogsEnabled"))

    @is_incident_logs_enabled.setter
    def is_incident_logs_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__767c181c98bec40fdbdec8c5f323102157154d07b1b48626542ee4233a0b21e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isIncidentLogsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudVmClusterDataCollectionOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudVmClusterDataCollectionOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudVmClusterDataCollectionOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d420e449ec6b2647e962a9a232204732148cd3ec040082711508b888d328cfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.odbCloudVmCluster.OdbCloudVmClusterIormConfigCache",
    jsii_struct_bases=[],
    name_mapping={},
)
class OdbCloudVmClusterIormConfigCache:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbCloudVmClusterIormConfigCache(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.odbCloudVmCluster.OdbCloudVmClusterIormConfigCacheDbPlans",
    jsii_struct_bases=[],
    name_mapping={},
)
class OdbCloudVmClusterIormConfigCacheDbPlans:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbCloudVmClusterIormConfigCacheDbPlans(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OdbCloudVmClusterIormConfigCacheDbPlansList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.odbCloudVmCluster.OdbCloudVmClusterIormConfigCacheDbPlansList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17458344a1f3dd0691bec8476d2665600ceea4e0fb6097d95be382d27d43fd6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OdbCloudVmClusterIormConfigCacheDbPlansOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4fcb75a0fb020b7db16a55c303ee144e24a9eda8b75d395d12c3cb231e05655)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OdbCloudVmClusterIormConfigCacheDbPlansOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec193aba5ed92ce4071617a2add883dbfd1f55e8eae8f95d0e12f36c73f97c97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c815c0afb15b6c36c8fd20fe5d238fddd4d2479d378b910d5fc4014fc34cb772)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22969bd18f92d7f1a8bdf8b00f269622d85107af86527cabf99ea2d5553e2574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OdbCloudVmClusterIormConfigCacheDbPlansOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.odbCloudVmCluster.OdbCloudVmClusterIormConfigCacheDbPlansOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59b93f756d9dad5e84e536b01812bc3b3d009eda37e7bd3bc69d665ee2243dad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dbName")
    def db_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbName"))

    @builtins.property
    @jsii.member(jsii_name="flashCacheLimit")
    def flash_cache_limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flashCacheLimit"))

    @builtins.property
    @jsii.member(jsii_name="share")
    def share(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "share"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OdbCloudVmClusterIormConfigCacheDbPlans]:
        return typing.cast(typing.Optional[OdbCloudVmClusterIormConfigCacheDbPlans], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OdbCloudVmClusterIormConfigCacheDbPlans],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d026fcf26c832d2343cb6803f01afccd69b19aa46cb11ad2b6a85ae6ccd63bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OdbCloudVmClusterIormConfigCacheList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.odbCloudVmCluster.OdbCloudVmClusterIormConfigCacheList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6b86373d56f4f60ddb7f43483a221e02c2128dbb9ed05ddc7227207bf07c654)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OdbCloudVmClusterIormConfigCacheOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed227bebfd30ce3b95a78a4a184d9aca01746b0fad194f5172b62598390710cc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OdbCloudVmClusterIormConfigCacheOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70874ecf79ed9d3315829b1572a33498e00196a00c7d4a58a1c0d0e80ec3ffb8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a2cf28f58a2f9cb8ffb26f4c2750a0c66128531d745a14ff97c3b6dc277f449)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52b7566f151411a9b1df217c8a1e3162cc4c253cc44bf72a4a9fd13c133eb75b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OdbCloudVmClusterIormConfigCacheOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.odbCloudVmCluster.OdbCloudVmClusterIormConfigCacheOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da72a416d7f379b221a90f6292516fb3b3f29d48c3fd7fa283dfb9a825d81ec6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dbPlans")
    def db_plans(self) -> OdbCloudVmClusterIormConfigCacheDbPlansList:
        return typing.cast(OdbCloudVmClusterIormConfigCacheDbPlansList, jsii.get(self, "dbPlans"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleDetails")
    def lifecycle_details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleDetails"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleState")
    def lifecycle_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleState"))

    @builtins.property
    @jsii.member(jsii_name="objective")
    def objective(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objective"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OdbCloudVmClusterIormConfigCache]:
        return typing.cast(typing.Optional[OdbCloudVmClusterIormConfigCache], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OdbCloudVmClusterIormConfigCache],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05fa754bc1ef928d8756322aa8a3c4ab7e878fb380f49ed7c6003dbe757485b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-aws.odbCloudVmCluster.OdbCloudVmClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class OdbCloudVmClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#create OdbCloudVmCluster#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#delete OdbCloudVmCluster#delete}
        :param update: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#update OdbCloudVmCluster#update}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05ba72135ae4103c8b4e9822ab40705c745d5b6409f811ec067ebdc31870075a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#create OdbCloudVmCluster#create}
        '''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#delete OdbCloudVmCluster#delete}
        '''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.28.0/docs/resources/odb_cloud_vm_cluster#update OdbCloudVmCluster#update}
        '''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OdbCloudVmClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OdbCloudVmClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-aws.odbCloudVmCluster.OdbCloudVmClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8451118255e9b3fa62547860a34b792bc40b92c70e5f5b3950d9b609824446cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccf78656791d11a2a73b724358bc7dc80d1e83bd227293095dbde90e25a6442e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4851b79b9640a13673cbc060f8ad7db696022334e530cd9e14e62f91eb00badb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__152fd26030a06d3187e9f347b88aa49545b3165214b1c3839ae07fa504e0879b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudVmClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudVmClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudVmClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b87df6aa7b35e16fffef0e842cb6225efc5e6dc5a420a1608aca6b843885923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OdbCloudVmCluster",
    "OdbCloudVmClusterConfig",
    "OdbCloudVmClusterDataCollectionOptions",
    "OdbCloudVmClusterDataCollectionOptionsList",
    "OdbCloudVmClusterDataCollectionOptionsOutputReference",
    "OdbCloudVmClusterIormConfigCache",
    "OdbCloudVmClusterIormConfigCacheDbPlans",
    "OdbCloudVmClusterIormConfigCacheDbPlansList",
    "OdbCloudVmClusterIormConfigCacheDbPlansOutputReference",
    "OdbCloudVmClusterIormConfigCacheList",
    "OdbCloudVmClusterIormConfigCacheOutputReference",
    "OdbCloudVmClusterTimeouts",
    "OdbCloudVmClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__001dc733a1fa4ae4d53916f2774a4007b8c1c9d6773e10857e163a226e1b3374(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cpu_core_count: jsii.Number,
    data_storage_size_in_tbs: jsii.Number,
    db_servers: typing.Sequence[builtins.str],
    display_name: builtins.str,
    gi_version: builtins.str,
    hostname_prefix: builtins.str,
    ssh_public_keys: typing.Sequence[builtins.str],
    cloud_exadata_infrastructure_arn: typing.Optional[builtins.str] = None,
    cloud_exadata_infrastructure_id: typing.Optional[builtins.str] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    data_collection_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OdbCloudVmClusterDataCollectionOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    db_node_storage_size_in_gbs: typing.Optional[jsii.Number] = None,
    is_local_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_sparse_diskgroup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    license_model: typing.Optional[builtins.str] = None,
    memory_size_in_gbs: typing.Optional[jsii.Number] = None,
    odb_network_arn: typing.Optional[builtins.str] = None,
    odb_network_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    scan_listener_port_tcp: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[OdbCloudVmClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timezone: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__e2b97420e9120267b7bcb123a084073ec9aa223f3c92509147be4cd83d0444ab(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccd2bdd4cf4451b9a1ede1109ba3305cd65fd094a70c62d0397d90ae8aba57e5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OdbCloudVmClusterDataCollectionOptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95a6af93116a71031cc10ee1fb4957667d5adb35cbf5d854d83ccac062fc7e3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd9783dc11297a9d1a28ae3fa449064778f976cd17e1e80329b8d1213997189(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c05e14111e238a5da8df49a19d155205647c036b9da31f8d365b6dfcd57a66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e075499e48cbca2d0a483f8cc31b0d39f1a6845110e6cd0cdfbbaf9be7d41dd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b9203865c0b3b39517bda9179d98f908804e35e951f377300f213f50d2af565(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeaee6273b57f877789e0e7639a8beab405aaa25ff112235727eb19c52b0882b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfc8579573b95eee3dba016646e57f16044ca5a278a3720c1e0cb15d5dfb9c91(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__793b1afe8f55ce28919fadcd1402fe4c4223f8a7fbd09daef24624abc343bea9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb82411165eace2dbf06cf68a42b6787db6df7c63970af530bc5654a26b713f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf887f212e3fd05095ae716503f68c3831a5e167fa206111d874d66856765c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d792d012ac46bffdac948815335d875c015cb237cf3ce56aa4017e0266f3499(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e6af43d7d4fa013001c907fa05368669569f4dc16671ba0a8836f296c57c60(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca1887b97ce7192b4b814e613bcc264212e788cc3b0c268213454ea179455422(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b039f72f5d977fb616b375b7f6cdcda849c87d53f2f5b27922eb6f5cf89261b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e658e79b7cb14a75a70120c1ed1349fbd2066495933d8a0d12281e98a85642(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bbc264a323451f682da1476bfee043c0bbc6a063ae80c705cd14aada920775d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b35bdc192ff63bb2bf0409305f1fe961adc350e56ee4ea9e821a414dcc8cf830(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26aa7401e1a658885a1f9d2beea26422c540dd563550b5f17a322042d7fb023b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bb157c5165acd79110bf70ba0f661703af17311043cc1532d04bd9c06384856(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26635f215a4323da4715fcf6fcfb705855e282962951a33b10c6d1c9a1e6029e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d4b02d19da9cbee2067d357fd510e259d1591320915b4a3c476c716e58eaca6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de766057cee7ffad1d0269d4046666f3e9752815795dd8303dd09b2e69bbf63(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cpu_core_count: jsii.Number,
    data_storage_size_in_tbs: jsii.Number,
    db_servers: typing.Sequence[builtins.str],
    display_name: builtins.str,
    gi_version: builtins.str,
    hostname_prefix: builtins.str,
    ssh_public_keys: typing.Sequence[builtins.str],
    cloud_exadata_infrastructure_arn: typing.Optional[builtins.str] = None,
    cloud_exadata_infrastructure_id: typing.Optional[builtins.str] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    data_collection_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OdbCloudVmClusterDataCollectionOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    db_node_storage_size_in_gbs: typing.Optional[jsii.Number] = None,
    is_local_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_sparse_diskgroup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    license_model: typing.Optional[builtins.str] = None,
    memory_size_in_gbs: typing.Optional[jsii.Number] = None,
    odb_network_arn: typing.Optional[builtins.str] = None,
    odb_network_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    scan_listener_port_tcp: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[OdbCloudVmClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timezone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966737cdd23e722288a98bb5c9168f5676390f374f0df7a0b4ac62f2a2b4d41a(
    *,
    is_diagnostics_events_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    is_health_monitoring_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    is_incident_logs_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d7f70ada3389ab15d3b787f3e82d417a1151fbffe3ab22dac2f2c6bc323190(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec372c1cc92f66d1cfc7bcc0f6f47600d879a662d1f230bec98c533a1431f900(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a2e1980e5eaca97994d70c8e84700b2556071ed0db59d3a823609014b18eae4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fb9fd9a41a56964f69e139d98ef2b33bb273e2e02d8f420d901c04dbfe1ae00(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b941e2ea7f85d6807912cade850a05654df06cfea3f0294d78fca8645b620fe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__266fb1083c8272da272551da337bcd80a0505a656d48acd9b6549b58d7fe16cf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OdbCloudVmClusterDataCollectionOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ebebf8658375aef5f6281843521ab6fdd6e9e0d35d274e1ee017a4083069be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37206e272776f3395f56cf475db44744c13f552f2186eea3adb3da895acbaa56(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__518cb7649255efa4066995955a4deffcbcfe62c881f756d09f2d660e9de20c3f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__767c181c98bec40fdbdec8c5f323102157154d07b1b48626542ee4233a0b21e1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d420e449ec6b2647e962a9a232204732148cd3ec040082711508b888d328cfb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudVmClusterDataCollectionOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17458344a1f3dd0691bec8476d2665600ceea4e0fb6097d95be382d27d43fd6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4fcb75a0fb020b7db16a55c303ee144e24a9eda8b75d395d12c3cb231e05655(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec193aba5ed92ce4071617a2add883dbfd1f55e8eae8f95d0e12f36c73f97c97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c815c0afb15b6c36c8fd20fe5d238fddd4d2479d378b910d5fc4014fc34cb772(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22969bd18f92d7f1a8bdf8b00f269622d85107af86527cabf99ea2d5553e2574(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b93f756d9dad5e84e536b01812bc3b3d009eda37e7bd3bc69d665ee2243dad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d026fcf26c832d2343cb6803f01afccd69b19aa46cb11ad2b6a85ae6ccd63bd(
    value: typing.Optional[OdbCloudVmClusterIormConfigCacheDbPlans],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b86373d56f4f60ddb7f43483a221e02c2128dbb9ed05ddc7227207bf07c654(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed227bebfd30ce3b95a78a4a184d9aca01746b0fad194f5172b62598390710cc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70874ecf79ed9d3315829b1572a33498e00196a00c7d4a58a1c0d0e80ec3ffb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2cf28f58a2f9cb8ffb26f4c2750a0c66128531d745a14ff97c3b6dc277f449(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b7566f151411a9b1df217c8a1e3162cc4c253cc44bf72a4a9fd13c133eb75b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da72a416d7f379b221a90f6292516fb3b3f29d48c3fd7fa283dfb9a825d81ec6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05fa754bc1ef928d8756322aa8a3c4ab7e878fb380f49ed7c6003dbe757485b2(
    value: typing.Optional[OdbCloudVmClusterIormConfigCache],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05ba72135ae4103c8b4e9822ab40705c745d5b6409f811ec067ebdc31870075a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8451118255e9b3fa62547860a34b792bc40b92c70e5f5b3950d9b609824446cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf78656791d11a2a73b724358bc7dc80d1e83bd227293095dbde90e25a6442e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4851b79b9640a13673cbc060f8ad7db696022334e530cd9e14e62f91eb00badb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__152fd26030a06d3187e9f347b88aa49545b3165214b1c3839ae07fa504e0879b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b87df6aa7b35e16fffef0e842cb6225efc5e6dc5a420a1608aca6b843885923(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OdbCloudVmClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
